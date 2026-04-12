# 📊 Estructura del Proyecto Azul v3.0

```
jarvis_vista/
│
├── 🧠 jarvis_funcional.py          # CEREBRO PRINCIPAL DE AZUL
│   ├── Clase AzulGUI
│   ├── Sistema de voz (pyttsx3)
│   ├── Reconocimiento de voz
│   ├── Interfaz gráfica (CustomTkinter)
│   ├── Integración con Supabase
│   ├── Sistema de aprendizaje
│   └── 🆕 Integración con módulos de calendario
│
├── 📦 modules/                     # MÓDULOS DE FUNCIONALIDADES
│   │
│   ├── __init__.py                # Exporta módulos
│   │
│   ├── 📅 calendario.py           # Gestión de Calendario
│   │   ├── EventoCalendario       # Clase de eventos
│   │   │   ├── Propiedades: id, título, fecha, tipo
│   │   │   ├── to_dict() / from_dict()
│   │   │   └── tiempo_restante()
│   │   │
│   │   └── GestorCalendario       # Gestión completa
│   │       ├── agregar_evento()
│   │       ├── eliminar_evento()
│   │       ├── obtener_eventos_proximos()
│   │       ├── iniciar_monitor()  # Thread en background
│   │       └── obtener_contexto_para_ia()
│   │
│   └── 🤖 analizador_calendario.py # IA para Calendario
│       │
│       ├── AnalizadorCalendario
│       │   ├── interpretar_comando()     # Llama3 interpreta
│       │   └── _procesar_fecha_hora()    # Procesa tiempo
│       │
│       └── GeneradorNotificacionesInteligentes
│           ├── generar_notificacion()          # Notif personalizada
│           ├── generar_comentario_proactivo()  # Comentarios
│           └── debe_comentar_proactivamente()  # Lógica de timing
│
├── 💾 data/                        # DATOS PERSISTENTES
│   └── calendario.json            # Eventos guardados (auto-creado)
│
├── 🧪 test_calendario.py          # PRUEBAS DEL SISTEMA
│   ├── prueba_basica()
│   ├── prueba_analizador()
│   ├── prueba_notificaciones()
│   ├── prueba_monitor()
│   └── menu_principal()
│
├── 📖 README_CALENDARIO.md        # Documentación completa
├── 🚀 INICIO_RAPIDO.md           # Guía de inicio
└── 📋 ESTRUCTURA.md              # Este archivo

```

---

## 🔄 Flujo de Datos

### 1️⃣ **Creación de Evento**
```
Usuario (voz/texto)
    ↓
jarvis_funcional.py
    ├─→ aprendizaje_en_tiempo_real()
    └─→ procesar_calendario()
         ↓
    AnalizadorCalendario
    .interpretar_comando()
         ↓
    Llama3 (IA Local)
    Extrae: tipo, título, fecha
         ↓
    GestorCalendario
    .agregar_evento()
         ↓
    EventoCalendario (objeto)
         ↓
    data/calendario.json
    (Guardado persistente)
```

### 2️⃣ **Sistema de Notificaciones**
```
GestorCalendario.monitor (thread)
Revisa cada 30 segundos
    ↓
Detecta: evento próximo
    ↓
GeneradorNotificaciones
.generar_notificacion()
    ↓
Llama3 genera mensaje
(Personalizado con perfil)
    ↓
cola_voz.put(mensaje)
    ↓
pyttsx3 habla
    ↓
Usuario escucha notificación
```

### 3️⃣ **Comentarios Proactivos**
```
obtener_respuesta_ia()
    ↓
verificar_comentarios_proactivos()
    ↓
¿Hay eventos próximos?
¿Pasó suficiente tiempo?
    ↓ (SÍ)
generar_comentario_proactivo()
    ↓
Llama3 genera comentario natural
    ↓
Se agrega al chat
    ↓
Azul lo menciona en conversación
```

---

## 🧩 Componentes Clave

### **jarvis_funcional.py** - El Cerebro
- ✅ **No se modificó lo que funciona**
- ✅ Solo se agregaron integraciones nuevas
- ✅ Mantiene toda funcionalidad existente

**Nuevas funciones agregadas:**
```python
- procesar_calendario(texto)
- manejar_notificacion_evento(evento, minutos)
- verificar_comentarios_proactivos()
```

### **modules/calendario.py** - Gestión
**Clases:**
- `EventoCalendario`: Representa un evento
- `GestorCalendario`: Gestiona todo el calendario

**Características:**
- 💾 Persistencia en JSON
- 🔄 Monitor en background
- 🔔 Sistema de callbacks
- 🧹 Limpieza automática

### **modules/analizador_calendario.py** - IA
**Clases:**
- `AnalizadorCalendario`: Interpreta comandos
- `GeneradorNotificacionesInteligentes`: Crea mensajes

**Características:**
- 🤖 Usa Llama3 local
- 🧠 Aprende del perfil
- 💬 Mensajes naturales
- ⏰ Lógica temporal

---

## 📦 Dependencias

### Ya Instaladas (Existentes)
```python
import ollama              # IA Local
import pyttsx3            # Síntesis de voz
import customtkinter      # Interfaz gráfica
import speech_recognition # Reconocimiento de voz
from supabase import *    # Base de datos
```

### Nativas de Python (No requieren instalación)
```python
import json       # Persistencia de datos
import datetime   # Manejo de fechas
import threading  # Procesos en background
import time       # Delays y timing
import os         # Sistema de archivos
import re         # Expresiones regulares
```

---

## 🎯 Puntos de Integración

### Cerebro ← Calendario
```python
# En jarvis_funcional.py.__init__()
self.gestor_calendario = GestorCalendario()
self.analizador_calendario = AnalizadorCalendario()
self.generador_notificaciones = GeneradorNotificacionesInteligentes()

# Registrar callback
self.gestor_calendario.registrar_callback_notificacion(
    self.manejar_notificacion_evento
)

# Iniciar monitor
self.gestor_calendario.iniciar_monitor()
```

### Calendario → IA (Llama3)
```python
# AnalizadorCalendario.interpretar_comando()
response = ollama.generate(model='llama3', prompt=prompt)

# GeneradorNotificaciones.generar_notificacion()
response = ollama.generate(model='llama3', prompt=prompt)
```

### Calendario → Contexto
```python
# actualizar_instrucciones_sistema()
contexto_eventos = self.gestor_calendario.obtener_contexto_para_ia()
# Se incluye en las instrucciones del sistema
```

---

## 🔐 Seguridad y Datos

### Almacenamiento Local
```json
// data/calendario.json
[
  {
    "id": "evt_12345",
    "titulo": "Cita médica",
    "fecha_hora": "2026-01-26T14:30:00",
    "tipo": "cita",
    "notificaciones": [30, 10, 5],
    "completado": false
  }
]
```

### Limpieza Automática
- Eventos completados > 7 días se eliminan
- Eventos pasados se marcan automáticamente
- No se acumula basura

---

## 🚀 Extensibilidad

### Agregar Nueva Funcionalidad

**Paso 1**: Crear módulo en `modules/`
```python
# modules/nueva_funcionalidad.py
class NuevaFuncionalidad:
    def hacer_algo(self):
        pass
```

**Paso 2**: Exportar en `modules/__init__.py`
```python
from .nueva_funcionalidad import NuevaFuncionalidad
```

**Paso 3**: Integrar en `jarvis_funcional.py`
```python
from modules import NuevaFuncionalidad

# En __init__():
self.nueva_funcionalidad = NuevaFuncionalidad()
```

**Paso 4**: Usar en lógica existente
```python
# En enviar_mensaje() o donde corresponda
self.nueva_funcionalidad.hacer_algo()
```

---

## 📈 Roadmap de Funcionalidades

```
✅ Fase 1: IA Conversacional con Memoria
   └─ jarvis_funcional.py base

✅ Fase 2: Sistema de Calendario Inteligente  ← ESTAMOS AQUÍ
   ├─ modules/calendario.py
   └─ modules/analizador_calendario.py

🔄 Fase 3: Control de Dispositivos (Próximo)
   └─ modules/control_dispositivos.py

📋 Fase 4: Gestión de Tareas
   └─ modules/gestor_tareas.py

🔗 Fase 5: Integraciones Externas
   ├─ modules/google_calendar.py
   ├─ modules/spotify.py
   └─ modules/email.py

📊 Fase 6: Análisis y Reportes
   └─ modules/analytics.py
```

---

## 🎓 Principios de Diseño

### 1. **Modularidad**
Cada funcionalidad en su propio archivo.

### 2. **No Romper lo que Funciona**
Nuevas features se agregan sin modificar código existente.

### 3. **Independencia**
Los módulos funcionan solos, sin dependencias cruzadas.

### 4. **Extensibilidad**
Fácil agregar nuevas funcionalidades.

### 5. **Persistencia**
Datos importantes se guardan localmente.

---

## 💻 Comandos Útiles

```bash
# Ejecutar Azul
python jarvis_funcional.py

# Probar calendario
python test_calendario.py

# Ver estructura
tree /F

# Limpiar cache Python
del /S *.pyc
rmdir /S __pycache__
```

---

## 🐛 Debugging

### Ver eventos guardados
```bash
type data\calendario.json
```

### Verificar imports
```python
python -c "from modules import GestorCalendario; print('✅ OK')"
```

### Test rápido
```python
from modules import GestorCalendario
from datetime import datetime, timedelta

g = GestorCalendario("data/test.json")
e = g.agregar_evento("Test", datetime.now() + timedelta(hours=1))
print(f"Evento: {e.titulo} - {e.fecha_hora}")
```

---

## 📞 Soporte

Si algo no funciona:
1. Verifica que Llama3 esté corriendo: `ollama list`
2. Chequea la estructura de carpetas
3. Revisa los errores en consola
4. Prueba con `test_calendario.py`

---

*Azul v3.0 - Arquitectura Modular Inteligente* 🤖
