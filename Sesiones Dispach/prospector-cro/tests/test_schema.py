import jsonschema
import pytest

from prospector.schema import validar_empresa

EMPRESA_VALIDA = {
    "empresa": {
        "nombre": "Acme Ecommerce",
        "dominio": "acme.example",
        "pais": "Argentina",
        "industria": "ecommerce",
        "empleados_rango": "11-50",
        "fuente_descubrimiento": "apollo",
    },
    "auditoria": {
        "ahrefs": {
            "domain_rating": 32.5,
            "trafico_organico_mensual": 4200,
            "problemas_tecnicos": ["imágenes sin optimizar", "meta description faltante"],
            "top_keywords": ["zapatillas running", "envio gratis"],
        },
        "scraping": {
            "tecnologia_detectada": ["Shopify", "Google Analytics"],
            "tiene_chat_vivo": True,
            "capturas": {"home": "data/lote1/capturas/acme.example/home.png", "checkout_o_landing": None},
            "senales_ux": {"formulario_largo": False, "cta_visible": True, "pasos_checkout": 3},
        },
    },
    "oportunidad": {
        "score": 62,
        "categoria": "media",
        "razones": ["DR bajo para su antigüedad", "checkout de 3 pasos"],
    },
    "propuesta": {
        "diagnostico": ["El sitio tarda en cargar en mobile", "El checkout tiene fricción evitable"],
        "servicio_sugerido": "Auditoría CRO + quick wins de velocidad",
        "estado_envio": "borrador_generado",
    },
}


def test_empresa_valida_no_lanza_error():
    validar_empresa(EMPRESA_VALIDA)  # no debe levantar excepción


def test_falta_un_campo_requerido_lanza_error():
    invalida = {**EMPRESA_VALIDA, "empresa": {**EMPRESA_VALIDA["empresa"]}}
    del invalida["empresa"]["dominio"]
    with pytest.raises(jsonschema.ValidationError):
        validar_empresa(invalida)


def test_fuente_descubrimiento_invalida_lanza_error():
    invalida = {
        **EMPRESA_VALIDA,
        "empresa": {**EMPRESA_VALIDA["empresa"], "fuente_descubrimiento": "inventado"},
    }
    with pytest.raises(jsonschema.ValidationError):
        validar_empresa(invalida)


def test_campo_no_declarado_en_el_esquema_lanza_error():
    """Un dato inventado que no está en el esquema del spec no debe colarse silenciosamente."""
    invalida = {**EMPRESA_VALIDA, "campo_inventado": "no debería existir"}
    with pytest.raises(jsonschema.ValidationError):
        validar_empresa(invalida)
