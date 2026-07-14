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
- [ ] B1. `discovery.py`: `marcar_fuente_apollo(df)` — adapta el resultado de Apollo a las columnas del esquema (nombre, dominio, país, industria, empleados, `fuente_descubrimiento="apollo"`).
- [ ] B2. `discovery.py`: `fallback_busqueda_web(mercado, pais, cantidad_faltante)` — scraping de resultados de búsqueda, respetando `robots.txt` y rate limit (plan, sección 4), marca `fuente_descubrimiento="fallback_busqueda_web"`.
- [ ] B3. `discovery.py`: `fallback_directorio_publico(mercado, pais, cantidad_faltante)` — ídem contra un directorio público, marca `fuente_descubrimiento="fallback_directorio_publico"`.
- [ ] B4. `discovery.py`: `combinar_resultados(df_apollo, fallbacks...)` — arma la tabla final que te muestro para elegir en el paso 5.
- [ ] B5. Test: con datos de ejemplo fijos (sin red), confirmar que la tabla combinada marca correctamente cada fuente.

## C. Auditoría por empresa (pasos 5-7 del spec)
- [ ] C1. `audit.py`: `detectar_tecnologia(url)` combinando `webtech` + heurísticas propias (CRO-específicas: chat en vivo, pixel de ads, tipo de checkout).
- [ ] C2. `audit.py`: `capturar_pantallas(url)` con Playwright — home + checkout/landing, guarda en `data/<lote-id>/capturas/<dominio>/`.
- [ ] C3. `audit.py`: `detectar_senales_ux(html)` — formulario largo, ausencia de CTA, pasos de checkout.
- [ ] C4. `audit.py`: `armar_json_empresa(datos_apollo, datos_ahrefs, datos_scraping)` — combina todo contra el esquema de `schema.py`, marcando `null`/"no disponible" donde falte un dato (nunca inventa).
- [ ] C5. Test: `test_audit_heuristics.py` con HTML de ejemplo guardado localmente (sin red) para C1 y C3.

## D. Score y propuesta (pasos 8-9 del spec)
- [ ] D1. `scoring.py`: `calcular_score(empresa_json)` — reglas documentadas (spec sección 8), devuelve `score`, `categoria`, `razones`.
- [ ] D2. Test: `test_scoring.py` con 3-4 casos de ejemplo (sitio rápido y prolijo → score bajo; sitio lento y sin CTA → score alto), confirmando que las razones coinciden con las reglas.
- [ ] D3. `proposal.py`: `armar_propuesta(empresa_json)` — diagnóstico (hallazgos concretos desde `razones`), servicio sugerido, llamado a la acción.

## E. Orquestación y estado (resumibilidad)
- [ ] E1. `pipeline.py`: `nueva_corrida(mercado, pais, tamaño)` — crea `data/<lote-id>/` y `state.json`.
- [ ] E2. `pipeline.py`: `guardar_estado(lote_id, dominio, paso)` / `listar_pendientes(lote_id)` — para poder retomar un lote cortado a la mitad.

## F. Primera corrida real (validación end-to-end)
- [ ] F1. Corro yo mismo, en la sesión, un lote de prueba chico (1 mercado + país, 3-5 empresas) llamando a Apollo/Ahrefs/Gmail reales, para validar que el pipeline completo funciona de punta a punta.
- [ ] F2. Reviso con vos la tabla, los JSON generados y un borrador de propuesta de ejemplo, antes de dar la v1 por terminada.
- [ ] F3. Confirmamos juntos que se cumplen los criterios de aceptación del spec (sección 5), uno por uno.

## G. Documentación
- [ ] G1. `README.md` del proyecto: cómo correr una búsqueda, cómo retomar un lote, dónde quedan los JSON/capturas, qué significa cada campo del esquema.

---
**Nota:** la interfaz visual y la Rutina de notificación push (`BACKLOG.md`) no están acá — son proyectos/tareas separados, para después de validar esta v1.
