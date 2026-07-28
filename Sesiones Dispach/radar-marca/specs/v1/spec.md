# Spec — Radar de Marca (v1)

Estado: **borrador, pendiente de tu aprobación** (checkpoint SDD fase 1).

## 1. Qué hay que lograr y por qué

Una skill que dispara un monitoreo de tendencias en redes, palabras clave y
menciones de marca (vía un agente), y deja el resultado en un **"centro de
noticias"**: un artifact web que se actualiza en el mismo link cada vez que
hay una monitorización nueva — nunca genera un link distinto.

Objetivo: enterarte de qué se dice de tu marca/keywords sin tener que pedirlo
a mano cada vez, y tener siempre el mismo lugar para mirarlo.

## 2. Alcance de esta versión (v1)

**Sí incluye:**
- Una skill (`.claude/skills/radar-marca/`) que, al invocarse, dispara un
  **agente** (vía la herramienta Agent) para investigar.
- El agente usa **Ahrefs Brand Radar** (menciones, share of voice, respuestas
  de IA) y **Ahrefs Social Media** (posts, canales, métricas) — ya conectados
  a tu cuenta, sin scraping propio.
- Un archivo de configuración (`config.json`) con marca, competidores y
  palabras clave — **arranca con datos de ejemplo/placeholder**, vos lo
  completás con los datos reales antes de la primera corrida en serio.
- El "centro de noticias" (artifact HTML) con 4 secciones (ver punto 4).
- Una **Rutina** programada que dispara el monitoreo automáticamente,
  **atada a esta misma sesión** (self-bind), para que cada corrida
  republique al mismo artifact y el link nunca cambie.

**No incluye (queda para después):**
- Carga de la marca/competidores/keywords reales (la hacemos vos y yo juntos
  antes de la primera corrida real, no es parte de "construir la
  estructura").
- Envío de notificaciones (push, mail) cuando hay novedades — se puede
  agregar después como una tarea aparte.
- Mover el monitoreo a una sesión dedicada separada de esta conversación
  (ver sección 6, queda anotado para más adelante si esta sesión se llena).

## 3. Flujo, paso a paso

1. Una **Rutina** (Routine) con trigger de horario (a definir la frecuencia
   en PLAN) se dispara y manda un mensaje a **esta misma sesión**
   ("corré el monitoreo de marca").
2. Yo invoco la skill `radar-marca`.
3. La skill me instruye a lanzar un **Agente** (herramienta Agent) con un
   prompt autocontenido: "investigá menciones/tendencias de \<marca\>,
   \<competidores\>, \<keywords\> usando Ahrefs Brand Radar y Social Media,
   y devolveme los hallazgos estructurados".
4. El agente devuelve los hallazgos (menciones recientes, serie de tiempo,
   comparación vs. competidores, top keywords/temas).
5. Yo actualizo un archivo de datos del reporte (`reporte/datos.json`) con
   lo nuevo, sin perder el historial de corridas anteriores (para que la
   sección de "tendencia en el tiempo" tenga con qué comparar).
6. Regenero el HTML del "centro de noticias" a partir de esos datos, y lo
   publico con el **mismo `file_path`** de siempre — como estamos en la
   misma conversación (Rutina atada a esta sesión), el artifact se
   actualiza en el mismo link, no se crea uno nuevo.

## 4. Contenido del "centro de noticias" (las 4 secciones que pediste)

1. **Feed de menciones recientes** — tipo timeline de noticias: últimas
   menciones de marca/keywords, con fecha y fuente.
2. **Tendencia en el tiempo** — gráfico de volumen de menciones a lo largo
   de las corridas, para ver si sube o baja.
3. **Comparación con competidores (share of voice)** — cuánto se habla de
   tu marca vs. la competencia configurada.
4. **Top palabras clave / temas** — qué términos/temas dominan en cada
   corrida.

## 5. Criterios de aceptación

- [ ] La skill `radar-marca` existe y, al invocarla, dispara un agente real
      (no simula los datos).
- [ ] El agente usa Ahrefs Brand Radar/Social Media — no inventa menciones
      ni números si la fuente no devuelve datos (mismo principio de
      "nunca fabricar" del proyecto anterior).
- [ ] Cada corrida nueva republica el **mismo** artifact (mismo link),
      nunca uno distinto.
- [ ] El centro de noticias muestra las 4 secciones, aunque sea con datos
      de ejemplo mientras no carguemos la marca real.
- [ ] La Rutina programada dispara el monitoreo sin que yo tenga que
      pedirlo a mano.

## 6. Preguntas que quedan para PLAN (no bloquean el spec)

- Frecuencia exacta de la Rutina (¿diaria? ¿semanal?).
- Formato concreto de `config.json` y `reporte/datos.json`.
- Cómo se ve exactamente el HTML (tipografía, layout) del centro de
  noticias — se define con el mismo cuidado de diseño que usamos en los
  otros artifacts.
- Qué pasa si en algún momento esta sesión deja de existir o se archiva
  (la Rutina atada a "esta sesión" dejaría de tener dónde resumir) — anotar
  como riesgo conocido, no bloqueante para v1.
