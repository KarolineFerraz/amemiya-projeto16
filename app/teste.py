from supabase_client import supabase

print(supabase.table("usuarios").select("*").execute())
