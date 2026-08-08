import { useState } from 'react'
import type { Activity, AnalysisReport, Persona } from './types'
import ExercisesPage from './pages/ExercisesPage'
import PersonasPage from './pages/PersonasPage'
import RecorderPage from './pages/RecorderPage'
import ResultsPage from './pages/ResultsPage'

type Tab = 'exercises' | 'personas'
type Stage = 'home' | 'record' | 'results'

function toActivity(p: Persona): Activity {
  return {
    title: p.name,
    subtitle: p.category,
    prompt: p.challenge,
    sample: p.sample_text,
    structure: p.structure,
    tips: p.tips,
    minutes: p.minutes,
  }
}

export default function App() {
  const [report, setReport] = useState<AnalysisReport | null>(null)
  const [activity, setActivity] = useState<Activity | null>(null)
  const [tab, setTab] = useState<Tab>('exercises')
  const [stage, setStage] = useState<Stage>('home')

  const start = (a: Activity | null) => {
    setActivity(a)
    setReport(null)
    setStage('record')
  }

  const reset = () => {
    setReport(null)
    setActivity(null)
    setStage('home')
  }

  return (
    <div className="container">
      <header>
        <h1>
          Habla<span>Mejor</span>
        </h1>
        {stage === 'home' && (
          <nav className="tabs">
            <button className={`tab ${tab === 'exercises' ? 'active' : ''}`} onClick={() => setTab('exercises')}>
              Ejercicios
            </button>
            <button className={`tab ${tab === 'personas' ? 'active' : ''}`} onClick={() => setTab('personas')}>
              Imitar oradores
            </button>
          </nav>
        )}
        {stage !== 'home' && (
          <button className="btn secondary" onClick={reset}>
            ← Volver
          </button>
        )}
      </header>

      {stage === 'home' && tab === 'exercises' && (
        <ExercisesPage
          language="es-AR"
          onSelect={(ex) =>
            start({
              title: ex.title,
              subtitle: `Nivel ${ex.level} · ${ex.category}`,
              prompt: ex.prompt,
              structure: ex.structure,
              tips: ex.tips,
              minutes: ex.minutes,
            })
          }
        />
      )}

      {stage === 'home' && tab === 'personas' && (
        <PersonasPage onSelect={(p) => start(toActivity(p))} />
      )}

      {stage === 'record' && (
        <RecorderPage activity={activity} onAnalyzed={(r) => { setReport(r); setStage('results') }} onBack={reset} />
      )}

      {stage === 'results' && report && <ResultsPage report={report} activity={activity} />}
    </div>
  )
}
