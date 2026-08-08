"""Genera feedback textual automatico (reglas) a partir de las metricas."""

IDEAL_WPM_MIN = 120
IDEAL_WPM_MAX = 150


def _build_feedback(m: dict, language: str) -> dict:
    es = language.lower().startswith("es")

    def t(es_text: str, en_text: str) -> str:
        return es_text if es else en_text

    score = 100.0
    verdicts: list[dict] = []
    suggestions: list[str] = []

    # Velocidad
    wpm = m["words_per_minute"]
    if wpm == 0:
        verdicts.append({"category": "velocidad", "verdict": "media", "text": t("Sin voz detectada.", "No speech detected.")})
    elif wpm > IDEAL_WPM_MAX + 30:
        score -= 15
        verdicts.append({"category": "velocidad", "verdict": "alta", "text": t(f"{wpm} ppm — hablás muy rápido para una exposición.", f"{wpm} wpm — you speak too fast for a talk.")})
        suggestions.append(t("Desacelerá y hacé pausas breves entre ideas.", "Slow down and pause briefly between ideas."))
    elif wpm > IDEAL_WPM_MAX:
        verdicts.append({"category": "velocidad", "verdict": "media-alta", "text": t(f"{wpm} ppm — ritmo vivo, cuidado de no acelerarte.", f"{wpm} wpm — lively pace; watch out not to speed up.")})
    elif wpm < IDEAL_WPM_MIN - 15:
        score -= 10
        verdicts.append({"category": "velocidad", "verdict": "baja", "text": t(f"{wpm} ppm — ritmo muy lento, podés perder atención.", f"{wpm} wpm — too slow, you may lose attention.")})
        suggestions.append(t("Procurá un ritmo más fluido entre 120 y 150 palabras por minuto.", "Aim for a more fluid pace between 120 and 150 words per minute."))
    else:
        verdicts.append({"category": "velocidad", "verdict": "optima", "text": t(f"{wpm} ppm — ritmo adecuado.", f"{wpm} wpm — good pace.")})

    # Muletillas
    fillers = m["filler_total"]
    if fillers > 0:
        tops = ", ".join(f"{f['word']} ({f['count']})" for f in m["filler_words"][:5])
        if fillers >= 10:
            score -= 20
            verdicts.append({"category": "muletillas", "verdict": "alta", "text": t(f"Detectadas {fillers} muletillas ({tops}).", f"Detected {fillers} filler words ({tops}).")})
            suggestions.append(t("Sustituí las muletillas por un silencio breve mientras pensás.", "Replace filler words with a short silence while you think."))
        else:
            score -= 8
            verdicts.append({"category": "muletillas", "verdict": "media", "text": t(f"{fillers} muletillas ({tops}).", f"{fillers} filler words ({tops}).")})
            suggestions.append(t("Anotá tus muletillas y practicá reemplazarlas por pausas.", "Note your fillers and practice replacing them with pauses."))
    else:
        verdicts.append({"category": "muletillas", "verdict": "ninguna", "text": t("Sin muletillas. ¡Excelente!", "No filler words. Excellent!")})

    # Vocabulario / repeticiones
    if m["repeated_words"]:
        top_word = m["repeated_words"][0]
        score -= 10
        syn_text = f" Probá: {', '.join(top_word['synonyms'][:3])}." if top_word["synonyms"] else ""
        verdicts.append({"category": "vocabulario", "verdict": "repetido", "text": t(
            f"Repetís mucho '{top_word['word']}' ({top_word['count']} veces).{syn_text}",
            f"You repeat '{top_word['word']}' a lot ({top_word['count']} times).{syn_text}",
        )})
        if top_word["synonyms"]:
            suggestions.append(t(f"Usá sinónimos de '{top_word['word']}': {', '.join(top_word['synonyms'][:4])}.", f"Use synonyms for '{top_word['word']}': {', '.join(top_word['synonyms'][:4])}."))
    else:
        verdicts.append({"category": "vocabulario", "verdict": "variado", "text": t("Vocabulario variado, sin repeticiones marcadas.", "Varied vocabulary, no marked repetitions.")})

    ttr = m["type_token_ratio"]
    if ttr < 0.35:
        score -= 5
        verdicts.append({"category": "riqueza_lexica", "verdict": "baja", "text": t(f"Riqueza léxica baja (TTR {ttr:.2f}); variás poco las palabras.", f"Low lexical richness (TTR {ttr:.2f}); little word variety.")})
    elif ttr > 0.55:
        verdicts.append({"category": "riqueza_lexica", "verdict": "alta", "text": t(f"Buena riqueza léxica (TTR {ttr:.2f}).", f"Good lexical richness (TTR {ttr:.2f}).")})

    # Pausas
    long_pauses = m["long_pauses_count"]
    if long_pauses >= 5:
        score -= 10
        verdicts.append({"category": "pausas", "verdict": "muchas", "text": t(f"{long_pauses} pausas largas (>0.5s): cortan el discurso.", f"{long_pauses} long pauses (>0.5s): they break the flow.")})
        suggestions.append(t("Reducí las pausas largas; mantení el hilo con frases conectadas.", "Reduce long pauses; keep the thread with connected phrases."))
    elif long_pauses > 0:
        verdicts.append({"category": "pausas", "verdict": "algunas", "text": t(f"{long_pauses} pausas largas: aceptables si las usás para enfatizar.", f"{long_pauses} long pauses: fine if used to emphasize.")})

    # Carraspeos / ruidos
    bursts = m["noise_bursts_count"]
    if bursts:
        score -= bursts * 2
        verdicts.append({"category": "defectos", "verdict": "detectado", "text": t(f"Posibles carraspeos/ruidos: {bursts}.", f"Possible throat clearings/noises: {bursts}.")})
        suggestions.append(t("Hidratate antes de exponer y respirá por la nariz antes de empezar.", "Hydrate before speaking and breathe through your nose before starting."))

    # Tono / expresividad
    var = m["loudness_variance"]
    if 0 < var < 0.03:
        score -= 5
        verdicts.append({"category": "tono", "verdict": "monotono", "text": t("Variación de volumen muy baja: suena monótono.", "Very low volume variation: sounds monotone.")})
        suggestions.append(t("Variá el volumen y la entonación para destacar ideas clave.", "Vary volume and intonation to highlight key ideas."))
    elif var >= 0.08:
        verdicts.append({"category": "tono", "verdict": "expresivo", "text": t("Buena expresividad y variación de volumen.", "Good expressiveness and volume variation.")})

    score = max(0, round(score))
    verdicts.append({"category": "puntuacion", "verdict": "total", "text": t(f"Puntuación general: {score}/100", f"Overall score: {score}/100")})

    return {"score": score, "verdicts": verdicts, "suggestions": suggestions}


def generate_feedback(metrics: dict, language: str) -> dict:
    return _build_feedback(metrics, language)
