import { useRef, useState } from 'react'
import type { Activity, AnalysisReport } from '../types'
import { analyzeAudio } from '../api/client'
import { Recorder } from '../lib/recorder'

interface Props {
  activity: Activity | null
  onAnalyzed: (r: AnalysisReport) => void
  onBack: () => void
}

export default function RecorderPage({ activity, onAnalyzed, onBack }: Props) {
  const [recording, setRecording] = useState(false)
  const [analyzing, setAnalyzing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [elapsed, setElapsed] = useState(0)
  const [language, setLanguage] = useState('es-AR')

  const recorderRef = useRef<Recorder | null>(null)
  const timerRef = useRef<number | null>(null)

  const start = async () => {
    setError(null)
    try {
      recorderRef.current = await Recorder.create()
      setRecording(true)
      setElapsed(0)
      timerRef.current = window.setInterval(() => {
        setElapsed(recorderRef.current?.elapsedMs() ?? 0)
      }, 100)
    } catch (e) {
      setError('No se pudo acceder al micrófono. Revisá los permisos del navegador.')
      console.error(e)
    }
  }

  const stop = async () => {
    const rec = recorderRef.current
    if (!rec) return
    if (timerRef.current) window.clearInterval(timerRef.current)
    setRecording(false)
    setAnalyzing(true)
    setError(null)
    try {
      const wav = await rec.stop()
      const report = await analyzeAudio(wav, language)
      onAnalyzed(report)
    } catch (e: any) {
      setError(e?.response?.data?.detail || e?.message || 'Error al analizar el audio.')
      console.error(e)
    } finally {
      setAnalyzing(false)
    }
  }

  const seconds = Math.floor(elapsed / 1000)
  const timer = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`

  return (
    <div>
      {activity && (
        <div className="card exercise-card">
          <h2 style={{ color: 'var(--text)', textTransform: 'none', letterSpacing: 0, fontSize: 18, margin: 0 }}>
            {activity.title}
          </h2>
          {activity.subtitle && <p className="ex-cat" style={{ marginTop: 4 }}>{activity.subtitle}</p>}
          {activity.sample && <p className="ex-sample">“{activity.sample}”</p>}
          <p style={{ margin: '8px 0' }}>{activity.prompt}</p>
          <ul className="ex-structure">
            {activity.structure.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="card recorder">
        <h2>Grabación de práctica</h2>
        <p style={{ color: 'var(--muted)', marginTop: 8 }}>
          {activity
            ? 'Grabá tu respuesta siguiendo la estructura y el estilo del ejercicio.'
            : 'Grabá entre 30 segundos y 3 minutos hablando. Podés leer un texto, preparar una exposición o simplemente contar algo.'}
        </p>

      <div style={{ margin: '16px 0', display: 'flex', gap: 12, justifyContent: 'center', alignItems: 'center' }}>
        <label style={{ color: 'var(--muted)', fontSize: 14 }}>Idioma:</label>
        <select value={language} onChange={(e) => setLanguage(e.target.value)} disabled={recording || analyzing}>
          <option value="es-AR">Español (Argentina)</option>
          <option value="en-US">English (US)</option>
        </select>
      </div>

      {recording && (
        <div className="timer" style={{ color: 'var(--bad)' }}>
          ● {timer}
        </div>
      )}

      {!recording && !analyzing && (
        <div style={{ display: 'flex', gap: 10, justifyContent: 'center' }}>
          <button className="btn secondary" onClick={onBack} disabled={analyzing}>
            ← Elegir otro ejercicio
          </button>
          <button className="btn" onClick={start}>
            Comenzar a grabar
          </button>
        </div>
      )}

      {recording && (
        <button className="btn" onClick={stop}>
          Detener y analizar
        </button>
      )}

      {analyzing && (
        <div className="loading">
          Analizando tu forma de hablar...
          <br />
          <span style={{ fontSize: 13 }}>(transcripción + métricas)</span>
        </div>
      )}

      {error && <div className="error">{error}</div>}

      <p className="hint">
        Tu audio se transcribe localmente con Whisper (sin nube): nada sale de tu PC.
      </p>
      </div>
    </div>
  )
}
