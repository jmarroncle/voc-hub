import Link from 'next/link'

export const metadata = {
  title: 'Dashboard — VOC Hub',
}

const FEEDBACKS = [
  {
    id: 1,
    nombre: 'María González',
    empresa: 'Acme S.A.',
    preview: '"La atención fue excelente, resolvieron mi problema en minutos..."',
    categoria: 'servicio',
    duracion: '1:24',
    sentimiento: 'pos',
    label: 'Positivo',
    tiempo: 'hace 5 min',
  },
  {
    id: 2,
    nombre: 'Carlos Ruiz',
    empresa: null,
    preview: '"El precio me parece un poco alto comparado con la competencia..."',
    categoria: 'precio',
    duracion: '0:48',
    sentimiento: 'neg',
    label: 'Negativo',
    tiempo: 'hace 1 h',
  },
  {
    id: 3,
    nombre: 'Anónimo',
    empresa: 'TechCorp',
    preview: '"El producto cumple lo que promete, nada más que agregar..."',
    categoria: 'producto',
    duracion: '0:33',
    sentimiento: 'neu',
    label: 'Neutro',
    tiempo: 'hace 3 h',
  },
  {
    id: 4,
    nombre: 'Laura Pérez',
    empresa: 'StartupXYZ',
    preview: '"Increíble la rapidez con la que respondieron, muy recomendable..."',
    categoria: 'servicio',
    duracion: '1:02',
    sentimiento: 'pos',
    label: 'Positivo',
    tiempo: 'hace 5 h',
  },
  {
    id: 5,
    nombre: 'Martín López',
    empresa: 'Industrias ML',
    preview: '"Buena experiencia en general, aunque el onboarding podría mejorar..."',
    categoria: 'atención',
    duracion: '1:15',
    sentimiento: 'neu',
    label: 'Neutro',
    tiempo: 'ayer',
  },
]

const BARS = [
  { name: 'Servicio',  pct: 75, color: '#4C6EF5' },
  { name: 'Producto',  pct: 50, color: '#7C3AED' },
  { name: 'Precio',    pct: 30, color: '#D69E2E' },
  { name: 'Atención',  pct: 20, color: '#38A169' },
  { name: 'Otro',      pct: 10, color: '#CBD5E1' },
]

/* Donut segments: pos=71%, neu=20%, neg=9%. Circumference = 2π×28 ≈ 175.9 */
const C = 175.9
const DONUT = [
  { pct: 0.71, color: '#22863a', offset: 0 },
  { pct: 0.20, color: '#f0ad00', offset: 0.71 },
  { pct: 0.09, color: '#d93f0b', offset: 0.91 },
]

export default function DashboardPage() {
  return (
    <div className="dash-layout">
      <nav className="dash-nav">
        <div className="dash-nav-logo">VOC Hub</div>
        <div className="dash-nav-right">
          <span className="dash-nav-badge">24 feedbacks · Actualizado hace 2 min</span>
          <Link href="/" className="dash-nav-cta">+ Nuevo feedback</Link>
        </div>
      </nav>

      <div className="dash-body">

        {/* ── Stats ── */}
        <div className="stat-row">
          <div className="stat-card">
            <div className="stat-label">Total</div>
            <div className="stat-value">24</div>
            <div className="stat-sub">feedbacks recibidos</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Positivos</div>
            <div className="stat-value green">71%</div>
            <div className="stat-sub">17 de 24</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Prom. duración</div>
            <div className="stat-value">1:12</div>
            <div className="stat-sub">minutos por audio</div>
          </div>
        </div>

        {/* ── Charts ── */}
        <div className="charts-row">
          {/* Donut */}
          <div className="chart-box">
            <div className="chart-title">Sentimiento</div>
            <div className="donut-wrap">
              <svg width="80" height="80" viewBox="0 0 80 80" style={{ transform: 'rotate(-90deg)', flexShrink: 0 }}>
                <circle cx="40" cy="40" r="28" fill="none" stroke="#f0f0f0" strokeWidth="10" />
                {DONUT.map(({ pct, color, offset }) => (
                  <circle
                    key={color}
                    cx="40" cy="40" r="28"
                    fill="none"
                    stroke={color}
                    strokeWidth="10"
                    strokeDasharray={`${pct * C} ${C}`}
                    strokeDashoffset={-offset * C}
                  />
                ))}
              </svg>
              <div className="donut-legend">
                {[
                  { color: '#22863a', label: 'Positivo', pct: '71%' },
                  { color: '#f0ad00', label: 'Neutro',   pct: '20%' },
                  { color: '#d93f0b', label: 'Negativo', pct: '9%'  },
                ].map(({ color, label, pct }) => (
                  <div key={label} className="legend-row">
                    <div className="dot" style={{ background: color }} />
                    <span>{label} {pct}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Bars */}
          <div className="chart-box">
            <div className="chart-title">Categorías</div>
            <div className="bars">
              {BARS.map(({ name, pct, color }) => (
                <div key={name} className="bar-row">
                  <div className="bar-name">{name}</div>
                  <div className="bar-track">
                    <div className="bar-fill" style={{ width: `${pct}%`, background: color }} />
                  </div>
                  <div className="bar-pct">{pct}%</div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* ── List ── */}
        <div className="list-box">
          <div className="list-title">Últimos registros</div>
          {FEEDBACKS.map(({ id, nombre, empresa, preview, categoria, duracion, sentimiento, label, tiempo }) => (
            <div key={id} className="feedback-item">
              <button className="play-btn" aria-label="Reproducir audio">
                <svg viewBox="0 0 10 12"><path d="M0 0l10 6-10 6z" /></svg>
              </button>
              <div className="feedback-text">
                <div className="feedback-name">
                  {nombre}{empresa ? ` · ${empresa}` : ''}
                </div>
                <div className="feedback-preview">{preview}</div>
                <div className="feedback-meta">{categoria} · {duracion}</div>
              </div>
              <div className="feedback-right">
                <span className={`pill pill-${sentimiento}`}>{label}</span>
                <span className="feedback-time">{tiempo}</span>
              </div>
            </div>
          ))}
        </div>

      </div>
    </div>
  )
}
