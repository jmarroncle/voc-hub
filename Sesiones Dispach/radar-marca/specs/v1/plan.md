# Plan — Radar de Marca (v1)

Estado: **borrador, pendiente de tu aprobación** (checkpoint SDD fase 2).
Basado en: `spec.md` de esta misma carpeta.

## 1. Dónde vive cada cosa

```
Sesiones Dispach/radar-marca/
  specs/v1/                    spec.md, plan.md, tasks.md
  .claude/skills/radar-marca/  SKILL.md (solo aplica a este proyecto)
  config.json                  marca, competidores, keywords (arranca con demo)
  reporte/
    datos.json                 historial acumulado de corridas (hasta 30)
    centro-de-noticias.html    se regenera cada corrida, mismo archivo siempre
```

La skill vive **adentro del proyecto** (no en `Sesiones Dispach/.claude/skills/`
como `glosario`), porque es específica de este monitoreo — no tiene sentido
que aparezca disponible en `voc-hub` o `prospector-cro`.

## 2. La Rutina

- **Frecuencia:** diaria.
- **A quién dispara:** a **esta misma sesión** (self-bind) — así cada corrida
  es la misma conversación, y republicar el artifact con el mismo
  `file_path` mantiene el mismo link, sin trabajo extra de "recordar" una URL.
- **Prompt que manda la Rutina:** algo simple, tipo *"Ejecutá la skill
  radar-marca para generar el monitoreo de hoy"* — la skill ya sabe qué hacer.
- **Riesgo conocido (ya anotado en el spec):** si esta sesión se archiva o
  deja de existir, la Rutina atada a ella se queda sin dónde resumir. No lo
  resolvemos en v1; si pasa, se nota fácil (la Rutina falla) y se re-ata a
  una sesión nueva.
- Horario exacto: la armo para las 9:00 (hora del servidor) — si al ver la
  primera corrida el horario no te queda cómodo, lo ajustamos con
  `update_trigger`.

## 3. El agente

- Se dispara con la herramienta **Agent**, `subagent_type: general-purpose`
  (necesita poder llamar herramientas MCP de Ahrefs).
- Corre **en primer plano** (`run_in_background: false`): necesito su
  resultado antes de poder armar el reporte en la misma corrida.
- Prompt autocontenido (la skill lo arma con los datos de `config.json`):
  "Investigá menciones, tendencias y comparación con competidores para
  \<marca\>, \<competidores\>, \<keywords\> usando las herramientas de Ahrefs
  Brand Radar y Social Media. Devolveme: menciones recientes con fecha y
  fuente, volumen total, comparación porcentual vs. cada competidor, y los
  temas/keywords más repetidos. Si una fuente no tiene datos para algo,
  decilo explícitamente — no inventes números."

## 4. Formato de los datos

`config.json`:
```json
{
  "marca": "Marca de Ejemplo S.A.",
  "competidores": ["Competidor Uno", "Competidor Dos"],
  "keywords": ["palabra clave 1", "palabra clave 2"],
  "demo": true
}
```
`demo: true` marca que todavía no cargaste los datos reales — el centro de
noticias muestra un aviso mientras este flag siga en `true`.

`reporte/datos.json` (se le agrega una entrada por corrida, tope 30):
```json
{
  "corridas": [
    {
      "fecha": "2026-07-16T09:00:00Z",
      "menciones_recientes": [
        {"fecha": "...", "fuente": "...", "texto": "...", "url": "..."}
      ],
      "volumen_total": 42,
      "share_of_voice": {"Marca de Ejemplo S.A.": 55, "Competidor Uno": 30, "Competidor Dos": 15},
      "top_keywords": ["...", "..."]
    }
  ]
}
```

## 5. El "centro de noticias" (artifact)

- Tratamiento de **dashboard/UI**, no de documento: se escanea, no se lee de
  arriba a abajo. Superficie el resumen (share of voice, tendencia) antes
  que el detalle (feed de menciones).
- Las 4 secciones del spec, cada una diseñada con el mismo cuidado que los
  artifacts anteriores (voy a invocar la skill de diseño de artifacts antes
  de construir el HTML, como corresponde).
- Mientras `config.json` tenga `demo: true`, un aviso visible arriba: "Datos
  de ejemplo — todavía no cargaste tu marca real".
- Se republica siempre con el mismo `file_path`, para mantener el mismo link.

## 6. Qué falta para la primera corrida real

Antes de dar la v1 por terminada, vos y yo completamos `config.json` con tu
marca real, competidores y keywords — recién ahí corremos el primer
monitoreo "de verdad" y confirmamos los criterios de aceptación del spec.
