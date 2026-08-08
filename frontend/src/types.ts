export interface Word {
  word: string
  start_ms: number
  end_ms: number
  confidence: number
  is_filler: boolean
  is_repeated: boolean
}

export interface FillerWord {
  word: string
  count: number
}

export interface RepeatedWord {
  word: string
  count: number
  occurrences: number[]
  synonyms: string[]
}

export interface TimeSpan {
  start_ms: number
  end_ms: number
  duration_ms: number
}

export interface Metrics {
  words: Word[]
  transcript: string
  total_words: number
  unique_content_words: number
  type_token_ratio: number
  words_per_minute: number
  speaking_ms: number
  filler_total: number
  filler_words: FillerWord[]
  repeated_words: RepeatedWord[]
  long_pauses_count: number
  long_pauses: TimeSpan[]
  noise_bursts_count: number
  noise_bursts: TimeSpan[]
  loudness_variance: number
  duration_ms: number
}

export interface Verdict {
  category: string
  verdict: string
  text: string
}

export interface Feedback {
  score: number
  verdicts: Verdict[]
  suggestions: string[]
}

export interface AnalysisReport {
  language: string
  metrics: Metrics
  feedback: Feedback
}

export interface Exercise {
  id: string
  language: string
  level: 'principiante' | 'intermedio' | 'avanzado'
  category: string
  title: string
  prompt: string
  structure: string[]
  tips: string[]
  minutes: number
}
