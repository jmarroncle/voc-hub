# Backlog de ideas — Sesiones Dispach

Ideas que surgieron en el chat pero que decidimos hacer **más adelante**, no ahora. Cuando quieras retomar una, decime "hagamos la idea de X" y la convertimos en una tarea real siguiendo SDD (spec → plan → tasks → implement).

---

## 1. Rutina: revisor automático de PRs contra las reglas de SDD

- **Estado:** pendiente, no iniciada.
- **Proyecto:** voc-hub (o cualquiera dentro de `Sesiones Dispach/`).
- **Qué haría:** una Rutina de Claude Code con trigger de GitHub (`pull_request.opened`) que revise cada PR nuevo y chequee si respeta lo que pide `Sesiones Dispach/CLAUDE.md`:
  - ¿Existe `specs/<tarea>/spec.md` para el cambio?
  - ¿Existe `plan.md` con las decisiones técnicas?
  - ¿`tasks.md` está con sus checkboxes marcados?
  - Si falta algo, deja un comentario en el PR señalando qué falta (no bloquea, solo avisa).
- **Por qué la anotamos:** te gustó la idea de automatizar el control de la metodología SDD en vez de acordarte de revisarlo a mano cada vez.
- **Para cuando la retomemos, hay que definir:**
  - ¿Debe bloquear el merge si falta algo, o solo comentar?
  - ¿Corre en todos los repos de la carpeta o solo en algunos?
  - ¿Quién configura la GitHub App de Claude en el repo (paso previo obligatorio para triggers de GitHub)?

---

<!-- Agregar próximas ideas debajo de esta línea -->
