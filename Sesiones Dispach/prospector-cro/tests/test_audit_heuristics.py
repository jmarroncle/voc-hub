from prospector.audit import (
    armar_json_empresa,
    detectar_senales_ux,
    detectar_tecnologia_heuristica,
    tiene_chat_vivo,
)
from prospector.schema import validar_empresa

HTML_TIENDA_SHOPIFY_CON_CHAT = """
<html><head>
  <script src="https://cdn.shopify.com/s/files/tienda.js"></script>
  <script>gtag('config', 'UA-XXXX');</script>
  <script src="https://widget.intercom.io/widget/abc"></script>
</head><body>
  <button>Agregar al carrito</button>
</body></html>
"""

HTML_SITIO_SIMPLE_SIN_MARCAS = """
<html><body>
  <p>Somos una empresa que hace cosas.</p>
  <a href="/contacto">Ir a contacto</a>
</body></html>
"""

HTML_FORMULARIO_LARGO = """
<html><body>
  <form>
    <input name="nombre" /><input name="apellido" /><input name="email" />
    <input name="telefono" /><input name="empresa" /><input name="cargo" />
    <input name="mensaje" /><input type="hidden" name="csrf" />
  </form>
</body></html>
"""

HTML_CHECKOUT_TRES_PASOS = """
<html><body>
  <div class="checkout-wizard">
    <div class="step">Datos</div>
    <div class="step">Envío</div>
    <div class="step">Pago</div>
  </div>
</body></html>
"""


def test_detectar_tecnologia_heuristica_encuentra_shopify_y_analytics():
    tecnologia = detectar_tecnologia_heuristica(HTML_TIENDA_SHOPIFY_CON_CHAT)
    assert "Shopify" in tecnologia
    assert "Google Analytics" in tecnologia
    assert "WooCommerce" not in tecnologia


def test_detectar_tecnologia_heuristica_sitio_sin_marcas_devuelve_vacio():
    assert detectar_tecnologia_heuristica(HTML_SITIO_SIMPLE_SIN_MARCAS) == []


def test_tiene_chat_vivo_detecta_intercom():
    assert tiene_chat_vivo(HTML_TIENDA_SHOPIFY_CON_CHAT) is True
    assert tiene_chat_vivo(HTML_SITIO_SIMPLE_SIN_MARCAS) is False


def test_detectar_senales_ux_formulario_largo():
    senales = detectar_senales_ux(HTML_FORMULARIO_LARGO)
    assert senales["formulario_largo"] is True


def test_detectar_senales_ux_cta_visible():
    senales = detectar_senales_ux(HTML_TIENDA_SHOPIFY_CON_CHAT)
    assert senales["cta_visible"] is True

    senales_sin_cta = detectar_senales_ux(HTML_SITIO_SIMPLE_SIN_MARCAS)
    assert senales_sin_cta["cta_visible"] is False


def test_detectar_senales_ux_pasos_checkout_cuenta_pasos():
    senales = detectar_senales_ux(HTML_CHECKOUT_TRES_PASOS)
    assert senales["pasos_checkout"] == 3


def test_detectar_senales_ux_pasos_checkout_none_si_no_hay_checkout():
    senales = detectar_senales_ux(HTML_SITIO_SIMPLE_SIN_MARCAS)
    assert senales["pasos_checkout"] is None


def test_armar_json_empresa_respeta_el_esquema_y_no_inventa_datos_faltantes():
    datos_empresa = {
        "nombre": "Tienda Shopify SA", "dominio": "tienda-shopify.example",
        "pais": "Argentina", "industria": "ecommerce", "empleados_rango": "11-50",
        "fuente_descubrimiento": "apollo",
    }
    senales = detectar_senales_ux(HTML_TIENDA_SHOPIFY_CON_CHAT)
    tecnologia = detectar_tecnologia_heuristica(HTML_TIENDA_SHOPIFY_CON_CHAT)

    empresa_json = armar_json_empresa(
        datos_empresa=datos_empresa,
        datos_ahrefs=None,  # simula que Ahrefs no devolvió nada para este dominio
        tecnologia_detectada=tecnologia,
        tiene_chat=tiene_chat_vivo(HTML_TIENDA_SHOPIFY_CON_CHAT),
        capturas={"home": None, "checkout_o_landing": None},
        senales_ux=senales,
    )

    assert empresa_json["auditoria"]["ahrefs"]["domain_rating"] is None
    assert empresa_json["auditoria"]["ahrefs"]["problemas_tecnicos"] == []
    assert "Shopify" in empresa_json["auditoria"]["scraping"]["tecnologia_detectada"]
    validar_empresa(empresa_json)  # no debe lanzar excepción
