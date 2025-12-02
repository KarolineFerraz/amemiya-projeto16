from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.supabase_client import supabase
from app.auth import verify_token

router = APIRouter(prefix="/instrumentos", tags=["Instrumentos"])


class InstrumentoCreate(BaseModel):
    nome: str
    descricao: str = ""


@router.get("/listar")
def listar_instrumentos(user=Depends(verify_token)):
    try:
        r = supabase.table("instrumentos").select("*").execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar instrumentos: {e}")
    return {"instrumentos": r.data or []}


@router.post("/criar")
def criar_instrumento(dados: InstrumentoCreate, user=Depends(verify_token)):
    # apenas admin pode criar
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Apenas admin pode criar instrumentos")

    novo = {"nome": dados.nome, "descricao": dados.descricao}
    try:
        supabase.table("instrumentos").insert(novo).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar instrumento: {e}")

    return {"status": "Instrumento criado"}


@router.delete("/deletar/{id}")
def deletar_instrumento(id: str, user=Depends(verify_token)):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Apenas admin pode excluir instrumentos")
    try:
        supabase.table("instrumentos").delete().eq("id", id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir instrumento: {e}")
    return {"status": "Instrumento removido"}
