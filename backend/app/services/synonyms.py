"""Diccionario basico de sinonimos para sugerir ampliacion de vocabulario."""

SYNONYMS_ES: dict[str, list[str]] = {
    "bueno": ["correcto", "adecuado", "apropiado", "acertado", "valioso"],
    "cosa": ["objeto", "elemento", "cuestión", "asunto", "tema"],
    "hacer": ["realizar", "ejecutar", "llevar a cabo", "elaborar", "desarrollar"],
    "ver": ["observar", "examinar", "analizar", "contemplar", "revisar"],
    "decir": ["expresar", "manifestar", "señalar", "indicar", "mencionar"],
    "muy": ["sumamente", "extremadamente", "notablemente", "altamente"],
    "mucho": ["considerable", "abundante", "numeroso", "cuantioso"],
    "grande": ["amplio", "extenso", "considerable", "voluminoso", "enorme"],
    "pequeño": ["reducido", "escaso", "diminuto", "menor"],
    "importante": ["relevante", "significativo", "trascendente", "destacado", "fundamental"],
    "problema": ["dificultad", "inconveniente", "obstáculo", "complicación", "adversidad"],
    "trabajo": ["tarea", "labor", "ocupación", "actividad", "tarea"],
    "gente": ["personas", "público", "individuos", "ciudadanos"],
    "tiempo": ["período", "lapso", "duración", "momento"],
    "lugar": ["espacio", "sitio", "zona", "área", "ubicación"],
    "ayudar": ["asistir", "colaborar", "apoyar", "contribuir", "facilitar"],
    "pensar": ["reflexionar", "considerar", "meditar", "razonar", "valorar"],
    "saber": ["conocer", "dominar", "entender", "comprender"],
    "entender": ["comprender", "asimilar", "interpretar", "captar"],
    "querer": ["desear", "anhelar", "pretender", "aspirar"],
    "necesitar": ["requerir", "precisar", "demandar"],
    "lograr": ["conseguir", "alcanzar", "obtener", "concretar", "materializar"],
    "empezar": ["comenzar", "iniciar", "emprender", "arrancar"],
    "terminar": ["finalizar", "concluir", "culminar", "cerrar"],
    "rápido": ["veloz", "ágil", "expedito", "ligero"],
    "fácil": ["sencillo", "simple", "cómodo", "accesible"],
    "difícil": ["complicado", "complejo", "arduo", "engorroso"],
    "claro": ["evidente", "nítido", "preciso", "inconfundible", "lúcido"],
}

SYNONYMS_EN: dict[str, list[str]] = {
    "good": ["excellent", "outstanding", "suitable", "appropriate"],
    "thing": ["object", "item", "matter", "element"],
    "do": ["perform", "carry out", "execute", "accomplish"],
    "see": ["observe", "examine", "perceive", "witness"],
    "say": ["express", "mention", "state", "indicate"],
    "very": ["extremely", "highly", "remarkably"],
    "big": ["large", "extensive", "considerable"],
    "small": ["little", "reduced", "modest", "minor"],
    "important": ["relevant", "significant", "crucial", "essential"],
    "problem": ["difficulty", "issue", "obstacle", "challenge"],
    "work": ["task", "labor", "assignment", "job"],
    "people": ["individuals", "citizens", "public"],
    "help": ["assist", "support", "collaborate", "aid"],
    "think": ["reflect", "consider", "reason", "contemplate"],
    "know": ["understand", "be familiar with", "recognize"],
    "want": ["desire", "wish", "aim"],
    "need": ["require", "demand", "necessitate"],
    "start": ["begin", "initiate", "commence"],
    "end": ["finish", "conclude", "terminate", "complete"],
    "easy": ["simple", "straightforward", "effortless"],
    "difficult": ["hard", "challenging", "demanding"],
}


def synonyms_for(word: str, language: str) -> list[str]:
    table = SYNONYMS_EN if language.lower().startswith("en") else SYNONYMS_ES
    return table.get(word.lower(), [])
