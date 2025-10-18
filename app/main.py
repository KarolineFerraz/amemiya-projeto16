SUPABASE_URL=https://ungsoxiccnjhjbzgwxcg.supabase.com
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVuZ3NveGljY25qaGpiemd3eGNnIiwicm9sZSI6ImFub24iLC>
DATABASE_URL'=postgresql://postgres:K%40h200340@db.ungsoxiccnjhjbzgwxcg.supabase.co:5432/postgres'
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, timedelta
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="API de Metrologia - Amemiya")
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/calibrate")
async def calibrate_instrument(
    tag: str = Form(...),
    name: str = Form(...),
    last_date: str = Form(...),
    file: UploadFile = File(...)
):
    filename = f"{tag}_{file.filename}"
    content = await file.read()
    supabase.storage.from_("instrumentos").upload(filename, content)
    image_url = f"{os.getenv('SUPABASE_URL')}/storage/v1/object/public/instrumentos/{filename}"

    next_date = date.fromisoformat(last_date) + timedelta(days=180)
    supabase.table("instruments").insert({
        "tag": tag,
        "name": name,
        "last_calibration_date": last_date,
        "next_calibration_date": str(next_date),
        "image_url": image_url
    }).execute()

    return {"status": "ok", "next_calibration": next_date, "image": image_url}

@app.get("/alerts")
def get_alerts():
    today = date.today()
    alert_limit = today + timedelta(days=15)
    data = supabase.table("instruments").select("*").execute().data
    alerts = [item for item in data if date.fromisoformat(item["next_calibration_date"]) <= alert_limit]
    return alerts

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000


