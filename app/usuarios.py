from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.supabase_client import supabase
from app.auth import verify_token

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

class UsuarioCreate(BaseModel):
    username: str
    password: str
    role: str = "funcionario"

@router.get("/listar")
def listar_usuarios(user=Depends(verify_token)):
    r = supabase.table("usuarios").select("*").execute()
    return {"usuarios": r.data or []}

@router.post("/criar")
def criar_usuario(dados: UsuarioCreate, user=Depends(verify_token)):
    # apenas gerente pode criar (exemplo)
    if user.get("role") != "gerente":
        raise HTTPException(403, "Apenas gerente pode criar usuários")
    novo = {"username": dados.username, "password": dados.password, "role": dados.role}
    supabase.table("usuarios").insert(novo).execute()
    return {"status":"ok"}

@router.delete("/deletar/{id}")
def deletar_usuario(id: str, user=Depends(verify_token)):
    if user.get("role") != "gerente":
        raise HTTPException(403, "Apenas gerente pode deletar usuários")
    supabase.table("usuarios").delete().eq("id", id).execute()
    return {"status":"ok"}
