# 🚀 FASE 3: Deploy en Render.com
## Estado: ⏳ PENDIENTE

---

## 🎯 Por qué Render

- ✅ **750 horas/mes gratis** (más que Railway: 500 hrs)
- ✅ **Deploy automático** desde GitHub
- ✅ **SSL gratis** incluido
- ✅ **$0/mes indefinidamente**
- ✅ **Documentación excelente**
- ⚠️ Sleep después de 15 min inactividad (solucionable)

---

## 📋 Pre-requisitos

### ✅ Ya Completado (Fase 2)
- [x] Backend completo en `backend/`
- [x] Groq API funcionando
- [x] Supabase funcionando
- [x] TTS con fallback operativo
- [x] Variables de entorno en `.env`
- [x] Servidor probado localmente

### ⏳ Por Hacer (Fase 3)
- [ ] Crear cuenta en Render.com
- [ ] Subir código a GitHub
- [ ] Crear Web Service en Render
- [ ] Configurar variables de entorno
- [ ] Deploy automático
- [ ] Configurar keep-alive (evitar sleep)
- [ ] Probar URL pública

---

## 🚀 Paso 1: Preparar Código para Render

### 1.1. Verificar Archivos de Configuración

Ya tienes estos archivos listos:
- ✅ `backend/requirements.txt`
- ✅ `Procfile`
- ✅ `.gitignore`

### 1.2. Crear archivo `render.yaml` (Opcional pero recomendado)

Render puede auto-detectar, pero un archivo de configuración es mejor:

**Crear**: `render.yaml` en la raíz del proyecto

```yaml
services:
  - type: web
    name: azul-backend
    env: python
    region: oregon  # o frankfurt para Europa
    buildCommand: pip install -r backend/requirements.txt
    startCommand: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.12.0
      - key: GROQ_API_KEY
        sync: false  # Configurar manual en dashboard
      - key: AI_MODEL
        value: llama-3.3-70b-versatile
      - key: AI_TEMPERATURE
        value: 0.7
      - key: AI_MAX_TOKENS
        value: 150
      - key: SUPABASE_URL
        sync: false  # Configurar manual en dashboard
      - key: SUPABASE_KEY
        sync: false  # Configurar manual en dashboard
      - key: VOICE_MODEL
        value: es-MX-DaliaNeural
```

---

## 🐙 Paso 2: Subir a GitHub

### 2.1. Inicializar Git (si no está inicializado)

```bash
cd "c:\Users\Chich\OneDrive\Desktop\Proyectos P\jarvis_vista"
git init
git branch -M main
```

### 2.2. Verificar .gitignore

Asegurar que `.gitignore` protege credenciales:

```bash
cat .gitignore
# Debe incluir:
# .env
# __pycache__/
# *.pyc
# temp_audio/
# temp_upload/
```

### 2.3. Crear Repositorio en GitHub

1. Ir a https://github.com/new
2. **Nombre**: `azul-backend`
3. **Descripción**: "Backend de Azul - Asistente IA con Groq y Supabase"
4. **Visibilidad**: 
   - Público (si quieres compartir)
   - Privado (para proteger código)
5. **NO** inicializar con README (ya tienes archivos)
6. Clic en "Create repository"

### 2.4. Subir Código

```bash
# Agregar todos los archivos
git add .

# Commit inicial
git commit -m "Fase 2 completa: Backend FastAPI + Groq + Supabase + TTS fallback"

# Agregar remote (reemplaza TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/azul-backend.git

# Push
git push -u origin main
```

**⚠️ IMPORTANTE**: Si tienes 2FA en GitHub, usa Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Scopes: `repo` (todos)
4. Copy token
5. Usar en lugar de password al hacer push

---

## 🌐 Paso 3: Crear Cuenta en Render

### 3.1. Registrarse

1. Ir a https://render.com
2. Clic en "Get Started"
3. **Opciones de registro:**
   - **GitHub** (RECOMENDADO) - autoriza acceso a repos
   - Google
   - GitLab
   - Email

**Recomendación**: Usar GitHub para integración automática

### 3.2. Verificar Free Tier

- **750 horas/mes** incluidas
- **SSL automático**
- **Deploy ilimitados**
- **No requiere tarjeta de crédito**

---

## 🚢 Paso 4: Deploy en Render

### 4.1. Crear Nuevo Web Service

1. En dashboard de Render → **"New +"** → **"Web Service"**
2. **Conectar Repositorio:**
   - Si conectaste con GitHub: Ver lista de repos
   - Seleccionar `azul-backend`
   - Si es privado: Autorizar acceso

### 4.2. Configurar Servicio

**Name**: `azul-backend` (o el nombre que quieras)
- URL será: `https://azul-backend.onrender.com`

**Region**: 
- `Oregon (US West)` - Más cercano a México
- `Frankfurt` - Si estás en Europa

**Branch**: `main`

**Root Directory**: (dejar vacío, Render detecta `backend/`)

**Environment**: `Python 3`

**Build Command**:
```bash
pip install -r backend/requirements.txt
```

**Start Command**:
```bash
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Plan**: 
- Seleccionar **"Free"** ($0/mes)

### 4.3. Configurar Variables de Entorno

**⚠️ CRÍTICO**: Agregar antes de crear el servicio

En **"Environment Variables"** → **"Add Environment Variable"**:

```env
GROQ_API_KEY=<tu_groq_api_key_aqui>
AI_MODEL=llama-3.3-70b-versatile
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=150
SUPABASE_URL=<tu_supabase_url>
SUPABASE_KEY=<tu_supabase_key>
VOICE_MODEL=es-MX-DaliaNeural
VOICE_RATE=+0%
VOICE_PITCH=+0Hz
PYTHON_VERSION=3.12.0
```

**Agregar una por una** o usar **"Add from .env"** (pegar contenido de `.env`)

### 4.4. Opciones Avanzadas (Opcional)

**Auto-Deploy**: `Yes` (deploy automático al hacer push a main)

**Health Check Path**: `/health`

**Docker Command**: (dejar vacío, no usamos Docker)

### 4.5. Crear Web Service

1. Clic en **"Create Web Service"**
2. Render comenzará el build (2-5 minutos)
3. Ver logs en tiempo real

---

## 📊 Paso 5: Monitorear el Deploy

### 5.1. Build Logs

Deberías ver algo como:

```bash
==> Cloning from https://github.com/TU_USUARIO/azul-backend...
==> Checking out commit XXXXXXX in branch main
==> Running build command 'pip install -r backend/requirements.txt'...
    Collecting fastapi==0.109.0
    ✅ Successfully installed fastapi-0.109.0 ...
==> Build succeeded 🎉
==> Starting service with 'cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT'
    INFO: Started server process
    ✅ Configuración validada correctamente
    ✅ IAService inicializado con modelo: llama-3.3-70b-versatile
    ✅ MemoryService conectado a Supabase
    ✅ VoiceService inicializado con voz: es-MX-DaliaNeural
    ============================================================
    ✨ SERVIDOR LISTO PARA RECIBIR REQUESTS
    ============================================================
==> Your service is live 🎉
```

### 5.2. Ver Estado

En el dashboard verás:
- **Status**: `Live` (verde)
- **URL**: `https://azul-backend.onrender.com`
- **Last deployed**: Hace X minutos
- **Region**: Oregon

---

## 🧪 Paso 6: Probar el Deploy

### 6.1. Health Check

**En navegador o curl:**

```bash
# PowerShell
Invoke-RestMethod -Uri https://azul-backend.onrender.com/health
```

**Esperado:**
```json
{
  "status": "healthy",
  "version": "3.0.0",
  "timestamp": "2026-04-12T...",
  "services": {
    "groq": true,
    "supabase": true,
    "edge_tts": true
  }
}
```

### 6.2. Documentación API

Abrir en navegador:
```
https://azul-backend.onrender.com/docs
```

Deberías ver Swagger UI con todos los endpoints.

### 6.3. Test de Conversación

```powershell
$url = "https://azul-backend.onrender.com/api/chat/message"
$json = '{"message":"Hola Azul desde Render","user_id":"default","stream":false}'
$result = Invoke-RestMethod -Uri $url -Method POST -ContentType "application/json" -Body $json
$result | ConvertTo-Json
```

**Esperado:**
```json
{
  "text": "¡Hola! ¿Cómo estás?...",
  "audio_urls": ["/audio/xxxxx.mp3"],
  "frases": ["¡Hola!", "¿Cómo estás?"],
  "usage": {"total_tokens": 1200}
}
```

### 6.4. Test de Audio

```bash
# Descargar un audio
Invoke-WebRequest -Uri https://azul-backend.onrender.com/audio/xxxxx.mp3 -OutFile test.mp3
```

---

## ⚠️ Paso 7: Solucionar Sleep Problem con UptimeRobot

### Problema: Free tier duerme después de 15 minutos de inactividad

**Síntomas:**
- Primera request después de 15 min tarda ~30 segundos
- Experiencia de usuario pobre

**Solución: Keep-Alive con UptimeRobot (GRATIS)**

Ver guía completa en: [CONFIGURAR_UPTIMEROBOT.md](CONFIGURAR_UPTIMEROBOT.md)

**Resumen rápido:**

1. Ir a https://uptimerobot.com/signUp
2. Crear cuenta gratis (50 monitores incluidos)
3. Dashboard → **"+ Add New Monitor"**
4. Configurar:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: "Azul Backend - Keep Alive"
   - **URL**: `https://azul-backend.onrender.com/health`
   - **Interval**: Every 5 minutes
   - **Expected Status**: 200
   - **Keyword**: "healthy" (opcional pero recomendado)
5. Crear Monitor

**Resultado**: 
- ✅ Tu backend NUNCA duerme (0 cold starts)
- ✅ Dashboard visual con uptime stats
- ✅ Alertas por email si API cae
- ✅ App móvil para monitorear desde celular

---

## 🔧 Paso 8: Configuración Avanzada

### 8.1. Custom Domain (Opcional)

Si tienes dominio propio:

1. Settings → Custom Domain
2. Agregar: `api.azul.tudominio.com`
3. Configurar DNS CNAME → Render te da instrucciones
4. SSL automático

### 8.2. Logs Persistentes

Render guarda logs por 7 días (free tier).

**Ver logs:**
- Dashboard → Logs (tiempo real)
- Descargar logs para debugging

### 8.3. Alertas

Settings → Notifications:
- Email cuando servicio cae
- Slack integration (opcional)
- Discord webhooks (opcional)

### 8.4. Environment Groups

Para reutilizar env vars en múltiples servicios:

1. Dashboard → Environment Groups
2. Crear grupo: "Azul Production"
3. Agregar todas las vars
4. Sincronizar con servicio

---

## 📊 Monitoreo y Maintenance

### Métricas Disponibles (Free Tier)

**Dashboard muestra:**
- CPU usage
- Memory usage
- Bandwidth (egress)
- HTTP requests
- Response times
- Error rates (5xx)

### Límites Free Tier

- **750 horas/mes** = 31 días completo (con keep-alive)
- **512 MB RAM**
- **0.1 CPU**
- **100 GB bandwidth/mes**

**⚠️ Si excedes**: Servicio se suspende hasta próximo mes

---

## 🔄 Auto-Deploy desde GitHub

### Configurar Webhook (ya está por defecto)

Cada vez que haces `git push`:

1. GitHub envía webhook a Render
2. Render detecta cambios
3. Build automático
4. Deploy automático
5. Zero downtime (gradual rollout)

**Para deshabilitar auto-deploy:**
- Settings → Build & Deploy → Auto-Deploy: `Off`

---

## 🚨 Troubleshooting

### Error: "Build failed"

**Solución:**
1. Ver logs de build en dashboard
2. Verificar `requirements.txt`
3. Verificar que `backend/` existe
4. Intentar build manual: Settings → Manual Deploy

### Error: "Application crashed"

**Solución:**
1. Ver logs de runtime
2. Verificar variables de entorno
3. Verificar que Groq/Supabase keys son correctas
4. Restart service: Manual Deploy

### Error: "503 Service Unavailable"

**Causa**: Servicio despertando de sleep

**Solución:**
- Esperar 30 segundos
- O configurar keep-alive (ver Paso 7)

### Error: "Out of memory"

**Solución:**
- Reducir `AI_MAX_TOKENS`
- Upgrade a Starter plan ($7/mes, 512 MB)

---

## 💰 Upgrade Options (Opcional)

Si necesitas más recursos:

### Starter Plan ($7/mes)
- **Sin sleep** (24/7 uptime)
- 512 MB RAM
- 0.5 CPU
- SSL incluido

### Standard Plan ($25/mes)
- 1 GB RAM
- 1 CPU
- Prioridad builds
- Más bandwidth

**¿Cuándo upgrade?**
- Si sleep es molesto
- Si excedes 750 horas/mes
- Si necesitas más RAM

---

## ✅ Checklist de Fase 3

- [ ] Crear `render.yaml` (opcional)
- [ ] Verificar `.gitignore`
- [ ] Crear repositorio en GitHub
- [ ] Subir código a GitHub
- [ ] Crear cuenta en Render
- [ ] Crear Web Service
- [ ] Configurar variables de entorno
- [ ] Esperar build exitoso
- [ ] Probar /health endpoint
- [ ] Probar /docs
- [ ] Probar /api/chat/message
- [ ] Verificar audio generation
- [ ] Configurar keep-alive cron
- [ ] Guardar URL pública
- [ ] Actualizar documentación

---

## 🎯 Resultado Esperado

Al finalizar Fase 3:

```
✅ Backend deployado en Render
✅ URL pública: https://azul-backend.onrender.com
✅ SSL habilitado (HTTPS)
✅ Groq + Supabase funcionando
✅ TTS operativo
✅ Auto-deploy configurado
✅ Keep-alive activo (0 sleep)
✅ $0/mes costo
```

---

## 📚 Recursos

- **Render Docs**: https://render.com/docs
- **Python en Render**: https://render.com/docs/deploy-fastapi
- **Environment Variables**: https://render.com/docs/environment-variables
- **Custom Domains**: https://render.com/docs/custom-domains

---

## 🏁 Siguiente Fase

**Fase 4**: Adaptar app de escritorio para usar la URL de Render en lugar de Ollama local.

**Archivo**: [FASE_4_ADAPTAR_DESKTOP.md](FASE_4_ADAPTAR_DESKTOP.md) (próximo)

---

**Preparado para**: 2026-04-12  
**Tiempo estimado**: 20-40 minutos  
**Dificultad**: ⭐⭐☆☆☆ (Fácil)  
**Costo**: $0/mes (con keep-alive gratis)
