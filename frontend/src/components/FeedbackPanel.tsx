import type { Feedback, RepeatedWord } from '../types'

export default function FeedbackPanel({
  feedback,
  repeatedWords,
}: {
  feedback: Feedback
  repeatedWords: RepeatedWord[]
}) {
  return (
    <div>
      <div className="card">
        <h2>Evaluación</h2>
        {feedback.verdicts.map((v, i) => (
          <div className="verdict" key={i}>
            <span className="cat">{v.category}: </span>
            {v.text}
          </div>
        ))}
      </div>

      {feedback.suggestions.length > 0 && (
        <div className="card">
          <h2>Qué mejorar</h2>
          <ul className="suggestions">
            {feedback.suggestions.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ul>
        </div>
      )}

      {repeatedWords.length > 0 && (
        <div className="card">
          <h2>Sinónimos sugeridos</h2>
          <ul className="suggestions">
            {repeatedWords.map((r, i) => (
              <li key={i}>
                <strong>"{r.word}"</strong> ({r.count} veces) →{' '}
                {r.synonyms.length > 0 ? r.synonyms.join(', ') : 'sin sugerencias para esta palabra'}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
