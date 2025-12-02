from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel
from app.supabase_client import supabase
import jwt
import os
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = os.getenv("SECRET_KEY", "minha_chave_secreta_de_desenvolvimento_123")


# Modelo simples para login
class LoginPayload(BaseModel):
    username: str
    password: str


def verify_token(
    authorization: Optional[str] = Header(default=None, alias="Authorization")
):
    """
    Valida o token JWT recebido no header Authorization.
    Retorna o usuário (dict) se token ok; lança HTTPException caso contrário.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Cabeçalho de autorização ausente")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token mal formatado")

    token = authorization.split(" ", 1)[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido")

    user_id = payload.get("id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token mal formado (id ausente)")

    # consulta no Supabase
    r = supabase.table("usuarios").select("*").eq("id", user_id).execute()
    if not r.data:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    return r.data[0]  # retorna dict do usuário para usar no Depends


@router.post("/login")
def login(dados: LoginPayload):
    """
    Faz login; retorna {"token": "<jwt>"} em caso de sucesso.
    OBS: nesse projeto o password está em texto (igual ao seu banco atual).
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
    # jwt.encode no pyjwt>=2 retorna string
    return {"token": token}
