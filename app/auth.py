from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from app.supabase_client import supabase
import jwt
import os
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "minha_chave_secreta_de_desenvolvimento_123")


# Modelo para login
class LoginPayload(BaseModel):
    username: str
    password: str


# ------------------------------------------------------------
#   VALIDAÇÃO DO TOKEN — ACEITA AUTORIZAÇÃO COM A E SEM A
# ------------------------------------------------------------
def verify_token(
    authorization: Optional[str] = Header(default=None),
    Authorization: Optional[str] = Header(default=None)
):
    """
    Valida o token enviado. Agora funciona tanto para o frontend
    quanto para o Swagger (que usa 'authorization' minúsculo).
    """

    header = authorization or Authorization

    if not header:
        raise HTTPException(status_code=401, detail="Cabeçalho de autorização ausente")

    if not header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token mal formatado")

    token = header.split(" ", 1)[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token mal formado (id ausente)")

    # Busca o usuário no Supabase
    r = supabase.table("usuarios").select("*").eq("id", user_id).execute()

    if not r.data:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return r.data[0]  # retorna dict do usuário


# ------------------------------------------------------------
#   LOGIN
# ------------------------------------------------------------
@router.post("/login")
def login(dados: LoginPayload):
    """
    Efetua login. Retorna {"token": "..."} se correto.
    """

    r = (
        supabase.table("usuarios")
        .select("*")
        .eq("username", dados.username)
        .eq("password", dados.password)
        .execute()
    )

    if not r.data:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    user = r.data[0]

    token = jwt.encode({"id": user["id"]}, SECRET_KEY, algorithm="HS256")

    return {
        "token": token,
        "usuario": {
            "id": user["id"],
            "username": user["username"],
            "role": user["role"]
        }
    }
