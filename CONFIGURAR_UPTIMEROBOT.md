# ⏰ Configurar UptimeRobot - Keep Alive para Render

## 🎯 Objetivo

Evitar que Render.com duerma tu servicio después de 15 minutos de inactividad usando **UptimeRobot** (100% gratis).

---

## 📊 ¿Qué es UptimeRobot?

**UptimeRobot** es un servicio de monitoreo de uptime que:
- ✅ **50 monitores gratis** (más que suficiente)
- ✅ **Checks cada 5 minutos** (perfecto para evitar sleep)
- ✅ **Alertas por email** (si tu API cae)
- ✅ **Dashboard visual** con estadísticas
- ✅ **Sin límite de tiempo** (gratis para siempre)

---

## 🚀 Paso a Paso

### Paso 1: Crear Cuenta

1. Ir a: https://uptimerobot.com/signUp
2. **Registrarse gratis**:
   - Email
   - Password
   - Nombre (opcional)
3. Verificar email (revisar bandeja/spam)
4. Login en: https://uptimerobot.com/login

---

### Paso 2: Crear Monitor

#### 2.1. Agregar Nuevo Monitor

1. Dashboard → Clic en **"+ Add New Monitor"**

#### 2.2. Configuración del Monitor

**Monitor Type**: `HTTP(s)`

**Friendly Name**: `Azul Backend - Keep Alive`

**URL (or IP)**: 
```
https://azul-backend.onrender.com/health
```
*(Reemplaza con tu URL real de Render)*

**Monitoring Interval**: `Every 5 minutes`
- Opciones: 1, 5, 10, 15, 30 min
- **Recomendado**: 5 minutos (margen de seguridad, Render duerme a los 15)

**Monitor Timeout**: `30 seconds`

**HTTP Method**: `GET`

**HTTP Auth Type**: `None` (tu API es pública)

**Alert Contacts To Notify**: 
- Seleccionar tu email (para recibir alertas si el servicio cae)

**Advanced Settings** (Expandir):

**Expected Status Code**: `200`

**Keyword Exists**: (Opcional)
- Type: `Exists`
- Value: `healthy`
- Esto verifica que la respuesta contenga la palabra "healthy"

**SSL Certificate Validation**: `Enabled` (verificar SSL de Render)

#### 2.3. Crear Monitor

Clic en **"Create Monitor"** (botón verde)

---

### Paso 3: Verificar Funcionamiento

#### 3.1. Ver Estado

En el dashboard verás:

```
✅ Azul Backend - Keep Alive
   Status: Up
   Uptime: 100%
   Last Check: 2 minutes ago
   Response Time: 250ms
```

#### 3.2. Ver Logs

Clic en el monitor → **Logs**:
- Verás cada check realizado
- Response codes (200 = OK)
- Response times
- Errores (si los hay)

#### 3.3. Gráficas

Monitor → **Response Time**:
- Gráfica de últimas 24 horas
- Útil para detectar lentitud

---

## 📧 Paso 4: Configurar Alertas (Opcional)

### 4.1. Alert Contacts

Settings → **Alert Contacts**:
- Por defecto: Email que usaste para registro
- Opcional: Agregar más emails

### 4.2. Tipos de Alertas

**Puedes recibir alertas cuando:**
- ✅ Servicio cae (Status DOWN)
- ✅ Servicio vuelve a estar arriba (Status UP)
- ✅ SSL por expirar
- ✅ Timeout excedido

**Canales disponibles (Free tier):**
- Email ✅
- Webhook ✅
- Push notifications (app móvil) ✅

### 4.3. Configurar Notificaciones

En el monitor → **Edit** → **Alert Contacts**:
- Seleccionar cuándo notificar:
  - ☑️ When down
  - ☑️ When up (opcional)
  - ☐ SSL expiry (no aplica para Render)

---

## 🎯 Resultados Esperados

### ✅ Con UptimeRobot Activo

**Sin Keep-Alive:**
```
00:00 - Usuario hace request → 30s cold start 😞
00:01 - Backend responde
00:16 - Backend duerme 💤
00:17 - Usuario hace request → 30s cold start 😞
```

**Con UptimeRobot (cada 5 min):**
```
00:00 - UptimeRobot hace check → Backend despierto ✅
00:05 - UptimeRobot hace check → Backend despierto ✅
00:10 - UptimeRobot hace check → Backend despierto ✅
00:12 - Usuario hace request → Response instantánea 🚀
00:15 - UptimeRobot hace check → Backend despierto ✅
Resultado: 0 cold starts, 100% uptime
```

---

## 📊 Dashboard de UptimeRobot

### Métricas Disponibles (Gratis)

**Panel principal muestra:**
- ✅ **Overall Uptime**: 99.9%
- ✅ **Average Response Time**: 250ms
- ✅ **Checks hoy**: 288 (cada 5 min = 12/hora × 24)
- ✅ **Downtime**: 0 minutos
- ✅ **Gráfica de uptime** (últimos 30 días)

### Vista por Monitor

Clic en monitor para ver:
- Response times (últimas 24 horas)
- Uptime ratio (7, 30, 90 días)
- Historial de eventos (up/down)
- Average response time

---

## 🔧 Configuraciones Avanzadas

### Monitor HTTP Personalizado

Si quieres más control:

**Request Headers** (Advanced):
```
User-Agent: UptimeRobot/2.0
```

**POST Data** (si usas POST en lugar de GET):
```json
{"ping": "keep-alive"}
```

**Expected Response Contains**:
```
"status": "healthy"
```

### Múltiples Endpoints

Puedes monitorear varios endpoints (hasta 50 gratis):

1. **Keep-Alive**: `/health` cada 5 min
2. **Monitoring Real**: `/api/chat/message` cada 30 min (probar funcionalidad)
3. **Database**: Check específico cada 30 min

---

## 📱 App Móvil (Opcional)

### Descargar

- **iOS**: https://apps.apple.com/app/uptimerobot/id1104878581
- **Android**: https://play.google.com/store/apps/details?id=com.uptimerobot

### Funciones

- Ver status en tiempo real
- Recibir push notifications
- Pausar/reanudar monitores
- Ver gráficas de uptime

---

## 🆚 UptimeRobot vs Otras Alternativas

| Feature | UptimeRobot | Cron-Job.org | StatusCake |
|---------|-------------|--------------|------------|
| **Monitores** | 50 | Ilimitado | 10 |
| **Intervalo mínimo** | 5 min | 1 min | 5 min |
| **Dashboard** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Alertas** | Email, Push, Webhook | Email | Email, SMS* |
| **App móvil** | ✅ Sí | ❌ No | ✅ Sí |
| **Gráficas** | ✅ Sí | ❌ No | ✅ Sí |
| **Uptime %** | ✅ Sí | ❌ No | ✅ Sí |
| **Facilidad** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

**Veredicto**: UptimeRobot es la mejor opción para tu caso ✅

---

## 💡 Tips y Mejores Prácticas

### 1. Intervalo Óptimo

**Recomendación**: 5 minutos

**¿Por qué?**
- Render duerme a los 15 min
- 5 min da margen de seguridad (3 checks antes de sleep)
- No sobrecarga el servidor
- Free tier permite checks cada 5 min

**No usar intervalo de 1 min:**
- Innecesario (desperdicia checks)
- Puede verse como "abuse" del servicio
- Free tier tiene límites diarios

### 2. Keyword Validation

Siempre valida un keyword:
```
Expected keyword: "healthy"
```

**Beneficio:**
- Verifica que API responde correctamente
- No solo que server está arriba (200)
- Detecta errores silenciosos (500 interno)

### 3. Multiple Checks

Para alta disponibilidad:

**Monitor 1** (Keep-Alive):
- Endpoint: `/health`
- Interval: 5 min
- Purpose: Evitar sleep

**Monitor 2** (Funcionalidad):
- Endpoint: `/` (root)
- Interval: 30 min
- Purpose: Verificar que API responde

**Monitor 3** (Database):
- Endpoint: `/api/chat/history?user_id=test&limit=1`
- Interval: 1 hora
- Purpose: Verificar conexión a Supabase

### 4. Maintenance Windows

Si necesitas hacer mantenimiento:

1. Dashboard → Monitor → **Pause**
2. Hacer cambios/deploy
3. **Resume** cuando esté listo

---

## 🚨 Troubleshooting

### Monitor marca como DOWN

**Causa 1**: Cold start (primera vez)
```
Solución: Esperar 30 segundos, auto-resolverá
```

**Causa 2**: Deploy en progreso
```
Solución: Pausar monitor durante deploy
```

**Causa 3**: Error real en el backend
```
Solución: 
1. Ver logs en Render dashboard
2. Verificar variables de entorno
3. Restart service en Render
```

### Response Time Alto (>1000ms)

**Causas:**
- Cold start normal (después de sleep)
- Groq API lento
- Supabase lento
- Región lejana de Render

**Solución:**
- Aceptable si sucede esporádicamente
- Si es constante: Upgrade a Render Starter ($7/mes)

### Alertas Falsas

**Si recibes emails de DOWN cuando está UP:**

1. Aumentar timeout: 30s → 60s
2. Verificar que keyword sea correcto
3. Desactivar alertas de UP (solo DOWN)

---

## 📊 Ejemplo de Configuración Completa

### Monitor Keep-Alive (Principal)

```
Monitor Type: HTTP(s)
Friendly Name: Azul Backend - Keep Alive
URL: https://azul-backend.onrender.com/health
Interval: Every 5 minutes
Timeout: 30 seconds
Method: GET
Expected Status: 200
Keyword: "healthy"
Alert Contacts: tu@email.com
Notifications: When DOWN only
```

### Monitor Funcional (Secundario)

```
Monitor Type: HTTP(s)
Friendly Name: Azul API - Root Check
URL: https://azul-backend.onrender.com/
Interval: Every 30 minutes
Timeout: 30 seconds
Method: GET
Expected Status: 200
Keyword: "Azul Backend API"
Alert Contacts: tu@email.com
Notifications: When DOWN only
```

---

## ✅ Checklist de Configuración

- [ ] Crear cuenta en UptimeRobot.com
- [ ] Verificar email de confirmación
- [ ] Hacer login en dashboard
- [ ] Crear monitor principal (Keep-Alive)
  - [ ] URL: /health
  - [ ] Intervalo: 5 minutos
  - [ ] Keyword: "healthy"
  - [ ] Alertas: cuando DOWN
- [ ] Esperar primer check (5 min)
- [ ] Verificar que status = UP
- [ ] (Opcional) Crear monitor funcional
- [ ] (Opcional) Descargar app móvil
- [ ] (Opcional) Configurar webhook para Slack/Discord
- [ ] Guardar credenciales de UptimeRobot

---

## 🎯 Resultado Final

```
✅ UptimeRobot configurado
✅ Monitor activo (check cada 5 min)
✅ Backend NUNCA duerme
✅ 0 cold starts
✅ Alertas configuradas
✅ Dashboard monitoreando 24/7
✅ 100% uptime garantizado
✅ $0 costo adicional
```

---

## 📚 Recursos

- **UptimeRobot**: https://uptimerobot.com
- **Dashboard**: https://uptimerobot.com/dashboard
- **Docs**: https://uptimerobot.com/api/
- **Help Center**: https://blog.uptimerobot.com/
- **Status Page**: https://stats.uptimerobot.com/

---

## 🔗 Integración con Render

### Flujo Completo

```
1. Render deploy completado
   ↓
2. Obtener URL: https://azul-backend.onrender.com
   ↓
3. Crear monitor en UptimeRobot
   ↓
4. URL monitoreada: /health cada 5 min
   ↓
5. Backend recibe ping → No duerme
   ↓
6. Usuario hace request → Response instantánea
   ↓
7. UptimeRobot envía dashboard daily summary
```

---

**Creado**: 2026-04-12  
**Para**: Azul Backend en Render.com  
**Costo**: $0/mes  
**Uptime esperado**: 99.9%
