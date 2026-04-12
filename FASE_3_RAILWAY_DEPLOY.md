# 🚢 FASE 3: Deploy en Railway
## Estado: ⏳ PENDIENTE

---

## 🎯 Objetivo
Deployar el backend de Azul en Railway.app para obtener una URL pública accesible desde cualquier dispositivo (desktop + móvil).

---

## 📋 Pre-requisitos

### ✅ Ya Completado (Fase 2)
- [x] Backend completo en carpeta `backend/`
- [x] Groq API funcionando
- [x] Supabase funcionando
- [x] Variables de entorno en `.env`
- [x] Servidor probado localmente

### ⏳ Por Hacer (Fase 3)
- [ ] Crear cuenta en Railway.app
- [ ] Crear repositorio de GitHub
- [ ] Subir código a GitHub
- [ ] Configurar proyecto Railway
- [ ] Configurar variables de entorno
- [ ] Deploy automático
- [ ] Probar URL pública

---

## 🚀 Pasos Detallados

### Paso 1: Preparar Código para Railway

#### 1.1. Crear Procfile
Railway necesita saber cómo iniciar el servidor.

**Crear archivo**: `backend/Procfile`
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### 1.2. Verificar requirements.txt
Ya está listo en `backend/requirements.txt`

#### 1.3. Crear railway.json (opcional)
**Crear archivo**: `railway.json` en la raíz del proyecto
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install -r backend/requirements.txt"
  },
  "deploy": {
    "startCommand": "cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

### Paso 2: Subir a GitHub

#### 2.1. Inicializar Git (si no está inicializado)
```bash
cd "c:\Users\Chich\OneDrive\Desktop\Proyectos P\jarvis_vista"
git init
```

#### 2.2. Agregar .gitignore
Ya existe, verifica que incluya:
```
.env
__pycache__/
*.pyc
temp_audio/
temp_upload/
```

#### 2.3. Crear repositorio en GitHub
1. Ir a https://github.com/new
2. Nombre: `azul-backend`
3. Descripción: "Backend de Azul - Asistente IA con Groq y Supabase"
4. Visibilidad: Privado (para proteger credenciales)
5. NO inicializar con README (ya tienes archivos)
6. Crear repositorio

#### 2.4. Subir código
```bash
git add .
git commit -m "Fase 2: Backend completo con FastAPI + Groq + Supabase"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/azul-backend.git
git push -u origin main
```

---

### Paso 3: Crear Cuenta en Railway

#### 3.1. Registrarse
1. Ir a https://railway.app
2. Clic en "Start a New Project"
3. Login con GitHub (recomendado)
4. Autorizar Railway para acceder a repositorios

#### 3.2. Plan Gratuito
- **Límites**: 500 horas/mes, $5 crédito inicial
- **Costo después**: ~$5/mes (si excedes límites)
- **Para proyecto pequeño**: 100% gratis (<500 hrs/mes)

---

### Paso 4: Deploy en Railway

#### 4.1. Crear Nuevo Proyecto
1. Dashboard Railway → "New Project"
2. Seleccionar "Deploy from GitHub repo"
3. Buscar y seleccionar `azul-backend`
4. Railway detectará Python y usará Nixpacks

#### 4.2. Configurar Variables de Entorno
En Railway Dashboard → Settings → Variables:

```env
GROQ_API_KEY=<tu_groq_api_key_aqui>
AI_MODEL=llama-3.3-70b-versatile
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=150
SUPABASE_URL=<tu_supabase_url>
SUPABASE_KEY=<tu_supabase_key>
VOICE_MODEL=es-MX-DaliaNeural
PORT=8000
```

**⚠️ CRÍTICO**: No subir `.env` a GitHub, solo configurar en Railway.

#### 4.3. Configurar Build
Railway generalmente detecta automáticamente, pero verifica:
- **Build Command**: `pip install -r backend/requirements.txt`
- **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

#### 4.4. Deploy
1. Railway iniciará el build automáticamente
2. Ver logs en tiempo real
3. Esperar "Deployment successful" (2-5 minutos)
4. Railway asignará una URL pública

---

### Paso 5: Obtener URL Pública

#### 5.1. Generar Dominio
1. Settings → Networking → Generate Domain
2. Railway asigna: `azul-backend-production-XXXX.up.railway.app`
3. Copiar URL completa

#### 5.2. Verificar Health
```bash
curl https://azul-backend-production-XXXX.up.railway.app/health
```

Debe retornar:
```json
{
  "status": "healthy",
  "version": "3.0.0",
  "services": {
    "groq": true,
    "supabase": true,
    "edge_tts": true
  }
}
```

---

### Paso 6: Probar Endpoints

#### 6.1. Test con curl
```bash
curl -X POST https://azul-backend-production-XXXX.up.railway.app/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message":"Hola Azul desde Railway","user_id":"default","stream":false}'
```

#### 6.2. Test con Python
```python
import requests

url = "https://azul-backend-production-XXXX.up.railway.app/api/chat/message"
data = {
    "message": "Hola Azul desde Python",
    "user_id": "default",
    "stream": False
}

response = requests.post(url, json=data)
print(response.json())
```

#### 6.3. Documentación Online
Abrir en navegador:
```
https://azul-backend-production-XXXX.up.railway.app/docs
```

---

## 🔧 Configuración Avanzada (Opcional)

### Custom Domain
Si tienes dominio propio:
1. Settings → Networking → Custom Domain
2. Agregar: `api.azul.tudominio.com`
3. Configurar DNS CNAME apuntando a Railway

### Monitoreo
Railway incluye:
- **Logs**: Ver en tiempo real
- **Métricas**: CPU, RAM, Network
- **Alertas**: Cuando servicio cae

### Auto-Deploy
Railway hace deploy automático cuando:
- Haces push a `main` en GitHub
- Detecta cambios en el código
- No necesitas hacer nada manual

---

## 🚨 Troubleshooting

### Error: "Build failed"
**Solución**: Verificar `requirements.txt` y logs de build

### Error: "Application crashed"
**Solución**: 
1. Verificar variables de entorno
2. Ver logs: Railway Dashboard → Logs
3. Verificar que Supabase/Groq keys sean correctas

### Error: "502 Bad Gateway"
**Solución**: Servidor no inició correctamente
- Verificar Start Command
- Verificar que puerto sea $PORT (no hardcoded 8000)

### Error: "Out of memory"
**Solución**: Reducir `AI_MAX_TOKENS` o upgrade plan

---

## 💰 Costos Estimados

### Uso Típico de Azul

**Horas/mes**: 
- Desktop: 50 horas
- Móvil: 100 horas
- **Total**: 150 horas < 500 horas free tier

**Conclusión**: 100% GRATIS por varios meses

### Si excedes 500 horas:
- Costo: ~$0.01/hora adicional
- 600 horas total = $1/mes
- 700 horas total = $2/mes

**Recomendación**: Monitorear uso en Railway Dashboard

---

## ✅ Checklist de Fase 3

- [ ] Crear Procfile en backend/
- [ ] Crear railway.json en raíz
- [ ] Verificar .gitignore
- [ ] Crear repositorio en GitHub
- [ ] Subir código a GitHub
- [ ] Crear cuenta Railway
- [ ] Crear nuevo proyecto Railway
- [ ] Conectar repo de GitHub
- [ ] Configurar variables de entorno
- [ ] Esperar build exitoso
- [ ] Generar dominio público
- [ ] Probar /health endpoint
- [ ] Probar /api/chat/message
- [ ] Verificar logs sin errores
- [ ] Guardar URL pública
- [ ] Actualizar documentación

---

## 🎯 Resultado Esperado

Al finalizar Fase 3:

```
✅ Backend deployado en Railway
✅ URL pública accesible 24/7
✅ Groq + Supabase funcionando
✅ Auto-deploy configurado
✅ $0 costo mensual (bajo uso típico)

📡 URL: https://azul-backend-production-XXXX.up.railway.app
📚 Docs: https://azul-backend-production-XXXX.up.railway.app/docs
```

---

## 📚 Recursos

- **Railway Docs**: https://docs.railway.app
- **Railway Python Guide**: https://docs.railway.app/guides/python
- **FastAPI Deploy**: https://fastapi.tiangolo.com/deployment/
- **Nixpacks**: https://nixpacks.com/docs

---

## 🏁 Siguiente Fase

**Fase 4**: Adaptar app de escritorio para usar la URL de Railway en lugar de Ollama local.

---

**Preparado para**: 2026-04-12  
**Tiempo estimado**: 30-60 minutos  
**Dificultad**: ⭐⭐☆☆☆ (Media)
