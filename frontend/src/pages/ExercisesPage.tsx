import { useEffect, useMemo, useState } from 'react'
import type { Exercise } from '../types'
import { getDailyExercise, getExercises } from '../api/client'

const LEVELS = [
  { value: '', label: 'Todos' },
  { value: 'principiante', label: 'Principiante' },
  { value: 'intermedio', label: 'Intermedio' },
  { value: 'avanzado', label: 'Avanzado' },
]

const LEVEL_BADGE: Record<string, string> = {
  principiante: 'var(--good)',
  intermedio: 'var(--warn)',
  avanzado: 'var(--bad)',
}

interface Props {
  language: string
  onSelect: (ex: Exercise) => void
}

export default function ExercisesPage({ language, onSelect }: Props) {
  const [daily, setDaily] = useState<Exercise | null>(null)
  const [all, setAll] = useState<Exercise[]>([])
  const [level, setLevel] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    Promise.all([getDailyExercise(language), getExercises(language)])
      .then(([d, list]) => {
        if (cancelled) return
        setDaily(d)
        setAll(list)
      })
      .catch((e) => console.error(e))
      .finally(() => !cancelled && setLoading(false))
    return () => {
      cancelled = true
    }
  }, [language])

  const groups = useMemo(() => {
    const filtered = level ? all.filter((e) => e.level === level) : all
    const map = new Map<string, Exercise[]>()
    for (const e of filtered) {
      const key = e.category
      if (!map.has(key)) map.set(key, [])
      map.get(key)!.push(e)
    }
    return Array.from(map.entries())
  }, [all, level])

  if (loading) {
    return <div className="loading">Cargando ejercicios...</div>
  }

  return (
    <div>
      {daily && (
        <div className="card daily">
          <div className="daily-badge">Ejercicio del día</div>
          <h2 style={{ color: 'var(--text)', textTransform: 'none', letterSpacing: 0, fontSize: 20 }}>
            {daily.title}
          </h2>
          <p>{daily.prompt}</p>
          <div className="ex-meta">
            <span className="ex-badge" style={{ color: LEVEL_BADGE[daily.level], borderColor: LEVEL_BADGE[daily.level] }}>
              {daily.level}
            </span>
            <span className="ex-cat">{daily.category}</span>
            <span className="ex-cat">{daily.minutes} min</span>
          </div>
          <button className="btn" onClick={() => onSelect(daily)}>
            Practicar este ejercicio
          </button>
        </div>
      )}

      <div className="card">
        <h2>Catálogo de ejercicios</h2>
        <div className="level-tabs">
          {LEVELS.map((l) => (
            <button
              key={l.value}
              className={`chip ${level === l.value ? 'active' : ''}`}
              onClick={() => setLevel(l.value)}
            >
              {l.label}
            </button>
          ))}
        </div>
      </div>

      {groups.map(([cat, items]) => (
        <div className="card" key={cat}>
          <h2>{cat}</h2>
          {items.map((ex) => (
            <div className="exercise" key={ex.id}>
              <div className="ex-head">
                <div>
                  <span className="ex-title">{ex.title}</span>
                  <div className="ex-meta">
                    <span className="ex-badge" style={{ color: LEVEL_BADGE[ex.level], borderColor: LEVEL_BADGE[ex.level] }}>
                      {ex.level}
                    </span>
                    <span className="ex-cat">{ex.minutes} min</span>
                  </div>
                </div>
                <button className="btn secondary" onClick={() => onSelect(ex)}>
                  Practicar
                </button>
              </div>
              <p className="ex-prompt">{ex.prompt}</p>
              <ul className="ex-structure">
                {ex.structure.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      ))}
    </div>
  )
}
