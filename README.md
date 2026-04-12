# 🔵 AZUL - Asistente IA Personal v3.0

> **Tu amiga cercana y directa, disponible en móvil y desktop**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Groq](https://img.shields.io/badge/Groq-Llama3.3-green.svg)](https://groq.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-teal.svg)](https://fastapi.tiangolo.com/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

---

## 📖 Descripción

**Azul v3.0** es un asistente de IA conversacional que funciona **100% en la nube gratis** ($0/mes) con acceso desde múltiples dispositivos. Utiliza Groq (Llama 3.3) para respuestas ultrarrápidas y mantiene contexto sincronizado a través de Supabase.

### 🆕 Novedades v3.0 (Cloud Edition)
- ☁️ **Backend en la nube**: No necesitas PC encendida
- 📱 **Multi-Plataforma**: Desktop + Móvil con mismo contexto
- ⚡ **10x más rápido**: Groq vs Ollama local (300-500 tokens/seg)
- 💾 **Memoria Sincronizada**: Mismo Azul en todos tus dispositivos
- 💰 **$0 costo mensual**: Groq + Railway + Supabase gratis

---

## ✨ Características Principales

### 🤖 IA Conversacional Avanzada
- **Modelo**: Llama 3.3 (70B parámetros)
- **Proveedor**: Groq (ultra-rápido)
- **Personalidad**: Directa, cercana, como tu amiga
- **Memoria**: Aprende de cada conversación
- **Contexto**: Recuerda hasta 50 mensajes anteriores

### 💾 Sistema de Memoria Persistente
- **Perfil de Usuario**: Aprende gustos, hábitos, preferencias
- **Historial**: Todas las conversaciones guardadas
- **Sincronización**: Mismo contexto en desktop y móvil
- **Base de Datos**: Supabase PostgreSQL (nube)

### 🎙️ Voz Natural
- **TTS**: Edge TTS con voz mexicana (Dalia)
- **STT**: Google Speech Recognition
- **Idioma**: Español (México)
- **Activación**: Comando "Azul"

### 📅 Calendario Inteligente (Legacy - Desktop Only)
- Eventos con lenguaje natural
- Notificaciones personalizadas
- Comentarios proactivos en conversación

---

## 🏗️ Arquitectura

```
┌──────────────────┐         ┌─────────────────┐
│  Desktop App     │────────▶│   FastAPI       │
│  (CustomTkinter) │         │   Backend       │
└──────────────────┘         │  (Railway.app)  │
                             └────────┬────────┘
┌──────────────────┐                 │
│   Mobile App     │─────────────────┤
│   (Kivy/KivyMD)  │ (Próximamente)  │
└──────────────────┘                 │
                   ┌─────────────────┴─────────────────┐
                   │                                   │
              ┌────▼─────┐                      ┌─────▼──────┐
              │   Groq   │                      │  Supabase  │
              │ Llama3.3 │                      │ PostgreSQL │
              │  (Free)  │                      │   (Free)   │
              └──────────┘                      └────────────┘
```

---

## 🚀 Instalación
- Síntesis de voz natural
- Visualización con esfera 3D animada

### 💾 Persistencia de Datos
- Historial guardado en Supabase
- Calendario en JSON local
- Sistema de aprendizaje continuo

---

## 📁 Estructura del Proyecto

```
jarvis_vista/
│
├── 🧠 jarvis_funcional.py          # Cerebro principal
│
├── 📦 modules/                     # Módulos funcionales
│   ├── calendario.py              # Gestión de eventos
│   ├── analizador_calendario.py   # IA para interpretar
│   └── __init__.py
│
├── 💾 data/                        # Datos persistentes
│   └── calendario.json            # (auto-generado)
│
├── 🧪 test_calendario.py          # Pruebas
├── 🔧 config_calendario.py        # Configuración
│
└── 📚 Documentación
    ├── README.md                  # Este archivo
    ├── INICIO_RAPIDO.md          # Guía rápida
    ├── README_CALENDARIO.md       # Docs del calendario
    ├── EJEMPLOS_USO.md           # Ejemplos prácticos
    └── ESTRUCTURA.md             # Arquitectura detallada
```

---

## 🚀 Instalación y Uso

### Prerequisitos

1. **Python 3.8+**
2. **Ollama con Llama3**
   ```bash
   # Instalar Ollama desde: https://ollama.ai/
   ollama pull llama3
   ```

3. **Librerías Python** (ya deberías tenerlas de v2.5)
   ```bash
   pip install ollama pyttsx3 customtkinter speechrecognition supabase numpy
   ```

### Ejecutar Azul

```bash
cd "C:\Users\Chich\OneDrive\Desktop\Proyectos P\jarvis_vista"
python jarvis_funcional.py
```

### Probar Solo el Calendario

```bash
python test_calendario.py
```

---

## 💡 Ejemplos de Uso

### Crear Eventos

```python
# Por voz
"Azul, tengo reunión mañana a las 10am"

# Por texto (en el chat)
"Recuérdame comprar leche en 2 horas"
```

### Consultar Agenda

```python
"¿Qué tengo hoy?"
"¿Cuáles son mis citas de mañana?"
```

### Ejemplo Completo

```
🗣️ Tú: "Azul, tengo dentista mañana a las 6pm"
🤖 Azul: "Perfecto Cristian, he anotado tu cita con el dentista 
         para mañana a las 6pm."

[Al día siguiente, 2:30pm]
🔔 Azul: "Cristian, son las 2:30pm. Tienes dentista a las 6pm 
         y tú sabes que tardas mucho en alistarte..."

[5:30pm]
🔔 Azul: "Dentista en 30 minutos. Ya deberías estar en camino."
```

Ver más ejemplos en: [EJEMPLOS_USO.md](EJEMPLOS_USO.md)

---

## 🛠️ Arquitectura Modular

### Principio de Diseño

> **"No modificar lo que funciona mientras construimos nuevo"**

- Código base intacto
- Funcionalidades modulares e independientes
- Fácil de extender
- Sin dependencias cruzadas

### Flujo de Datos

```
Usuario (voz/texto)
    ↓
jarvis_funcional.py (cerebro)
    ↓
AnalizadorCalendario (interpreta con IA)
    ↓
GestorCalendario (gestiona eventos)
    ↓
Monitor (revisa cada 30s)
    ↓
GeneradorNotificaciones (crea mensaje personalizado)
    ↓
Azul habla (pyttsx3)
```

Ver arquitectura completa en: [ESTRUCTURA.md](ESTRUCTURA.md)

---

## 📊 Tipos de Eventos

| Tipo | Uso | Ejemplo |
|------|-----|---------|
| **Cita** 🗓️ | Reuniones, doctores | "Cita con el abogado" |
| **Alarma** ⏰ | Despertadores | "Alarma a las 7am" |
| **Recordatorio** 📝 | Tareas, pendientes | "Recordar comprar pan" |

---

## 🎨 Personalización

### Configuración Rápida

Edita `config_calendario.py`:

```python
# Tiempos de notificación
NOTIFICACIONES_DEFAULT = [30, 10, 5]

# Nivel de formalidad (1-5)
NIVEL_FORMALIDAD = 3

# Usar humor
USAR_HUMOR = True
```

### Perfil de Usuario

Azul aprende de ti mientras conversas:
- Tu sentido del humor
- Tus hábitos (tardas en alistarte, etc.)
- Tus preferencias
- Tu forma de hablar

---

## 📚 Documentación Completa

| Documento | Contenido |
|-----------|-----------|
| [INICIO_RAPIDO.md](INICIO_RAPIDO.md) | Guía de inicio en 5 minutos |
| [README_CALENDARIO.md](README_CALENDARIO.md) | Documentación técnica del calendario |
| [EJEMPLOS_USO.md](EJEMPLOS_USO.md) | 20+ ejemplos prácticos |
| [ESTRUCTURA.md](ESTRUCTURA.md) | Arquitectura y componentes |
| `config_calendario.py` | Todas las opciones de configuración |

---

## 🧪 Testing

### Probar Módulo de Calendario

```bash
python test_calendario.py
```

Opciones disponibles:
1. Crear y listar eventos
2. Analizador de lenguaje natural
3. Generador de notificaciones
4. Monitor en tiempo real
5. Contexto para IA
6. Todas las pruebas

---

## 🐛 Solución de Problemas

### Error: "No module named 'modules'"
```bash
# Asegúrate de estar en la carpeta correcta
cd "C:\Users\Chich\OneDrive\Desktop\Proyectos P\jarvis_vista"
```

### Azul no reconoce eventos
- Usa palabras clave: "cita", "alarma", "recordatorio"
- Especifica la hora: "a las 3pm"
- Menciona el día: "mañana", "hoy"

### No recibo notificaciones
- Verifica que Llama3 esté instalado: `ollama list`
- Revisa que el evento esté en el futuro
- Chequea `data/calendario.json`

### Llama3 muy lento
```python
# En config_calendario.py
MODELO_IA = 'llama2'  # Más rápido pero menos preciso
```

---

## 🗺️ Roadmap

### ✅ Fase 1: IA Conversacional (Completado)
- Memoria de conversación
- Sistema de aprendizaje
- Integración con Supabase

### ✅ Fase 2: Calendario Inteligente (Completado)
- Eventos con lenguaje natural
- Notificaciones personalizadas
- Comentarios proactivos

### 🔄 Fase 3: Control de Dispositivos (Próximo)
- Luces inteligentes
- Control de temperatura
- Integración IoT

### 📋 Fase 4: Gestión de Tareas
- Todo list inteligente
- Priorización automática
- Seguimiento de productividad

### 🔗 Fase 5: Integraciones Externas
- Google Calendar
- Spotify
- Email
- WhatsApp

### 📊 Fase 6: Analytics
- Análisis de productividad
- Patrones de comportamiento
- Reportes personalizados

---

## 🤝 Contribuir

Este es un proyecto personal en evolución. Si tienes ideas:
1. Prueba la funcionalidad actual
2. Documenta bugs o mejoras
3. Propón nuevas funcionalidades

---

## 📝 Notas Técnicas

### Tecnologías
- **IA**: Llama3 (Ollama)
- **Lenguaje**: Python 3.8+
- **Interfaz**: CustomTkinter
- **Voz**: pyttsx3 + SpeechRecognition
- **Base de datos**: Supabase + JSON local
- **Persistencia**: JSON para calendario

### Rendimiento
- Monitor de eventos: cada 30 segundos
- Uso de CPU: mínimo (threads en background)
- Almacenamiento: <1MB para miles de eventos
- Internet: NO requerido (excepto Supabase sync)

### Seguridad
- Todo local, sin envío de datos
- Opcional: sync con Supabase
- No se almacenan credenciales sensibles

---

## 📄 Licencia

Proyecto personal de código abierto para aprendizaje.
Usa herramientas 100% gratuitas.

---

## 👨‍💻 Autor

**Cristian** (Chich)
- Proyecto: Azul - AI Assistant
- Versión: 3.0
- Fecha: Enero 2026

---

## 🎉 Agradecimientos

- **Ollama** por Llama3 local
- **Supabase** por base de datos gratuita
- Comunidad de Python y CustomTkinter

---

## 📞 Soporte

Si tienes problemas:
1. Lee [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
2. Revisa [ESTRUCTURA.md](ESTRUCTURA.md)
3. Prueba con `test_calendario.py`
4. Verifica que Llama3 esté corriendo

---

## 🔥 Quick Start (TL;DR)

```bash
# 1. Instalar Ollama y Llama3
ollama pull llama3

# 2. Ejecutar Azul
python jarvis_funcional.py

# 3. Decir o escribir
"Azul, tengo reunión mañana a las 10am"

# 4. Recibir notificaciones automáticas
# ¡Listo! 🎉
```

---

**¿Listo para empezar? Ejecuta Azul y di: "Hola Azul"** 🚀

---

*Azul v3.0 - Tu asistente personal inteligente, privado y gratuito*
