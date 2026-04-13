# 🖥️ FASE 4: APP DE ESCRITORIO CON BACKEND EN LA NUBE

## ✅ COMPLETADO

Tu aplicación de escritorio ahora usa el backend en la nube en lugar de Ollama local.

---

## 📁 **Archivos Creados**

### **jarvis_cloud.py**
- Versión cloud de tu asistente de escritorio
- **Cambios principales:**
  - ❌ **Removido:** `import ollama` y `import edge_tts` 
  - ✅ **Agregado:** Cliente HTTP que se conecta a `https://azul-4xsp.onrender.com`
  - ✅ **Audio:** Se descarga desde la API en lugar de generarse localmente
  - ✅ **IA:** Groq en la nube (no Ollama local)
  - ✅ **Memoria:** Supabase compartida entre todos tus dispositivos

### **requirements_desktop.txt**
- Dependencias para la app de escritorio
- Incluye: `customtkinter`, `speechrecognition`, `pygame`, `requests`, etc.
- **No incluye:** `ollama` ni `edge-tts` (ya no son necesarios)

### **.env** (actualizado)
- Agregada variable: `API_URL=https://azul-4xsp.onrender.com`

---

## 🚀 **Cómo Usar la App Cloud**

### **1. Instalar Dependencias**

```powershell
# Crear entorno virtual (recomendado)
python -m venv venv
.\\venv\\Scripts\\Activate

# Instalar dependencias
pip install -r requirements_desktop.txt
```

### **2. Verificar .env**

Abre el archivo `.env` y verifica que tenga:

```env
API_URL=https://azul-4xsp.onrender.com
SUPABASE_URL=https://lovcwnqviaovthtcxjjr.supabase.co
SUPABASE_KEY=eyJhb...
```

### **3. Ejecutar la App**

```powershell
python jarvis_cloud.py
```

### **4. Usar la Interfaz**

La app abrirá con:

- **Chat visual** con historial de mensajes
- **Entrada de texto** en la parte inferior
- **Botón de micrófono (🎤)** para hablar por voz
- **Botón "Enviar"** para mensajes escritos

**Flujo:**
1. Escribe un mensaje **O** presiona el micrófono y habla
2. La app envía tu mensaje al backend en la nube
3. El backend procesa con Groq AI
4. Recibe respuesta de texto **+ audio generado**
5. La app descarga y reproduce el audio automáticamente
6. Todo se guarda en Supabase (memoria compartida)

---

## 🔄 **Diferencias: Local vs Cloud**

| Característica | Jarvis Local (Original) | Jarvis Cloud (Nuevo) |
|----------------|-------------------------|----------------------|
| **IA** | Ollama local (llama3) | Groq Cloud (llama-3.3-70b) |
| **Audio TTS** | Edge TTS local | Edge TTS en backend → descarga MP3 |
| **Velocidad** | Depende de tu PC | Rápido (Groq es muy veloz) |
| **Requiere PC potente** | ✅ Sí | ❌ No |
| **Necesita internet** | ❌ No | ✅ Sí |
| **Memoria compartida** | ❌ Solo local | ✅ Sincronizada en Supabase |
| **Costo** | Gratis (hardware local) | Gratis (Render + Groq free tier) |

---

## 🎯 **Ventajas de la Versión Cloud**

### ✅ **Sin Dependencia de Hardware**
- Ya no necesitas una PC potente para correr LLama3
- Funciona en cualquier computadora con internet

### ✅ **Memoria Sincronizada**
- Tu historial y contexto se guarda en Supabase
- Puedes usar la app desde cualquier dispositivo
- El asistente te reconoce en todos lados

### ✅ **IA Más Potente**
- Groq usa llama-3.3-70b (más inteligente que llama3-8b local)
- Respuestas más rápidas (Groq tiene GPUs especializadas)

### ✅ **Sin Instalaciones Pesadas**
- No necesitas instalar Ollama (varios GB)
- No necesitas descargar modelos LLM
- Solo dependencias Python básicas

---

## 📊 **Arquitectura Cloud**

```
┌──────────────────┐
│  JARVIS_CLOUD.PY │  ← Tu app de escritorio
│  (Windows/Mac)   │
└────────┬─────────┘
         │ HTTP
         │
         ▼
┌────────────────────────────┐
│  BACKEND EN RENDER         │
│  https://azul-4xsp...      │
│                            │
│  ┌──────────────────────┐  │
│  │ FastAPI              │  │
│  │ - Recibe mensaje     │  │
│  │ - Consulta Groq      │  │
│  │ - Genera audio TTS   │  │
│  │ - Guarda en Supabase │  │
│  └──────────────────────┘  │
└───────┬────────────────────┘
        │
        ├──────────► GROQ API (IA)
        ├──────────► SUPABASE (BD)
        └──────────► EDGE TTS (Audio)
```

**Flujo:**
1. Usuario escribe/habla → `jarvis_cloud.py`
2. App envía HTTP POST → `https://azul-4xsp.onrender.com/api/chat/message`
3. Backend procesa con Groq (llama-3.3-70b)
4. Backend genera audio con Edge TTS
5. Backend retorna: `{"text": "respuesta", "audio_urls": ["/audio/abc.mp3"]}`
6. App descarga y reproduce el MP3
7. Todo se guarda en Supabase

---

## 🐛 **Solución de Problemas**

### **Error: "No se pudo conectar al backend"**

```bash
# Verificar que el backend está funcionando
curl https://azul-4xsp.onrender.com/health
```

Debería retornar:
```json
{"status": "healthy", "version": "3.0.0"}
```

Si no funciona: El backend puede estar "dormido" (Render free tier duerme después de 15 min). La primera petición tomará ~30s para despertar.

### **Error: "Module 'pyaudio' not found"**

PyAudio necesita compilación en Windows:

```powershell
# Opción 1: Instalar desde wheel pre-compilado
pip install pipwin
pipwin install pyaudio

# Opción 2: Descargar wheel manual
# https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
```

### **El micrófono no funciona**

Verifica permisos:
1. Windows → Configuración → Privacidad → Micrófono
2. Permitir que apps accedan al micrófono
3. Permitir `python.exe`

---

## 🎨 **Personalización**

### **Cambiar la voz**

Edita `.env`:
```env
VOICE_MODEL=es-ES-ElviraNeural  # Voz española
# o
VOICE_MODEL=es-AR-ElenaNeural   # Voz argentina
```

Voces disponibles: [Lista de voces Edge TTS](https://speech.microsoft.com/portal/voicegallery)

### **Cambiar el modelo de IA**

Edita `.env`:
```env
AI_MODEL=llama-3.1-8b-instant  # Más rápido
# o
AI_MODEL=mixtral-8x7b-32768     # Contexto muy largo
```

Modelos disponibles en [Groq Console](https://console.groq.com)

---

## 📈 **Próximos Pasos**

### **Fase 5: App Móvil con Kivy** (Opcional)
- Crear app Android con la misma lógica
- Usar el mismo backend `https://azul-4xsp.onrender.com`
- Memoria compartida entre desktop y móvil

### **Mejoras Opcionales:**
- ✨ Agregar streaming de respuestas (actualizar texto en tiempo real)
- ✨ Modo offline (cache de respuestas frecuentes)
- ✨ Temas visuales (modo oscuro)
- ✨ Integración con Google Calendar
- ✨ Shortcuts de teclado personalizados

---

## 📝 **Notas Importantes**

1. **Primer arranque lento:** Si el backend estaba dormido (15+ min sin uso), la primera petición tomará ~30 segundos. Después será instantáneo.

2. **Límites de Groq:** El tier gratuito tiene límite de requests/minuto. Si haces muchas preguntas muy rápido, puede dar error 429. Espera unos segundos.

3. **UptimeRobot:** Configúralo para evitar que el backend se duerma. Ver: `CONFIGURAR_UPTIMEROBOT.md`

4. **Privacidad:** Todo se guarda en Supabase. Si compartes el proyecto, cambia las credenciales en `.env`

---

## ✅ **Checklist de Verificación**

- [ ] Dependencias instaladas: `pip install -r requirements_desktop.txt`
- [ ] `.env` actualizado con `API_URL`
- [ ] Backend funcional: `curl https://azul-4xsp.onrender.com/health`
- [ ] Permisos de micrófono habilitados
- [ ] PyAudio instalado correctamente
- [ ] App ejecuta sin errores: `python jarvis_cloud.py`
- [ ] Puedo enviar mensajes de texto
- [ ] Puedo hablar por voz
- [ ] El audio se reproduce correctamente
- [ ] UptimeRobot configurado (opcional pero recomendado)

---

## 🎉 **¡Listo!**

Tu app de escritorio ahora funciona con IA en la nube. Ya no depende de Ollama local, usa Groq para respuestas más rápidas y potentes.

**Beneficios:**
- 🚀 Más rápido (Groq es ultra-veloz)
- 🧠 Más inteligente (llama-3.3-70b vs llama3-8b)
- 💾 Memoria compartida (Supabase)
- 💰 $0 costo total
- 🌐 Accesible desde cualquier dispositivo

**Para dudas o problemas, revisa:**
- Logs del backend: Render Dashboard → Logs
- Logs de la app: Terminal de PowerShell
- Documentación completa: `GUIA_DOCUMENTACION.md`
