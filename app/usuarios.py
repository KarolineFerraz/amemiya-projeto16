from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.supabase_client import supabase
from app.auth import verify_token

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

# -----------------------------
# Modelos
# -----------------------------
class UsuarioCreate(BaseModel):
    username: str
    password: str
    role: str  # "admin" ou "tecnico"


# -----------------------------
# LISTAR TODOS OS USUÁRIOS
# -----------------------------
@router.get("/listar")
def listar_usuarios(user_id=Depends(verify_token)):
    # Buscar usuário logado para ver nível de acesso
    usuario = supabase.table("usuarios").select("*").eq("id", user_id).execute().data

    if not usuario:
        raise HTTPException(401, "Usuário não encontrado")

    if usuario[0]["role"] != "admin":
        raise HTTPException(403, "Apenas ADMIN pode listar usuários")

    result = supabase.table("usuarios").select("*").execute()
    return {"usuarios": result.data}


# -----------------------------
# CRIAR NOVO USUÁRIO
# -----------------------------
@router.post("/criar")
def criar_usuario(dados: UsuarioCreate, user_id=Depends(verify_token)):

    usuario = supabase.table("usuarios").select("*").eq("id", user_id).execute().data
    if not usuario or usuario[0]["role"] != "admin":
        raise HTTPException(403, "Apenas ADMIN pode criar usuários")

    # Verificar se username já existe
    ja_existe = (
        supabase.table("usuarios")
        .select("*")
        .eq("username", dados.username)
        .execute()
    ).data

    if ja_existe:
        raise HTTPException(400, "Nome de usuário já existe")

    novo_usuario = {
        "username": dados.username,
        "password": dados.password,  # sem hash — igual seu banco atual
        "role": dados.role,
    }

    supabase.table("usuarios").insert(novo_usuario).execute()

    return {"status": "Usuário criado com sucesso!"}


# -----------------------------
# EXCLUIR USUÁRIO
# -----------------------------
@router.delete("/deletar/{id}")
def deletar_usuario(id: str, user_id=Depends(verify_token)):

    usuario = supabase.table("usuarios").select("*").eq("id", user_id).execute().data
    if not usuario or usuario[0]["role"] != "admin":
        raise HTTPException(403, "Apenas ADMIN pode excluir usuários")

    # Não permitir excluir outros administradores
    alvo = supabase.table("usuarios").select("*").eq("id", id).execute().data
    if alvo and alvo[0]["role"] == "admin":
        raise HTTPException(403, "Não é permitido excluir administradores")

    supabase.table("usuarios").delete().eq("id", id).execute()

    return {"status": "Usuário excluído"}
