from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth import router as auth_router
from app.instrumentos import router as instrumentos_router
from app.calibracoes import router as calibracoes_router
from app.usuarios import router as usuarios_router
from app.instrumentos_alerta import router as alerta_router

app = FastAPI()
# adicionar logo após app = FastAPI() no app/main.py

from fastapi import FastAPI
# ... (se já importou FastAPI e criou app, apenas adicione abaixo)
@app.get("/_debug/supabase")
def debug_supabase():
    """
    Endp temporário: checa se o supabase client consegue executar uma consulta simples.
    NÃO EXIBE CHAVES. Remova quando resolver.
    """
    try:
        r = supabase.table("usuarios").select("id").limit(1).execute()
        # r.data pode ser None ou lista
        rows = len(r.data or [])
        return {"ok": True, "rows": rows}
    except Exception as e:
        # retorna somente os primeiros 400 chars do erro
        return {"ok": False, "error": str(e)[:400]}
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROTAS
app.include_router(auth_router)
app.include_router(instrumentos_router)
app.include_router(calibracoes_router)
app.include_router(usuarios_router)
app.include_router(alerta_router)

@app.get("/")
def root():
    return {"status": "Backend funcionando!"}
