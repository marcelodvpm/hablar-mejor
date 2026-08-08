import axios from 'axios'
import type { AnalysisReport, Exercise, Persona } from '../types'

export async function analyzeAudio(file: Blob, language: string): Promise<AnalysisReport> {
  const form = new FormData()
  form.append('file', file, 'audio.wav')
  form.append('language', language)
  const { data } = await axios.post<AnalysisReport>('/api/analyze', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export async function getExercises(language: string, level?: string): Promise<Exercise[]> {
  const { data } = await axios.get<Exercise[]>('/api/exercises', {
    params: { language, level: level || undefined },
  })
  return data
}

export async function getDailyExercise(language: string): Promise<Exercise> {
  const { data } = await axios.get<Exercise>('/api/exercises/daily', {
    params: { language },
  })
  return data
}

export async function getPersonas(): Promise<Persona[]> {
  const { data } = await axios.get<Persona[]>('/api/personas')
  return data
}
