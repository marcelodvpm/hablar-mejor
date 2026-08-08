from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import analysis, exercises, personas

app = FastAPI(title="Habla Mejor API", description="Análisis de oratoria y expresión oral", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router)
app.include_router(exercises.router)
app.include_router(personas.router)


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}
