---
name: glosario
description: Mantiene Sesiones Dispach/GLOSARIO.md al día. Úsala cada vez que se explique o mencione un término nuevo de Git, GitHub, SDD (spec/plan/tasks) o de Claude Code (Routine, Dispatch, Skill, Rutina, Trigger, etc.) en la conversación, para agregarlo al glosario personal del usuario si todavía no está. También se invoca manualmente con /glosario para ver el estado del archivo o forzar una revisión.
---

# Glosario personal

El usuario está aprendiendo a programar y pidió explícitamente que se le arme, solo,
un apunte de todos los términos técnicos que va viendo en las sesiones. Este archivo
es ese apunte: `Sesiones Dispach/GLOSARIO.md`.

## Cuándo actuar (automático, sin que el usuario lo pida)

Cada vez que en la conversación se explique un término nuevo que encaje en alguna
de estas categorías:
- Git / GitHub: commit, branch, push, pull, diff, merge, rebase, PR, issue, fork,
  tag, remote, clone, checkout, stash, etc.
- SDD: spec, plan, tasks, criterio de aceptación, trazabilidad, constitución.
- Claude Code / Dispatch: Routine (Rutina), trigger, Dispatch, skill, sesión,
  entorno (environment), conector (MCP), Cowork, etc.

Antes de agregarlo:
1. Leé `Sesiones Dispach/GLOSARIO.md` (si no existe, creálo con el encabezado de la
   plantilla de abajo).
2. Fijate si el término ya está (buscá el encabezado `## Término`). Si ya está, no
   dupliques — como mucho, mejorá la definición existente si la nueva explicación
   suma algo que no estaba.
3. Si es nuevo, agregalo al final del archivo con este formato:

   ```
   ## Nombre del término
   Definición corta, en criollo, tal como se la explicaste en el chat.
   _Agregado: AAAA-MM-DD_
   ```

4. Commiteá el cambio junto con lo que estés haciendo en ese momento (no hace
   falta un commit aparte solo para esto, salvo que el usuario no esté tocando
   código en esa sesión — en ese caso sí hacé un commit propio tipo
   `docs: agregar "X" al glosario`).

No se lo menciones al usuario cada vez que lo hagas — es un efecto secundario
silencioso de la conversación, no una tarea que reporte cada vez. Si el usuario
pregunta o usa `/glosario`, ahí sí mostrale el estado del archivo o los términos
agregados recientemente.

## Plantilla para crear el archivo si no existe

```markdown
# Glosario personal

Términos que fui aprendiendo en las sesiones de "Sesiones Dispach", explicados
en criollo. Se arma solo, a medida que aparecen en las conversaciones.

---
```
