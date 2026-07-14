# Prospector CRO

Herramienta de prospección: encuentra empresas de un mercado + país + tamaño, investiga sus sitios con fuentes confiables, prioriza cuáles son mejor oportunidad de venta (auditoría web CRO + vibe coding), y arma una propuesta lista como borrador de Gmail — nunca se envía sola.

Ver el proceso completo de diseño en `specs/v1/spec.md`, `plan.md` y `tasks.md`.

## Estado actual (v1)

| Parte | Estado |
|---|---|
| Base del proyecto, esquema de datos | ✅ Completo, 29/29 tests verdes |
| Descubrimiento (Apollo + fallbacks) | ✅ Completo y probado con datos reales de Apollo |
| Auditoría propia (heurísticas de tecnología, señales UX, capturas) | ✅ Código completo. ⚠️ El scraping real está bloqueado en este entorno (ver "Bloqueos" abajo) |
| Score de oportunidad + propuesta | ✅ Completo, incluye manejo correcto de datos "no disponibles" |
| Orquestación y estado (retomar un lote cortado) | ✅ Completo |
| Corrida real end-to-end | ⏸️ Pausada — ver `BACKLOG.md` |
| Borradores de Gmail | No generados todavía (esperando resolver los bloqueos) |

## Bloqueos activos

Ver `BACKLOG.md` para el detalle completo. Resumen:
1. El plan de Ahrefs conectado no incluye tráfico ni problemas técnicos (solo Domain Rating gratis).
2. El entorno cloud de esta sesión bloquea el scraping de sitios de terceros (acceso de red "Trusted"). Hace falta cambiarlo a "Full" en la configuración del entorno.

Sin resolver esto, las propuestas generadas son pobres en contenido (puede pasar que una empresa quede con 0 hallazgos).

## Cómo correr los tests

```bash
cd "Sesiones Dispach/prospector-cro"
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m pytest tests/ -v
```

Los tests no usan red real: cubren las heurísticas, el esquema, el scoring y la orquestación con datos de ejemplo fijos.

## Cómo se usa (una vez resueltos los bloqueos)

Esto lo ejecuta el agente (Claude) durante una sesión, llamando a los conectores de Apollo/Ahrefs/Gmail ya autenticados en la cuenta — no es un script que corra solo. Ver `specs/v1/plan.md` sección 1 para el porqué de esta arquitectura.

1. Pedile al agente: "buscá empresas de \<mercado\> en \<país\>, de \<rango de empleados\>".
2. El agente busca en Apollo, completa con fallbacks si hace falta (marcados en la tabla), y te muestra los resultados.
3. Elegís qué dominios investigar en profundidad.
4. El agente combina Ahrefs + scraping propio por cada dominio elegido, arma el JSON (`prospector/audit.py`), calcula el score (`prospector/scoring.py`) y la propuesta (`prospector/proposal.py`).
5. Todo el estado del lote queda en `data/<lote-id>/state.json` — si se corta a la mitad, se retoma desde ahí con `prospector.pipeline.listar_pendientes(lote_id)`.
6. Con tu aprobación del lote completo, el agente crea los borradores en Gmail. El envío siempre lo hacés vos, manualmente.

## Estructura

```
prospector/
  discovery.py   descubrimiento de empresas (Apollo + fallbacks marcados)
  audit.py       heurísticas de tecnología, señales UX/CRO, capturas (Playwright), armado del JSON
  scoring.py     reglas explícitas de puntaje de oportunidad
  proposal.py    redacción de la propuesta y el cuerpo del mail
  pipeline.py    estado del lote (crear, guardar avance, listar pendientes)
  schema.py      esquema del JSON de empresa + validación
data/            JSON por empresa, capturas, estado de cada lote (gitignored — datos de terceros)
tests/           29 tests, sin red real
```

## Reglas duras (no negociables, vienen del spec)

- Nunca se inventa un dato: si algo no se pudo conseguir, queda `null` o `"no disponible"`, nunca un valor fabricado.
- El score de oportunidad siempre viene con sus razones — nunca es una caja negra.
- Los borradores de Gmail se generan en lote, pero el envío siempre requiere tu acción manual.
