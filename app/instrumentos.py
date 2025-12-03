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
    r = supabase.table("instrumentos").select("*").execute()
    return {"instrumentos": r.data or []}

@router.post("/criar")
def criar_instrumento(dados: InstrumentoCreate, user=Depends(verify_token)):
    # permite só admin/gerente se quiser
    novo = {"nome": dados.nome, "descricao": dados.descricao}
    supabase.table("instrumentos").insert(novo).execute()
    return {"status":"ok"}

@router.delete("/deletar/{id}")
def deletar_instrumento(id: str, user=Depends(verify_token)):
    supabase.table("instrumentos").delete().eq("id", id).execute()
    return {"status":"ok"}
