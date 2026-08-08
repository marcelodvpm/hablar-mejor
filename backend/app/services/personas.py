"""Catalogo de oradores y personajes para practicar la imitacion de estilo.

Cada persona tiene: categoria, descripcion de estilo, un texto modelo
ORIGINAL de practica (no una cita del orador), un desafio, estructura
recomendada y tips.
"""

PERSONAS: list[dict] = [
    {
        "id": "perez-laguna",
        "name": "Miguel Ángel Pérez Laguna",
        "category": "orador motivacional",
        "style": "Cercano y enérgico, cuenta historias y habla de tú a tú con el auditorio. Especialista en liderazgo, motivación e innovación.",
        "sample_text": "La innovación no espera. No nace en una sala de reuniones: nace cuando alguien decide hacer las cosas distinto. Hoy no vine a hablarles de tecnología; vine a hablarles de ustedes, de la fuerza que tienen y todavía no usan.",
        "challenge": "Convencé a un equipo de trabajo de que el cambio es urgente. Hablá con energía y cercanía, como si fueras su líder.",
        "structure": ["Abrí con una historia corta o una pregunta al público", "Dos frases cortas y directas sobre el cambio", "Un cierre que los deje con ganas de actuar"],
        "tips": ["Frases cortas: una idea por oración", "Hacé preguntas directas al público", "Contá una historia personal breve", "Subí la energía variando el volumen", "Mirá al micrófono como si fuera una persona"],
        "minutes": 2,
    },
    {
        "id": "ivan-espinosa",
        "name": "Iván Espinosa de los Monteros",
        "category": "orador retórico",
        "style": "Sobrio, con ironía medida y contundencia. Habla sin notas y arma cada frase con precisión.",
        "sample_text": "Permítanme ser directo: los discursos bonitos sobran. Lo que realmente sobra es la distancia entre lo que prometemos y lo que hacemos. Si hay algo de lo que podamos hablar con honestidad hoy, es de eso.",
        "challenge": "Elegí un tema de actualidad y opiná con sobriedad e ironía, sin leer ni usar apuntes.",
        "structure": ["Una frase contundente de apertura", "La crítica con ironía medida", "Una propuesta concreta de cierre"],
        "tips": ["Sin notas: hablá de memoria o con una sola idea guía", "Ironía fina: el contraste entre lo que se dice y lo que se quiere decir", "Frases contundentes: evitá 'quizás' y 'más o menos'", "Pausa antes de la frase clave"],
        "minutes": 2,
    },
    {
        "id": "alan-garcia",
        "name": "Alan García",
        "category": "orador político",
        "style": "Manejo poético y persuasivo del idioma. Vocabulario amplio, imágenes y un ritmo solemne que envuelve al auditorio.",
        "sample_text": "Hay naciones que avanzan porque saben mirar el horizonte. Nosotros también podemos mirarlo: no como un sueño lejano, sino como el mapa de lo que estamos dispuestos a construir. Nuestra tierra sabe de palabras; ahora debe saber de hechos.",
        "challenge": "Hablá sobre el futuro de tu comunidad en un tono solemne, poético y persuasivo.",
        "structure": ["Una imagen o metáfora de apertura", "El contraste entre la realidad y el futuro posible", "Un cierre con fuerza y esperanza"],
        "tips": ["Vocabulario amplio y preciso: usá sinónimos exactos", "Metáforas e imágenes que pinten lo que decís", "Ritmo lento y solemne: dejá que la frase respire", "Pausa dramática antes del cierre", "Gesto amplio y mirada al auditorio"],
        "minutes": 2,
    },
    {
        "id": "garcia-chaparro",
        "name": "Alberto García Chaparro",
        "category": "campeón de oratoria",
        "style": "Estructura perfecta y dominio escénico. Campeón mundial de oratoria en español: aperturas impactantes y cierres que se recuerdan.",
        "sample_text": "¿Cuántas veces callamos por miedo al ridículo? ¿Cuántas veces dejamos que el silencio hable por nosotros? La palabra es el músculo más poderoso que tenemos, y hoy, aquí, vamos a ejercitarlo.",
        "challenge": "Armá un discurso de un minuto con apertura impactante, tres argumentos y un cierre memorable.",
        "structure": ["Apertura con pregunta retórica o dato impactante", "Tres argumentos en orden creciente", "Cierre que repite la apertura (anáfora)"],
        "tips": ["Empezá con una pregunta retórica al auditorio", "Estructura en tres partes: se recuerda mejor", "Anáfora: repetí una frase al inicio de cada párrafo", "Proyectá la voz: el final debe sonar más fuerte", "Controlá el tiempo: un minuto exacto"],
        "minutes": 1,
    },
]


def list_personas() -> list[dict]:
    return PERSONAS
