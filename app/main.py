import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.auth import router as auth_router
from app.instrumentos import router as instrumentos_router
from app.calibracoes import router as calibracoes_router
from app.usuarios import router as usuarios_router
from app.instrumentos_alerta import router as alerta_router

from app.supabase_client import supabase

app = FastAPI()

# ---------------------------------------------------------
# DEBUG SUPABASE
# ---------------------------------------------------------
@app.get("/_debug/supabase")
def debug_supabase():
    try:
        r = supabase.table("usuarios").select("id").limit(1).execute()
        rows = len(r.data or [])
        return {"ok": True, "rows": rows}
    except Exception as e:
        return {"ok": False, "error": str(e)[:400]}


# ---------------------------------------------------------
# STATIC FILES (IMAGENS)
# ---------------------------------------------------------
STATIC_DIR = "app/static"
os.makedirs(STATIC_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://amemiya-frontend-karol.onrender.com",
        "https://amemiya-projeto-autogest.onrender.com",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# ROTAS
# ---------------------------------------------------------
app.include_router(auth_router)
app.include_router(instrumentos_router)
app.include_router(calibracoes_router)
app.include_router(usuarios_router)
app.include_router(alerta_router)


# ---------------------------------------------------------
# ROTA RAIZ
# ---------------------------------------------------------
@app.get("/")
def root():
    return {"status": "Backend funcionando no Render!"}
