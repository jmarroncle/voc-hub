# VOC Hub

Prototipo de producto: un sistema de feedback de clientes **por voz** en vez de formulario. La idea es que agencias y negocios de servicio reemplacen la encuesta post-venta típica (que casi nadie completa) por un mensaje de audio de hasta 2 minutos, sin login ni registro.

**Estado actual: prototipo de interfaz (UI/UX).** El flujo de pantallas está construido y navegable; la grabación real de audio, la transcripción por IA y la persistencia de datos todavía no están conectadas — el dashboard usa datos de ejemplo.

## Flujo

1. **`/`** — Pantalla de captura: el cliente graba su mensaje de voz.
2. **`/gracias`** — Confirmación de envío.
3. **`/dashboard`** — Panel para el negocio: feedbacks recientes, sentimiento (positivo / neutro / negativo) y categorías más mencionadas.

## Stack

Next.js 15 · React 19

## Modelo de datos (mock)

El dashboard (`app/dashboard/page.jsx`) arma cada fila de feedback a partir de un array hardcodeado en el componente — no hay modelo de datos declarado en ningún otro lugar del repo. Estos son los campos que usa hoy:

| Campo | Tipo | Notas |
|---|---|---|
| `id` | `number` | Identificador secuencial del mock (1 a 5). |
| `nombre` | `string` | Nombre del cliente, o `"Anónimo"` en el ejemplo sin identificar. |
| `empresa` | `string \| null` | Empresa del cliente. `null` cuando no se registró. |
| `preview` | `string` | Fragmento de texto entre comillas — simula la transcripción del audio. |
| `categoria` | `string` (enum) | Valores usados en el mock: `servicio`, `precio`, `producto`, `atención`. El gráfico de categorías agrega una quinta, `otro`, que no aparece en ningún registro de ejemplo. |
| `duracion` | `string` | Duración del audio en formato `m:ss` (ej. `"1:24"`). |
| `sentimiento` | `string` (enum) | `pos` \| `neu` \| `neg`. Define qué color de pill se usa (`.pill-pos` / `.pill-neu` / `.pill-neg` en `globals.css`). |
| `label` | `string` | Versión legible de `sentimiento` para mostrar en la UI: `"Positivo"`, `"Neutro"`, `"Negativo"`. |
| `tiempo` | `string` | Texto libre de tiempo relativo (ej. `"hace 5 min"`, `"ayer"`) — no es una fecha real. |

Ningún campo tiene validación de tipos (no hay TypeScript ni schema): esto documenta la forma que asume el mock hoy, no un contrato garantizado por código.

## Próximos pasos

- Grabación de audio real (MediaRecorder API del navegador)
- Transcripción y clasificación automática por IA
- Persistencia de datos (base de datos real en vez de datos de ejemplo)

---

Parte de la exploración de [Juan Marroncle](https://github.com/jmarroncle) en Behavioral Design aplicado a producto — capturar la voz real del cliente sin fricción.
