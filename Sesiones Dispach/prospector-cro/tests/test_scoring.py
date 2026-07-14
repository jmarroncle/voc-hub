import copy

from prospector.proposal import armar_cuerpo_email, armar_propuesta
from prospector.scoring import calcular_score

BASE_EMPRESA = {
    "empresa": {
        "nombre": "Tienda Ejemplo", "dominio": "tienda.example", "pais": "Argentina",
        "industria": "ecommerce", "empleados_rango": "11-50", "fuente_descubrimiento": "apollo",
    },
    "auditoria": {
        "ahrefs": {
            "domain_rating": None, "trafico_organico_mensual": None,
            "problemas_tecnicos": [], "top_keywords": [],
        },
        "scraping": {
            "tecnologia_detectada": [], "tiene_chat_vivo": True,
            "capturas": {"home": None, "checkout_o_landing": None},
            "senales_ux": {"formulario_largo": False, "cta_visible": True, "pasos_checkout": None},
        },
    },
    "oportunidad": {"score": 0, "categoria": "baja", "razones": []},
    "propuesta": {"diagnostico": [], "servicio_sugerido": "", "estado_envio": "borrador_generado"},
}


def _empresa(**overrides):
    empresa = copy.deepcopy(BASE_EMPRESA)
    ahrefs_overrides = overrides.pop("ahrefs", {})
    ux_overrides = overrides.pop("senales_ux", {})
    scraping_overrides = overrides.pop("scraping", {})
    empresa["auditoria"]["ahrefs"].update(ahrefs_overrides)
    empresa["auditoria"]["scraping"]["senales_ux"].update(ux_overrides)
    empresa["auditoria"]["scraping"].update(scraping_overrides)
    return empresa


def test_sitio_prolijo_da_score_bajo():
    """DR alto, sin problemas técnicos, CTA visible, formulario corto, chat activo -> score bajo."""
    empresa = _empresa(ahrefs={"domain_rating": 55})
    resultado = calcular_score(empresa)
    assert resultado["categoria"] == "baja"
    assert resultado["score"] < 40


def test_sitio_lento_y_sin_cta_da_score_alto():
    empresa = _empresa(
        ahrefs={"domain_rating": 12, "problemas_tecnicos": ["carga lenta en mobile", "imágenes sin optimizar"]},
        senales_ux={"cta_visible": False, "formulario_largo": True, "pasos_checkout": 5},
        scraping={"tiene_chat_vivo": False},
    )
    resultado = calcular_score(empresa)
    assert resultado["categoria"] == "alta"
    assert resultado["score"] >= 70
    # Cada razón debe ser rastreable a una regla concreta, no una caja negra.
    assert any("Domain Rating bajo" in r for r in resultado["razones"])
    assert any("problema" in r.lower() for r in resultado["razones"])
    assert any("CTA" in r for r in resultado["razones"])
    assert any("checkout" in r.lower() for r in resultado["razones"])


def test_dr_no_disponible_no_rompe_y_queda_registrado_como_tal():
    empresa = _empresa()  # domain_rating None por default
    resultado = calcular_score(empresa)
    assert any("no disponible" in r.lower() for r in resultado["razones"])


def test_problemas_tecnicos_tienen_tope_de_puntos():
    pocos = _empresa(ahrefs={"domain_rating": 50, "problemas_tecnicos": ["a", "b"]})
    muchos = _empresa(ahrefs={"domain_rating": 50, "problemas_tecnicos": ["a", "b", "c", "d", "e", "f", "g", "h"]})
    score_pocos = calcular_score(pocos)["score"]
    score_muchos = calcular_score(muchos)["score"]
    # 8 problemas no deberían sumar 8x5=40, sino toparse en 20.
    assert score_muchos - score_pocos <= 20 - (2 * 5)


def test_datos_no_disponibles_por_scraping_bloqueado_no_penalizan_a_la_empresa():
    """Si no se pudo scrapear (ej. el entorno bloquea la salida de red), cta_visible/
    tiene_chat_vivo/formulario_largo llegan en None. None no es lo mismo que False:
    no hay que sumar puntos como si hubiéramos confirmado el problema."""
    empresa = _empresa(
        ahrefs={"domain_rating": 50},
        senales_ux={"cta_visible": None, "formulario_largo": None},
        scraping={"tiene_chat_vivo": None},
    )
    resultado = calcular_score(empresa)
    assert resultado["categoria"] == "baja"
    assert not any("no tiene chat en vivo" in r for r in resultado["razones"])
    assert not any("No se detectó un llamado a la acción" in r for r in resultado["razones"])
    assert any("no disponible" in r.lower() for r in resultado["razones"])


def test_armar_propuesta_usa_las_razones_del_score_sin_inventar_hallazgos():
    empresa = _empresa(
        ahrefs={"domain_rating": 12, "problemas_tecnicos": ["carga lenta en mobile"]},
        senales_ux={"cta_visible": False},
    )
    empresa["oportunidad"] = calcular_score(empresa)
    propuesta = armar_propuesta(empresa)

    assert propuesta["estado_envio"] == "borrador_generado"
    assert len(propuesta["diagnostico"]) == len(empresa["oportunidad"]["razones"]) - 0
    assert propuesta["servicio_sugerido"]  # no vacío para categoría alta/media


def test_armar_cuerpo_email_incluye_diagnostico_y_servicio():
    empresa = _empresa(ahrefs={"domain_rating": 12}, senales_ux={"cta_visible": False})
    empresa["oportunidad"] = calcular_score(empresa)
    empresa["propuesta"] = armar_propuesta(empresa)

    cuerpo = armar_cuerpo_email("Tienda Ejemplo", empresa)
    assert "Tienda Ejemplo" in cuerpo
    assert empresa["propuesta"]["servicio_sugerido"] in cuerpo
    for hallazgo in empresa["propuesta"]["diagnostico"]:
        assert hallazgo in cuerpo
