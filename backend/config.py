"""
Configuración centralizada del backend de Azul
Carga variables de entorno y proporciona configuración global
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# --- API KEYS ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# --- CONFIGURACIÓN DE IA ---
AI_MODEL = os.getenv("AI_MODEL", "llama-3.3-70b-versatile")
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))
AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "150"))

# --- CONFIGURACIÓN DE VOZ ---
VOICE_MODEL = os.getenv("VOICE_MODEL", "es-MX-DaliaNeural")
VOICE_RATE = "+10%"
VOICE_PITCH = "+0Hz"

# --- CONFIGURACIÓN DEL SERVIDOR ---
HOST = "0.0.0.0"
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# --- DIRECTORIOS ---
TEMP_AUDIO_DIR = "temp_audio"
TEMP_UPLOAD_DIR = "temp_uploads"

# Crear directorios si no existen
os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)
os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)

# Validación de configuración
def validate_config():
    """Valida que las configuraciones necesarias estén presentes"""
    errors = []
    
    if not GROQ_API_KEY or GROQ_API_KEY == "tu_api_key_aqui_comienza_con_gsk":
        errors.append("GROQ_API_KEY no está configurada en .env")
    
    if not SUPABASE_URL:
        errors.append("SUPABASE_URL no está configurada en .env")
    
    if not SUPABASE_KEY:
        errors.append("SUPABASE_KEY no está configurada en .env")
    
    if errors:
        raise ValueError(f"Errores de configuración:\n" + "\n".join(f"- {e}" for e in errors))
    
    return True

# NO validar al importar en producción
# La validación se hace en el startup event de main.py
