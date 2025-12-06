from fastapi import APIRouter, File, UploadFile, Form, Depends
from datetime import datetime
from app.supabase_client import supabase
from app.auth import verify_token
import uuid
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
# REGISTRAR CALIBRAÇÃO (UPLOAD NO SUPABASE STORAGE)
# ---------------------------------------------------------
@router.post("/registrar")
async def registrar_calibracao(
    instrumento_id: str = Form(...),
    resultado: str = Form(...),
    imagem: Optional[UploadFile] = File(None),
    user=Depends(verify_token),
):
    url_imagem = None

    # ---------------------------------------------------------
    # UPLOAD PARA SUPABASE STORAGE
    # ---------------------------------------------------------
    if imagem:
        ext = imagem.filename.split(".")[-1].lower()
        nome_arquivo = f"{uuid.uuid4()}.{ext}"

        bucket = "calibracoes_imgs"  # <-- CONFIRA SE ESTE É O NOME DO SEU BUCKET

        file_bytes = await imagem.read()

        upload_response = supabase.storage.from_(bucket).upload(
            path=nome_arquivo,
            file=file_bytes,
            file_options={"content-type": imagem.content_type}
        )

        # URL pública
        url_imagem = supabase.storage.from_(bucket).get_public_url(nome_arquivo)

    # ---------------------------------------------------------
    # REGISTRO NO SUPABASE DATABASE
    # ---------------------------------------------------------
    registro = {
        "instrumento_id": instrumento_id,
        "usuario_id": user["id"],
        "resultado": resultado,
        "imagem_url": url_imagem,
        "created_at": datetime.utcnow().isoformat(),
    }

    supabase.table("calibracoes").insert(registro).execute()

    return {"status": "ok"}
