# 📱 EVALUACIÓN: APLICACIÓN MÓVIL PARA AZUL

## 📋 ANÁLISIS DE VIABILIDAD

---

## 🎯 OBJETIVO
Crear una aplicación móvil (Android/iOS) que permita interactuar con Azul desde cualquier lugar, manteniendo todas sus funcionalidades principales:
- 🎤 Reconocimiento de voz
- 🔊 Síntesis de voz
- 💬 Chat conversacional
- 📅 Calendario y recordatorios
- 🧠 Memoria persistente
- 📲 Notificaciones push

---

## 🔍 ANÁLISIS DE ARQUITECTURA ACTUAL

### Componentes Desktop (Azul v3.0)
```
✅ CustomTkinter (UI)          → 🚫 NO compatible móvil
✅ Ollama + Llama3 (IA Local)  → ⚠️ Muy pesado para móvil
✅ Edge TTS (Voz)              → ✅ Compatible (requiere internet)
✅ SpeechRecognition           → ✅ Compatible móvil
✅ Supabase (Cloud DB)         → ✅ Perfecto para móvil
✅ pygame.mixer                → ⚠️ Posible en móvil
✅ Módulos calendario          → ✅ 100% compatible
```

### Problemas Principales
1. **Llama3 es muy pesado** (~4-7GB RAM) - imposible en móviles promedio
2. **CustomTkinter no existe para móvil** - UI debe reescribirse
3. **Procesamiento local** - móviles no tienen potencia suficiente

---

## 🏗️ ARQUITECTURAS POSIBLES

### OPCIÓN 1: Cliente-Servidor (⭐ RECOMENDADA)
**Arquitectura**: Separar backend y frontend

```
┌─────────────────────────────────────────────────┐
│  📱 APP MÓVIL (Frontend)                        │
│  ├─ Kivy/KivyMD o React Native                 │
│  ├─ UI nativa para móvil                       │
│  ├─ Captura de voz local                       │
│  ├─ Reproducción de audio                      │
│  └─ Comunicación vía WebSocket/REST API        │
└─────────────────────────────────────────────────┘
                    ↕️ Internet
┌─────────────────────────────────────────────────┐
│  🖥️ SERVIDOR (Backend - PC/Cloud)              │
│  ├─ FastAPI o Flask                            │
│  ├─ Ollama + Llama3 (procesamiento IA)        │
│  ├─ Lógica de calendario                       │
│  ├─ Sistema de aprendizaje                     │
│  ├─ Supabase (memoria compartida)              │
│  └─ Edge TTS (síntesis de voz)                 │
└─────────────────────────────────────────────────┘
```

#### Ventajas ✅
- ✅ Mantiene toda la potencia de Llama3
- ✅ Móvil solo necesita UI ligera
- ✅ Backend puede estar en tu PC o en la nube
- ✅ Misma base de datos (Supabase) para ambos
- ✅ Desktop y móvil comparten memoria/aprendizaje
- ✅ Actualizar IA no requiere actualizar app

#### Desventajas ⚠️
- ⚠️ Requiere conexión a internet
- ⚠️ Necesitas servidor corriendo (PC o cloud)
- ⚠️ Latencia de red (0.5-2s adicionales)

#### Flujo de Trabajo
```
1. Usuario habla en móvil
2. App graba audio → envía a servidor
3. Servidor: Speech Recognition + Llama3
4. Servidor: Genera respuesta + TTS
5. Servidor: Envía audio de vuelta
6. App: Reproduce audio de Azul
```

---

### OPCIÓN 2: App Híbrida con IA en la Nube
**Arquitectura**: Todo en cloud, app es solo cliente

```
┌─────────────────────────────────────────────┐
│  📱 APP MÓVIL (Cliente ligero)              │
│  └─ React Native / Flutter / Kivy          │
└─────────────────────────────────────────────┘
                    ↕️
┌─────────────────────────────────────────────┐
│  ☁️ BACKEND EN LA NUBE                     │
│  ├─ Railway / Render / AWS                 │
│  ├─ API REST + WebSockets                  │
│  ├─ OpenAI API (en lugar de Llama3)       │
│  │  └─ GPT-4 o Claude                      │
│  ├─ Google Cloud TTS                       │
│  └─ Supabase (base de datos)               │
└─────────────────────────────────────────────┘
```

#### Ventajas ✅
- ✅ No necesitas PC encendida
- ✅ Funciona desde cualquier lugar
- ✅ Escalable (múltiples usuarios)
- ✅ Backups automáticos

#### Desventajas ⚠️
- ⚠️ Costos mensuales (OpenAI API ~$10-30/mes)
- ⚠️ Pierde privacidad (no es 100% local)
- ⚠️ Depende de servicios externos
- ⚠️ Requiere reescribir lógica de IA

---

### OPCIÓN 3: App Nativa Python (Kivy/BeeWare)
**Arquitectura**: Todo en el móvil con IA ligera

```
┌─────────────────────────────────────────────┐
│  📱 APP MÓVIL (Todo incluido)               │
│  ├─ Kivy/KivyMD o BeeWare                  │
│  ├─ IA Ligera (DistilBERT, TinyLlama)     │
│  │  └─ Modelos < 500MB                     │
│  ├─ TTS Local (pyttsx3-mobile)            │
│  ├─ Speech Recognition (Android/iOS API)   │
│  ├─ SQLite local + sync Supabase           │
│  └─ Todo offline-first                      │
└─────────────────────────────────────────────┘
```

#### Ventajas ✅
- ✅ Funciona 100% offline
- ✅ No requiere servidor
- ✅ Privacidad total
- ✅ Sin latencia de red

#### Desventajas ⚠️
- ⚠️ IA muy limitada (modelos pequeños)
- ⚠️ Conversaciones menos naturales
- ⚠️ Consume batería rápidamente
- ⚠️ App muy pesada (~1GB+)
- ⚠️ Difícil de programar (Python en móvil es complejo)

---

### OPCIÓN 4: Progressive Web App (PWA)
**Arquitectura**: Web app que se comporta como nativa

```
┌─────────────────────────────────────────────┐
│  🌐 PWA (Navegador móvil)                   │
│  ├─ HTML/CSS/JavaScript                     │
│  ├─ Service Workers (cache offline)        │
│  ├─ Web Speech API                          │
│  └─ Push Notifications                      │
└─────────────────────────────────────────────┘
                    ↕️
┌─────────────────────────────────────────────┐
│  🖥️ BACKEND (Mismo de desktop)              │
│  └─ FastAPI + Llama3                        │
└─────────────────────────────────────────────┘
```

#### Ventajas ✅
- ✅ No requiere instalación
- ✅ Funciona en cualquier navegador
- ✅ Desarrollo más rápido (web estándar)
- ✅ Una sola codebase para todo

#### Desventajas ⚠️
- ⚠️ No es app nativa real
- ⚠️ Limitaciones de permisos
- ⚠️ Experiencia menos pulida
- ⚠️ No en app stores (iPhone tiene limitaciones)

---

## 📊 COMPARATIVA DE OPCIONES

| Característica | Cliente-Servidor | Cloud API | App Nativa | PWA |
|---------------|------------------|-----------|------------|-----|
| **IA Potente** | ✅ Llama3 completo | ✅ GPT-4 | ⚠️ Limitada | ✅ Llama3 |
| **Offline** | ❌ Necesita conexión | ❌ Necesita conexión | ✅ 100% offline | ⚠️ Parcial |
| **Costos** | 💰 Gratis (tu PC) | 💰💰 $10-30/mes | 💰 Gratis | 💰 Gratis |
| **Desarrollo** | ⏱️ 2-3 semanas | ⏱️ 1-2 semanas | ⏱️ 1-2 meses | ⏱️ 1 semana |
| **Batería** | ✅ Bajo consumo | ✅ Bajo consumo | ⚠️ Alto consumo | ✅ Bajo consumo |
| **Privacidad** | ✅ Alta (tu servidor) | ⚠️ Media (terceros) | ✅ Total | ✅ Alta |
| **Experiencia** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

---

## 🎯 RECOMENDACIÓN: OPCIÓN 1 (Cliente-Servidor)

### ¿Por qué es la mejor opción?

1. **Mantiene la potencia de Llama3** - Sin degradar calidad de IA
2. **Reutiliza código existente** - Backend ya está hecho (jarvis_funcional.py)
3. **Sin costos mensuales** - Tu PC hace el procesamiento
4. **Flexibilidad** - Puedes mover servidor a cloud después
5. **Memoria compartida** - Desktop y móvil usan mismo Supabase

### Plan de Implementación

#### FASE 1: Backend API (1 semana)
Convertir Azul en un servidor API

**Stack Técnico**:
- **FastAPI** - Framework moderno y rápido para Python
- **WebSockets** - Para comunicación en tiempo real
- **uvicorn** - Servidor ASGI

**Archivos a crear**:
```
backend/
├── main.py                  # Servidor FastAPI
├── routes/
│   ├── chat.py             # Endpoints de conversación
│   ├── calendar.py         # Endpoints de calendario
│   └── voice.py            # Endpoints de voz
├── services/
│   ├── ia_service.py       # Llama3 + lógica de IA
│   ├── voice_service.py    # TTS + STT
│   └── memory_service.py   # Supabase + aprendizaje
└── models/
    └── schemas.py          # Modelos de datos (Pydantic)
```

**Endpoints necesarios**:
```python
POST   /api/chat/message          # Enviar mensaje texto
POST   /api/chat/voice            # Enviar audio
GET    /api/chat/history          # Obtener historial
POST   /api/calendar/event        # Crear evento
GET    /api/calendar/events       # Listar eventos
DELETE /api/calendar/event/{id}   # Eliminar evento
GET    /api/profile               # Obtener perfil usuario
WebSocket /ws                     # Stream de respuestas
```

#### FASE 2: App Móvil (2-3 semanas)
Crear frontend móvil

**Opción A: Kivy/KivyMD** (Python - más fácil para ti)
```python
# Ventajas:
✅ Mismo lenguaje (Python)
✅ Aprende rápido si sabes Python
✅ Buena documentación
✅ Material Design incluido (KivyMD)

# Desventajas:
⚠️ Apps un poco más pesadas
⚠️ Menos rendimiento que nativas
```

**Opción B: React Native** (JavaScript)
```javascript
// Ventajas:
✅ Rendimiento excelente
✅ Experiencia muy nativa
✅ Comunidad gigante
✅ Hot reload (desarrollo rápido)

// Desventajas:
⚠️ Debes aprender JavaScript/React
⚠️ Curva de aprendizaje más alta
```

**Opción C: Flutter** (Dart)
```dart
// Ventajas:
✅ UI hermosa por defecto
✅ Rendimiento superior
✅ Una codebase para iOS + Android

// Desventajas:
⚠️ Nuevo lenguaje (Dart)
⚠️ Más complejo inicial
```

**Recomendación**: **Kivy/KivyMD** - Aprovecha tu conocimiento de Python

#### FASE 3: Conexión y Testing (1 semana)
Integrar todo

---

## 💻 IMPLEMENTACIÓN DETALLADA - OPCIÓN 1

### Paso 1: Crear Backend API con FastAPI

**1.1 Instalar dependencias**
```bash
pip install fastapi uvicorn websockets python-multipart
```

**1.2 Estructura de archivos**
```
jarvis_vista/
├── jarvis_funcional.py         # Desktop app (existente)
├── backend/                     # NUEVO
│   ├── main.py                 # Servidor FastAPI
│   ├── api_service.py          # Lógica de negocio
│   └── requirements.txt        # Dependencias backend
├── mobile/                      # NUEVO (Fase 2)
│   └── azul_mobile/            # App Kivy
└── modules/                     # Existente (compartido)
```

**1.3 Archivo backend/main.py (ejemplo básico)**
```python
from fastapi import FastAPI, WebSocket, UploadFile
from fastapi.responses import FileResponse
import ollama
import edge_tts
from supabase import create_client
import tempfile
import os

app = FastAPI(title="Azul Backend API")

# Configuración (igual que desktop)
SUPABASE_URL = "https://lovcwnqviaovthtcxjjr.supabase.co"
SUPABASE_KEY = "tu_key_aqui"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Estado global (similar a desktop)
historial = []
contexto_usuario = ""

@app.post("/api/chat/message")
async def send_message(message: str, user_id: str = "default"):
    """Envía un mensaje de texto y obtiene respuesta"""
    # 1. Agregar a historial
    historial.append({"role": "user", "content": message})
    
    # 2. Obtener respuesta de Llama3
    response = ollama.chat(model='llama3', messages=historial)
    respuesta_texto = response['message']['content']
    
    # 3. Guardar en Supabase
    supabase.table("mensajes_chat").insert({
        "role": "assistant", 
        "content": respuesta_texto
    }).execute()
    
    # 4. Generar audio con Edge TTS
    audio_path = await generar_audio(respuesta_texto)
    
    # 5. Retornar respuesta + URL de audio
    return {
        "text": respuesta_texto,
        "audio_url": f"/audio/{os.path.basename(audio_path)}"
    }

@app.post("/api/chat/voice")
async def send_voice(audio: UploadFile):
    """Procesa audio de voz, convierte a texto y responde"""
    # 1. Guardar audio temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
        tmp.write(await audio.read())
        temp_path = tmp.name
    
    # 2. Convertir audio a texto con speech_recognition
    import speech_recognition as sr
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_path) as source:
        audio_data = recognizer.record(source)
        texto = recognizer.recognize_google(audio_data, language="es-ES")
    
    # 3. Procesar como mensaje normal
    return await send_message(texto)

@app.get("/api/chat/history")
async def get_history():
    """Obtiene historial de conversación"""
    res = supabase.table("mensajes_chat")\
        .select("role, content, created_at")\
        .order("created_at", desc=False)\
        .limit(50)\
        .execute()
    return res.data

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket para streaming de respuestas"""
    await websocket.accept()
    
    while True:
        # Recibir mensaje del móvil
        data = await websocket.receive_text()
        
        # Procesar con IA (streaming)
        historial.append({"role": "user", "content": data})
        stream = ollama.chat(model='llama3', messages=historial, stream=True)
        
        respuesta = ""
        for chunk in stream:
            parte = chunk['message']['content']
            respuesta += parte
            # Enviar chunk al móvil en tiempo real
            await websocket.send_text(parte)
        
        historial.append({"role": "assistant", "content": respuesta})

async def generar_audio(texto: str) -> str:
    """Genera audio con Edge TTS y retorna path"""
    output_path = f"temp_audio/{hash(texto)}.mp3"
    os.makedirs("temp_audio", exist_ok=True)
    
    communicate = edge_tts.Communicate(texto, "es-MX-DaliaNeural")
    await communicate.save(output_path)
    
    return output_path

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    """Sirve archivos de audio generados"""
    return FileResponse(f"temp_audio/{filename}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**1.4 Ejecutar servidor**
```bash
cd backend
python main.py

# Servidor corriendo en: http://localhost:8000
# Docs automáticas en: http://localhost:8000/docs
```

---

### Paso 2: Crear App Móvil con Kivy

**2.1 Instalar Kivy**
```bash
pip install kivy kivymd plyer  # plyer para notificaciones
```

**2.2 Estructura básica**
```
mobile/azul_mobile/
├── main.py              # Entrada de la app
├── screens/
│   ├── chat_screen.py   # Pantalla de chat
│   └── calendar_screen.py  # Pantalla de calendario
├── services/
│   ├── api_client.py    # Cliente para backend
│   └── voice_handler.py # Manejo de audio
└── buildozer.spec       # Config para compilar APK
```

**2.3 Ejemplo main.py**
```python
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFabButton
from kivymd.uix.list import OneLineAvatarIconListItem
import requests
import json

API_URL = "http://192.168.1.100:8000"  # IP de tu PC

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        # Campo de texto
        self.input_field = MDTextField(
            hint_text="Escribe algo...",
            mode="rectangle",
            size_hint_x=0.8
        )
        self.add_widget(self.input_field)
        
        # Botón enviar
        btn_send = MDFabButton(
            icon="send",
            on_release=self.send_message
        )
        self.add_widget(btn_send)
        
        # Botón voz
        btn_voice = MDFabButton(
            icon="microphone",
            on_release=self.record_voice
        )
        self.add_widget(btn_voice)
    
    def send_message(self, instance):
        """Envía mensaje al backend"""
        texto = self.input_field.text
        if not texto:
            return
        
        try:
            # Llamada al API
            response = requests.post(
                f"{API_URL}/api/chat/message",
                json={"message": texto}
            )
            data = response.json()
            
            # Mostrar respuesta
            self.add_message("Tú", texto)
            self.add_message("Azul", data['text'])
            
            # Reproducir audio de respuesta
            self.play_audio(data['audio_url'])
            
            self.input_field.text = ""
        except Exception as e:
            print(f"Error: {e}")
    
    def record_voice(self, instance):
        """Graba voz y envía al backend"""
        # TODO: Implementar grabación de audio
        pass
    
    def play_audio(self, audio_url):
        """Reproduce audio de respuesta"""
        from kivy.core.audio import SoundLoader
        sound = SoundLoader.load(f"{API_URL}{audio_url}")
        if sound:
            sound.play()

class AzulMobileApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Cyan"
        
        sm = ScreenManager()
        sm.add_widget(ChatScreen(name='chat'))
        return sm

if __name__ == "__main__":
    AzulMobileApp().run()
```

**2.4 Compilar para Android**
```bash
# Instalar buildozer
pip install buildozer

# Configurar buildozer.spec (archivo generado)
buildozer init

# Compilar APK
buildozer -v android debug

# APK generado en: bin/azulmobile-0.1-debug.apk
```

---

### Paso 3: Despliegue y Conexión

#### Opción A: Servidor en tu PC (desarrollo/uso personal)
```bash
# En tu PC
1. Ejecutar backend: python backend/main.py
2. Obtener IP local: ipconfig (Windows) / ifconfig (Linux/Mac)
   Ejemplo: 192.168.1.100
3. En app móvil: Cambiar API_URL = "http://192.168.1.100:8000"
4. Conectar móvil a misma red WiFi que PC
5. Instalar APK en móvil
6. ¡Listo! Mobile se comunica con PC
```

#### Opción B: Servidor en la nube (uso desde cualquier lugar)
```bash
# Servicios gratuitos/baratos:
1. Railway.app (gratis hasta 500 hrs/mes)
2. Render.com (gratis con limitaciones)
3. Fly.io (gratis hasta 3 apps)
4. PythonAnywhere (gratis tier básico)

# Pasos:
1. Crear cuenta en Railway
2. Conectar repositorio GitHub
3. Deploy automático
4. Obtener URL pública: https://azul-backend.up.railway.app
5. Cambiar API_URL en app móvil
6. ¡Funciona desde cualquier lugar con internet!
```

---

## 📱 CARACTERÍSTICAS MÓVILES ADICIONALES

### 1. Notificaciones Push
```python
# En backend: Enviar notificación
from plyer import notification

def enviar_notificacion_movil(titulo, mensaje):
    notification.notify(
        title=titulo,
        message=mensaje,
        app_icon='icon.png',
        timeout=10
    )

# En móvil: Recibir y mostrar
```

### 2. Widget de Pantalla de Inicio
```python
# Widget para acceso rápido a Azul
# Mostrar próximo evento
# Acceso directo a "Hablar con Azul"
```

### 3. Modo Offline Básico
```python
# Cache local con SQLite
# Mensajes pendientes de sincronizar
# Calendario offline-first
```

### 4. Geolocalización
```python
# "Recuérdame comprar leche cuando esté cerca del super"
# Notificaciones basadas en ubicación
```

---

## ⏱️ TIMELINE ESTIMADO

### Fase 1: Backend API (1 semana)
- Día 1-2: Setup FastAPI + endpoints básicos
- Día 3-4: Integrar Ollama + Llama3
- Día 5-6: Sistema de voz (TTS + STT)
- Día 7: Testing + documentación

### Fase 2: App Móvil (2-3 semanas)
- Semana 1: UI básica (chat + calendario)
- Semana 2: Integración con API + voz
- Semana 3: Polish + notificaciones + testing

### Fase 3: Deploy (3-5 días)
- Día 1-2: Compilar APKs debug/release
- Día 3: Deploy backend a cloud (opcional)
- Día 4-5: Testing en dispositivos reales

**Total: 4-5 semanas para versión funcional** 📱✨

---

## 💰 COSTOS ESTIMADOS

### Desarrollo Local (Tu PC como servidor)
- Backend: ✅ Gratis (tu PC)
- Desarrollo móvil: ✅ Gratis (Kivy es open source)
- Base de datos: ✅ Gratis (Supabase free tier)
- **TOTAL: $0/mes** 🎉

### Deploy en la Nube
- Railway/Render: 💰 $0-5/mes (free tier generoso)
- Supabase: ✅ Gratis (hasta 500MB DB)
- OpenAI API (si usas GPT): ❌ No aplicable (usas Llama3)
- **TOTAL: $0-5/mes**

---

## 🎯 PRÓXIMOS PASOS RECOMENDADOS

### Paso 1: Prototipo Mínimo (MVP)
Crear versión básica para probar concepto:
```
✅ Chat texto simple
✅ Backend responde con Llama3
✅ App móvil muestra respuesta
```

### Paso 2: Agregar Voz
```
✅ Botón de micrófono
✅ Grabar audio → enviar a backend
✅ Reproducir respuesta de Azul
```

### Paso 3: Calendario
```
✅ Mostrar eventos
✅ Crear eventos por voz
✅ Notificaciones
```

### Paso 4: Polish
```
✅ Animaciones
✅ Temas claro/oscuro
✅ Configuraciones
```

---

## 🤔 PREGUNTAS FRECUENTES

### ¿Necesito tener mi PC encendida?
- **Opción A (PC local)**: Sí, el servidor debe estar corriendo
- **Opción B (Cloud)**: No, el servidor está en la nube 24/7

### ¿Funcionará sin internet?
- No en la arquitectura cliente-servidor
- Posible con modo offline (cache local + sincronización)

### ¿iOS también?
- Kivy: ✅ Sí, compila para iOS (necesitas Mac para Build)
- React Native: ✅ Sí, soporta iOS
- Flutter: ✅ Sí, soporta iOS

### ¿Cuánto espacio ocupa la app?
- Kivy app: ~30-50MB
- React Native: ~20-30MB
- Con cache: +50-100MB

### ¿Consume mucha batería?
- No, el procesamiento está en el servidor
- Solo usa red, micrófono y audio
- Consumo similar a WhatsApp

---

## 🚀 ¿EMPEZAMOS?

Si decides continuar, puedo ayudarte a:

1. ✅ **Crear el backend API** (FastAPI con Llama3)
2. ✅ **Setup proyecto Kivy** (estructura de app móvil)
3. ✅ **Implementar endpoints** (chat, voz, calendario)
4. ✅ **Configurar compilación** (generar APK)
5. ✅ **Deploy a cloud** (si lo deseas)

**¿Por dónde quieres empezar?** 🎯

---

**Documento creado**: Abril 12, 2026  
**Próxima actualización**: Después de implementación MVP
