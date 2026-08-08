import { useEffect, useState } from 'react'
import type { Persona } from '../types'
import { getPersonas } from '../api/client'

interface Props {
  onSelect: (p: Persona) => void
}

export default function PersonasPage({ onSelect }: Props) {
  const [personas, setPersonas] = useState<Persona[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    getPersonas()
      .then((list) => !cancelled && setPersonas(list))
      .catch((e) => console.error(e))
      .finally(() => !cancelled && setLoading(false))
    return () => {
      cancelled = true
    }
  }, [])

  if (loading) {
    return <div className="loading">Cargando oradores...</div>
  }

  return (
    <div>
      <div className="card">
        <h2>Imitá a un orador</h2>
        <p style={{ color: 'var(--muted)', fontSize: 14, marginTop: 8 }}>
          Elegí un orador destacado, leé su estilo y su texto modelo de práctica, y grabá tu
          propia versión. El texto modelo es original (no es una cita del orador): sirve para
          imitar su ritmo, vocabulario y recursos retóricos.
        </p>
      </div>

      {personas.map((p) => (
        <div className="card exercise" key={p.id}>
          <div className="ex-head">
            <div>
              <span className="ex-title">{p.name}</span>
              <div className="ex-meta">
                <span className="ex-cat">{p.category}</span>
                <span className="ex-cat">{p.minutes} min</span>
              </div>
            </div>
            <button className="btn secondary" onClick={() => onSelect(p)}>
              Imitar
            </button>
          </div>
          <p className="ex-prompt">{p.style}</p>
          <p className="ex-sample">“{p.sample_text}”</p>
          <p className="ex-challenge">
            <strong>Desafío:</strong> {p.challenge}
          </p>
        </div>
      ))}
    </div>
  )
}
