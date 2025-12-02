from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from datetime import datetime
from app.supabase_client import supabase
from app.auth import verify_token
import uuid
import os

router = APIRouter(prefix="/calibracoes", tags=["Calibrações"])

# caminho absoluto da pasta uploads (para salvar localmente)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
# pasta que será servida como /static/... (main.py monta /static -> app/uploads)
os.makedirs(UPLOADS_DIR, exist_ok=True)


@router.get("/listar")
def listar_calibracoes(user=Depends(verify_token)):
    """
    Retorna um objeto com a lista: {"calibracoes": [...]}
    Mantemos esse formato para o frontend que espera 'calibracoes'.
    """
    try:
        r = (
            supabase.table("calibracoes")
            .select("id, instrumento_id, usuario_id, resultado, imagem_url, created_at")
            .order("created_at", desc=True)
            .execute()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar DB: {e}")

    return {"calibracoes": r.data or []}


@router.post("/registrar")
async def registrar_calibracao(
    instrumento_id: str = Form(...),
    resultado: str = Form(...),
    imagem: UploadFile = File(None),
    user=Depends(verify_token),
):
    """
    Recebe instrumento_id (string/uuid), resultado e imagem opcional.
    Salva imagem em uploads/ e grava URL em imagem_url.
    """
    url_imagem = None
    if imagem:
        # preserva extensão simples
        ext = imagem.filename.rsplit(".", 1)[-1] if "." in imagem.filename else "bin"
        nome_arquivo = f"{uuid.uuid4()}.{ext}"
        caminho = os.path.join(UPLOADS_DIR, nome_arquivo)

        # salva local
        try:
            with open(caminho, "wb") as f:
                f.write(await imagem.read())
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao salvar imagem: {e}")

        # URL pública do backend (quando rodando local)
        url_imagem = f"http://127.0.0.1:8000/static/{nome_arquivo}"

    calib = {
        "instrumento_id": instrumento_id,
        "usuario_id": user["id"],
        "resultado": resultado,
        "imagem_url": url_imagem,
    }

    try:
        r = supabase.table("calibracoes").insert(calib).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir calibração: {e}")

    return {"status": "Calibração registrada com sucesso!", "registro": r.data}
