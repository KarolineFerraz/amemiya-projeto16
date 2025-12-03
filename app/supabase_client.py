import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega o .env na raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Verificação clara e sem quebrar o código
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        f"[ERRO] Falha ao carregar credenciais do Supabase.\n"
        f"Arquivo .env utilizado: {ENV_PATH}\n"
        f"SUPABASE_URL: {SUPABASE_URL}\n"
        f"SUPABASE_KEY começa com: {SUPABASE_KEY[:6] if SUPABASE_KEY else 'NULO'}"
    )

# Cria o cliente corretamente
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
