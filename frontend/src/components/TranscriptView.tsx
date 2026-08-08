import type { Word } from '../types'

export default function TranscriptView({ words }: { words: Word[] }) {
  return (
    <div className="card">
      <h2>Transcripción</h2>
      <p style={{ lineHeight: 1.9, fontSize: 16, margin: 0 }}>
        {words.map((w, i) => {
          const classes = ['transcript-word']
          if (w.is_filler) classes.push('filler')
          if (w.is_repeated) classes.push('repeated')
          return (
            <span key={i} className={classes.join(' ')} title={`${Math.round(w.start_ms / 1000)}s`}>
              {w.word}
              {i < words.length - 1 ? ' ' : ''}
            </span>
          )
        })}
      </p>
      <div className="legend">
        <span>
          <span className="dot" style={{ background: 'rgba(251,191,36,0.5)' }} />
          muletilla
        </span>
        <span>
          <span className="dot" style={{ background: 'rgba(248,113,113,0.5)' }} />
          palabra repetida
        </span>
      </div>
    </div>
  )
}
