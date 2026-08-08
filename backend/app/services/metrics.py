"""Calculo de metricas de oratoria a partir de la transcripcion y el audio."""

from . import synonyms as syn
from .audio_analysis import AudioFeatures

# Muletillas por idioma (palabras sueltas y frases de dos palabras)
FILLERS_ES = {
    "eh", "mmm", "mm", "este", "digamos", "osea", "tipo", "viste",
    "bueno", "entonces", "mirá", "imaginate",
}
FILLER_PHRASES_ES = ["o sea", "este eh", "bueno este", "por asi decirlo", "quiero decir", "como quien dice"]
FILLERS_EN = {"uh", "um", "er", "like", "well", "basically", "actually", "you", "so", "kind"}
FILLER_PHRASES_EN = ["you know", "i mean", "you know what", "sort of", "kind of"]

# Palabras funcionales que no cuentan como riqueza lexica
STOPWORDS_ES = {
    "el", "la", "los", "las", "de", "del", "que", "y", "o", "u", "a", "al",
    "en", "es", "un", "una", "unos", "unas", "con", "por", "para", "se", "su",
    "lo", "le", "les", "mi", "tu", "me", "te", "no", "si", "ya", "como", "mas",
    "menos", "pero", "este", "esta", "eso", "esa", "hay", "ser", "está", "son",
}
STOPWORDS_EN = {
    "the", "a", "an", "of", "and", "or", "to", "in", "on", "at", "is", "are",
    "was", "were", "be", "been", "it", "its", "this", "that", "these", "those",
    "i", "you", "he", "she", "we", "they", "my", "your", "his", "her", "our",
    "their", "for", "with", "but", "so", "if", "do", "does", "did", "have",
    "has", "had", "not", "no", "as", "from", "by",
}


def _normalize(word: str) -> str:
    return word.lower().strip(".,;:!?¿¡()\"'-")


def _fillers_for(language: str):
    if language.lower().startswith("en"):
        return FILLERS_EN, FILLER_PHRASES_EN, STOPWORDS_EN
    return FILLERS_ES, FILLER_PHRASES_ES, STOPWORDS_ES


def compute_metrics(words: list[dict], audio: AudioFeatures, language: str) -> dict:
    fillers_set, filler_phrases, stopwords = _fillers_for(language)

    normalized = [_normalize(w["word"]) for w in words]
    total_words = len(words)

    # marca muletillas (palabra suelta)
    for i, w in enumerate(words):
        w["is_filler"] = normalized[i] in fillers_set

    # muletillas de varias palabras ("o sea", "you know"...) sobre el texto plano
    plain_words = [w["word"] for w in words]
    plain_text = " ".join(plain_words).lower()
    filler_counts: dict[str, int] = {}
    for w, w_dict in zip(normalized, words):
        if w in fillers_set:
            filler_counts[w] = filler_counts.get(w, 0) + 1
    for phrase in filler_phrases:
        count = plain_text.count(phrase)
        if count:
            filler_counts[phrase] = filler_counts.get(phrase, 0) + count

    # frecuencia de palabras de contenido (para repeticiones)
    freq: dict[str, int] = {}
    for i, w in enumerate(words):
        n = normalized[i]
        if not n or n in fillers_set or n in stopwords:
            continue
        freq[n] = freq.get(n, 0) + 1

    content_words = [w for i, w in enumerate(words) if normalized[i] not in stopwords and not w.get("is_filler")]
    unique_content = len({_normalize(w["word"]) for w in content_words})
    type_token_ratio = round(unique_content / total_words, 3) if total_words else 0

    # palabras mas repetidas (de contenido)
    repeated = sorted(((c, w) for w, c in freq.items() if c >= 3), reverse=True)
    repeated_words = []
    for count, word in repeated:
        occurrences = [int(w["start_ms"]) for i, w in enumerate(words) if normalized[i] == word]
        repeated_words.append(
            {
                "word": word,
                "count": count,
                "occurrences": occurrences,
                "synonyms": syn.synonyms_for(word, language),
            }
        )
        for w, n in zip(words, normalized):
            if n == word:
                w["is_repeated"] = True

    for w in words:
        w.setdefault("is_repeated", False)

    # velocidad
    pause_ms = sum(p["duration_ms"] for p in audio.pauses)
    speaking_ms = max(1, audio.duration_ms - pause_ms)
    words_per_minute = round(total_words / (speaking_ms / 60000.0), 1) if speaking_ms else 0

    return {
        "words": words,
        "transcript": " ".join(plain_words),
        "total_words": total_words,
        "unique_content_words": unique_content,
        "type_token_ratio": type_token_ratio,
        "words_per_minute": words_per_minute,
        "speaking_ms": speaking_ms,
        "filler_total": sum(filler_counts.values()),
        "filler_words": [{"word": w, "count": c} for w, c in sorted(filler_counts.items(), key=lambda x: -x[1])],
        "repeated_words": repeated_words,
        "long_pauses_count": len(audio.long_pauses),
        "long_pauses": audio.long_pauses,
        "noise_bursts_count": len(audio.noise_bursts),
        "noise_bursts": audio.noise_bursts[:10],
        "loudness_variance": round(audio.rms_voice_std, 4),
        "duration_ms": audio.duration_ms,
    }
