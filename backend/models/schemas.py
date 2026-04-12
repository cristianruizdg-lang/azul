"""
Modelos de datos (Schemas) con Pydantic
Define la estructura de requests y responses del API
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

# --- MODELOS DE CHAT ---

class MessageRequest(BaseModel):
    """Request para enviar un mensaje de texto"""
    message: str = Field(..., min_length=1, description="Mensaje del usuario")
    user_id: str = Field(default="default", description="ID del usuario")
    stream: bool = Field(default=False, description="Si True, usa streaming")

class MessageResponse(BaseModel):
    """Response de un mensaje"""
    text: str = Field(..., description="Respuesta completa de Azul")
    audio_urls: List[str] = Field(default=[], description="URLs de archivos de audio")
    frases: List[str] = Field(default=[], description="Frases individuales")
    usage: Optional[Dict] = Field(default=None, description="Estadísticas de uso de tokens")

class HistoryResponse(BaseModel):
    """Response del historial de chat"""
    historial: List[Dict[str, str]] = Field(..., description="Lista de mensajes")
    total: int = Field(..., description="Número total de mensajes")

# --- MODELOS DE PERFIL ---

class ProfileItem(BaseModel):
    """Item del perfil del usuario"""
    clave: str = Field(..., description="Clave del dato")
    valor: str = Field(..., description="Valor del dato")

class ProfileResponse(BaseModel):
    """Response del perfil del usuario"""
    perfil: Dict[str, str] = Field(..., description="Perfil completo")
    perfil_texto: str = Field(..., description="Perfil formateado como texto")
    total_items: int = Field(..., description="Número de items en el perfil")

class LearningRequest(BaseModel):
    """Request para agregar aprendizaje manual"""
    clave: str = Field(..., min_length=1, description="Clave del aprendizaje")
    valor: str = Field(..., min_length=1, description="Valor del aprendizaje")
    user_id: str = Field(default="default", description="ID del usuario")

# --- MODELOS DE CALENDARIO ---

class EventRequest(BaseModel):
    """Request para crear un evento"""
    titulo: str = Field(..., min_length=1, description="Título del evento")
    fecha_hora: str = Field(..., description="Fecha y hora en formato ISO 8601")
    descripcion: str = Field(default="", description="Descripción opcional")
    notificaciones: List[int] = Field(
        default=[30, 10, 5, 0], 
        description="Minutos antes para notificaciones"
    )
    user_id: str = Field(default="default", description="ID del usuario")

class EventResponse(BaseModel):
    """Response de un evento"""
    id: str = Field(..., description="ID único del evento")
    titulo: str = Field(..., description="Título del evento")
    fecha_hora: str = Field(..., description="Fecha y hora del evento")
    descripcion: str = Field(..., description="Descripción")
    notificaciones: List[int] = Field(..., description="Notificaciones configuradas")
    created_at: Optional[str] = Field(None, description="Fecha de creación")

class EventsResponse(BaseModel):
    """Response de lista de eventos"""
    eventos: List[Dict] = Field(..., description="Lista de eventos")
    total: int = Field(..., description="Número total de eventos")

# --- MODELOS DE VOZ ---

class VoiceRequest(BaseModel):
    """Request para enviar audio de voz"""
    user_id: str = Field(default="default", description="ID del usuario")
    idioma: str = Field(default="es-ES", description="Idioma del audio")

class TTSRequest(BaseModel):
    """Request para síntesis de voz"""
    texto: str = Field(..., min_length=1, description="Texto a sintetizar")
    voz: Optional[str] = Field(None, description="Modelo de voz a usar")

class TTSResponse(BaseModel):
    """Response de síntesis de voz"""
    audio_url: str = Field(..., description="URL del archivo de audio")
    texto: str = Field(..., description="Texto sintetizado")

# --- MODELOS DE SISTEMA ---

class HealthResponse(BaseModel):
    """Response del health check"""
    status: str = Field(..., description="Estado del servicio")
    version: str = Field(..., description="Versión del backend")
    timestamp: str = Field(..., description="Timestamp actual")
    services: Dict[str, bool] = Field(..., description="Estado de servicios")

class ErrorResponse(BaseModel):
    """Response de error estándar"""
    error: str = Field(..., description="Mensaje de error")
    detail: Optional[str] = Field(None, description="Detalles adicionales")
    code: Optional[str] = Field(None, description="Código de error")
