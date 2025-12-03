from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
from app.supabase_client import supabase
from app.auth import verify_token

router = APIRouter(prefix="/instrumentos", tags=["Alertas"])

@router.get("/alertas")
def verificar_alertas(user=Depends(verify_token)):
    hoje = datetime.utcnow().date()
    proximidade = hoje + timedelta(days=5)

    r = supabase.table("instrumentos").select("*").execute()
    instrumentos = r.data or []

    alertas = []

    for inst in instrumentos:
        prox = inst.get("proxima_calibracao")
        if not prox:
            continue

        data_prox = datetime.fromisoformat(prox).date()

        if data_prox < hoje:
            alertas.append({
                "id": inst["id"],
                "nome": inst.get("nome"),
                "proxima_calibracao": inst.get("proxima_calibracao"),
                "status": "vencido",
                "mensagem": "Calibração VENCIDA!"
            })

        elif hoje <= data_prox <= proximidade:
            alertas.append({
                "id": inst["id"],
                "nome": inst.get("nome"),
                "proxima_calibracao": inst.get("proxima_calibracao"),
                "status": "perto_vencer",
                "mensagem": "Calibração perto do vencimento"
            })

    return {"alertas": alertas}
