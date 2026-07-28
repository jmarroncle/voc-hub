"""Auditoría propia de cada sitio (spec sección 3, pasos 5-7): tecnología, capturas y señales UX/CRO.

Las funciones que necesitan red real (fetch de HTML, webtech, Playwright) están
separadas de las heurísticas puras, para poder testear las heurísticas sin red
(ver plan.md, tarea C5) y ejercitar las que sí pegan a internet recién en la
corrida real (Grupo F).
"""

import os
import re

from bs4 import BeautifulSoup

# Chromium viene preinstalado en este entorno; evita que Playwright intente descargarlo.
CHROMIUM_PATH = os.environ.get("PLAYWRIGHT_CHROMIUM_PATH", "/opt/pw-browsers/chromium")

USER_AGENT = "ProspectorCROBot/0.1 (uso propio, prospección B2B; contacto a completar)"

# Marcadores de chat en vivo conocidos, buscados en el HTML crudo (scripts, clases, ids).
MARCADORES_CHAT_VIVO = {
    "Intercom": ["intercom", "widget.intercom.io"],
    "Drift": ["drift.com", "driftt"],
    "Tawk.to": ["tawk.to", "embed.tawk"],
    "Zendesk Chat": ["zendesk", "zdassets.com"],
    "WhatsApp widget": ["wa.me", "api.whatsapp.com"],
}

# Marcadores de tecnología (CMS, ecommerce, analytics/ads) detectables por heurística propia.
MARCADORES_TECNOLOGIA = {
    "Shopify": ["cdn.shopify.com", "shopify.com/s/"],
    "WooCommerce": ["wp-content/plugins/woocommerce", "woocommerce"],
    "VTEX": ["vtexassets.com", "vtex.com.br"],
    "Google Analytics": ["google-analytics.com", "gtag(", "googletagmanager.com"],
    "Meta Pixel": ["connect.facebook.net", "fbq("],
}

PALABRAS_CTA = [
    "comprar", "agregar al carrito", "añadir al carrito", "empezar ahora",
    "empezar", "contactanos", "contáctanos", "solicitar demo", "pedir cotización",
    "suscribirme", "quiero saber más", "buy now", "add to cart", "get started",
]

UMBRAL_FORMULARIO_LARGO = 6


def detectar_tecnologia_heuristica(html: str) -> list[str]:
    """Busca marcadores conocidos de plataformas/analytics en el HTML crudo."""
    encontrados = []
    html_lower = html.lower()
    for nombre, patrones in MARCADORES_TECNOLOGIA.items():
        if any(p.lower() in html_lower for p in patrones):
            encontrados.append(nombre)
    return encontrados


def tiene_chat_vivo(html: str) -> bool:
    html_lower = html.lower()
    return any(
        any(p.lower() in html_lower for p in patrones)
        for patrones in MARCADORES_CHAT_VIVO.values()
    )


def _nombre_chat_detectado(html: str) -> list[str]:
    html_lower = html.lower()
    return [
        nombre for nombre, patrones in MARCADORES_CHAT_VIVO.items()
        if any(p.lower() in html_lower for p in patrones)
    ]


def detectar_senales_ux(html: str) -> dict:
    """Señales de UX/CRO que Ahrefs no mide: formulario largo, CTA visible, pasos de checkout."""
    soup = BeautifulSoup(html, "html.parser")

    formulario_largo = False
    for form in soup.find_all("form"):
        campos = form.find_all(["input", "select", "textarea"])
        campos_visibles = [c for c in campos if c.get("type") != "hidden"]
        if len(campos_visibles) > UMBRAL_FORMULARIO_LARGO:
            formulario_largo = True
            break

    texto_botones = " ".join(
        el.get_text(strip=True).lower()
        for el in soup.find_all(["button", "a"])
    )
    cta_visible = any(palabra in texto_botones for palabra in PALABRAS_CTA)

    pasos_checkout = _contar_pasos_checkout(soup)

    return {
        "formulario_largo": formulario_largo,
        "cta_visible": cta_visible,
        "pasos_checkout": pasos_checkout,
    }


def _contar_pasos_checkout(soup: BeautifulSoup) -> int | None:
    """Cuenta pasos dentro de un contenedor de checkout, si se puede identificar uno.

    Devuelve None ("no disponible") si la página no tiene un checkout identificable,
    en vez de inventar un número.
    """
    contenedor = soup.find(attrs={"class": re.compile("checkout", re.I)}) or \
        soup.find(attrs={"id": re.compile("checkout", re.I)})
    if contenedor is None:
        return None
    pasos = contenedor.find_all(attrs={"class": re.compile("step", re.I)})
    return len(pasos) if pasos else None


def capturar_pantallas(url: str, url_checkout_o_landing: str | None, carpeta_destino: str) -> dict:
    """Screenshots de home y checkout/landing con Playwright headless.

    Requiere red real y el navegador preinstalado — se ejercita en la corrida
    real (Grupo F), no en los tests unitarios de este grupo.
    Si una URL falla (timeout, bloqueo, etc.), esa captura queda en None
    en vez de cortar todo el proceso de la empresa.
    """
    from playwright.sync_api import sync_playwright

    os.makedirs(carpeta_destino, exist_ok=True)
    resultado = {"home": None, "checkout_o_landing": None}

    with sync_playwright() as p:
        navegador = p.chromium.launch(executable_path=CHROMIUM_PATH, headless=True)
        pagina = navegador.new_page(user_agent=USER_AGENT)

        for clave, destino_url in (("home", url), ("checkout_o_landing", url_checkout_o_landing)):
            if not destino_url:
                continue
            ruta = os.path.join(carpeta_destino, f"{clave}.png")
            try:
                pagina.goto(destino_url, timeout=15000, wait_until="load")
                pagina.screenshot(path=ruta)
                resultado[clave] = ruta
            except Exception:
                resultado[clave] = None

        navegador.close()

    return resultado


def armar_json_empresa(
    datos_empresa: dict,
    datos_ahrefs: dict | None,
    tecnologia_detectada: list[str],
    tiene_chat: bool,
    capturas: dict,
    senales_ux: dict,
) -> dict:
    """Combina todo en el JSON del esquema (schema.py). Nunca inventa: falta un dato -> None.

    `datos_ahrefs` viene ya resuelto por el agente (llamada MCP a Ahrefs) — acá solo
    se combina, no se llama a Ahrefs desde este módulo.
    """
    ahrefs = datos_ahrefs or {}
    return {
        "empresa": {
            "nombre": datos_empresa["nombre"],
            "dominio": datos_empresa["dominio"],
            "pais": datos_empresa["pais"],
            "industria": datos_empresa["industria"],
            "empleados_rango": datos_empresa["empleados_rango"],
            "fuente_descubrimiento": datos_empresa["fuente_descubrimiento"],
        },
        "auditoria": {
            "ahrefs": {
                "domain_rating": ahrefs.get("domain_rating"),
                "trafico_organico_mensual": ahrefs.get("trafico_organico_mensual"),
                "problemas_tecnicos": ahrefs.get("problemas_tecnicos", []),
                "top_keywords": ahrefs.get("top_keywords", []),
            },
            "scraping": {
                "tecnologia_detectada": tecnologia_detectada,
                "tiene_chat_vivo": tiene_chat,
                "capturas": {
                    "home": capturas.get("home"),
                    "checkout_o_landing": capturas.get("checkout_o_landing"),
                },
                "senales_ux": senales_ux,
            },
        },
        # oportunidad y propuesta se completan en los módulos scoring.py / proposal.py
        "oportunidad": {"score": 0, "categoria": "baja", "razones": []},
        "propuesta": {"diagnostico": [], "servicio_sugerido": "", "estado_envio": "borrador_generado"},
    }
