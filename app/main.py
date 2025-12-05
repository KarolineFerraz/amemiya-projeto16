from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.auth import router as auth_router
from app.instrumentos import router as instrumentos_router
from app.calibracoes import router as calibracoes_router
from app.usuarios import router as usuarios_router
from app.instrumentos_alerta import router as alerta_router

from app.supabase_client import supabase

# ---------------------------------------------------------
# APP FASTAPI
# ---------------------------------------------------------
app = FastAPI()


# ---------------------------------------------------------
# DEBUG DO SUPABASE (opcional)
# ---------------------------------------------------------
@app.get("/_debug/supabase")
def debug_supabase():
    """
    Testa se o Supabase responde corretamente no Render.
    """
    try:
        r = supabase.table("usuarios").select("id").limit(1).execute()
        rows = len(r.data or [])
        return {"ok": True, "rows": rows}
    except Exception as e:
        return {"ok": False, "error": str(e)[:400]}


# ---------------------------------------------------------
# ARQUIVOS ESTÁTICOS (IMAGENS DE CALIBRAÇÃO)
# ---------------------------------------------------------
# Serve os arquivos da pasta app/static
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# ---------------------------------------------------------
# CORS (LIBERA FRONTEND NO RENDER)
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://amemiya-projeto-autogest.onrender.com",
        "*",  # deixar liberado por enquanto
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# ROTAS DO SISTEMA
# ---------------------------------------------------------
app.include_router(auth_router)
app.include_router(instrumentos_router)
app.include_router(calibracoes_router)
app.include_router(usuarios_router)
app.include_router(alerta_router)


# ---------------------------------------------------------
# ROTA PRINCIPAL
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"status": "Backend funcionando no Render!"}
