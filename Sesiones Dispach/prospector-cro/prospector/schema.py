"""Esquema del JSON por empresa (ver spec.md sección 4) y su validación."""

import jsonschema

FUENTES_DESCUBRIMIENTO = ["apollo", "fallback_busqueda_web", "fallback_directorio_publico"]
CATEGORIAS_OPORTUNIDAD = ["alta", "media", "baja"]
ESTADOS_ENVIO = ["borrador_generado", "enviado"]

EMPRESA_SCHEMA = {
    "type": "object",
    "required": ["empresa", "auditoria", "oportunidad", "propuesta"],
    "additionalProperties": False,
    "properties": {
        "empresa": {
            "type": "object",
            "required": [
                "nombre", "dominio", "pais", "industria",
                "empleados_rango", "fuente_descubrimiento",
            ],
            "additionalProperties": False,
            "properties": {
                "nombre": {"type": "string"},
                "dominio": {"type": "string"},
                "pais": {"type": "string"},
                "industria": {"type": "string"},
                "empleados_rango": {"type": "string"},
                "fuente_descubrimiento": {"enum": FUENTES_DESCUBRIMIENTO},
            },
        },
        "auditoria": {
            "type": "object",
            "required": ["ahrefs", "scraping"],
            "additionalProperties": False,
            "properties": {
                "ahrefs": {
                    "type": "object",
                    "required": [
                        "domain_rating", "trafico_organico_mensual",
                        "problemas_tecnicos", "top_keywords",
                    ],
                    "additionalProperties": False,
                    "properties": {
                        "domain_rating": {"type": ["number", "null"]},
                        "trafico_organico_mensual": {"type": ["number", "null"]},
                        "problemas_tecnicos": {"type": "array", "items": {"type": "string"}},
                        "top_keywords": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "scraping": {
                    "type": "object",
                    "required": [
                        "tecnologia_detectada", "tiene_chat_vivo",
                        "capturas", "senales_ux",
                    ],
                    "additionalProperties": False,
                    "properties": {
                        "tecnologia_detectada": {"type": "array", "items": {"type": "string"}},
                        "tiene_chat_vivo": {"type": "boolean"},
                        "capturas": {
                            "type": "object",
                            "required": ["home", "checkout_o_landing"],
                            "additionalProperties": False,
                            "properties": {
                                "home": {"type": ["string", "null"]},
                                "checkout_o_landing": {"type": ["string", "null"]},
                            },
                        },
                        "senales_ux": {
                            "type": "object",
                            "required": ["formulario_largo", "cta_visible", "pasos_checkout"],
                            "additionalProperties": False,
                            "properties": {
                                "formulario_largo": {"type": "boolean"},
                                "cta_visible": {"type": "boolean"},
                                "pasos_checkout": {"type": ["number", "null"]},
                            },
                        },
                    },
                },
            },
        },
        "oportunidad": {
            "type": "object",
            "required": ["score", "categoria", "razones"],
            "additionalProperties": False,
            "properties": {
                "score": {"type": "number", "minimum": 0, "maximum": 100},
                "categoria": {"enum": CATEGORIAS_OPORTUNIDAD},
                "razones": {"type": "array", "items": {"type": "string"}},
            },
        },
        "propuesta": {
            "type": "object",
            "required": ["diagnostico", "servicio_sugerido", "estado_envio"],
            "additionalProperties": False,
            "properties": {
                "diagnostico": {"type": "array", "items": {"type": "string"}},
                "servicio_sugerido": {"type": "string"},
                "estado_envio": {"enum": ESTADOS_ENVIO},
            },
        },
    },
}


def validar_empresa(empresa_json: dict) -> None:
    """Levanta jsonschema.ValidationError si empresa_json no respeta el esquema.

    No devuelve nada en éxito: seguí, sin más, si no explotó.
    """
    jsonschema.validate(instance=empresa_json, schema=EMPRESA_SCHEMA)
