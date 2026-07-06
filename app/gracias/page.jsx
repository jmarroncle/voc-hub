import Link from 'next/link'

export const metadata = {
  title: 'Gracias — VOC Hub',
}

export default function GraciasPage() {
  return (
    <main className="gracias-main">
      <div className="gracias-card">
        <div className="gracias-icon">🎙️</div>
        <h1 className="gracias-title">¡Gracias por tu mensaje!</h1>
        <p className="gracias-sub">
          Tu feedback fue recibido y está siendo procesado.<br />
          Lo tendremos en cuenta para seguir mejorando.
        </p>
        <Link href="/" className="gracias-back">
          ← Dejar otro mensaje
        </Link>
      </div>
    </main>
  )
}
