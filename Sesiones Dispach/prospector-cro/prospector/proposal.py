"""Propuesta automatizada (spec sección 3, paso 9): diagnóstico + servicio sugerido + CTA."""

SERVICIO_POR_CATEGORIA = {
    "alta": "Auditoría CRO completa + implementación rápida (vibe coding) de las mejoras prioritarias.",
    "media": "Auditoría CRO focalizada en los puntos de mayor fricción detectados.",
    "baja": "Diagnóstico web inicial gratuito, para confirmar si conviene una auditoría completa.",
}

LLAMADO_A_LA_ACCION = (
    "Si te interesa, coordinamos una llamada corta de 15 minutos para mostrarte "
    "el detalle y ver si tiene sentido avanzar."
)


def armar_propuesta(empresa_json: dict) -> dict:
    """Arma la propuesta a partir del score/razones ya calculados en empresa_json["oportunidad"].

    El diagnóstico son las mismas razones del score, redactadas de cara al cliente
    (no se inventan hallazgos nuevos que no estén respaldados por el score).
    """
    oportunidad = empresa_json["oportunidad"]
    categoria = oportunidad["categoria"]
    razones = oportunidad["razones"]

    diagnostico = [_redactar_para_cliente(r) for r in razones if not r.startswith("Domain Rating no disponible")]

    return {
        "diagnostico": diagnostico,
        "servicio_sugerido": SERVICIO_POR_CATEGORIA[categoria],
        "estado_envio": "borrador_generado",
    }


def _redactar_para_cliente(razon: str) -> str:
    """Traduce una razón técnica del score a una frase de cara al cliente."""
    return razon.rstrip(".")


def armar_cuerpo_email(nombre_empresa: str, empresa_json: dict) -> str:
    """Texto completo del borrador de mail, listo para pasarle a Gmail (paso 10)."""
    propuesta = empresa_json["propuesta"]
    hallazgos = "\n".join(f"- {item}" for item in propuesta["diagnostico"])
    return (
        f"Hola,\n\n"
        f"Estuvimos revisando el sitio de {nombre_empresa} y encontramos algunas oportunidades "
        f"concretas de mejora:\n\n{hallazgos}\n\n"
        f"Lo que proponemos: {propuesta['servicio_sugerido']}\n\n"
        f"{LLAMADO_A_LA_ACCION}\n\n"
        f"Saludos."
    )
