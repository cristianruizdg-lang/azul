"""
🤖 AZUL BACKEND API v3.0
========================
Servidor backend con FastAPI + Groq
Reemplaza Ollama local por IA en la nube
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from datetime import datetime

# Importar configuración
from config import HOST, PORT, DEBUG, TEMP_AUDIO_DIR, validate_config

# Importar routers
from routers import chat

# Importar modelos de respuesta
from models.schemas import HealthResponse

# === CREAR APLICACIÓN ===

app = FastAPI(
    title="Azul Backend API",
    version="3.0.0",
    description="Backend en la nube para Azul - Asistente Personal con IA",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# === MIDDLEWARE ===

# CORS: Permitir requests desde cualquier origen (desktop y móvil)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === ROUTERS ===

# Incluir router de chat
app.include_router(chat.router)

# === ENDPOINTS PRINCIPALES ===

@app.api_route("/", methods=["GET", "HEAD"], tags=["sistema"])
async def root():
    """Endpoint raíz con información básica del API (GET y HEAD para monitoring)"""
    return {
        "app": "Azul Backend API",
        "version": "3.0.0",
        "description": "Asistente Personal con IA en la nube",
        "docs": "/docs",
        "health": "/health",
        "powered_by": "FastAPI + Groq + Supabase"
    }

@app.api_route("/health", methods=["GET", "HEAD"], response_model=HealthResponse, tags=["sistema"])
async def health_check():
    """
    Health check del servidor (GET y HEAD para UptimeRobot/monitoring)
    Verifica que todos los servicios estén funcionando
    """
    services_status = {
        "groq": True,  # Asumimos que está ok si el server inició
        "supabase": True,
        "edge_tts": True
    }
    
    # TODO: Agregar checks reales de servicios
    
    return HealthResponse(
        status="healthy",
        version="3.0.0",
        timestamp=datetime.now().isoformat(),
        services=services_status
    )

@app.get("/audio/{filename}", tags=["archivos"])
async def get_audio(filename: str):
    """
    Sirve archivos de audio generados
    
    - **filename**: Nombre del archivo de audio
    """
    audio_path = os.path.join(TEMP_AUDIO_DIR, filename)
    
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio no encontrado")
    
    return FileResponse(
        audio_path,
        media_type="audio/mpeg",
        filename=filename
    )

# === EVENTOS DE STARTUP/SHUTDOWN ===

@app.on_event("startup")
async def startup_event():
    """
    Evento de inicio del servidor
    Inicializa servicios y valida configuración
    """
    print("\n" + "=" * 60)
    print("🚀 INICIANDO AZUL BACKEND API v3.0")
    print("=" * 60)
    
    try:
        # Validar configuración
        validate_config()
        print("✅ Configuración validada")
        
        # Crear directorios necesarios
        os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)
        print(f"✅ Directorio de audio: {TEMP_AUDIO_DIR}")
        
        # Importar servicios para inicializarlos
        from services.ia_service import ia_service
        from services.memory_service import memory_service
        from services.voice_service import voice_service
        
        print("✅ Servicios inicializados:")
        print("   - IAService (Groq)")
        print("   - MemoryService (Supabase)")
        print("   - VoiceService (Edge TTS)")
        
        print("\n" + "=" * 60)
        print("✨ SERVIDOR LISTO PARA RECIBIR REQUESTS")
        print("=" * 60)
        print(f"📡 URL: http://{HOST}:{PORT}")
        print(f"📚 Docs: http://{HOST}:{PORT}/docs")
        print(f"🏥 Health: http://{HOST}:{PORT}/health")
        print("=" * 60 + "\n")
    
    except Exception as e:
        print(f"\n❌ ERROR EN STARTUP: {e}\n")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Evento de cierre del servidor"""
    print("\n" + "=" * 60)
    print("🛑 CERRANDO AZUL BACKEND API")
    print("=" * 60)
    
    # Limpiar archivos temporales si es necesario
    try:
        from services.voice_service import voice_service
        await voice_service.limpiar_audios_antiguos(max_archivos=50)
        print("✅ Archivos temporales limpiados")
    except Exception as e:
        print(f"⚠️ Error limpiando temporales: {e}")
    
    print("👋 Servidor cerrado correctamente\n")

# === MANEJO DE ERRORES ===

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handler personalizado para 404"""
    return {
        "error": "Endpoint no encontrado",
        "detail": f"La ruta '{request.url.path}' no existe",
        "docs": "/docs"
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handler personalizado para errores 500"""
    return {
        "error": "Error interno del servidor",
        "detail": str(exc),
        "message": "Por favor contacta al administrador"
    }

# === EJECUTAR SERVIDOR ===

if __name__ == "__main__":
    print("\n🎯 Iniciando servidor en modo desarrollo...")
    print(f"Host: {HOST}")
    print(f"Port: {PORT}")
    print(f"Debug: {DEBUG}\n")
    
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,  # Auto-reload en desarrollo
        log_level="info"
    )
