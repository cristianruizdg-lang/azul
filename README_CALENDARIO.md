# Azul - AI Assistant v3.0
## Sistema de Calendario y Recordatorios Inteligentes

### 🎯 Nueva Funcionalidad: Gestión de Citas, Alarmas y Recordatorios

Azul ahora puede gestionar tu calendario de forma inteligente y proactiva. No solo recuerda tus eventos, sino que hace comentarios contextuales basados en tu perfil y hábitos.

---

## 📁 Estructura Modular

El proyecto ahora tiene una arquitectura modular donde cada funcionalidad está en archivos separados:

```
jarvis_vista/
├── jarvis_funcional.py          # Cerebro principal de Azul
├── modules/                     # Módulos de funcionalidades
│   ├── __init__.py
│   ├── calendario.py           # Gestión de eventos
│   └── analizador_calendario.py # IA para interpretar comandos
├── data/                       # Datos persistentes
│   └── calendario.json         # Eventos guardados
└── README_CALENDARIO.md        # Esta documentación
```

---

## 🚀 Características

### 1. **Creación de Eventos con Lenguaje Natural**
Simplemente dile a Azul lo que necesitas:

**Ejemplos:**
- "Tengo una cita con el doctor mañana a las 8:30pm"
- "Recuérdame llamar a mamá en 2 horas"
- "Alarma para las 7:00am mañana"
- "Agenda una reunión pasado mañana a las 3pm"

### 2. **Notificaciones Inteligentes y Personalizadas**
Azul no solo te recuerda eventos, sino que adapta los recordatorios a tu perfil:

**Ejemplo para alguien que tarda en alistarse:**
> "Cristian, son las 2:30pm. Recuerda que tienes una cita a las 8:30pm y tú te tardas mucho en alistarte 😄"

**Ejemplo para alguien más serio:**
> "Tienes una reunión importante en 30 minutos. Hora: 3:00pm."

### 3. **Comentarios Proactivos**
Azul menciona tus eventos de forma natural durante la conversación:

> "Por cierto, recuerda que tienes esa cita con el dentista en un par de horas..."

### 4. **Sistema de Notificaciones Multinivel**
- ⏰ 30 minutos antes
- ⏰ 10 minutos antes  
- ⏰ 5 minutos antes

(Los tiempos son configurables por evento)

---

## 💻 Cómo Usar

### Crear Eventos

**Por Voz:**
1. Di "Azul" para activarla
2. Menciona tu evento: *"Tengo dentista mañana a las 4pm"*
3. Azul confirmará que lo anotó

**Por Texto:**
1. Escribe en el chat: *"Recuérdame comprar leche en 1 hora"*
2. Presiona Enter
3. Azul procesará y confirmará

### Ver tus Eventos

Pregúntale a Azul:
- "¿Qué tengo hoy?"
- "¿Cuáles son mis citas?"
- "¿Tengo algo programado?"

---

## 🔧 Componentes Técnicos

### 1. **GestorCalendario** (`modules/calendario.py`)
- Gestiona eventos (crear, leer, actualizar, eliminar)
- Monitor de eventos en segundo plano
- Sistema de notificaciones basado en tiempo
- Persistencia en JSON

### 2. **AnalizadorCalendario** (`modules/analizador_calendario.py`)
- Interpreta lenguaje natural con Llama3
- Extrae fecha, hora y tipo de evento
- Procesa tiempo relativo ("mañana", "en 2 horas")

### 3. **GeneradorNotificacionesInteligentes**
- Crea recordatorios personalizados
- Adapta tono según perfil del usuario
- Genera comentarios proactivos contextuales

---

## 🎨 Tipos de Eventos

| Tipo | Uso | Ejemplo |
|------|-----|---------|
| **Cita** | Reuniones, doctores, eventos | "Cita con el dentista" |
| **Alarma** | Despertadores, alertas | "Alarma a las 7am" |
| **Recordatorio** | Tareas, compras | "Recordar comprar pan" |

---

## 📊 Formato de Datos

Los eventos se guardan en `data/calendario.json`:

```json
[
  {
    "id": "evt_1738022400000",
    "titulo": "Cita con el doctor",
    "fecha_hora": "2026-01-26T20:30:00",
    "tipo": "cita",
    "descripcion": "",
    "notificaciones": [30, 10, 5],
    "notificaciones_enviadas": [],
    "completado": false,
    "creado_en": "2026-01-25T15:30:00"
  }
]
```

---

## 🔄 Cómo Funciona el Sistema

### Flujo de Creación de Evento:
```
Usuario dice/escribe
    ↓
AnalizadorCalendario interpreta (Llama3)
    ↓
GestorCalendario crea evento
    ↓
Se guarda en calendario.json
    ↓
Monitor detecta el evento
```

### Flujo de Notificación:
```
Monitor revisa eventos cada 30s
    ↓
Detecta evento próximo
    ↓
GeneradorNotificaciones crea mensaje personalizado
    ↓
Azul habla el recordatorio
    ↓
Marca notificación como enviada
```

---

## 🛠️ Extensión Futura

La arquitectura modular permite agregar fácilmente:
- ✅ Control de dispositivos (próximo)
- ✅ Gestión de tareas (próximo)
- ✅ Integración con calendarios externos
- ✅ Análisis de patrones de horarios
- ✅ Sugerencias de optimización de tiempo

---

## 🐛 Solución de Problemas

### "Azul no reconoce mi evento"
- Usa frases más claras: "Tengo cita mañana a las 3pm"
- Especifica la hora claramente
- Usa palabras clave: "cita", "alarma", "recordatorio"

### "No recibo notificaciones"
- Verifica que el monitor esté activo (se inicia automáticamente)
- Revisa que el evento esté en el futuro
- Chequea `data/calendario.json` para ver si se guardó

### "Azul no entiende 'pasado mañana'"
- El analizador aprende con el uso
- Prueba con: "dentro de 2 días a las..."

---

## 📝 Notas de Desarrollo

### Principio de Desarrollo:
> **"No modificar lo que funciona mientras construimos nuevo"**

- El código base de jarvis_funcional.py se mantiene intacto
- Nuevas funcionalidades se agregan de forma modular
- Los módulos son independientes y reutilizables

### Tecnologías Usadas:
- 🤖 **Llama3**: IA local para interpretación
- 🐍 **Python**: Lenguaje base
- 💾 **JSON**: Persistencia de datos
- 🗄️ **Supabase**: Historial y perfil (existente)
- 🎤 **Speech Recognition**: Voz (existente)

---

## 👨‍💻 Próximos Pasos

1. ✅ **Completado**: Sistema de calendario modular
2. 🔄 **Siguiente**: Control de dispositivos inteligentes
3. 📋 **Siguiente**: Gestión de tareas con prioridades
4. 🔗 **Siguiente**: Integración con Google Calendar

---

## 📞 Soporte

Si encuentras algún problema o quieres agregar más funcionalidades, el sistema modular hace que sea fácil extender Azul sin romper lo existente.

**Recuerda**: Cada módulo es independiente y se puede mejorar sin afectar el resto del sistema.

---

*Azul v3.0 - Inteligencia Adaptativa con Memoria y Calendario*
