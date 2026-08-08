import threading

from faster_whisper import WhisperModel

from app.core.config import settings


class TranscriptionError(Exception):
    pass


LANGUAGE_MAP = {
    "es-AR": "es",
    "en-US": "en",
}

_model: WhisperModel | None = None
_model_lock = threading.Lock()


def _get_model() -> WhisperModel:
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                _model = WhisperModel(
                    settings.whisper_model,
                    device=settings.whisper_device,
                    compute_type=settings.whisper_compute_type,
                )
    return _model


def transcribe_wav(wav_path: str, language: str) -> dict:
    """Transcribe un WAV localmente con Whisper (faster-whisper).

    Devuelve: { "words": [...], "segments": [...] } con timestamps en ms.
    El modelo se descarga una sola vez y queda cacheado en el contenedor.
    """
    whisper_lang = LANGUAGE_MAP.get(language)
    model = _get_model()

    segments, _info = model.transcribe(
        wav_path,
        language=whisper_lang,
        word_timestamps=True,
        vad_filter=True,
    )

    words: list[dict] = []
    segments_out: list[dict] = []
    for seg in segments:
        seg_words = list(seg.words or [])
        segments_out.append(
            {
                "text": seg.text.strip(),
                "offset_ms": int(seg.start * 1000),
                "duration_ms": int((seg.end - seg.start) * 1000),
                "confidence": float(getattr(seg, "avg_logprob", 0.0) or 0.0),
            }
        )
        for w in seg_words:
            words.append(
                {
                    "word": (w.word or "").strip().lower(),
                    "start_ms": int(w.start * 1000),
                    "end_ms": int(w.end * 1000),
                    "confidence": float(getattr(w, "probability", 0.0) or 0.0),
                }
            )

    if not words:
        raise TranscriptionError("No se pudo reconocer voz en el audio.")

    return {"words": words, "segments": segments_out}
