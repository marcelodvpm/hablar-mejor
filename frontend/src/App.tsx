import { useState } from 'react'
import type { AnalysisReport, Exercise } from './types'
import ExercisesPage from './pages/ExercisesPage'
import RecorderPage from './pages/RecorderPage'
import ResultsPage from './pages/ResultsPage'

export default function App() {
  const [report, setReport] = useState<AnalysisReport | null>(null)
  const [exercise, setExercise] = useState<Exercise | null>(null)
  const [stage, setStage] = useState<'exercises' | 'record' | 'results'>('exercises')

  const startExercise = (ex: Exercise) => {
    setExercise(ex)
    setReport(null)
    setStage('record')
  }

  const reset = () => {
    setReport(null)
    setExercise(null)
    setStage('exercises')
  }

  return (
    <div className="container">
      <header>
        <h1>
          Habla<span>Mejor</span>
        </h1>
        {stage !== 'exercises' && (
          <button className="btn secondary" onClick={reset}>
            ← Catálogo de ejercicios
          </button>
        )}
      </header>

      {stage === 'exercises' && (
        <ExercisesPage language="es-AR" onSelect={startExercise} />
      )}

      {stage === 'record' && (
        <RecorderPage
          exercise={exercise}
          onAnalyzed={(r) => {
            setReport(r)
            setStage('results')
          }}
          onBack={reset}
        />
      )}

      {stage === 'results' && report && <ResultsPage report={report} exercise={exercise} />}
    </div>
  )
}
