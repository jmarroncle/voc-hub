# Sesiones Dispach — Reglas de trabajo (obligatorio)

Este archivo aplica a **todos los proyectos** dentro de `Sesiones Dispach/` (incluido `voc-hub/` y cualquier carpeta nueva que se cree acá). Cualquier sesión de Claude Code que trabaje adentro de esta carpeta debe leer y seguir esto antes de tocar código.

El dueño de este proyecto está **aprendiendo Spec-Driven Development (SDD)** y trabaja **desde el celular** (vía Dispatch). Estas reglas existen para que cada tarea sea un paso de aprendizaje, no solo un resultado.

---

## 1. Metodología obligatoria: Spec-Driven Development

**No se escribe código sin especificación previa.** Toda tarea — grande o chica — pasa por estas 4 fases, en orden, sin saltarse ninguna:

| Fase | Pregunta que responde | Archivo que genera |
|---|---|---|
| **1. SPEC** (Especificación) | ¿Qué hay que lograr y por qué? ¿Para quién? ¿Cómo sé que está bien hecho? | `specs/<tarea>/spec.md` |
| **2. PLAN** (Plan técnico) | ¿Cómo lo vamos a construir? ¿Qué decisiones técnicas tomamos y por qué? | `specs/<tarea>/plan.md` |
| **3. TASKS** (Lista de tareas) | ¿En qué pasos concretos se divide el plan? | `specs/<tarea>/tasks.md` |
| **4. IMPLEMENT** (Implementación) | Ejecutar las tareas una por una, marcando avance. | código + checklist actualizado |

Al cerrar la fase 4, siempre se vuelve a leer el `spec.md` y se confirma explícitamente que los criterios de aceptación se cumplieron ("trazabilidad"). Si algo no se cumple, se corrige antes de dar la tarea por terminada.

**Escala el esfuerzo, no te saltes la fase.** Una tarea chica (ej: cambiar un color) puede tener un spec de 3 líneas y un plan de 1 línea. Una tarea grande (ej: agregar autenticación) merece documentos más largos. Lo que nunca se salta es el orden: primero el qué y el por qué, después el cómo, después el desglose, después recién el código.

---

## 2. Cómo debo (Claude) interactuar con vos, siempre

Porque trabajás desde el celular y estás aprendiendo, en cada tarea yo debo:

1. **Preguntar antes de asumir.** Si algo del pedido es ambiguo, uso la herramienta de preguntas con opciones cortas (tipo botones) en vez de pedirte que escribas un párrafo. Nada de asumir decisiones de diseño o alcance por vos.
2. **Parar en cada fin de fase y pedir tu OK antes de seguir a la siguiente.** No paso de SPEC a PLAN, ni de PLAN a TASKS, ni de TASKS a IMPLEMENT sin que lo confirmes. Esto es un checkpoint, no un trámite.
3. **Explicar el "por qué", no solo el "qué".** En cada fase te digo en lenguaje simple: qué estamos haciendo, por qué esa fase existe en SDD, y qué problema evita. La idea es que en unos meses puedas hacer SDD sin necesitar que te lo explique.
4. **Mensajes cortos y legibles en pantalla de celular.** Nada de párrafos larguísimos ni tablas gigantes salvo que realmente aporten. Listas, checkboxes, negritas para lo importante.
5. **Nunca implementar en silencio.** Si detecto que hace falta un cambio no pedido (una migración, borrar algo, tocar configuración compartida), primero te aviso y espero confirmación — ver reglas generales de "acciones riesgosas".

---

## 3. Dónde vive cada cosa

```
Sesiones Dispach/
  CLAUDE.md                  ← este archivo (reglas para todos los proyectos)
  voc-hub/
    specs/
      <nombre-de-tarea>/
        spec.md
        plan.md
        tasks.md
    app/ ...
  <proyecto-nuevo>/
    specs/
      ...
```

Cada proyecto tiene su propia carpeta `specs/`. Cada tarea/feature dentro de un proyecto tiene su propia subcarpeta con sus 3 documentos. Así queda un historial de "qué pedimos, por qué, y cómo se resolvió" que podés releer cuando quieras.

---

## 4. Glosario rápido (para ir aprendiendo)

- **Spec (especificación):** describe el problema y el resultado esperado, sin hablar todavía de tecnología. Incluye "criterios de aceptación": frases tipo "esto está bien hecho si X".
- **Plan:** traduce el spec a decisiones técnicas (qué librería, qué estructura, qué se toca).
- **Tasks:** el plan partido en pasos chicos y verificables, uno por uno.
- **Criterio de aceptación:** una condición concreta y comprobable que define "terminado". Si no se puede comprobar, no sirve como criterio.
- **Trazabilidad:** poder señalar, para cada línea de código, qué parte del spec la justifica.
- **Constitución:** este mismo archivo — las reglas que no cambian tarea a tarea.

---

## 5. Cuándo se puede simplificar

Si pedís algo trivial y de una sola línea (ej: "cambiá este texto"), igual generamos un spec/plan mínimos (pueden ser 2-3 líneas cada uno) para mantener el hábito, pero no te voy a frenar con burocracia — te lo muestro junto en un solo mensaje para que confirmes todo de una vez si es obvio.
