import tempfile
import os
import shutil

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel

from app.core.config import settings
from app.services import audio_analysis, feedback, metrics, transcriber

router = APIRouter(prefix="/api", tags=["analisis"])


class AnalyzeResponse(BaseModel):
    language: str
    metrics: dict
    feedback: dict


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    file: UploadFile = File(...),
    language: str = Form("es-AR"),
):
    if language not in settings.supported_languages:
        raise HTTPException(status_code=400, detail=f"Idioma no soportado. Usar: {', '.join(settings.supported_languages)}")
    if not file.filename or not file.filename.lower().endswith(".wav"):
        raise HTTPException(status_code=400, detail="Se espera un archivo WAV (PCM 16-bit).")

    tmp_dir = tempfile.mkdtemp(prefix="habla_")
    wav_path = os.path.join(tmp_dir, "audio.wav")
    try:
        with open(wav_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        audio = audio_analysis.analyze_audio(wav_path)

        try:
            stt = transcriber.transcribe_wav(wav_path, language)
        except transcriber.TranscriptionError as exc:
            raise HTTPException(status_code=422, detail=str(exc))

        met = metrics.compute_metrics(stt["words"], audio, language)
        fb = feedback.generate_feedback(met, language)
        return AnalyzeResponse(language=language, metrics=met, feedback=fb)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
