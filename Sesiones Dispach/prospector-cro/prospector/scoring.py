"""Score de oportunidad de venta (spec sección 3, paso 8): reglas explícitas, nunca caja negra."""

UMBRAL_ALTA = 70
UMBRAL_MEDIA = 40

PUNTOS_DR_BAJO = 25
PUNTOS_DR_MEDIO = 10
PUNTOS_POR_PROBLEMA_TECNICO = 5
TOPE_PUNTOS_PROBLEMAS_TECNICOS = 20
PUNTOS_SIN_CTA = 20
PUNTOS_FORMULARIO_LARGO = 15
PUNTOS_CHECKOUT_LARGO = 15
PASOS_CHECKOUT_RECOMENDADOS = 3
PUNTOS_SIN_CHAT = 5


def calcular_score(empresa_json: dict) -> dict:
    """Calcula score (0-100), categoría y las razones legibles de cada punto sumado.

    Reglas (documentadas acá para que sean auditables, no una caja negra):
    - Domain Rating bajo (<20): +25. Entre 20 y 40: +10. Si no hay dato, no suma.
    - Cada problema técnico de Ahrefs: +5, tope +20 en total.
    - Sin CTA visible: +20.
    - Formulario principal largo (>6 campos): +15.
    - Checkout con más de 3 pasos: +15.
    - Sin chat en vivo: +5.
    """
    ahrefs = empresa_json["auditoria"]["ahrefs"]
    scraping = empresa_json["auditoria"]["scraping"]
    senales_ux = scraping["senales_ux"]

    puntos = 0
    razones = []

    dr = ahrefs.get("domain_rating")
    if dr is None:
        razones.append("Domain Rating no disponible: no se pudo evaluar este factor.")
    elif dr < 20:
        puntos += PUNTOS_DR_BAJO
        razones.append(f"Domain Rating bajo ({dr}): poca autoridad SEO construida.")
    elif dr < 40:
        puntos += PUNTOS_DR_MEDIO
        razones.append(f"Domain Rating medio ({dr}): autoridad SEO mejorable.")

    problemas = ahrefs.get("problemas_tecnicos") or []
    if problemas:
        puntos_problemas = min(len(problemas) * PUNTOS_POR_PROBLEMA_TECNICO, TOPE_PUNTOS_PROBLEMAS_TECNICOS)
        puntos += puntos_problemas
        razones.append(f"Se detectaron {len(problemas)} problema(s) técnico(s) en Ahrefs (ej: \"{problemas[0]}\").")

    cta_visible = senales_ux.get("cta_visible")
    if cta_visible is False:
        puntos += PUNTOS_SIN_CTA
        razones.append("No se detectó un llamado a la acción (CTA) claro en el sitio.")
    elif cta_visible is None:
        razones.append("No se pudo revisar el CTA del sitio (scraping no disponible).")

    formulario_largo = senales_ux.get("formulario_largo")
    if formulario_largo is True:
        puntos += PUNTOS_FORMULARIO_LARGO
        razones.append("El formulario principal tiene más de 6 campos, lo que genera fricción.")
    elif formulario_largo is None:
        razones.append("No se pudo revisar el formulario del sitio (scraping no disponible).")

    pasos_checkout = senales_ux.get("pasos_checkout")
    if pasos_checkout is not None and pasos_checkout > PASOS_CHECKOUT_RECOMENDADOS:
        puntos += PUNTOS_CHECKOUT_LARGO
        razones.append(
            f"El checkout tiene {pasos_checkout} pasos, más de los {PASOS_CHECKOUT_RECOMENDADOS} recomendados."
        )

    tiene_chat = scraping.get("tiene_chat_vivo")
    if tiene_chat is False:
        puntos += PUNTOS_SIN_CHAT
        razones.append("El sitio no tiene chat en vivo, una herramienta simple de conversión.")
    elif tiene_chat is None:
        razones.append("No se pudo revisar si el sitio tiene chat en vivo (scraping no disponible).")

    score = min(puntos, 100)
    if score >= UMBRAL_ALTA:
        categoria = "alta"
    elif score >= UMBRAL_MEDIA:
        categoria = "media"
    else:
        categoria = "baja"

    return {"score": score, "categoria": categoria, "razones": razones}
