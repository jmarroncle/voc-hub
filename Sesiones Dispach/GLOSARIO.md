# Glosario personal

Términos que fui aprendiendo en las sesiones de "Sesiones Dispach", explicados
en criollo. Se arma solo, a medida que aparecen en las conversaciones (ver la
skill `glosario` en `.claude/skills/`).

---

## Commit
Una foto fija de un cambio, con un mensaje que explica qué hiciste y por qué.
_Agregado: 2026-07-15_

## Branch (rama)
Una copia paralela del proyecto para probar cosas sin tocar la versión principal.
_Agregado: 2026-07-15_

## Push
Subir tus commits locales al repositorio remoto, donde los demás los ven.
_Agregado: 2026-07-15_

## Diff
La comparación línea por línea entre dos versiones: qué se agregó (+) y qué se
borró (−).
_Agregado: 2026-07-15_

## PR (Pull Request)
Una propuesta formal para fusionar tu rama a la principal, abierta a revisión
antes de integrarse.
_Agregado: 2026-07-15_

## Merge
Fusionar los cambios de una rama a otra, uniendo el trabajo para siempre.
_Agregado: 2026-07-15_

## Repo (Repositorio)
La carpeta completa de un proyecto, con todo su historial de commits.
_Agregado: 2026-07-15_

## Main
La rama principal: la versión "oficial" del proyecto.
_Agregado: 2026-07-15_

## Spec (especificación)
Describe el problema y el resultado esperado de una tarea, sin hablar todavía
de tecnología. Incluye los "criterios de aceptación".
_Agregado: 2026-07-15_

## Plan
Traduce el spec a decisiones técnicas: qué librería, qué estructura, qué se toca.
_Agregado: 2026-07-15_

## Tasks
El plan partido en pasos chicos y verificables, uno por uno.
_Agregado: 2026-07-15_

## Criterio de aceptación
Una condición concreta y comprobable que define "esto está terminado". Si no se
puede comprobar, no sirve como criterio.
_Agregado: 2026-07-15_

## Trazabilidad
Poder señalar, para cada línea de código, qué parte del spec la justifica.
_Agregado: 2026-07-15_

## Constitución
Las reglas que no cambian tarea a tarea — en este proyecto, es el archivo
`Sesiones Dispach/CLAUDE.md`.
_Agregado: 2026-07-15_

## Dispatch
Una conversación persistente con Claude (en la pestaña Cowork) a la que le
mandás una tarea desde el celular. Ella decide si la resuelve ahí mismo o si
abre una sesión de Claude Code para hacerlo, y te avisa por notificación
cuando termina o necesita tu aprobación.
_Agregado: 2026-07-15_

## Routine (Rutina)
Una configuración guardada de Claude Code (prompt + repos + conectores) que
corre sola, disparada por un horario, un evento de GitHub, o una llamada API —
sin pedir permisos durante la ejecución.
_Agregado: 2026-07-15_

## Evento de GitHub (trigger)
Un disparador de Rutina que arranca una sesión automáticamente cuando pasa
algo en un repo (ej: se abre un Pull Request, se publica una Release), con
filtros opcionales (autor, rama, labels, etc.) para afinar cuándo sí y cuándo no.
_Agregado: 2026-07-15_

## Skill
Un archivo de instrucciones (`SKILL.md`) que le enseña a Claude un procedimiento
específico. Se puede invocar a mano con `/nombre-skill`, o Claude la usa sola
cuando detecta que aplica.
_Agregado: 2026-07-15_
