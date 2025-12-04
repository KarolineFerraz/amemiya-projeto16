# app/supabase_client.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
# tenta carregar .env local (não faz diferença no Render)
load_dotenv(ENV_PATH)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "[ERRO] SUPABASE_URL ou SUPABASE_KEY não estão definidas no ambiente. "
        "Verifique as Environment Variables no Render ou o arquivo .env local."
    )

# cria client (vai lançar erro se as credenciais forem inválidas)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
