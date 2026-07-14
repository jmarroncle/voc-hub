"""Descubrimiento de empresas: Apollo como fuente principal + fallbacks marcados (spec sección 3, paso 4)."""

import time
import urllib.robotparser as robotparser
from urllib.parse import urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

COLUMNAS_EMPRESA = ["nombre", "dominio", "pais", "industria", "empleados_rango", "fuente_descubrimiento"]
USER_AGENT = "ProspectorCROBot/0.1 (uso propio, prospección B2B; contacto a completar)"
RATE_LIMIT_SEGUNDOS = 1.0

# Directorios públicos por país. Vacío a propósito: si un país no está acá,
# no inventamos una URL — devolvemos 0 resultados de este fallback para ese país
# (ver plan.md: "no se fabrica un dato/fuente que no exista").
DIRECTORIOS_POR_PAIS: dict[str, str] = {}


def marcar_fuente_apollo(registros_apollo: list[dict]) -> pd.DataFrame:
    """Normaliza resultados de la búsqueda de organizaciones de Apollo a las columnas del esquema."""
    filas = []
    for r in registros_apollo:
        filas.append({
            "nombre": r.get("name") or r.get("nombre") or "",
            "dominio": (r.get("primary_domain") or r.get("website_url") or r.get("dominio") or "").lower().replace("www.", ""),
            "pais": r.get("country") or r.get("pais") or "",
            "industria": r.get("industry") or r.get("industria") or "",
            "empleados_rango": r.get("estimated_num_employees_range") or r.get("empleados_rango") or "desconocido",
            "fuente_descubrimiento": "apollo",
        })
    return pd.DataFrame(filas, columns=COLUMNAS_EMPRESA)


def _fetch_html(url: str) -> str:
    respuesta = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=10)
    respuesta.raise_for_status()
    return respuesta.text


def _permitido_por_robots(url: str, user_agent: str = USER_AGENT) -> bool:
    partes = urlparse(url)
    robots_url = f"{partes.scheme}://{partes.netloc}/robots.txt"
    rp = robotparser.RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
    except Exception:
        # Si no se puede leer robots.txt, por prudencia no se scrapea ese sitio.
        return False
    return rp.can_fetch(user_agent, url)


def _parsear_resultados_busqueda(html: str, mercado: str, pais: str, cantidad_faltante: int) -> pd.DataFrame:
    soup = BeautifulSoup(html, "html.parser")
    filas = []
    for enlace in soup.select("a.result__a")[:cantidad_faltante]:
        dominio = urlparse(enlace.get("href", "")).netloc.replace("www.", "")
        if not dominio:
            continue
        filas.append({
            "nombre": enlace.get_text(strip=True),
            "dominio": dominio,
            "pais": pais,
            "industria": mercado,
            "empleados_rango": "desconocido",
            "fuente_descubrimiento": "fallback_busqueda_web",
        })
    return pd.DataFrame(filas, columns=COLUMNAS_EMPRESA)


def fallback_busqueda_web(
    mercado: str, pais: str, cantidad_faltante: int,
    fetcher=None, dormir=time.sleep,
) -> pd.DataFrame:
    """Completa empresas faltantes buscando resultados públicos de búsqueda.

    `fetcher` es inyectable para tests (evita red real). Respeta robots.txt
    y aplica un rate limit antes de pedir la página (límites éticos, plan.md sección 4).
    """
    if cantidad_faltante <= 0:
        return pd.DataFrame(columns=COLUMNAS_EMPRESA)
    fetcher = fetcher or _fetch_html
    url_busqueda = f"https://duckduckgo.com/html/?q=empresas+de+{mercado}+en+{pais}"
    if not _permitido_por_robots(url_busqueda):
        return pd.DataFrame(columns=COLUMNAS_EMPRESA)
    dormir(RATE_LIMIT_SEGUNDOS)
    html = fetcher(url_busqueda)
    return _parsear_resultados_busqueda(html, mercado, pais, cantidad_faltante)


def fallback_directorio_publico(
    mercado: str, pais: str, cantidad_faltante: int,
    fetcher=None, dormir=time.sleep,
) -> pd.DataFrame:
    """Completa empresas faltantes contra un directorio público específico del país.

    Si el país no tiene un directorio configurado en DIRECTORIOS_POR_PAIS,
    devuelve una tabla vacía en vez de inventar una fuente.
    """
    if cantidad_faltante <= 0 or pais not in DIRECTORIOS_POR_PAIS:
        return pd.DataFrame(columns=COLUMNAS_EMPRESA)
    fetcher = fetcher or _fetch_html
    url_directorio = DIRECTORIOS_POR_PAIS[pais]
    if not _permitido_por_robots(url_directorio):
        return pd.DataFrame(columns=COLUMNAS_EMPRESA)
    dormir(RATE_LIMIT_SEGUNDOS)
    html = fetcher(url_directorio)
    soup = BeautifulSoup(html, "html.parser")
    filas = []
    for enlace in soup.select("a")[:cantidad_faltante]:
        dominio = urlparse(enlace.get("href", "")).netloc.replace("www.", "")
        if not dominio:
            continue
        filas.append({
            "nombre": enlace.get_text(strip=True),
            "dominio": dominio,
            "pais": pais,
            "industria": mercado,
            "empleados_rango": "desconocido",
            "fuente_descubrimiento": "fallback_directorio_publico",
        })
    return pd.DataFrame(filas, columns=COLUMNAS_EMPRESA)


def combinar_resultados(
    df_apollo: pd.DataFrame, cantidad_esperada: int, mercado: str, pais: str,
    fallback_web=fallback_busqueda_web, fallback_directorio=fallback_directorio_publico,
) -> pd.DataFrame:
    """Arma la tabla final (spec paso 4): Apollo primero, fallbacks marcados solo si hacen falta."""
    partes = [df_apollo]
    faltan = cantidad_esperada - len(df_apollo)

    if faltan > 0:
        df_web = fallback_web(mercado, pais, faltan)
        partes.append(df_web)
        faltan -= len(df_web)

    if faltan > 0:
        df_dir = fallback_directorio(mercado, pais, faltan)
        partes.append(df_dir)

    resultado = pd.concat(partes, ignore_index=True)
    return resultado.drop_duplicates(subset="dominio").reset_index(drop=True)
