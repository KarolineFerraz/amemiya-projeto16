import os
from supabase import create_client, Client
from dotenv import load_dotenv

# --- CARREGA .env USANDO CAMINHO ABSOLUTO ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")

# força carregar o .env do projeto
load_dotenv(ENV_PATH)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        f"[ERRO] Não carregou SUPABASE_URL ou SUPABASE_KEY.\n"
        f"Arquivo .env usado: {ENV_PATH}\n"
        f"URL='{SUPABASE_URL}', KEY='{SUPABASE_KEY}'"
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
