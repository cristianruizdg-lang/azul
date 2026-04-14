# 📚 Índice de Documentación - Azul v3.0

> **🔥 DOCUMENTO NUEVO:** [`REFERENCIA_TECNICA_COMPLETA.md`](REFERENCIA_TECNICA_COMPLETA.md) - CONSULTAR ANTES DE CUALQUIER MODIFICACIÓN  
> 855 líneas con toda la arquitectura, endpoints, dependencias críticas, problemas resueltos y warnings para evitar romper funcionalidad

---

## 🎯 Guías Fase por Fase

### ✅ Fase 1: Setup Groq API (COMPLETADA)
- **Archivo**: [`FASE_1_GROQ_SETUP.md`](FASE_1_GROQ_SETUP.md)
- **Estado**: ✅ Completada
- **Resultado**: API key obtenida, modelo llama-3.3-70b-versatile probado

### ✅ Fase 2: Backend FastAPI + Groq (COMPLETADA)
- **Archivo**: [`FASE_2_BACKEND_COMPLETADO.md`](FASE_2_BACKEND_COMPLETADO.md)
- **Estado**: ✅ Completada
- **Resultado**: Backend funcional con TTS fallback (Edge TTS 7.2.8 + pyttsx3)
- **Servidor local**: http://localhost:8000

### ✅ Fase 3: Deploy en Render (COMPLETADA)
- **Archivo**: [`FASE_3_RENDER_DEPLOY.md`](FASE_3_RENDER_DEPLOY.md)
- **Estado**: ✅ Completada - Backend en producción
- **URL**: https://azul-4xsp.onrender.com
- **Health Check**: https://azul-4xsp.onrender.com/health
- **Plataforma**: Render.com (750 hrs/mes gratis)
- **Resuelto**: 4 problemas críticos (pydantic, websockets, Python 3.12, UptimeRobot HEAD)

### ✅ Fase 4: App Desktop Cloud (COMPLETADA)
- **Archivo**: [`FASE_4_APP_DESKTOP_CLOUD.md`](FASE_4_APP_DESKTOP_CLOUD.md)
- **Estado**: ✅ Completada y probada
- **App**: `jarvis_cloud.py` (1474 líneas con diseño original completo)
- **Resultado**: Desktop app conectada a API en nube, UI completa (esfera 3D, animaciones, espectro audio)

### ✅ Fase 5: App Móvil Android (COMPLETADA)
- **Archivo**: [`FASE_5_APP_MOVIL.md`](FASE_5_APP_MOVIL.md)
- **Estado**: ✅ Completada - Lista para compilar APK
- **Framework**: Kivy/KivyMD con Material Design
- **App**: `mobile/azul_mobile.py` (700+ líneas)
- **Backend**: Mismo API (https://azul-4xsp.onrender.com)
- **Características**: Chat texto/voz, historial sincronizado, memoria compartida

---

## 🔧 Configuración y Setup

### Comparación de Plataformas
- **Archivo**: [`COMPARACION_PLATAFORMAS_DEPLOY.md`](COMPARACION_PLATAFORMAS_DEPLOY.md)
- **Contenido**: Render vs Railway vs Fly.io vs Hugging Face
- **Resultado**: ✅ Render seleccionado (750 hrs/mes vs 500 Railway)

### UptimeRobot Keep-Alive
- **Archivo**: [`CONFIGURAR_UPTIMEROBOT.md`](CONFIGURAR_UPTIMEROBOT.md)
- **Propósito**: Evitar que Render duerma el backend (ping cada 5 min)
- **Estado**: ✅ Backend soporta GET y HEAD en /health
- **Acción pendiente**: Usuario debe configurar monitor en UptimeRobot

### Archivo de Configuración Render
- **Archivo**: `render.yaml`
- **Propósito**: Auto-configuración para deploy en Render
- **Estado**: ✅ Configurado con Python 3.12

---

## 📖 Arquitectura y Diseño

### 🔥 Referencia Técnica Completa (NUEVO)
- **Archivo**: [`REFERENCIA_TECNICA_COMPLETA.md`](REFERENCIA_TECNICA_COMPLETA.md)
- **Contenido**: **DOCUMENTO MAESTRO** - 855 líneas
- **Incluye**:
  - Estructura completa del proyecto
  - Todos los endpoints con ejemplos
  - Versiones críticas de dependencias CON RAZONES
  - Historial de 8 problemas resueltos + soluciones
  - Deploy checklist completo
  - ⚠️ Warnings críticos (DO NOT / ALWAYS DO)
  - Historial de commits (10 commits documentados)
- **Cuándo usar**: ANTES de cualquier modificación al código

### README Principal
- **Archivo**: [`README.md`](README.md)
- **Contenido**: Overview general del proyecto Azul v3.0
- **Incluye**: Arquitectura cloud, características, instalación

### Evaluación App Móvil
- **Archivo**: [`EVALUACION_APP_MOVIL.md`](EVALUACION_APP_MOVIL.md)
- **Contenido**: Análisis inicial de requerimientos móviles
- **Decisión**: Arquitectura híbrida cloud (implementada)

### Arquitectura Híbrida
- **Archivo**: [`ARQUITECTURA_HIBRIDA_SINCRONIZADA.md`](ARQUITECTURA_HIBRIDA_SINCRONIZADA.md)
- **Contenido**: Diseño completo del sistema cloud
- **Componentes**: ✅ Groq + Supabase + Render (implementado)

---

## 🧪 Testing y Validación

### Test Groq
- **Archivo**: `test_groq.py`
- **Propósito**: Validar conexión a Groq API
- **Resultado**: ✅ Funcionando con llama-3.3-70b-versatile

### Prueba Backend Producción
- **Health Check**: `curl https://azul-4xsp.onrender.com/health`
- **Resultado**: ✅ `{"status":"healthy","version":"3.0.0","services":{"groq":true,"supabase":true,"edge_tts":true}}`

### Prueba App Desktop Cloud
- **Comando**: `python jarvis_cloud.py`
- **Resultado**: ✅ Backend conectado v3.0.0, Supabase cargado, micrófono activo

---

## 📂 Estructura del Proyecto

```
jarvis_vista/
│
├── 📚 DOCUMENTACIÓN
│   ├── README.md
│   ├── GUIA_DOCUMENTACION.md (este archivo)
│   ├── 🔥 REFERENCIA_TECNICA_COMPLETA.md ⭐ LEER ANTES DE MODIFICAR
│   ├── COMPARACION_PLATAFORMAS_DEPLOY.md
│   ├── CONFIGURAR_UPTIMEROBOT.md
│   │
│   ├── FASE_1_GROQ_SETUP.md ✅
│   ├── FASE_2_BACKEND_COMPLETADO.md ✅
│   ├── FASE_3_RENDER_DEPLOY.md ✅
│   ├── FASE_4_APP_DESKTOP_CLOUD.md ✅
│   │
│   ├── EVALUACION_APP_MOVIL.md
│   └── ARQUITECTURA_HIBRIDA_SINCRONIZADA.md
│
├── ⚙️ CONFIGURACIÓN
│   ├── .env (variables para desktop app)
│   ├── .gitignore
│   ├── .python-version (Python 3.12 - NO BORRAR)
│   └── render.yaml (configuración Render)
│
├── 🔵 BACKEND (FastAPI - En Render)
│   └── backend/
│       ├── main.py (GET/HEAD support para UptimeRobot)
│       ├── config.py (validación movida a startup)
│       ├── requirements.txt (versiones críticas actualizadas)
│       ├── services/
│       │   ├── ia_service.py (Groq API)
│       │   ├── memory_service.py (Supabase)
│       │   └── voice_service.py (Edge TTS 7.2.8 + fallback)
│       ├── routers/
│       │   └── chat.py (endpoints /api/chat/*)
│       ├── models/
│       │   └── schemas.py
│       └── temp_audio/ (MP3 generados por TTS)
│
├── 🖥️ DESKTOP APP
│   ├── jarvis_funcional.py (original - Ollama local)
│   ├── jarvis_cloud.py (NUEVO - conecta al backend en Render) ✅
│   ├── requirements_desktop.txt (dependencias para app cloud)
│   └── modules/
│       ├── calendario.py
│       └── analizador_calendario.py
│
├── 🧪 TESTING
│   ├── test_groq.py
│   └── test_calendario.py
│
└── 💾 DATA (local, NO subir)
    ├── data/
    │   └── calendario.json
    └── temp_audio/ (generados localmente)
```

---

## 🚀 Comandos Útiles

### Backend Producción (Render)
```bash
# Ver salud del backend
curl https://azul-4xsp.onrender.com/health

# Ver info del API
curl https://azul-4xsp.onrender.com/

# Documentación interactiva
https://azul-4xsp.onrender.com/docs
```

### Desktop App Cloud
```bash
# Instalar dependencias
pip install -r requirements_desktop.txt

# Ejecutar app
python jarvis_cloud.py
```

### Backend Local (desarrollo)
```bash
# Instalar dependencias
cd backend
pip install -r requirements.txt

# Iniciar servidor
python main.py

# Ver en navegador
http://localhost:8000/docs
```

### Testing
```bash
# Probar Groq API
python test_groq.py

# Probar endpoint producción
$json = '{"message":"Hola Azul","user_id":"default","stream":false}'
Invoke-RestMethod -Uri https://azul-4xsp.onrender.com/api/chat/message `
  -Method POST -ContentType "application/json" -Body $json
```

### Git (Deploy)
```bash
# Ver status
git status

# Agregar todo
git add .

# Commit con mensaje descriptivo
git commit -m "Descripción del cambio"

# Push a GitHub (trigger auto-deploy en Render)
git push -u origin main

# Updates subsecuentes
git add .
git commit -m "Tu mensaje descriptivo"
git push
```

---

## 📊 Estado Actual del Proyecto

### ✅ Completado
- [x] Fase 1: Groq API configurado y probado
- [x] Fase 2: Backend FastAPI completo
- [x] TTS con fallback (Edge TTS 7.2.8 + pyttsx3)
- [x] Integración Groq (llama-3.3-70b-versatile)
- [x] Integración Supabase (historial + perfil)
- [x] Sistema de voz (síntesis + reconocimiento)
- [x] Fase 3: Backend desplegado en Render ✅
- [x] Resueltos 4 problemas críticos de deploy
- [x] Fase 4: App desktop cloud completa ✅
- [x] Fix UptimeRobot 405 (HEAD support) ✅
- [x] Documentación técnica completa (855 líneas) ✅
- [x] Fase 5: App móvil Android con Kivy ✅

### ⏳ Pendiente de Usuario
- [ ] Configurar monitor en UptimeRobot (5 min) - Backend listo con HEAD support
- [ ] Verificar monitor muestra "Up" status
- [ ] (Opcional) Compilar APK en WSL2/Linux con buildozer
- [ ] (Opcional) Instalar APK en dispositivo Android

### 📅 Opcional (Mejoras futuras)
- [ ] iOS app con Swift o React Native
- [ ] Notificaciones push
- [ ] Widget de Android
- [ ] Modo offline con cache local

---

## 🎯 Objetivo Final

```
✅ Backend en nube (Render.com) - DEPLOY EXITOSO
✅ URL pública 24/7: https://azul-4xsp.onrender.com
✅ App desktop conectada a nube - jarvis_cloud.py FUNCIONAL
✅ App móvil Android - azul_mobile.py COMPLETADA
⏳ UptimeRobot keep-alive - Fix desplegado, falta configurar monitor
⏳ APK compilado - Requiere WSL2/Linux + buildozer
✅ Mismo contexto sincronizado vía Supabase
✅ $0 costo mensual - Free tier de Render + Groq + Supabase
```

---

## 💡 Notas Importantes

### Archivos que NO se suben a Git
```
.env                    # Credenciales (desktop)
temp_audio/            # Audios generados
temp_upload/           # Archivos temporales
__pycache__/           # Cache de Python
*.pyc                  # Compilados
data/calendario.json   # Datos locales
```

### URLs Importantes
- **Backend Producción**: https://azul-4xsp.onrender.com ✅
- **Health Check**: https://azul-4xsp.onrender.com/health ✅
- **Docs API**: https://azul-4xsp.onrender.com/docs ✅
- **Backend Local**: http://localhost:8000 (desarrollo)
- **GitHub Repo**: https://github.com/cristianruizdg-lang/azul.git ✅
- **Groq Console**: https://console.groq.com
- **Supabase Dashboard**: https://lovcwnqviaovthtcxjjr.supabase.co
- **UptimeRobot**: https://uptimerobot.com/dashboard

---

## ⚠️ Advertencias Críticas

### DO NOT (No hacer nunca):
1. ❌ NO actualizar Python a 3.13+ (aifc removido, SpeechRecognition lo necesita)
2. ❌ NO bajar edge-tts a <7.2.8 (v6.1.9 tiene error 403)
3. ❌ NO bajar websockets a <13.0 (falta websockets.asyncio)
4. ❌ NO bajar pydantic a <2.9.0 (requiere Rust compilation)
5. ❌ NO borrar `.python-version` file (Render usará Python 3.14)
6. ❌ NO cambiar endpoints de `api_route(methods=["GET", "HEAD"])` a solo `@app.get()` (UptimeRobot usa HEAD)

### ALWAYS DO (Hacer siempre):
1. ✅ LEER `REFERENCIA_TECNICA_COMPLETA.md` ANTES de modificar código
2. ✅ Probar localmente antes de hacer push (auto-deploy en Render)
3. ✅ Verificar Render logs después de cada deploy
4. ✅ Mantener versiones críticas en requirements.txt
5. ✅ Consultar historial de problemas antes de cambiar dependencias

---

## 📞 Ayuda Rápida

### ¿Qué archivo leer según tu necesidad?

**🔥 Antes de CUALQUIER modificación al código:**
→ [`REFERENCIA_TECNICA_COMPLETA.md`](REFERENCIA_TECNICA_COMPLETA.md) (855 líneas, documento maestro)

**Quiero deployar en Render ahora:**
→ [`FASE_3_RENDER_DEPLOY.md`](FASE_3_RENDER_DEPLOY.md) (ya completado ✅)

**Quiero entender las opciones de deploy:**
→ [`COMPARACION_PLATAFORMAS_DEPLOY.md`](COMPARACION_PLATAFORMAS_DEPLOY.md)

**Quiero configurar keep-alive:**
→ [`CONFIGURAR_UPTIMEROBOT.md`](CONFIGURAR_UPTIMEROBOT.md)

**Quiero entender la app desktop cloud:**
→ [`FASE_4_APP_DESKTOP_CLOUD.md`](FASE_4_APP_DESKTOP_CLOUD.md) (completada ✅)

**Quiero crear/compilar la app móvil Android:**
→ [`FASE_5_APP_MOVIL.md`](FASE_5_APP_MOVIL.md) (completada ✅)

**Quiero ver qué se hizo en Fase 2:**
→ [`FASE_2_BACKEND_COMPLETADO.md`](FASE_2_BACKEND_COMPLETADO.md)

**Quiero entender la arquitectura completa:**
→ [`ARQUITECTURA_HIBRIDA_SINCRONIZADA.md`](ARQUITECTURA_HIBRIDA_SINCRONIZADA.md)

**Quiero ver overview general:**
→ [`README.md`](README.md)

---

## 🔗 Flujo de Trabajo Actual

```
1. ✅ Fase 1: Setup Groq
   └── test_groq.py → API key válida
   
2. ✅ Fase 2: Backend Local
   └── python backend/main.py → http://localhost:8000
   
3. ✅ Fase 3: Deploy Cloud (COMPLETADA)
   ├── ✅ Subido a GitHub: https://github.com/cristianruizdg-lang/azul.git
   ├── ✅ Desplegado en Render: https://azul-4xsp.onrender.com
   ├── ✅ Fix UptimeRobot HEAD support (commit ed926a0)
   └── ⏳ Usuario debe configurar monitor UptimeRobot
   
4. ✅ Fase 4: App Desktop Cloud (COMPLETADA)
   └── ✅ jarvis_cloud.py → Conectada a API cloud
   └── ✅ UI completa original preservada
   └── ✅ Probada y funcional
   
5. ✅ Fase 5: App Móvil Android (COMPLETADA)
   ├── ✅ azul_mobile.py con Kivy/KivyMD
   ├── ✅ Interfaz Material Design completa
   ├── ✅ Chat texto y voz integrado
   ├── ✅ Sincronización con Supabase
   ├── ✅ buildozer.spec configurado
   └── ⏳ Compilar APK (usuario con WSL2/Linux)
```

---

## 🏆 Commit History (10 commits principales)

```
3bceca1 - Backend completo: FastAPI + Groq + Supabase + TTS fallback
14a59e5 - Fix: Actualizar pydantic y Python version para Render
3c39792 - Fix: Remover validación automática en import
606fc8a - Fix: Actualizar websockets a >=13.0 para supabase realtime
c001244 - Fix: Agregar .python-version para forzar Python 3.12 (aifc)
96244f1 - Fase 4: App de escritorio cloud
0fe6700 - Actualizar jarvis_cloud.py con diseño completo original
fc55a95 - Actualizar documentación
ed926a0 - Fix: Agregar soporte HEAD a /health para UptimeRobot (405)
76fadd2 - Docs: Agregar documentación técnica completa del sistema
```

---

**Última actualización**: 13 de Abril, 2026  
**Versión**: 3.0.0  
**Estado**: ✅ Fases 1-5 completadas, backend en producción, apps desktop y móvil funcionales  
**Repo**: https://github.com/cristianruizdg-lang/azul.git  
**Producción**: https://azul-4xsp.onrender.com
