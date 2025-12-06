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
# REGISTRAR CALIBRAÇÃO (com Supabase Storage!)
# ---------------------------------------------------------
@router.post("/registrar")
async def registrar_calibracao(
    instrumento_id: str = Form(...),
    resultado: str = Form(...),
    imagem: Optional[UploadFile] = File(None),
    user=Depends(verify_token),
):

    url_imagem = None

    # ---------- UPLOAD PARA SUPABASE STORAGE ----------
    if imagem:
        ext = imagem.filename.split(".")[-1]
        nome_arquivo = f"{uuid.uuid4()}.{ext}"
        caminho = f"calibracoes/{nome_arquivo}"

        conteudo = await imagem.read()

        # upload para Storage
        supabase.storage.from_("calibracoes").upload(
            caminho, conteudo,
            file_options={"content-type": imagem.content_type}
        )

        # torna o arquivo público e obtém URL
        dados_url = supabase.storage.from_("calibracoes").get_public_url(caminho)
        url_imagem = dados_url.get("publicUrl")

    # ---------- SALVAR NO BANCO ----------
    calib = {
        "instrumento_id": instrumento_id,
        "usuario_id": user["id"],
        "resultado": resultado,
        "imagem_url": url_imagem,
        "created_at": datetime.utcnow().isoformat()
    }

    supabase.table("calibracoes").insert(calib).execute()

    return {"status": "ok"}
