# Tasks — Prospector CRO (v1)

Estado: **borrador, pendiente de tu aprobación** (checkpoint SDD fase 3).
Basado en: `spec.md` + `plan.md` de esta misma carpeta.

Orden de ejecución. Cada tarea se marca `[x]` cuando está hecha y verificada (no solo escrita).

## A. Base del proyecto
- [x] A1. Crear estructura de carpetas (`prospector/`, `data/`, `tests/`) y `requirements.txt` (pandas, requests, beautifulsoup4, playwright, webtech, jsonschema, pytest).
- [x] A2. Agregar `data/` al `.gitignore` del proyecto (son datos de terceros, no código).
- [x] A3. `schema.py`: definir el esquema del JSON de empresa (del spec, sección 4) y `validar_empresa(json)` con `jsonschema`.
- [x] A4. Test: `test_schema.py` — un JSON válido pasa, uno con un campo inventado/mal tipado falla. (4/4 tests verdes)

## B. Descubrimiento (paso 4 del spec)
- [x] B1. `discovery.py`: `marcar_fuente_apollo(df)` — adapta el resultado de Apollo a las columnas del esquema (nombre, dominio, país, industria, empleados, `fuente_descubrimiento="apollo"`).
- [x] B2. `discovery.py`: `fallback_busqueda_web(mercado, pais, cantidad_faltante)` — scraping de resultados de búsqueda, respetando `robots.txt` y rate limit (plan, sección 4), marca `fuente_descubrimiento="fallback_busqueda_web"`.
- [x] B3. `discovery.py`: `fallback_directorio_publico(mercado, pais, cantidad_faltante)` — ídem contra un directorio público, marca `fuente_descubrimiento="fallback_directorio_publico"`. (Nota: `DIRECTORIOS_POR_PAIS` arranca vacío; sin entrada configurada, devuelve 0 resultados en vez de inventar una fuente — hay que cargar directorios reales cuando se use.)
- [x] B4. `discovery.py`: `combinar_resultados(df_apollo, fallbacks...)` — arma la tabla final que te muestro para elegir en el paso 5.
- [x] B5. Test: con datos de ejemplo fijos (sin red), confirmar que la tabla combinada marca correctamente cada fuente. (5/5 tests verdes)

## C. Auditoría por empresa (pasos 5-7 del spec)
- [x] C1. `audit.py`: heurísticas propias de tecnología (`detectar_tecnologia_heuristica`, `tiene_chat_vivo`). (Nota: la combinación con `webtech` real se ejercita en la corrida real del Grupo F, porque necesita red.)
- [x] C2. `audit.py`: `capturar_pantallas(url, url_checkout_o_landing, carpeta_destino)` con Playwright (Chromium preinstalado) — home + checkout/landing. Se ejercita en el Grupo F (necesita red/navegador real).
- [x] C3. `audit.py`: `detectar_senales_ux(html)` — formulario largo, ausencia de CTA, pasos de checkout.
- [x] C4. `audit.py`: `armar_json_empresa(...)` — combina todo contra el esquema de `schema.py`, marcando `null`/"no disponible" donde falte un dato (nunca inventa).
- [x] C5. Test: `test_audit_heuristics.py` con HTML de ejemplo guardado localmente (sin red) para C1, C3 y C4. (8/8 tests verdes, 17/17 en total)

## D. Score y propuesta (pasos 8-9 del spec)
- [x] D1. `scoring.py`: `calcular_score(empresa_json)` — reglas documentadas (spec sección 8), devuelve `score`, `categoria`, `razones`.
- [x] D2. Test: `test_scoring.py` con casos de ejemplo (sitio prolijo → score bajo; sitio lento y sin CTA → score alto; DR no disponible; tope de puntos por problemas técnicos), confirmando que las razones coinciden con las reglas.
- [x] D3. `proposal.py`: `armar_propuesta(empresa_json)` + `armar_cuerpo_email(...)` — diagnóstico (hallazgos concretos desde `razones`, sin inventar), servicio sugerido, llamado a la acción. (6/6 tests verdes, 23/23 en total)

## E. Orquestación y estado (resumibilidad)
- [x] E1. `pipeline.py`: `nueva_corrida(mercado, pais, tamaño)` — crea `data/<lote-id>/` y `state.json`.
- [x] E2. `pipeline.py`: `guardar_estado(lote_id, dominio, paso)` / `listar_pendientes(lote_id)` — para poder retomar un lote cortado a la mitad. (5/5 tests verdes, 28/28 en total, incluye test de "reinicio" simulado)

## F. Primera corrida real (validación end-to-end)
- [x] F1. Corrida real con ecommerce/Argentina/11-50: Apollo devolvió 3 empresas reales (1 crédito gastado), Ahrefs Domain Rating real (gratis) para las 3. **Hallazgos importantes** (ver abajo). JSON de cada empresa generado y validado contra el esquema, guardado en `data/20260714-212421-abb2af/empresas/`.
- [ ] F2. Reviso con vos la tabla, los JSON generados y un borrador de propuesta de ejemplo, antes de dar la v1 por terminada. **Pausado**: las propuestas quedaron muy débiles (una con 0 hallazgos) por las limitaciones de abajo — a la espera de tu decisión antes de crear los borradores en Gmail.
- [ ] F3. Confirmamos juntos que se cumplen los criterios de aceptación del spec (sección 5), uno por uno.

### Hallazgos reales de esta corrida (no estaban previstos en el plan)
1. **Ahrefs, plan insuficiente**: `site-explorer-metrics` (tráfico) y `site-audit-issues` (problemas técnicos) devuelven "Insufficient plan" con la cuenta conectada. Solo funciona el Domain Rating gratuito (`public-domain-rating-free`).
2. **Scraping propio bloqueado por la red del entorno**: este entorno cloud (acceso "Trusted") solo permite un listado fijo de dominios (registries, APIs). Los sitios de las empresas devuelven 403 del proxy — no es un bug del código (que falla "cerrado" correctamente), es la política de red del entorno.
3. **Bug real encontrado y corregido**: el esquema no permitía `null` en `tiene_chat_vivo`/`formulario_largo`/`cta_visible`, y el scoring trataba "no disponible" como `False` (penalizaba sin datos). Corregido en `schema.py` y `scoring.py`, con test de regresión agregado.
4. **Consecuencia de negocio**: sin tráfico/problemas técnicos de Ahrefs ni señales de scraping, las propuestas generadas son débiles (EcomExperts quedó con 0 hallazgos). No cumplen todavía el objetivo de "investigación interesante" del pedido original.

## G. Documentación
- [ ] G1. `README.md` del proyecto: cómo correr una búsqueda, cómo retomar un lote, dónde quedan los JSON/capturas, qué significa cada campo del esquema.

---
**Nota:** la interfaz visual y la Rutina de notificación push (`BACKLOG.md`) no están acá — son proyectos/tareas separados, para después de validar esta v1.
