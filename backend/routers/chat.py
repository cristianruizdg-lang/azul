"""
Router de Chat
Endpoints para conversación con Azul
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
import sys
import os

# Agregar directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.schemas import MessageRequest, MessageResponse, HistoryResponse, ProfileResponse
from services.ia_service import ia_service
from services.memory_service import memory_service
from services.voice_service import voice_service
import tempfile
import asyncio

router = APIRouter(prefix="/api/chat", tags=["chat"])

@router.post("/message", response_model=MessageResponse)
async def send_message(request: MessageRequest):
    """
    Envía un mensaje de texto y obtiene respuesta de Azul
    
    - **message**: Mensaje del usuario
    - **user_id**: ID del usuario (default: "default")
    - **stream**: Si True, usa streaming (experimental)
    """
    try:
        # 1. Cargar contexto del usuario
        historial, perfil = await memory_service.cargar_contexto_completo(request.user_id)
        
        # 2. Crear prompt del sistema con el perfil
        prompt_sistema = ia_service.crear_prompt_sistema(perfil)
        
        # 3. Agregar prompt del sistema si no existe en historial
        if not historial or historial[0].get("role") != "system":
            historial.insert(0, {"role": "system", "content": prompt_sistema})
        else:
            historial[0] = {"role": "system", "content": prompt_sistema}
        
        # 4. Obtener respuesta de IA
        respuesta = await ia_service.obtener_respuesta(
            mensaje=request.message,
            historial=historial,
            stream=request.stream
        )
        
        # 5. Guardar mensaje del usuario
        await memory_service.guardar_mensaje("user", request.message, request.user_id)
        
        # 6. Guardar respuesta de Azul
        await memory_service.guardar_mensaje("assistant", respuesta["text"], request.user_id)
        
        # 7. Extraer aprendizaje en background (no bloquea respuesta)
        asyncio.create_task(_aprender_en_background(request.message, request.user_id))
        
        # 8. Generar audios para cada frase (opcional, no bloquear si falla)
        audio_urls = []
        try:
            audio_paths = await voice_service.generar_multiples_audios(respuesta["frases"])
            audio_urls = [voice_service.obtener_url_audio(path) for path in audio_paths]
        except Exception as e:
            print(f"⚠️ Audio TTS no disponible: {str(e)[:100]}")
            # Continuamos sin audio, solo texto
        
        return MessageResponse(
            text=respuesta["text"],
            audio_urls=audio_urls,
            frases=respuesta["frases"],
            usage=respuesta.get("usage")
        )
    
    except Exception as e:
        print(f"❌ Error en /api/chat/message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice")
async def send_voice(
    audio: UploadFile = File(...),
    user_id: str = "default",
    idioma: str = "es-ES"
):
    """
    Envía audio de voz, lo transcribe y obtiene respuesta
    
    - **audio**: Archivo de audio (WAV, MP3, etc.)
    - **user_id**: ID del usuario
    - **idioma**: Idioma del audio (default: es-ES)
    """
    temp_path = None
    try:
        # 1. Guardar audio temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
            content = await audio.read()
            tmp.write(content)
            temp_path = tmp.name
        
        # 2. Convertir audio a texto
        texto = await voice_service.audio_a_texto(temp_path, idioma)
        
        # 3. Procesar como mensaje normal
        request = MessageRequest(message=texto, user_id=user_id)
        return await send_message(request)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"❌ Error en /api/chat/voice: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Limpiar archivo temporal
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)

@router.get("/history", response_model=HistoryResponse)
async def get_history(user_id: str = "default", limit: int = 50):
    """
    Obtiene el historial de chat del usuario
    
    - **user_id**: ID del usuario
    - **limit**: Número máximo de mensajes (default: 50)
    """
    try:
        historial = await memory_service.cargar_historial(user_id, limit)
        
        # Filtrar mensaje del sistema
        historial_sin_sistema = [
            msg for msg in historial 
            if msg.get("role") != "system"
        ]
        
        return HistoryResponse(
            historial=historial_sin_sistema,
            total=len(historial_sin_sistema)
        )
    
    except Exception as e:
        print(f"❌ Error en /api/chat/history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/profile", response_model=ProfileResponse)
async def get_profile(user_id: str = "default"):
    """
    Obtiene el perfil del usuario (gustos/hábitos aprendidos)
    
    - **user_id**: ID del usuario
    """
    try:
        perfil_dict = await memory_service.obtener_perfil_completo(user_id)
        perfil_texto = await memory_service.cargar_perfil(user_id)
        
        return ProfileResponse(
            perfil=perfil_dict,
            perfil_texto=perfil_texto,
            total_items=len(perfil_dict)
        )
    
    except Exception as e:
        print(f"❌ Error en /api/chat/profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/history")
async def clear_history(user_id: str = "default", keep_last: int = 10):
    """
    Limpia el historial de chat antiguo
    
    - **user_id**: ID del usuario
    - **keep_last**: Número de mensajes a mantener (default: 10)
    """
    try:
        eliminados = await memory_service.limpiar_historial_antiguo(user_id, keep_last)
        return {"eliminados": eliminados, "message": f"Historial limpiado, manteniendo últimos {keep_last}"}
    
    except Exception as e:
        print(f"❌ Error en /api/chat/history DELETE: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- FUNCIONES AUXILIARES ---

async def _aprender_en_background(mensaje: str, user_id: str):
    """
    Extrae aprendizaje del mensaje en background sin bloquear respuesta
    
    Args:
        mensaje: Mensaje del usuario
        user_id: ID del usuario
    """
    try:
        aprendizaje = await ia_service.extraer_aprendizaje(mensaje)
        
        if aprendizaje:
            await memory_service.guardar_aprendizaje(
                clave=aprendizaje["clave"],
                valor=aprendizaje["valor"],
                user_id=user_id
            )
    except Exception as e:
        print(f"⚠️ Error en aprendizaje background: {e}")
        # No propagar error, es un proceso secundario
