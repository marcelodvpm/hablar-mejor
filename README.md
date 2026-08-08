# Habla Mejor

Entrenador de oratoria **100% local**: grabás un audio, te transcribe con Whisper y te da un reporte con métricas de tu forma de hablar (velocidad, muletillas, palabras repetidas, riqueza léxica, pausas, ruidos) y una puntuación de 0 a 100 con sugerencias.

Incluye un **catálogo de ejercicios** de práctica organizados por nivel (principiante / intermedio / avanzado) y por situación real: presentarte, hablar con tu jefe, entrevistas laborales, convencer a un cliente, resolver conflictos, hablar con tu pareja o tus hijos, y más. Cada día hay un **ejercicio del día** rotativo.

**Nada sale de tu PC**: la transcripción y el análisis corren en tu máquina, sin nube, sin claves ni cuentas. Los audios nunca se suben a ningún servidor externo.

---

## Requisitos

- [Docker](https://docs.docker.com/engine/install/) y [Docker Compose](https://docs.docker.com/compose/install/)
- ~3 GB de espacio libre (modelo de Whisper + imágenes)
- 4 GB de RAM recomendados

## Levantar el proyecto

```bash
docker compose up -d --build
```

La primera vez puede tardar varios minutos: descarga las imágenes, instala dependencias y baja el modelo de Whisper (se guarda en el volumen `whisper_cache` para no volver a descargarlo).

## Usar

| Servicio | URL |
|---|---|
| Aplicación (frontend) | http://localhost:8080 |
| API (backend) | http://localhost:8001 |

1. Abrí http://localhost:8080
2. Elegí un ejercicio del catálogo o el ejercicio del día y presioná **Practicar**
3. Grabá tu respuesta (entre 30 segundos y 3 minutos) y presioná **Detener y analizar**
4. Revisá el reporte: puntuación, métricas, transcripción con muletillas resaltadas y sugerencias

## Idiomas

- Español (Argentina) — principal
- English (US) — secundario

Se eligen en la pantalla de grabación antes de grabar.

## Arquitectura

```
┌─────────────┐   /api   ┌──────────────┐
│  frontend   │ ───────► │   backend    │
│  (nginx:80) │          │ (uvicorn:8000)│
│  puerto 8080│          │  puerto 8001  │
└─────────────┘          └──────┬───────┘
                                │
                          ┌─────▼─────┐
                          │  Whisper  │
                          │  (local)  │
                          └───────────┘
```

- **frontend**: React + Vite, compilado y servido por nginx. nginx redirige `/api` al backend y acepta audios de hasta 25 MB.
- **backend**: FastAPI. Recibe el WAV, lo transcribe con `faster-whisper` y calcula las métricas.
- El modelo de Whisper se descarga la primera vez y queda cacheado en el volumen `whisper_cache`.

## Configuración

El backend se configura con variables de entorno (ver `backend/.env.example`):

| Variable | Valor por defecto | Descripción |
|---|---|---|
| `WHISPER_MODEL` | `small` | Modelo de Whisper (`tiny` = más rápido / `small` = recomendado / `medium` = más preciso) |
| `WHISPER_DEVICE` | `cpu` | `cpu` o `cuda` |
| `WHISPER_COMPUTE_TYPE` | `int8` | Precisión del modelo |
| `LANGUAGES` | `es-AR,en-US` | Idiomas soportados |

## Detener

```bash
docker compose down
```

## Endpoints de la API

| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/health` | Estado del servicio |
| `POST` | `/api/analyze` | Analiza un audio WAV (`file` + `language`) |
| `GET` | `/api/exercises` | Catálogo de ejercicios (`?language=&level=`) |
| `GET` | `/api/exercises/daily` | Ejercicio del día (`?language=`) |
