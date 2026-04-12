# 🚀 FASE 1: SETUP DE GROQ API
## Crear Cuenta y Obtener API Key Gratuita

---

## 📋 OBJETIVO
Crear una cuenta gratuita en Groq y obtener tu API key para usar Llama3-70B ultra-rápido en la nube.

---

## ⏱️ TIEMPO ESTIMADO
**5-10 minutos**

---

## 📝 PASOS DETALLADOS

### Paso 1: Visitar Groq Console

1. Abre tu navegador
2. Ve a: **https://console.groq.com**
3. Verás la página de login/signup de Groq

### Paso 2: Crear Cuenta (Sign Up)

**Opción A: Con Google (más rápido)**
1. Click en "Sign up with Google"
2. Selecciona tu cuenta de Google
3. Acepta permisos
4. ✅ Cuenta creada

**Opción B: Con Email**
1. Click en "Sign up"
2. Ingresa tu email
3. Crea una contraseña
4. Verifica tu email (revisa tu bandeja de entrada)
5. Click en el link de verificación
6. ✅ Cuenta creada

### Paso 3: Completar Perfil (Opcional)

Groq puede pedirte información básica:
- Nombre
- Propósito de uso: "Personal Assistant / Education"
- ✅ No requiere tarjeta de crédito

### Paso 4: Generar API Key

Una vez dentro del dashboard:

1. En el menú lateral izquierdo, busca **"API Keys"** o **"Keys"**
2. Click en **"Create API Key"**
3. Dale un nombre a tu key (ejemplo: "Azul_Backend")
4. Click en **"Create"**
5. **⚠️ IMPORTANTE**: Se mostrará tu API key UNA SOLA VEZ
6. Copia la key completa (empieza con `gsk_...`)

**Ejemplo de API Key**:
```
gsk_aBc123XyZ456DeF789GhI012JkL345MnO678PqR901StU234VwX567
```

### Paso 5: Guardar API Key de Forma Segura

**Opción A: Crear archivo .env (RECOMENDADO)**

1. En tu proyecto, crea un archivo llamado `.env` en la raíz:

```bash
# En PowerShell
cd "c:\Users\Chich\OneDrive\Desktop\Proyectos P\jarvis_vista"
New-Item -Path ".env" -ItemType File
```

2. Abre `.env` con un editor de texto y agrega:

```env
# API Keys
GROQ_API_KEY=gsk_tu_key_completa_aqui

# Supabase (las que ya tienes)
SUPABASE_URL=https://lovcwnqviaovthtcxjjr.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxvdmN3bnF2aWFvdnRodGN4ampyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjcwNjI0MDMsImV4cCI6MjA4MjYzODQwM30.33OPrkBMRnFPJRW98SNJCkx6fG1x4Ffx4MKxfBmbbWE
```

3. **⚠️ IMPORTANTE**: Agrega `.env` a tu `.gitignore`:

```bash
# Crear o editar .gitignore
echo ".env" >> .gitignore
```

**Opción B: Guardar en un lugar seguro**
- Notepad (temporal)
- Password manager (recomendado)
- Archivo local encriptado

### Paso 6: Verificar Límites de Free Tier

En el dashboard de Groq, verifica tus límites:
- **Requests por día**: 14,400
- **Requests por minuto**: 600
- **Modelos disponibles**: Llama3-8B, Llama3-70B, Mixtral, Gemma

✅ Todo gratis, sin necesidad de tarjeta de crédito

---

## 🧪 PRUEBA RÁPIDA (OPCIONAL)

Antes de continuar, verifica que tu API key funciona:

### Instalar SDK de Groq

```bash
pip install groq
```

### Test Rápido en Python

Crea un archivo temporal `test_groq.py`:

```python
from groq import Groq

# Reemplaza con tu API key
client = Groq(api_key="gsk_tu_key_aqui")

# Test simple
response = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {"role": "user", "content": "Hola, di 'funciona' si me escuchas"}
    ],
    temperature=0.7,
    max_tokens=10
)

print("✅ Groq funciona!")
print(f"Respuesta: {response.choices[0].message.content}")
```

### Ejecutar Test

```bash
python test_groq.py
```

**Resultado esperado**:
```
✅ Groq funciona!
Respuesta: ¡Funciona! Te escucho perfectamente.
```

Si ves este resultado, ¡todo está listo! 🎉

---

## 📊 INFORMACIÓN ADICIONAL

### Modelos Disponibles en Groq (Free Tier)

| Modelo | Parámetros | Velocidad | Uso Recomendado |
|--------|-----------|-----------|-----------------|
| **llama3-8b-8192** | 8B | ⚡⚡⚡⚡⚡ | Respuestas rápidas |
| **llama3-70b-8192** | 70B | ⚡⚡⚡⚡ | Conversaciones complejas (RECOMENDADO) |
| **mixtral-8x7b-32768** | 8x7B | ⚡⚡⚡⚡ | Contexto largo |
| **gemma-7b-it** | 7B | ⚡⚡⚡⚡⚡ | Tareas específicas |

Para Azul usaremos: **llama3-70b-8192** (mejor balance calidad/velocidad)

### Comparación de Velocidad Real

```
📊 Benchmark: Generar 100 tokens

Ollama Local (tu PC):     ~2-4 segundos
OpenAI GPT-4:            ~1-2 segundos
Groq Llama3-70B:         ~0.2-0.5 segundos ⚡

→ Groq es 10x más rápido que local
```

---

## ⚠️ TROUBLESHOOTING

### Problema: "Invalid API Key"
**Solución**: 
- Verifica que copiaste la key completa (empieza con `gsk_`)
- No incluyas espacios al principio o final
- La key es case-sensitive

### Problema: "Rate limit exceeded"
**Solución**:
- Llegaste al límite de 14,400 requests/día
- Espera 24 horas para que se resetee
- O crea otra cuenta (permitido en free tier)

### Problema: "Model not found"
**Solución**:
- Usa el nombre exacto: `llama3-70b-8192`
- No uses `llama3` solo (nombre de Ollama)

---

## 🔐 SEGURIDAD

### ✅ Buenas Prácticas

1. **NUNCA** subas `.env` a GitHub
2. **NUNCA** compartas tu API key públicamente
3. **USA** variables de entorno en producción
4. **REGENERA** la key si la expones accidentalmente

### ❌ NO Hacer

```python
# ❌ MAL - Hardcoded en código
client = Groq(api_key="gsk_abc123...")

# ✅ BIEN - Desde variable de entorno
import os
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
```

---

## ✅ CHECKLIST FASE 1

Antes de continuar a Fase 2, verifica:

- [ ] Cuenta de Groq creada
- [ ] API Key obtenida (empieza con `gsk_`)
- [ ] API Key guardada en `.env`
- [ ] `.env` agregado a `.gitignore`
- [ ] SDK de Groq instalado (`pip install groq`)
- [ ] Test de API funcionando (opcional pero recomendado)

---

## 🎯 SIGUIENTE PASO

Una vez completada esta fase, continuaremos con:

**FASE 2: Implementar Backend con FastAPI + Groq**
- Crear estructura de carpetas
- Implementar servicios (IA, Voz, Memoria)
- Crear endpoints REST API
- Integrar Groq en lugar de Ollama

---

## 📞 AYUDA

Si tienes problemas en esta fase:
1. Verifica que estás en https://console.groq.com (no otro sitio)
2. Revisa tu email para verificación de cuenta
3. Intenta con otro navegador si hay problemas
4. La creación de cuenta es 100% gratuita, no piden tarjeta

---

**Completado**: ❌  
**Fecha**: Abril 12, 2026  
**Próxima Fase**: Implementar Backend con FastAPI + Groq
