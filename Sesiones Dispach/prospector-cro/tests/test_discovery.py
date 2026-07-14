import pandas as pd

from prospector.discovery import (
    COLUMNAS_EMPRESA,
    _parsear_resultados_busqueda,
    combinar_resultados,
    marcar_fuente_apollo,
)

HTML_RESULTADOS_FAKE = """
<html><body>
  <a class="result__a" href="https://tienda-uno.example/">Tienda Uno</a>
  <a class="result__a" href="https://tienda-dos.example/">Tienda Dos</a>
</body></html>
"""


def test_marcar_fuente_apollo_normaliza_columnas():
    registros = [
        {"name": "Acme SA", "primary_domain": "WWW.acme.example", "country": "Argentina",
         "industry": "ecommerce", "estimated_num_employees_range": "11-50"},
    ]
    df = marcar_fuente_apollo(registros)
    assert list(df.columns) == COLUMNAS_EMPRESA
    assert df.iloc[0]["dominio"] == "acme.example"
    assert df.iloc[0]["fuente_descubrimiento"] == "apollo"


def test_parsear_resultados_busqueda_marca_fallback_web():
    df = _parsear_resultados_busqueda(HTML_RESULTADOS_FAKE, "ecommerce", "Argentina", cantidad_faltante=5)
    assert len(df) == 2
    assert set(df["fuente_descubrimiento"]) == {"fallback_busqueda_web"}
    assert "tienda-uno.example" in set(df["dominio"])


def test_combinar_resultados_no_llama_fallback_si_apollo_alcanza():
    df_apollo = marcar_fuente_apollo([
        {"name": "Acme SA", "primary_domain": "acme.example", "country": "Argentina", "industry": "ecommerce"},
    ])

    llamadas = []

    def fallback_web_falso(*args, **kwargs):
        llamadas.append("web")
        return pd.DataFrame(columns=COLUMNAS_EMPRESA)

    def fallback_dir_falso(*args, **kwargs):
        llamadas.append("dir")
        return pd.DataFrame(columns=COLUMNAS_EMPRESA)

    resultado = combinar_resultados(
        df_apollo, cantidad_esperada=1, mercado="ecommerce", pais="Argentina",
        fallback_web=fallback_web_falso, fallback_directorio=fallback_dir_falso,
    )
    assert len(resultado) == 1
    assert llamadas == []  # Apollo ya alcanzó, no se debe llamar a ningún fallback


def test_combinar_resultados_usa_fallback_y_lo_marca_explicitamente():
    df_apollo = marcar_fuente_apollo([
        {"name": "Acme SA", "primary_domain": "acme.example", "country": "Argentina", "industry": "ecommerce"},
    ])

    def fallback_web_falso(mercado, pais, cantidad_faltante, **kwargs):
        return pd.DataFrame([{
            "nombre": "Tienda Web", "dominio": "tienda-web.example", "pais": pais,
            "industria": mercado, "empleados_rango": "desconocido",
            "fuente_descubrimiento": "fallback_busqueda_web",
        }], columns=COLUMNAS_EMPRESA)

    def fallback_dir_falso(mercado, pais, cantidad_faltante, **kwargs):
        return pd.DataFrame([{
            "nombre": "Tienda Directorio", "dominio": "tienda-directorio.example", "pais": pais,
            "industria": mercado, "empleados_rango": "desconocido",
            "fuente_descubrimiento": "fallback_directorio_publico",
        }], columns=COLUMNAS_EMPRESA)

    resultado = combinar_resultados(
        df_apollo, cantidad_esperada=3, mercado="ecommerce", pais="Argentina",
        fallback_web=fallback_web_falso, fallback_directorio=fallback_dir_falso,
    )
    assert len(resultado) == 3
    fuentes = dict(zip(resultado["dominio"], resultado["fuente_descubrimiento"]))
    assert fuentes["acme.example"] == "apollo"
    assert fuentes["tienda-web.example"] == "fallback_busqueda_web"
    assert fuentes["tienda-directorio.example"] == "fallback_directorio_publico"


def test_combinar_resultados_saltea_directorio_si_web_ya_completo():
    df_apollo = pd.DataFrame(columns=COLUMNAS_EMPRESA)

    def fallback_web_falso(mercado, pais, cantidad_faltante, **kwargs):
        return pd.DataFrame([
            {"nombre": f"Tienda {i}", "dominio": f"tienda-{i}.example", "pais": pais,
             "industria": mercado, "empleados_rango": "desconocido",
             "fuente_descubrimiento": "fallback_busqueda_web"}
            for i in range(cantidad_faltante)
        ], columns=COLUMNAS_EMPRESA)

    llamado_directorio = []

    def fallback_dir_falso(*args, **kwargs):
        llamado_directorio.append(True)
        return pd.DataFrame(columns=COLUMNAS_EMPRESA)

    resultado = combinar_resultados(
        df_apollo, cantidad_esperada=2, mercado="ecommerce", pais="Argentina",
        fallback_web=fallback_web_falso, fallback_directorio=fallback_dir_falso,
    )
    assert len(resultado) == 2
    assert llamado_directorio == []
