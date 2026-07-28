# Spec — Prospector CRO (v1)

Estado: **borrador, pendiente de tu aprobación** (checkpoint SDD fase 1).

## 1. Qué hay que lograr y por qué

Una herramienta que, a partir de un mercado + país + tamaño de empresa, encuentra empresas reales, investiga sus sitios web con fuentes confiables, prioriza cuáles son mejor oportunidad de venta, arma una propuesta de auditoría web (CRO + "vibe coding"), y la deja lista como borrador de mail — nunca se envía sola.

Objetivo de negocio: generar leads calificados para vender auditorías web sin tener que investigar cada empresa a mano.

## 2. Alcance de esta versión (v1)

**Sí incluye:**
- Backend en Python/pandas + orquestación. **Sin interfaz visual todavía** (eso es una fase aparte, después de esta).
- Descubrimiento de empresas: Apollo.io como fuente principal.
- Auditoría de cada sitio: Ahrefs + scraping propio, combinados.
- Score de oportunidad automático, por reglas explicables.
- Generación de propuesta y borrador en Gmail, envío en lote y siempre manual.

**No incluye (queda para después):**
- Interfaz visual (wizard con pantallas).
- Notificaciones push al celular (ya anotado en `Sesiones Dispach/BACKLOG.md` como idea de Rutina aparte).
- Envío automático sin revisión humana.
- Seguimiento de propuestas ya enviadas (CRM).

## 3. Flujo, paso a paso, con las decisiones ya tomadas

1-3. **Elegís mercado, país y tamaño de empresa** (ej: ecommerce, Argentina, 10-50 empleados) → parámetros de entrada del script.

4. **Descubrimiento de empresas.** Se busca primero en Apollo.io (industria + país + rango de empleados). Si Apollo no devuelve suficientes, se completa con **fallback** — tanto búsqueda web como directorios públicos por país — y cada empresa fallback queda **marcada explícitamente en la tabla de resultados** con de qué tipo de fallback vino (no se mezcla en silencio con los datos de Apollo).

5. **Elegís, de la tabla, qué empresas investigar en profundidad** (selección manual tuya, no automática).

6. **Mientras corre:** en esta v1 sin UI, el progreso se muestra como mensajes de estado en la sesión (las animaciones/frases quedan para cuando exista la interfaz visual).

7. **Investigación por empresa**, combinando:
   - **Ahrefs:** domain rating, tráfico orgánico, problemas técnicos del site audit, keywords principales.
   - **Scraping propio:** tecnología detectada (CMS/framework, chat en vivo, pixels), capturas de pantalla (home + checkout o landing principal), señales de UX/CRO en el HTML (formularios largos, ausencia de CTA claro, pasos del checkout).
   - Todo se guarda en un JSON por empresa (esquema abajo).

8. **Score de oportunidad:** reglas explícitas y explicables (ej: sitio lento + DR bajo + sin CTA claro + checkout largo → score alto). Cada empresa queda con un puntaje y una lista de "razones" legibles — nunca una caja negra.

9. **Propuesta automatizada:** por empresa, un documento con 3-4 hallazgos concretos (basados en las razones del score) + servicio sugerido (auditoría CRO / vibe coding) + llamado a la acción.

10. **Envío:** se generan **todos los borradores del lote juntos** en Gmail (ya conectado). Vos revisás el lote completo y enviás manualmente — nunca sale nada solo.

## 4. Esquema de datos por empresa (JSON)

```json
{
  "empresa": {
    "nombre": "string",
    "dominio": "string",
    "pais": "string",
    "industria": "string",
    "empleados_rango": "string",
    "fuente_descubrimiento": "apollo | fallback_busqueda_web | fallback_directorio_publico"
  },
  "auditoria": {
    "ahrefs": {
      "domain_rating": "number | null",
      "trafico_organico_mensual": "number | null",
      "problemas_tecnicos": ["string"],
      "top_keywords": ["string"]
    },
    "scraping": {
      "tecnologia_detectada": ["string"],
      "tiene_chat_vivo": "boolean",
      "capturas": { "home": "path", "checkout_o_landing": "path" },
      "senales_ux": {
        "formulario_largo": "boolean",
        "cta_visible": "boolean",
        "pasos_checkout": "number | null"
      }
    }
  },
  "oportunidad": {
    "score": "0-100",
    "categoria": "alta | media | baja",
    "razones": ["string"]
  },
  "propuesta": {
    "diagnostico": ["string"],
    "servicio_sugerido": "string",
    "estado_envio": "borrador_generado | enviado"
  }
}
```

Regla dura: si un dato no se pudo conseguir, se marca `null` o `"no disponible"` — **nunca se inventa un valor**.

## 5. Criterios de aceptación

- [ ] Dado mercado + país + tamaño, la tabla de resultados trae empresas reales con nombre + dominio, y cada fila indica su fuente (Apollo o el tipo de fallback).
- [ ] Cada empresa seleccionada genera un JSON válido con el esquema de arriba, sin datos inventados.
- [ ] El score de oportunidad es explicable: para cualquier empresa, se puede mostrar por qué quedó en ese puesto.
- [ ] Los borradores de Gmail del lote se generan juntos, pero el envío siempre requiere tu acción manual.
- [ ] Ningún paso escribe o envía nada fuera del repo/Gmail sin que vos lo hayas iniciado.

## 6. Preguntas que quedan para la fase de PLAN (no bloquean el spec)

Estas son decisiones técnicas, no de producto — se resuelven en `plan.md`, no acá:
- Qué librería de Python usamos para las capturas de pantalla (ej. Playwright).
- Cómo detectamos "tecnología" del sitio (heurísticas propias vs. librería tipo Wappalyzer).
- Dónde se guardan los JSON y las capturas (archivos locales en el repo vs. otra cosa).
- Cómo se recupera el proceso si se corta a la mitad (¿hace falta poder resumir un lote a medio hacer?).
