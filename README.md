# VOC Hub

Prototipo de producto: un sistema de feedback de clientes **por voz** en vez de formulario. La idea es que agencias y negocios de servicio reemplacen la encuesta post-venta típica (que casi nadie completa) por un mensaje de audio de hasta 2 minutos, sin login ni registro.

**Estado actual: prototipo de interfaz (UI/UX).** El flujo de pantallas está construido y navegable; la grabación real de audio, la transcripción por IA y la persistencia de datos todavía no están conectadas — el dashboard usa datos de ejemplo.

## Flujo

1. **`/`** — Pantalla de captura: el cliente graba su mensaje de voz.
2. **`/gracias`** — Confirmación de envío.
3. **`/dashboard`** — Panel para el negocio: feedbacks recientes, sentimiento (positivo / neutro / negativo) y categorías más mencionadas.

## Stack

Next.js 15 · React 19

## Próximos pasos

- Grabación de audio real (MediaRecorder API del navegador)
- Transcripción y clasificación automática por IA
- Persistencia de datos (base de datos real en vez de datos de ejemplo)

---

Parte de la exploración de [Juan Marroncle](https://github.com/jmarroncle) en Behavioral Design aplicado a producto — capturar la voz real del cliente sin fricción.
