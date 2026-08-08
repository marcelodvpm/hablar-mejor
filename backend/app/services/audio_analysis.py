"""Analisis acustico de un WAV PCM 16-bit mono.

Calcula actividad de voz, pausas, variacion de volumen (aprox. de tono)
y deteccion heuristica de carraspeos/ruidos (picos de energia en silencios).
"""
import math
import struct
import wave
from dataclasses import dataclass


@dataclass
class AudioFeatures:
    duration_ms: int
    sample_rate: int
    rms_voice_mean: float
    rms_voice_std: float
    pauses: list[dict]           # {start_ms, end_ms, duration_ms} (solo entre voz, sin silencios inicial/final)
    long_pauses: list[dict]
    noise_bursts: list[dict]     # {start_ms, end_ms, duration_ms} posibles carraspeos
    voice_segments: list[dict]   # {start_ms, end_ms, rms_mean}


WINDOW_MS = 20
LONG_PAUSE_MS = 500
BURST_MIN_MS = 80
BURST_MAX_MS = 600
MERGE_GAP_MS = 250


def _read_wav_channels(wav_path: str):
    with wave.open(wav_path, "rb") as wf:
        sample_rate = wf.getframerate()
        nchannels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        frames = wf.readframes(wf.getnframes())
    if sampwidth != 2:
        raise ValueError("El audio debe ser PCM 16-bit.")
    count = len(frames) // 2 // nchannels
    fmt = f"<{count * nchannels}h"
    samples = struct.unpack(fmt, frames[: count * nchannels * 2])
    if nchannels > 1:
        samples = samples[::nchannels]
    return list(samples), sample_rate


def _rms(chunk: list[int]) -> float:
    if not chunk:
        return 0.0
    acc = sum(s * s for s in chunk) / len(chunk)
    return math.sqrt(acc) / 32768.0


def analyze_audio(wav_path: str) -> AudioFeatures:
    samples, sample_rate = _read_wav_channels(wav_path)
    duration_ms = int(len(samples) / sample_rate * 1000)

    win = max(1, int(sample_rate * WINDOW_MS / 1000))
    windows: list[tuple[int, int, float]] = []  # (start_ms, end_ms, rms)
    for i in range(0, len(samples), win):
        chunk = samples[i : i + win]
        start_ms = int(i / sample_rate * 1000)
        end_ms = int((i + len(chunk)) / sample_rate * 1000)
        windows.append((start_ms, end_ms, _rms(chunk)))

    # Umbrales adaptativos segun la energia del audio (funcionan con bajo volumen)
    sorted_rms = sorted(w[2] for w in windows)
    n = len(sorted_rms)
    p10 = sorted_rms[n * 10 // 100] if n else 0.0
    p90 = sorted_rms[n * 90 // 100] if n else 0.0
    vad_threshold = max(0.012, p10 * 3.0)          # voz vs silencio
    burst_threshold = max(vad_threshold * 2.0, p90)  # picos de ruido/carraspeo

    # VAD: segmentos de voz crudos
    raw_voice: list[tuple[int, int]] = []
    cur = None
    for start_ms, end_ms, rms in windows:
        if rms >= vad_threshold:
            if cur is None:
                cur = [start_ms, end_ms]
            else:
                cur[1] = end_ms
        else:
            if cur is not None:
                raw_voice.append(tuple(cur))
                cur = None
    if cur is not None:
        raw_voice.append(tuple(cur))

    # Fusionar segmentos separados por micro-pausas (< 250 ms)
    merged: list[tuple[int, int]] = []
    for start_ms, end_ms in raw_voice:
        if merged and start_ms - merged[-1][1] < MERGE_GAP_MS:
            merged[-1] = (merged[-1][0], end_ms)
        else:
            merged.append((start_ms, end_ms))

    voice_segments: list[dict] = []
    for start_ms, end_ms in merged:
        seg_rms = [w[2] for w in windows if w[0] >= start_ms and w[1] <= end_ms]
        voice_segments.append(
            {
                "start_ms": start_ms,
                "end_ms": end_ms,
                "rms_mean": sum(seg_rms) / len(seg_rms) if seg_rms else 0.0,
            }
        )

    # Pausas: huecos ENTRE segmentos de voz (sin contar silencio inicial/final)
    pauses: list[dict] = []
    for i in range(len(merged) - 1):
        start_ms = merged[i][1]
        end_ms = merged[i + 1][0]
        pauses.append({"start_ms": start_ms, "end_ms": end_ms, "duration_ms": end_ms - start_ms})
    long_pauses = [p for p in pauses if p["duration_ms"] >= LONG_PAUSE_MS]

    # Carraspeos heuristicos: picos cortos de energia dentro de una pausa
    noise_bursts: list[dict] = []
    for start_ms, end_ms, rms in windows:
        if rms >= burst_threshold and any(p["start_ms"] <= start_ms and end_ms <= p["end_ms"] for p in pauses):
            if noise_bursts and start_ms - noise_bursts[-1]["end_ms"] <= 40:
                noise_bursts[-1]["end_ms"] = end_ms
                noise_bursts[-1]["duration_ms"] = end_ms - noise_bursts[-1]["start_ms"]
            else:
                noise_bursts.append({"start_ms": start_ms, "end_ms": end_ms, "duration_ms": end_ms - start_ms})
    noise_bursts = [b for b in noise_bursts if BURST_MIN_MS <= b["duration_ms"] <= BURST_MAX_MS]

    if voice_segments:
        rms_values = [v["rms_mean"] for v in voice_segments]
        mean = sum(rms_values) / len(rms_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in rms_values) / len(rms_values))
    else:
        mean, std = 0.0, 0.0

    return AudioFeatures(
        duration_ms=duration_ms,
        sample_rate=sample_rate,
        rms_voice_mean=mean,
        rms_voice_std=std,
        pauses=pauses,
        long_pauses=long_pauses,
        noise_bursts=noise_bursts,
        voice_segments=voice_segments,
    )
