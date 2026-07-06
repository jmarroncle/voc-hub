import './globals.css'

export const metadata = {
  title: 'VOC Hub — Voice of Customer',
  description: 'Capturá feedback de voz de tus clientes en segundos. Sin formularios, sin registro.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  )
}
