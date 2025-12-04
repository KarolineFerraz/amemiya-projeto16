from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import router as auth_router
from app.instrumentos import router as instrumentos_router
from app.calibracoes import router as calibracoes_router
from app.usuarios import router as usuarios_router
from app.instrumentos_alerta import router as alerta_router

from app.supabase_client import supabase  # <-- FALTAVA ISSO!!

app = FastAPI()

# ---------------------------------------------
# DEBUG DO SUPABASE (usar só para testar no Render)
# ---------------------------------------------
@app.get("/_debug/supabase")
def debug_supabase():
    """
    Teste simples p/ saber se o Supabase está respondendo no Render.
    NÃO EXIBE CHAVES!
    """
    try:
        r = supabase.table("usuarios").select("id").limit(1).execute()
        return {
            "ok": True,
            "rows": len(r.data or []),
        }
    except Exception as e:
        return {"ok": False, "error": str(e)[:400]}


# ---------------------------------------------
# CONFIGURAÇÃO DE CORS
# ---------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # deixe assim até funcionar no Render
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------
# ROTAS
# ---------------------------------------------
app.include_router(auth_router)
app.include_router(instrumentos_router)
app.include_router(calibracoes_router)
app.include_router(usuarios_router)
app.include_router(alerta_router)


@app.get("/")
def root():
    return {"status": "Backend funcionando!"}
