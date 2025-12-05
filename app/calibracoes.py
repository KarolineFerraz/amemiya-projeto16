from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from datetime import datetime
from app.supabase_client import supabase
from app.auth import verify_token
import uuid
import os
from typing import Optional

router = APIRouter(prefix="/calibracoes", tags=["Calibracoes"])

# ---------------------------------------------------------
# LISTAR CALIBRAÇÕES
# ---------------------------------------------------------
@router.get("/listar")
def listar_calibracoes(user=Depends(verify_token)):
    r = supabase.table("calibracoes").select("*").order("created_at", desc=True).execute()
    return {"calibracoes": r.data or []}

# ---------------------------------------------------------
# REGISTRAR CALIBRAÇÃO
# ---------------------------------------------------------
@router.post("/registrar")
async def registrar_calibracao(
    instrumento_id: str = Form(...),
    resultado: str = Form(...),
    imagem: Optional[UploadFile] = File(None),
    user=Depends(verify_token),
):
    url_imagem = None

    # -----------------------------------------
    # SE HOUVER UPLOAD DE IMAGEM
    # -----------------------------------------
    if imagem:
        ext = imagem.filename.split(".")[-1]
        nome_arquivo = f"{uuid.uuid4()}.{ext}"

        # garante que a pasta static exista
        os.makedirs("static", exist_ok=True)

        caminho = os.path.join("static", nome_arquivo)

        with open(caminho, "wb") as f:
            f.write(await imagem.read())

        # URL pública no Render
        url_imagem = f"https://amemiya-backend-karol.onrender.com/static/{nome_arquivo}"

    # -----------------------------------------
    # REGISTRO NO SUPABASE
    # -----------------------------------------
    calib = {
        "instrumento_id": instrumento_id,
        "usuario_id": user["id"],
        "resultado": resultado,
        "imagem_url": url_imagem,
        "created_at": datetime.utcnow().isoformat(),
    }

    supabase.table("calibracoes").insert(calib).execute()

    return {"status": "ok"}
