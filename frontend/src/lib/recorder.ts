const TARGET_RATE = 16000

function writeString(view: DataView, offset: number, text: string) {
  for (let i = 0; i < text.length; i++) {
    view.setUint8(offset + i, text.charCodeAt(i))
  }
}

async function toWav(blob: Blob): Promise<Blob> {
  const arrayBuffer = await blob.arrayBuffer()
  const audioCtx = new AudioContext()
  const audioBuffer = await audioCtx.decodeAudioData(arrayBuffer)

  const length = Math.floor(audioBuffer.duration * TARGET_RATE)
  const offline = new OfflineAudioContext(1, length, TARGET_RATE)
  const source = offline.createBufferSource()
  source.buffer = audioBuffer
  source.connect(offline.destination)
  source.start()
  const rendered = await offline.startRendering()
  const samples = rendered.getChannelData(0)

  const buffer = new ArrayBuffer(44 + samples.length * 2)
  const view = new DataView(buffer)
  writeString(view, 0, 'RIFF')
  view.setUint32(4, 36 + samples.length * 2, true)
  writeString(view, 8, 'WAVE')
  writeString(view, 12, 'fmt ')
  view.setUint32(16, 16, true)
  view.setUint16(20, 1, true)
  view.setUint16(22, 1, true)
  view.setUint32(24, TARGET_RATE, true)
  view.setUint32(28, TARGET_RATE * 2, true)
  view.setUint16(32, 2, true)
  view.setUint16(34, 16, true)
  writeString(view, 36, 'data')
  view.setUint32(40, samples.length * 2, true)
  for (let i = 0; i < samples.length; i++) {
    const s = Math.max(-1, Math.min(1, samples[i]))
    view.setInt16(44 + i * 2, s < 0 ? s * 0x8000 : s * 0x7fff, true)
  }
  return new Blob([buffer], { type: 'audio/wav' })
}

export class Recorder {
  private mediaRecorder: MediaRecorder | null = null
  private chunks: Blob[] = []
  private stream: MediaStream | null = null
  private startedAt = 0

  static async create(): Promise<Recorder> {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    const rec = new Recorder()
    rec.stream = stream
    rec.mediaRecorder = new MediaRecorder(stream)
    rec.mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) rec.chunks.push(e.data)
    }
    rec.mediaRecorder.start()
    rec.startedAt = Date.now()
    return rec
  }

  elapsedMs(): number {
    return Date.now() - this.startedAt
  }

  stop(): Promise<Blob> {
    return new Promise((resolve, reject) => {
      const mr = this.mediaRecorder
      if (!mr) return reject(new Error('No hay grabación activa'))
      mr.onstop = async () => {
        try {
          this.stream?.getTracks().forEach((t) => t.stop())
          const blob = new Blob(this.chunks, { type: mr.mimeType || 'audio/webm' })
          resolve(await toWav(blob))
        } catch (e) {
          reject(e)
        }
      }
      mr.stop()
    })
  }
}
