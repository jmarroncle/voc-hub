'use client'
import { useState, useRef, useEffect } from 'react'
import { useRouter } from 'next/navigation'

const WAVE_HEIGHTS = [8, 14, 20, 10, 24, 16, 8, 18, 12, 22, 6, 14]

function formatTime(s) {
  return `${Math.floor(s / 60)}:${(s % 60).toString().padStart(2, '0')}`
}

export default function CapturePage() {
  const [recording, setRecording] = useState(false)
  const [recorded, setRecorded] = useState(false)
  const [seconds, setSeconds] = useState(0)
  const timerRef = useRef(null)
  const router = useRouter()

  useEffect(() => {
    if (recording) {
      timerRef.current = setInterval(() => {
        setSeconds(s => {
          if (s >= 119) {
            stopRec(120)
            return 120
          }
          return s + 1
        })
      }, 1000)
    }
    return () => clearInterval(timerRef.current)
  }, [recording])

  function stopRec(finalSec) {
    clearInterval(timerRef.current)
    setRecording(false)
    if (finalSec > 0) setRecorded(true)
  }

  function toggleRec() {
    if (!recording) {
      setRecorded(false)
      setSeconds(0)
      setRecording(true)
    } else {
      stopRec(seconds)
    }
  }

  return (
    <main className="capture-main">
      <div className="capture-card">
        <div className="cap-logo">VOC · Voice of Customer</div>
        <h1 className="cap-title">Tu opinión nos hace mejores</h1>
        <p className="cap-sub">
          Grabá un mensaje de voz de hasta 2 minutos.<br />
          Sin formularios, sin registro.
        </p>

        <div className="field">
          <label>Tu nombre <span className="optional">(opcional)</span></label>
          <input type="text" placeholder="Ej: María González" />
        </div>
        <div className="field">
          <label>Empresa <span className="optional">(opcional)</span></label>
          <input type="text" placeholder="Ej: Acme S.A." />
        </div>

        <div className={`recorder${recording ? ' recording' : ''}`}>
          <button
            className={`rec-btn${recording ? ' recording' : ''}`}
            onClick={toggleRec}
            aria-label={recording ? 'Detener grabación' : 'Iniciar grabación'}
          >
            {recording ? (
              <svg viewBox="0 0 24 24"><rect x="6" y="6" width="12" height="12" rx="2" /></svg>
            ) : (
              <svg viewBox="0 0 24 24">
                <path d="M12 1a4 4 0 0 1 4 4v6a4 4 0 0 1-8 0V5a4 4 0 0 1 4-4zm-7 10a7 7 0 0 0 14 0h-2a5 5 0 0 1-10 0H5zm7 9v-3h-2v3H7v2h10v-2h-3z" />
              </svg>
            )}
          </button>

          {recording && (
            <div className="waveform">
              {WAVE_HEIGHTS.map((h, i) => (
                <div key={i} className="wave-bar" style={{ height: h }} />
              ))}
            </div>
          )}

          <div className="rec-label">
            {recorded ? '✓ Audio grabado' : recording ? 'Grabando...' : 'Tocá para grabar'}
          </div>
          <div className="rec-hint">
            {recording
              ? 'Tocá para detener'
              : recorded
              ? `Duración: ${formatTime(seconds)} · Tocá para volver a grabar`
              : 'Máximo 2 minutos · Solo audio'}
          </div>

          {(recording || recorded) && (
            <div className="timer">{formatTime(seconds)}</div>
          )}
        </div>

        <button
          className={`btn-send${recorded ? ' ready' : ''}`}
          disabled={!recorded}
          onClick={() => router.push('/gracias')}
        >
          Enviar mensaje de voz →
        </button>

        <p className="cap-footer">
          Procesado con IA · Tu voz no se comparte · © 2026
        </p>
      </div>
    </main>
  )
}
