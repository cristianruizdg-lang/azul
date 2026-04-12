# 📱 Guía: Azul en Tablet Android

## 🎯 Objetivo
Ejecutar Azul en tablet Android de forma **100% gratuita y offline**, con capacidad de conectarse a tu PC cuando esté disponible.

---

## 🚀 OPCIÓN 1: Termux + Phi-3 Mini (RECOMENDADO)

### Requisitos
- **Tablet Android 7.0+**
- **4GB RAM mínimo** (8GB recomendado)
- **10GB espacio libre**
- **Sin root necesario**

### Paso 1: Instalar Termux

1. Descarga **Termux** desde:
   - [F-Droid](https://f-droid.org/en/packages/com.termux/) (Recomendado)
   - O Play Store (versión antigua)

2. Abre Termux y actualiza:
```bash
pkg update && pkg upgrade
```

### Paso 2: Instalar Python y Dependencias

```bash
# Instalar Python
pkg install python python-pip

# Instalar git
pkg install git

# Instalar dependencias de sistema
pkg install libffi openssl libjpeg-turbo

# Dar acceso al almacenamiento
termux-setup-storage
```

### Paso 3: Clonar Azul

```bash
# Ir a carpeta compartida
cd ~/storage/shared

# Clonar el proyecto
git clone https://github.com/TU_USUARIO/azul-assistant.git
cd azul-assistant

# O copiar archivos manualmente desde tu PC
```

### Paso 4: Instalar Ollama para Android

```bash
# Descargar Ollama ARM64
wget https://ollama.ai/download/ollama-android-arm64

# Dar permisos
chmod +x ollama-android-arm64

# Mover a bin
mv ollama-android-arm64 $PREFIX/bin/ollama

# Verificar
ollama --version
```

### Paso 5: Instalar Modelo Ligero

```bash
# Phi-3 Mini (3.8B parámetros - PERFECTO para tablets)
ollama pull phi3

# O TinyLlama si tu tablet tiene poca RAM
ollama pull tinyllama
```

### Paso 6: Adaptar Azul para Móvil

Modifica `jarvis_funcional.py`:

```python
# Detectar si está en Android
import os
IS_ANDROID = 'ANDROID_ROOT' in os.environ

# Usar modelo ligero en Android
MODELO = 'phi3' if IS_ANDROID else 'llama3'

# Desactivar CustomTkinter en Android (usaremos Kivy)
if IS_ANDROID:
    from kivy.app import App
    # ... interfaz Kivy
else:
    import customtkinter as ctk
    # ... interfaz actual
```

### Paso 7: Ejecutar Azul

```bash
# Modo solo voz (sin interfaz gráfica)
python azul_voice_only.py

# O con interfaz Kivy
python azul_mobile.py
```

---

## 🔄 OPCIÓN 2: Cliente-Servidor (PC + Tablet)

### En tu PC (Servidor)

Crea `servidor_azul.py`:

```python
from fastapi import FastAPI
import ollama
import uvicorn

app = FastAPI()

@app.post("/chat")
async def chat(mensaje: str):
    response = ollama.generate(model='llama3', prompt=mensaje)
    return {"respuesta": response['response']}

if __name__ == "__main__":
    # Ejecutar en red local
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

```bash
# Instalar
pip install fastapi uvicorn

# Ejecutar servidor
python servidor_azul.py
```

### En tu Tablet (Cliente)

Conecta a tu PC vía WiFi:

```python
import requests

# IP de tu PC en la red local
PC_IP = "192.168.1.100"  # Cambiar por tu IP

def enviar_mensaje(texto):
    try:
        # Intentar conectar a PC
        response = requests.post(
            f"http://{PC_IP}:8000/chat",
            json={"mensaje": texto},
            timeout=2
        )
        return response.json()["respuesta"]
    except:
        # Si falla, usar modelo local
        return ollama.generate(model='phi3', prompt=texto)
```

---

## ☁️ OPCIÓN 3: Hugging Face Inference API (Requiere Internet)

### Configuración

1. Crea cuenta gratis en [Hugging Face](https://huggingface.co)
2. Genera token en: Settings → Access Tokens
3. **30,000 tokens/mes GRATIS**

### Código

```python
import requests

HF_TOKEN = "tu_token_aqui"

def chat_huggingface(mensaje):
    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    
    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": mensaje}
    )
    
    return response.json()[0]['generated_text']
```

---

## 🎨 Interfaz Móvil con Kivy

### Instalar Kivy

```bash
pip install kivy
```

### UI Simple

```python
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

class AzulMobileApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10)
        
        self.chat_display = Label(
            text='Azul: ¡Hola! ¿En qué puedo ayudarte?',
            size_hint_y=0.7
        )
        
        self.input_box = TextInput(
            hint_text='Escribe tu mensaje...',
            size_hint_y=0.2
        )
        
        send_btn = Button(
            text='Enviar',
            size_hint_y=0.1,
            on_press=self.enviar_mensaje
        )
        
        layout.add_widget(self.chat_display)
        layout.add_widget(self.input_box)
        layout.add_widget(send_btn)
        
        return layout
    
    def enviar_mensaje(self, instance):
        texto = self.input_box.text
        # Procesar con Ollama
        respuesta = ollama.generate(model='phi3', prompt=texto)
        self.chat_display.text = f"Azul: {respuesta['response']}"
        self.input_box.text = ''

if __name__ == '__main__':
    AzulMobileApp().run()
```

---

## 📊 Comparación de Modelos

| Modelo | Tamaño | RAM Necesaria | Velocidad | Calidad | Offline |
|--------|--------|---------------|-----------|---------|---------|
| **Llama3 70B** | 40GB | 64GB+ | Lenta | ⭐⭐⭐⭐⭐ | ✅ (Solo PC) |
| **Llama3 8B** | 4.7GB | 8GB+ | Media | ⭐⭐⭐⭐ | ✅ |
| **Phi-3 Mini** | 2.3GB | 4GB+ | Rápida | ⭐⭐⭐⭐ | ✅ ✨ **IDEAL TABLET** |
| **TinyLlama** | 1.1GB | 2GB+ | Muy rápida | ⭐⭐⭐ | ✅ |
| **Gemini Flash** | Cloud | - | Muy rápida | ⭐⭐⭐⭐⭐ | ❌ (Gratis limitado) |

---

## 🔋 Optimización de Batería

```python
# Reducir frecuencia de monitor de calendario
INTERVALO_MONITOR = 60  # De 30s a 60s

# Desactivar animaciones en móvil
if IS_ANDROID:
    ANIMACIONES_ACTIVAS = False

# Modo ahorro de energía
MODO_AHORRO = True  # Procesa solo cuando interactúas
```

---

## 🎯 Próximos Pasos

1. **Hoy**: Prueba Termux + Python básico
2. **Esta semana**: Instala Phi-3 y prueba respuestas
3. **Siguiente**: Adapta calendario para móvil
4. **Futuro**: Implementa servidor en PC para conexión híbrida

---

## ❓ FAQ

**¿Phi-3 es tan bueno como Llama3?**
- Phi-3 Mini es sorprendentemente bueno para su tamaño
- Microsoft lo entrenó para ser eficiente
- Perfecto para conversaciones y tareas del calendario

**¿Cuánta batería consume?**
- Phi-3: ~15-20% por hora de uso activo
- En standby: ~2-3% por hora (solo monitor de calendario)

**¿Necesito conocimientos avanzados?**
- No, sigue la guía paso a paso
- Termux es como una terminal de Linux
- Te ayudo con cada paso

---

## 📞 Siguiente Acción

Dime qué opción prefieres y empezamos:

1. **Termux + Phi-3** (100% offline, autónomo)
2. **Cliente-Servidor** (PC potente + tablet ligera)
3. **Híbrido** (ambas opciones con fallback)

