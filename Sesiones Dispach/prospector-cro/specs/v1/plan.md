# Plan — Prospector CRO (v1)

Estado: **borrador, pendiente de tu aprobación** (checkpoint SDD fase 2).
Basado en: `spec.md` de esta misma carpeta.

## 1. Arquitectura general

**El agente orquesta, Python hace el trabajo pesado de datos.**

- Apollo.io, Ahrefs y Gmail ya están conectados a esta cuenta → los llamo yo (el agente) durante la sesión o una Rutina, en el momento del pipeline que corresponda. No se duplican credenciales en ningún script.
- Todo lo demás (scraping propio, armar JSON, calcular score, redactar propuesta, validar datos) es código Python/pandas en el repo, reutilizable y testeable, que yo ejecuto con Bash paso a paso.
- Esto es lo que lo hace "agéntico": no es un cron corriendo solo — es un pipeline que yo voy ejecutando y donde vos elegís (paso 5) y aprobás (paso 10) en el medio.

## 2. Estructura de carpetas

```
Sesiones Dispach/prospector-cro/
  specs/v1/            spec.md, plan.md, tasks.md
  prospector/
    discovery.py       fallback de búsqueda web + directorios públicos, marcado por tipo
    audit.py           scraping propio: tecnología, capturas, señales UX/CRO
    scoring.py         reglas de puntaje de oportunidad (explicables)
    proposal.py        arma el texto de la propuesta por empresa
    pipeline.py        funciones que uso yo para encadenar los pasos y guardar estado
    schema.py          valida cada JSON de empresa contra el esquema del spec
  data/                JSON por empresa, capturas, estado del lote (gitignored — son datos de terceros)
  tests/               pruebas de scoring, schema y heurísticas (no de las llamadas a Apollo/Ahrefs/Gmail)
```

`data/` va a `.gitignore`: son datos de empresas de terceros recolectados para prospección, no código del proyecto, y no corresponde versionarlos en el repo.

## 3. Librerías (respondiendo tu pregunta de "qué existe")

| Necesidad | Librería | Por qué |
|---|---|---|
| Tablas y JSON | `pandas` | Ya lo pediste vos; estándar para esto. |
| Scraping liviano (HTML, fallback de búsqueda, señales UX) | `requests` + `beautifulsoup4` | Gratis, simple, suficiente para HTML estático. |
| Capturas de pantalla y sitios con JS pesado | `playwright` | Ya viene preinstalado en este entorno (Chromium listo), gratis, no hay que instalar nada extra. |
| Detección de tecnología | heurísticas propias **+** `webtech` (librería libre, offline, sin costo) | Elegiste "ambos, gratis y fácil de integrar": `webtech` da cobertura amplia (CMS, frameworks, analytics) y las heurísticas propias cubren lo específico de CRO que a una librería genérica no le importa (ej. tipo de checkout, chat en vivo). |
| Validar el JSON de cada empresa | `jsonschema` | Gratis, evita que se cuele un dato mal formado o inventado. |

## 4. Límites éticos del scraping (para que quede escrito, no implícito)

- Se respeta `robots.txt` de cada sitio.
- User-agent propio e identificable (no se hace pasar por un navegador para evadir bloqueos).
- Rate limit por dominio (ej. no más de 1 request por segundo al mismo sitio).
- Solo páginas públicas (home, landing, checkout visible sin login) — nunca se intenta sortear logins, paywalls o CAPTCHAs.
- Si un sitio bloquea el acceso, se marca `"no disponible"` en el JSON — no se reintenta agresivamente ni se simula humano para colarse.

## 5. Cómo se resuelven los puntos que quedaron abiertos en el spec

- **Capturas de pantalla →** Playwright, headless, dos capturas por empresa (home + checkout/landing).
- **Detección de tecnología →** combinar `webtech` + heurísticas propias (definido arriba).
- **Dónde se guardan los datos →** `data/<lote-id>/empresas/<dominio>.json` + `data/<lote-id>/capturas/<dominio>/*.png`, todo local al repo y gitignored.
- **Resumibilidad →** cada lote tiene `data/<lote-id>/state.json` con qué empresas ya se procesaron y en qué paso quedaron (descubierta / auditada / puntuada / con propuesta / con borrador). Si se corta a la mitad, se retoma desde ahí en vez de repetir todo.

## 6. Flujo técnico (mapeado a los módulos)

1. Yo llamo a Apollo (`mcp__Apollo_io__*`) con mercado/país/tamaño → DataFrame de pandas.
2. Si faltan empresas, `discovery.py` corre los fallbacks (búsqueda web / directorios), marcando el tipo en cada fila.
3. Te muestro la tabla combinada, elegís (paso 5 del spec) qué dominios investigar.
4. Por cada dominio elegido: yo llamo a Ahrefs (`mcp__Ahrefs__*`) + `audit.py` corre el scraping propio → arma el JSON, `schema.py` lo valida.
5. `scoring.py` calcula puntaje + razones para cada JSON.
6. `proposal.py` redacta el borrador de propuesta usando el score y sus razones.
7. Con tu aprobación del lote, yo creo los borradores en Gmail (`mcp__Gmail__create_draft`) — nunca los envío.

## 7. Fuera de este plan (siguen siendo parte del proyecto, pero después)

- Interfaz visual (wizard).
- La Rutina de notificación push (ya está en `BACKLOG.md`).
- Tests de integración reales contra Apollo/Ahrefs/Gmail (se prueban a mano en la primera corrida real, no con mocks todavía).
