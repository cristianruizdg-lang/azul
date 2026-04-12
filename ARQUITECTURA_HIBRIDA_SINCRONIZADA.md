# 🌐 ARQUITECTURA HÍBRIDA SINCRONIZADA - AZUL
## Contexto Compartido | $0 Costo | Sin PC Encendida

---

## 🎯 REQUISITOS DEL USUARIO

✅ **Costo**: $0 pesos mensuales  
✅ **PC Encendida**: NO necesaria  
✅ **Contexto Compartido**: Mismo Azul en móvil y desktop  
✅ **Sincronización**: Cambios en un dispositivo se reflejan en el otro  

---

## 💡 SOLUCIÓN: ARQUITECTURA HÍBRIDA CON BACKEND EN LA NUBE GRATIS

### Arquitectura Propuesta

```
┌─────────────────────────────────────────────────────────────────┐
│                    ☁️ BACKEND EN LA NUBE (GRATIS)               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Railway.app / Render.com / Fly.io (FREE TIER)          │  │
│  │  ├─ FastAPI (Servidor API)                              │  │
│  │  ├─ Groq API (Llama3 en cloud - GRATIS y RÁPIDO)       │  │
│  │  ├─ Edge TTS (Voz natural)                              │  │
│  │  └─ Lógica de calendario y aprendizaje                  │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              ↕️                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Supabase (Base de Datos en Cloud - GRATIS)            │  │
│  │  ├─ mensajes_chat (historial completo)                 │  │
│  │  ├─ perfil_usuario (aprendizaje/memoria)               │  │
│  │  └─ eventos_calendario (sincronizado)                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
              ↕️                              ↕️
┌───────────────────────┐        ┌───────────────────────┐
│  💻 DESKTOP APP       │        │  📱 MOBILE APP        │
│  (CustomTkinter)      │        │  (Kivy/KivyMD)        │
│                       │        │                       │
│  ├─ UI de escritorio  │        │  ├─ UI móvil          │
│  ├─ Conecta a API     │        │  ├─ Conecta a API     │
│  ├─ Voz local         │        │  ├─ Voz local         │
│  └─ Misma DB          │        │  └─ Misma DB          │
└───────────────────────┘        └───────────────────────┘

    Contexto Compartido en Tiempo Real
```

---

## 🔑 COMPONENTE CLAVE: GROQ API (100% GRATIS)

### ¿Qué es Groq?
**Groq** es una plataforma que ofrece **IA ultra-rápida GRATIS** con modelos como Llama3.

#### Ventajas Groq ✨
- ✅ **100% GRATIS** - Sin tarjeta de crédito, sin límites estrictos
- ✅ **Llama3-70B** - Mismo modelo que usas, más potente
- ✅ **Ultra Rápido** - 300-500 tokens/segundo (10x más rápido que local)
- ✅ **Sin servidor propio** - API en la nube
- ✅ **Límites generosos** - 14,400 requests/día gratis

#### Comparación de Velocidad
```
Ollama Local (tu PC):  ~30-50 tokens/seg  → Respuesta en 3-5 seg
Groq Cloud (gratis):   ~300-500 tokens/seg → Respuesta en 0.5-1 seg
```

### Cómo Usar Groq

**1. Crear cuenta gratis**
```bash
# Visit: https://console.groq.com
# Sign up (sin tarjeta de crédito)
# Obtener API Key gratis
```

**2. Instalar SDK**
```bash
pip install groq
```

**3. Usar en código (casi idéntico a Ollama)**
```python
from groq import Groq

client = Groq(api_key="gsk_...")  # Tu key gratis

# En lugar de:
# response = ollama.chat(model='llama3', messages=historial)

# Ahora:
response = client.chat.completions.create(
    model="llama3-70b-8192",  # Llama3 más potente
    messages=historial,
    temperature=0.7,
    max_tokens=150,
    stream=True  # Streaming como antes
)

for chunk in response:
    parte = chunk.choices[0].delta.content
    # Igual que antes
```

**Límites del Free Tier**:
- 14,400 requests/día (más que suficiente para uso personal)
- 600 requests/minuto
- Si llegas al límite, esperas 24h y se resetea

---

## 🖥️ SERVICIOS DE HOSTING GRATUITOS

### Opción 1: Railway.app (⭐ RECOMENDADO)
**Plan Gratuito**:
- ✅ 500 horas/mes (suficiente si duermes la app cuando no se usa)
- ✅ Deploy automático desde GitHub
- ✅ Base de datos PostgreSQL incluida
- ✅ HTTPS automático
- ✅ Logs en tiempo real

**Ideal para**: Prototipos y uso personal moderado

### Opción 2: Render.com
**Plan Gratuito**:
- ✅ Servicios ilimitados
- ✅ 750 horas/mes por servicio
- ⚠️ Se duerme después de 15 min de inactividad
- ⚠️ Tarda 30-60 seg en despertar

**Ideal para**: Si no te importa esperar al primer request

### Opción 3: Fly.io
**Plan Gratuito**:
- ✅ 3 apps gratis
- ✅ 256MB RAM por app
- ✅ Regiones globales
- ⚠️ Configuración más técnica

**Ideal para**: Usuarios avanzados

### Opción 4: PythonAnywhere
**Plan Gratuito**:
- ✅ Siempre activo (no se duerme)
- ✅ Bash console incluida
- ⚠️ CPU limitado
- ⚠️ Acceso externo limitado

---

## 🏗️ IMPLEMENTACIÓN PASO A PASO

### FASE 1: Migrar de Ollama a Groq (1-2 horas)

**Cambios necesarios en jarvis_funcional.py**

**Antes (Ollama local)**:
```python
import ollama

response = ollama.chat(model='llama3', messages=historial)
respuesta = response['message']['content']
```

**Después (Groq cloud)**:
```python
from groq import Groq

# Inicializar cliente (una vez)
groq_client = Groq(api_key="gsk_tu_key_aqui")

# Usar en lugar de ollama.chat()
response = groq_client.chat.completions.create(
    model="llama3-70b-8192",
    messages=historial,
    temperature=0.7,
    max_tokens=150
)
respuesta = response.choices[0].message.content
```

**Streaming (igual que antes)**:
```python
stream = groq_client.chat.completions.create(
    model="llama3-70b-8192",
    messages=historial,
    temperature=0.7,
    max_tokens=150,
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        parte = chunk.choices[0].delta.content
        respuesta_completa += parte
        # Agregar a cola de voz igual que antes
```

### FASE 2: Crear Backend API Unificado (1 semana)

**Estructura del proyecto**:
```
jarvis_vista/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── requirements.txt        # Dependencias
│   ├── config.py              # Configuración (API keys)
│   ├── services/
│   │   ├── ia_service.py      # Groq + lógica de IA
│   │   ├── voice_service.py   # Edge TTS
│   │   ├── memory_service.py  # Supabase
│   │   └── calendar_service.py # Calendario
│   ├── routers/
│   │   ├── chat.py            # Endpoints de chat
│   │   ├── voice.py           # Endpoints de voz
│   │   └── calendar.py        # Endpoints de calendario
│   └── models/
│       └── schemas.py         # Modelos de datos
│
├── desktop/
│   └── azul_desktop.py        # App desktop (modificada)
│
├── mobile/
│   └── azul_mobile.py         # App móvil (nueva)
│
└── modules/                   # Código compartido
    ├── calendario.py
    └── analizador_calendario.py
```

**backend/config.py**:
```python
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys (usar variables de entorno)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "gsk_...")
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://...")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJ...")

# Configuración
MODEL = "llama3-70b-8192"
VOICE = "es-MX-DaliaNeural"
```

**backend/services/ia_service.py**:
```python
from groq import Groq
from .memory_service import cargar_contexto, guardar_mensaje
from config import GROQ_API_KEY, MODEL

groq_client = Groq(api_key=GROQ_API_KEY)

class IAService:
    def __init__(self):
        self.historial = []
        self.contexto_usuario = ""
    
    async def cargar_memoria(self, user_id: str = "default"):
        """Carga historial y perfil del usuario"""
        self.historial, self.contexto_usuario = await cargar_contexto(user_id)
        self.actualizar_sistema()
    
    def actualizar_sistema(self):
        """Actualiza el prompt del sistema con perfil"""
        instrucciones = f"""Eres Azul, amiga del usuario. Natural, directa, concisa.

PERFIL DEL USUARIO:
{self.contexto_usuario if self.contexto_usuario else "Aún aprendiendo"}

REGLAS:
- MÁXIMO 2-3 frases cortas
- Tono cálido y cercano
- Menciona gustos solo cuando sean relevantes"""
        
        # Reemplazar o agregar mensaje de sistema
        if self.historial and self.historial[0].get("role") == "system":
            self.historial[0] = {"role": "system", "content": instrucciones}
        else:
            self.historial.insert(0, {"role": "system", "content": instrucciones})
    
    async def obtener_respuesta(self, mensaje: str, user_id: str = "default") -> dict:
        """Procesa mensaje y retorna respuesta"""
        # Agregar mensaje del usuario
        self.historial.append({"role": "user", "content": mensaje})
        
        # Guardar en Supabase
        await guardar_mensaje(user_id, "user", mensaje)
        
        # Generar respuesta con Groq (streaming)
        stream = groq_client.chat.completions.create(
            model=MODEL,
            messages=self.historial,
            temperature=0.7,
            max_tokens=150,
            stream=True
        )
        
        respuesta_completa = ""
        frases = []
        frase_actual = ""
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                parte = chunk.choices[0].delta.content
                respuesta_completa += parte
                frase_actual += parte
                
                # Detectar final de frase
                if any(s in parte for s in ['.', '!', '?', '\n']):
                    if frase_actual.strip():
                        frases.append(frase_actual.strip())
                    frase_actual = ""
        
        # Agregar última frase si quedó algo
        if frase_actual.strip():
            frases.append(frase_actual.strip())
        
        # Guardar respuesta
        self.historial.append({"role": "assistant", "content": respuesta_completa})
        await guardar_mensaje(user_id, "assistant", respuesta_completa)
        
        return {
            "text": respuesta_completa,
            "frases": frases  # Para TTS por partes
        }
```

**backend/main.py** (versión completa):
```python
from fastapi import FastAPI, WebSocket, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile
import os
import asyncio

from services.ia_service import IAService
from services.voice_service import VoiceService
from services.memory_service import MemoryService
from services.calendar_service import CalendarService

app = FastAPI(title="Azul Backend API", version="3.0")

# CORS para permitir requests desde apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servicios
ia_service = IAService()
voice_service = VoiceService()
memory_service = MemoryService()
calendar_service = CalendarService()

# --- MODELOS ---
class MessageRequest(BaseModel):
    message: str
    user_id: str = "default"

class EventRequest(BaseModel):
    titulo: str
    fecha_hora: str
    descripcion: str = ""
    notificaciones: list = [30, 10, 5, 0]
    user_id: str = "default"

# --- ENDPOINTS DE CHAT ---

@app.post("/api/chat/message")
async def send_message(request: MessageRequest):
    """Envía mensaje de texto y obtiene respuesta"""
    try:
        # Cargar contexto del usuario
        await ia_service.cargar_memoria(request.user_id)
        
        # Obtener respuesta
        respuesta = await ia_service.obtener_respuesta(
            request.message, 
            request.user_id
        )
        
        # Generar audio para cada frase
        audio_urls = []
        for i, frase in enumerate(respuesta["frases"]):
            audio_path = await voice_service.generar_audio(frase)
            audio_urls.append(f"/audio/{os.path.basename(audio_path)}")
        
        return {
            "text": respuesta["text"],
            "audio_urls": audio_urls,
            "frases": respuesta["frases"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/voice")
async def send_voice(
    audio: UploadFile = File(...),
    user_id: str = "default"
):
    """Procesa audio de voz y retorna respuesta"""
    try:
        # Guardar audio temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
            content = await audio.read()
            tmp.write(content)
            temp_path = tmp.name
        
        # Convertir audio a texto
        texto = await voice_service.audio_to_text(temp_path)
        os.unlink(temp_path)
        
        # Procesar como mensaje normal
        return await send_message(MessageRequest(
            message=texto,
            user_id=user_id
        ))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/history")
async def get_history(user_id: str = "default", limit: int = 50):
    """Obtiene historial de chat"""
    historial = await memory_service.obtener_historial(user_id, limit)
    return {"historial": historial}

@app.get("/api/profile")
async def get_profile(user_id: str = "default"):
    """Obtiene perfil del usuario"""
    perfil = await memory_service.obtener_perfil(user_id)
    return {"perfil": perfil}

# --- ENDPOINTS DE CALENDARIO ---

@app.post("/api/calendar/event")
async def create_event(request: EventRequest):
    """Crea un nuevo evento"""
    evento = await calendar_service.crear_evento(
        user_id=request.user_id,
        titulo=request.titulo,
        fecha_hora=request.fecha_hora,
        descripcion=request.descripcion,
        notificaciones=request.notificaciones
    )
    return {"evento": evento}

@app.get("/api/calendar/events")
async def get_events(
    user_id: str = "default",
    dias: int = 7
):
    """Obtiene eventos próximos"""
    eventos = await calendar_service.obtener_eventos(user_id, dias)
    return {"eventos": eventos}

@app.delete("/api/calendar/event/{evento_id}")
async def delete_event(evento_id: str, user_id: str = "default"):
    """Elimina un evento"""
    resultado = await calendar_service.eliminar_evento(evento_id, user_id)
    return {"success": resultado}

# --- ENDPOINTS DE AUDIO ---

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """Sirve archivos de audio generados"""
    audio_path = f"temp_audio/{filename}"
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio no encontrado")
    return FileResponse(audio_path, media_type="audio/mpeg")

# --- WEBSOCKET PARA STREAMING ---

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket para chat en tiempo real"""
    await websocket.accept()
    
    try:
        while True:
            # Recibir mensaje
            data = await websocket.receive_json()
            message = data.get("message")
            user_id = data.get("user_id", "default")
            
            # Cargar contexto
            await ia_service.cargar_memoria(user_id)
            
            # Enviar respuesta en streaming
            await websocket.send_json({"type": "start"})
            
            respuesta = await ia_service.obtener_respuesta(message, user_id)
            
            for frase in respuesta["frases"]:
                await websocket.send_json({
                    "type": "frase",
                    "content": frase
                })
            
            await websocket.send_json({"type": "end"})
    
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

# --- HEALTH CHECK ---

@app.get("/")
async def root():
    return {
        "app": "Azul Backend API",
        "version": "3.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# --- INICIALIZACIÓN ---

@app.on_event("startup")
async def startup_event():
    """Inicialización al arrancar servidor"""
    print("🚀 Azul Backend iniciado")
    
    # Crear directorio para audios temporales
    os.makedirs("temp_audio", exist_ok=True)
    
    # Precargar contexto de usuario default
    await ia_service.cargar_memoria("default")
    
    print("✅ Backend listo para recibir requests")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**backend/requirements.txt**:
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
groq==0.4.2
edge-tts==6.1.9
supabase==2.3.0
speechrecognition==3.10.1
pydantic==2.5.3
python-multipart==0.0.6
websockets==12.0
python-dotenv==1.0.0
```

### FASE 3: Modificar Desktop App para Usar API (2-3 días)

**desktop/azul_desktop.py** (versión híbrida):
```python
import customtkinter as ctk
import requests
import asyncio
from threading import Thread
import pygame

API_URL = "https://tu-backend.railway.app"  # URL de tu backend en Railway

class AzulDesktopAPI(ctk.CTk):
    """Versión desktop que se conecta al backend en la nube"""
    
    def __init__(self):
        super().__init__()
        self.title("AZUL v3.0 - Cloud Edition")
        self.geometry("1200x700")
        
        # Usar API en lugar de código local
        self.api_url = API_URL
        self.user_id = "default"  # Puedes implementar login después
        
        # Resto de UI igual que antes
        self.crear_interfaz()
        
        # Cargar historial desde API
        self.cargar_historial_api()
    
    def cargar_historial_api(self):
        """Carga historial desde la nube"""
        try:
            response = requests.get(
                f"{self.api_url}/api/chat/history",
                params={"user_id": self.user_id, "limit": 50}
            )
            historial = response.json()["historial"]
            # Cargar en UI
            print(f"✅ Historial cargado: {len(historial)} mensajes")
        except Exception as e:
            print(f"⚠️ Error cargando historial: {e}")
    
    def enviar_mensaje(self):
        """Envía mensaje al backend en la nube"""
        texto = self.entry_user.get().strip()
        if not texto:
            return
        
        # Limpiar input inmediatamente
        self.entry_user.delete(0, "end")
        self.entry_user.focus_set()
        
        # Mostrar mensaje del usuario en UI
        self.agregar_mensaje_ui("Tú", texto)
        
        # Enviar a API en thread separado
        Thread(target=self._enviar_a_api, args=(texto,), daemon=True).start()
    
    def _enviar_a_api(self, texto: str):
        """Envía mensaje a API y procesa respuesta"""
        try:
            response = requests.post(
                f"{self.api_url}/api/chat/message",
                json={"message": texto, "user_id": self.user_id},
                timeout=30
            )
            data = response.json()
            
            # Mostrar respuesta de Azul
            self.after(0, lambda: self.agregar_mensaje_ui("Azul", data["text"]))
            
            # Reproducir audio
            for audio_url in data["audio_urls"]:
                self.reproducir_audio(f"{self.api_url}{audio_url}")
        
        except Exception as e:
            print(f"❌ Error en API: {e}")
            self.after(0, lambda: self.agregar_mensaje_ui(
                "Sistema", 
                "Error de conexión. Verifica tu internet."
            ))
    
    def reproducir_audio(self, url: str):
        """Descarga y reproduce audio de respuesta"""
        try:
            # Descargar audio
            response = requests.get(url)
            
            # Guardar temporal
            temp_path = f"temp_{hash(url)}.mp3"
            with open(temp_path, 'wb') as f:
                f.write(response.content)
            
            # Reproducir
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            
            # Esperar a que termine
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)
            
            # Limpiar
            os.unlink(temp_path)
        except Exception as e:
            print(f"⚠️ Error reproduciendo audio: {e}")

if __name__ == "__main__":
    app = AzulDesktopAPI()
    app.mainloop()
```

#### Ventajas de Esta Arquitectura Desktop:
- ✅ Todo el procesamiento en la nube (no consume recursos locales)
- ✅ Sincronización automática con móvil (misma API)
- ✅ Actualizaciones sin reinstalar app
- ✅ Funciona aunque cambies de PC

### FASE 4: Crear App Móvil con Kivy (1-2 semanas)

**mobile/azul_mobile.py**:
```python
from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFabButton, MDIconButton
from kivymd.uix.list import TwoLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.scrollview import MDScrollView
from kivy.uix.boxlayout import BoxLayout
import requests
from threading import Thread
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import tempfile

API_URL = "https://tu-backend.railway.app"

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_url = API_URL
        self.user_id = "default"
        
        # Layout principal
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Lista de mensajes (scrollable)
        self.chat_list = MDScrollView()
        self.messages_container = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        self.messages_container.bind(
            minimum_height=self.messages_container.setter('height')
        )
        self.chat_list.add_widget(self.messages_container)
        
        layout.add_widget(self.chat_list)
        
        # Input area
        input_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        
        # Campo de texto
        self.input_field = MDTextField(
            hint_text="Escribe algo...",
            mode="rectangle",
            size_hint_x=0.7
        )
        input_layout.add_widget(self.input_field)
        
        # Botón enviar
        btn_send = MDIconButton(
            icon="send",
            on_release=self.send_message
        )
        input_layout.add_widget(btn_send)
        
        # Botón voz
        btn_voice = MDIconButton(
            icon="microphone",
            on_release=self.record_voice
        )
        input_layout.add_widget(btn_voice)
        
        layout.add_widget(input_layout)
        self.add_widget(layout)
        
        # Cargar historial al iniciar
        Thread(target=self.load_history, daemon=True).start()
    
    def load_history(self):
        """Carga historial desde API"""
        try:
            response = requests.get(
                f"{self.api_url}/api/chat/history",
                params={"user_id": self.user_id, "limit": 20}
            )
            historial = response.json()["historial"]
            
            # Mostrar en UI (en main thread)
            for msg in historial:
                role_text = "Tú" if msg["role"] == "user" else "Azul"
                Clock.schedule_once(
                    lambda dt, r=role_text, c=msg["content"]: 
                    self.add_message(r, c)
                )
        except Exception as e:
            print(f"Error cargando historial: {e}")
    
    def add_message(self, sender: str, message: str):
        """Agrega mensaje a la UI"""
        item = TwoLineAvatarIconListItem(
            text=sender,
            secondary_text=message,
        )
        
        # Ícono según sender
        if sender == "Azul":
            icon = IconLeftWidget(icon="robot")
        else:
            icon = IconLeftWidget(icon="account")
        
        item.add_widget(icon)
        self.messages_container.add_widget(item)
        
        # Scroll al final
        self.chat_list.scroll_y = 0
    
    def send_message(self, instance):
        """Envía mensaje a la API"""
        texto = self.input_field.text.strip()
        if not texto:
            return
        
        # Limpiar input
        self.input_field.text = ""
        
        # Mostrar mensaje del usuario
        self.add_message("Tú", texto)
        
        # Enviar a API en background
        Thread(target=self._send_to_api, args=(texto,), daemon=True).start()
    
    def _send_to_api(self, texto: str):
        """Envía mensaje a API y procesa respuesta"""
        try:
            response = requests.post(
                f"{self.api_url}/api/chat/message",
                json={"message": texto, "user_id": self.user_id},
                timeout=30
            )
            data = response.json()
            
            # Mostrar respuesta (en main thread)
            Clock.schedule_once(
                lambda dt: self.add_message("Azul", data["text"])
            )
            
            # Reproducir audio
            for audio_url in data["audio_urls"]:
                self.play_audio(f"{self.api_url}{audio_url}")
        
        except Exception as e:
            print(f"Error en API: {e}")
            Clock.schedule_once(
                lambda dt: self.add_message(
                    "Sistema",
                    "Error de conexión"
                )
            )
    
    def play_audio(self, url: str):
        """Descarga y reproduce audio"""
        try:
            # Descargar audio
            response = requests.get(url)
            
            # Guardar temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
                tmp.write(response.content)
                temp_path = tmp.name
            
            # Reproducir
            sound = SoundLoader.load(temp_path)
            if sound:
                sound.play()
        except Exception as e:
            print(f"Error reproduciendo audio: {e}")
    
    def record_voice(self, instance):
        """Graba voz y envía a API"""
        # TODO: Implementar grabación de audio con plyer
        print("Funcionalidad de voz próximamente")

class AzulMobileApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Cyan"
        return ChatScreen()

if __name__ == "__main__":
    AzulMobileApp().run()
```

### FASE 5: Deploy a Railway (2-3 horas)

**Pasos**:
1. Crear cuenta en Railway.app
2. Conectar repositorio GitHub
3. Configurar variables de entorno
4. Deploy automático

**Archivo railway.json**:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn backend.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Variables de entorno en Railway**:
```
GROQ_API_KEY=gsk_tu_key_aqui
SUPABASE_URL=https://lovcwnqviaovthtcxjjr.supabase.co
SUPABASE_KEY=eyJ...
```

---

## 💾 SINCRONIZACIÓN DE CONTEXTO

### Cómo Funciona

```
Usuario en MÓVIL:
1. Envía mensaje: "Me gusta el chocolate"
2. API guarda en Supabase: perfil_usuario
3. API aprende: gusto_comida=chocolate
4. API actualiza contexto en memoria

Usuario en DESKTOP:
1. Abre app → carga historial desde Supabase
2. Ve mensaje anterior sobre chocolate
3. Envía mensaje: "Recomiéndame un postre"
4. Azul responde: "¿Qué tal un brownie de chocolate?"
   ↑ Usa conocimiento aprendido en móvil
```

### Flujo de Sincronización

```
┌────────────────────────────────────────────┐
│  📱 MÓVIL: "Me gusta el café"              │
└────────────────┬───────────────────────────┘
                 ↓
     POST /api/chat/message
                 ↓
┌────────────────────────────────────────────┐
│  ☁️ BACKEND                                │
│  1. Procesar con Groq                      │
│  2. Guardar en Supabase                    │
│  3. Aprender: gusto_bebidas=café          │
│  4. Actualizar perfil en DB                │
└────────────────┬───────────────────────────┘
                 ↓
        Supabase actualizado
                 ↓
┌────────────────────────────────────────────┐
│  💻 DESKTOP: Abre app                      │
│  GET /api/chat/history                     │
│  → Ve mensaje de  café                     │
│  GET /api/profile                          │
│  → Carga gusto_bebidas=café               │
└────────────────────────────────────────────┘

RESULTADO: Ambos dispositivos tienen el MISMO contexto
```

---

## 📊 COSTOS FINALES

### Breakdown de Servicios

| Servicio | Plan | Costo Mensual |
|----------|------|---------------|
| **Railway.app** | Free Tier | $0 (500 hrs/mes) |
| **Groq API** | Free Tier | $0 (14,400 req/día) |
| **Supabase** | Free Tier | $0 (500MB DB + 2GB storage) |
| **Edge TTS** | Microsoft | $0 (gratis) |
| **Total** | - | **$0/mes** ✅ |

### Límites del Free Tier

**Railway**:
- 500 horas/mes = 16.6 horas/día
- Si duermes la app cuando no se use (con config), es suficiente
- Upgrade a $5/mes si necesitas más

**Groq**:
- 14,400 requests/día
- ~600 req/hora
- Más que suficiente para uso personal

**Supabase**:
- 500MB base de datos
- ~50,000 mensajes de chat
- 2GB de almacenamiento

---

## ⚙️ OPTIMIZACIONES PARA FREE TIER

### 1. Sleep Mode en Railway
**backend/main.py**:
```python
import time
from datetime import datetime

last_request_time = time.time()

@app.middleware("http")
async def track_requests(request, call_next):
    global last_request_time
    last_request_time = time.time()
    response = await call_next(request)
    return response

# Auto-sleep después de 10 minutos de inactividad
async def auto_sleep_check():
    while True:
        await asyncio.sleep(60)  # Check cada minuto
        if time.time() - last_request_time > 600:  # 10 min
            print("💤 Sin actividad, entrando en modo sleep...")
            # Railway detecta inactividad y duerme automáticamente
```

### 2. Cache de Respuestas Comunes
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def respuesta_directa(pregunta: str) -> str:
    """Cache para preguntas comunes"""
    if "hora" in pregunta.lower():
        return datetime.now().strftime("%I:%M %p")
    # ... más respuestas
```

### 3. Compresión de Audio
```python
# Usar formato más ligero
await communicate.save(audio_path, bitrate="64k")  # Menos tamaño
```

---

## 🔄 MIGRACIÓN DESDE VERSIÓN ACTUAL

### Paso 1: Backup
```bash
# Backup de base de datos Supabase (ya está en cloud, safe)
# Backup de código
git commit -am "Backup antes de migración a cloud"
git tag v3.0-local
```

### Paso 2: Crear Branch Nueva Arquitectura
```bash
git checkout -b cloud-architecture
mkdir backend desktop mobile
# Mover archivos existentes
mv jarvis_funcional.py desktop/azul_desktop_legacy.py
```

### Paso 3: Instalar Groq
```bash
pip install groq
# Testear conexión
python -c "from groq import Groq; print('✅ Groq instalado')"
```

### Paso 4: Crear .env
```bash
# .env (NO subir a GitHub)
GROQ_API_KEY=gsk_tu_key_aqui
SUPABASE_URL=https://lovcwnqviaovthtcxjjr.supabase.co
SUPABASE_KEY=eyJ...
```

### Paso 5: Implementar Backend
```bash
mkdir -p backend/services backend/routers backend/models
# Copiar archivos de ejemplo anteriores
# Instalar dependencias
pip install -r backend/requirements.txt
```

### Paso 6: Testear Local
```bash
cd backend
uvicorn main:app --reload
# Abrir http://localhost:8000/docs
# Testear endpoints
```

### Paso 7: Deploy a Railway
```bash
# Instalar Railway CLI
npm install -g @railway/cli
# Login
railway login
# Crear proyecto
railway init
# Deploy
railway up
# Obtener URL pública
railway domain
```

### Paso 8: Actualizar Apps
```python
# En desktop/azul_desktop.py y mobile/azul_mobile.py
API_URL = "https://tu-proyecto.railway.app"
```

---

## 🎯 ROADMAP DE IMPLEMENTACIÓN

### Semana 1: Backend + Groq
- ✅ Día 1: Setup proyecto + instalar dependencias
- ✅ Día 2-3: Migrar de Ollama a Groq
- ✅ Día 4-5: Crear API endpoints (chat, voice, calendar)
- ✅ Día 6: Testing local exhaustivo
- ✅ Día 7: Deploy a Railway

### Semana 2: Desktop App Híbrida
- ✅ Día 8-9: Refactorizar desktop para usar API
- ✅ Día 10: Implementar sistema de voz con API
- ✅ Día 11: Migrar calendario a API
- ✅ Día 12: Testing + bugfixes
- ✅ Día 13-14: Polish UI y UX

### Semana 3-4: Mobile App
- ✅ Día 15-16: Setup Kivy + estructura básica
- ✅ Día 17-18: Implementar chat UI
- ✅ Día 19-20: Conectar a API
- ✅ Día 21-22: Sistema de voz móvil
- ✅ Día 23-24: Calendario en móvil
- ✅ Día 25-26: Testing en dispositivos reales
- ✅ Día 27-28: Compilar APK + distribución

---

## 🚀 RESULTADO FINAL

### Lo que Tendrás

```
✅ Backend en la nube (Railway) - 24/7 sin PC encendida
✅ IA ultra-rápida (Groq) - Gratis y más rápida que local
✅ Base de datos compartida (Supabase) - Contexto sincronizado
✅ App Desktop (CustomTkinter) - Conectada a cloud
✅ App Móvil (Kivy) - Android con misma funcionalidad
✅ Sincronización automática - Cambios se reflejan en ambos
✅ Costo total: $0/mes
```

### Funcionalidades

🎤 **Conversación por Voz**
- Desktop: Micrófono → API → Groq → Edge TTS → Audio
- Móvil: Micrófono móvil → API → Groq → Edge TTS → Audio

💬 **Chat por Texto**
- Desktop: Input → API → Respuesta
- Móvil: Input → API → Respuesta

🧠 **Memoria Compartida**
- Aprendizaje en un dispositivo → disponible en all los dispositivos
- Historial completo sincronizado

📅 **Calendario Unificado**
- Crear evento en móvil → aparece en desktop
- Editar en desktop → se refleja en móvil

🔔 **Notificaciones**
- Desktop: Notificaciones de Windows
- Móvil: Push notifications nativas

---

## 🎓 CONCLUSIÓN

Esta arquitectura cumple **TODOS** tus requisitos:

### ✅ Requisitos Cumplidos

1. **$0 Costo**: Railway + Groq + Supabase free tiers
2. **Sin PC Encendida**: Todo en la nube
3. **Contexto Compartido**: Supabase sincroniza ambos dispositivos
4. **Mismo Azul**: Misma personalidad, memoria y capacidades

### 🎁 Beneficios Adicionales

- ⚡ **Más Rápido**: Groq es 10x más rápido que Ollama local
- 🔄 **Siempre Actualizado**: Cambios en backend afectan a ambas apps
- 📱 **Multiplataforma**: Usa desde cualquier dispositivo
- 🌍 **Acceso Global**: Funciona desde cualquier lugar con internet

### 🚀 Próximo Paso

**¿Empezamos con la migración?** Puedo ayudarte a:

1. ✅ Crear cuenta Groq y obtener API key
2. ✅ Implementar el backend con FastAPI
3. ✅ Migrar el código actual de Ollama a Groq
4. ✅ Desplegar a Railway
5. ✅ Adaptar desktop app
6. ✅ Crear mobile app

**¿Por dónde quieres comenzar?** 🎯
