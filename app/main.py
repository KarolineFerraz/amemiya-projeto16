from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import router as auth_router
from app.instrumentos import router as instrumentos_router
from app.calibracoes import router as calibracoes_router
from app.usuarios import router as usuarios_router

app = FastAPI()

# CORS — MUITO IMPORTANTE ESTAR AQUI, ANTES DE TUDO
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(instrumentos_router)
app.include_router(calibracoes_router)
app.include_router(usuarios_router)
