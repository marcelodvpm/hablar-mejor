import type { Activity, AnalysisReport } from '../types'
import MetricCard from '../components/MetricCard'
import TranscriptView from '../components/TranscriptView'
import FeedbackPanel from '../components/FeedbackPanel'

export default function ResultsPage({
  report,
  activity,
}: {
  report: AnalysisReport
  activity: Activity | null
}) {
  const { metrics, feedback } = report

  const wpmStatus =
    metrics.words_per_minute === 0
      ? 'none'
      : metrics.words_per_minute > 180
        ? 'bad'
        : metrics.words_per_minute < 105
          ? 'warn'
          : 'good'

  return (
    <div>
      {activity && (
        <div className="card" style={{ textAlign: 'center' }}>
          <span className="ex-cat">Actividad practicada</span>
          <div className="ex-title" style={{ fontSize: 20, marginTop: 4 }}>{activity.title}</div>
        </div>
      )}
      <div className="card">
        <div className="score-big">{feedback.score}</div>
        <div className="score-label">Puntuación general / 100</div>
        <div className="metrics-grid">
          <MetricCard
            value={String(metrics.words_per_minute)}
            label="Velocidad"
            sub="palabras por minuto"
            status={wpmStatus}
          />
          <MetricCard
            value={String(metrics.filler_total)}
            label="Muletillas"
            sub={metrics.filler_words.map((f) => `"${f.word}" ×${f.count}`).join(', ')}
            status={metrics.filler_total > 0 ? 'warn' : 'good'}
          />
          <MetricCard
            value={String(metrics.unique_content_words)}
            label="Palabras distintas"
            sub={`TTR ${metrics.type_token_ratio.toFixed(2)} (riqueza léxica)`}
            status={metrics.type_token_ratio >= 0.35 ? 'good' : 'warn'}
          />
          <MetricCard
            value={String(metrics.long_pauses_count)}
            label="Pausas largas"
            sub="mayores a 0.5 seg"
            status={metrics.long_pauses_count >= 5 ? 'bad' : metrics.long_pauses_count > 0 ? 'warn' : 'good'}
          />
          <MetricCard
            value={String(metrics.noise_bursts_count)}
            label="Carraspeos/ruidos"
            sub="picos de energía en silencios"
            status={metrics.noise_bursts_count > 0 ? 'warn' : 'good'}
          />
          <MetricCard
            value={String(Math.round(metrics.duration_ms / 1000))}
            label="Duración"
            sub="segundos grabados"
            status="none"
          />
        </div>
      </div>

      <TranscriptView words={metrics.words} />

      <FeedbackPanel feedback={feedback} repeatedWords={metrics.repeated_words} />
    </div>
  )
}
