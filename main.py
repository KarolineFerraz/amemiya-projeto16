import os
from dotenv import load_dotenv
from fastapi import FastAPI

# Carregar variáveis do .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "API funcionando com sucesso!"}
