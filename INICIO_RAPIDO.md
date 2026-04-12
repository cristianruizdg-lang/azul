# 🚀 Inicio Rápido - Azul v3.0

## ¿Qué hay de nuevo?

Azul ahora puede gestionar tu calendario con inteligencia artificial. Crea citas, alarmas y recordatorios usando lenguaje natural, y recibe notificaciones personalizadas basadas en tu perfil.

---

## 📋 Instalación Rápida

### Requisitos
- Python 3.8+
- Ollama con Llama3 instalado
- Librerías existentes de Azul

### No se requieren instalaciones adicionales
Todos los módulos usan las librerías que ya tienes instaladas.

---

## ▶️ Ejecutar Azul

```bash
python jarvis_funcional.py
```

---

## 🎯 Ejemplos de Uso

### Crear Eventos

**Por Voz:**
```
Tú: "Azul"
Azul: [se activa]
Tú: "Tengo dentista mañana a las 4pm"
Azul: "Perfecto, he anotado tu cita con el dentista para mañana a las 4pm"
```

**Por Texto:**
Escribe en el chat:
- "Recuérdame comprar leche en 2 horas"
- "Alarma para las 7am mañana"
- "Agenda reunión con Juan el lunes a las 10am"

### Consultar Eventos

Pregunta a Azul:
- "¿Qué tengo hoy?"
- "¿Cuáles son mis citas de mañana?"
- "¿Tengo algo programado?"

---

## 🔔 Notificaciones Automáticas

Azul te notificará:
- ⏰ **30 minutos antes** del evento
- ⏰ **10 minutos antes** del evento
- ⏰ **5 minutos antes** del evento

Las notificaciones son personalizadas según tu perfil:
- Si tardas en alistarte, te lo recordará con tiempo
- Si eres puntual, será más directa
- Se adapta a tu humor (serio, gracioso, etc.)

---

## 🧪 Probar la Funcionalidad

Si quieres probar el sistema de calendario sin ejecutar toda la interfaz:

```bash
python test_calendario.py
```

Esto te permitirá:
1. Crear eventos de prueba
2. Ver cómo funciona el analizador
3. Probar notificaciones
4. Monitorear eventos en tiempo real

---

## 📁 Archivos Importantes

| Archivo | Descripción |
|---------|-------------|
| `jarvis_funcional.py` | Cerebro principal (sin cambios en lo que funciona) |
| `modules/calendario.py` | Gestión de eventos y calendario |
| `modules/analizador_calendario.py` | IA para interpretar comandos |
| `data/calendario.json` | Tus eventos guardados |
| `test_calendario.py` | Script de pruebas |
| `README_CALENDARIO.md` | Documentación completa |

---

## 🐛 Solución Rápida de Problemas

### Error al importar módulos
```bash
# Verifica que estés en la carpeta correcta
cd "C:\Users\Chich\OneDrive\Desktop\Proyectos P\jarvis_vista"
```

### Azul no reconoce eventos
- Usa palabras clave: "cita", "alarma", "recordatorio"
- Especifica la hora claramente: "a las 3pm" en vez de "por la tarde"
- Menciona el día: "mañana", "hoy", "pasado mañana"

### No recibo notificaciones
- El monitor se inicia automáticamente al abrir Azul
- Verifica que el evento esté en el futuro
- Revisa `data/calendario.json` para confirmar que se guardó

---

## 🎨 Personalización

### Cambiar tiempos de notificación

Al crear un evento programáticamente:
```python
gestor.agregar_evento(
    titulo="Mi cita",
    fecha_hora=datetime.now() + timedelta(hours=2),
    notificaciones=[60, 30, 15]  # 60, 30 y 15 minutos antes
)
```

### Adaptar el tono de Azul

El sistema lee tu perfil desde Supabase. Cuanto más converses con Azul:
- Aprende tu humor
- Se adapta a tu forma de ser
- Personaliza las notificaciones

---

## ✅ Verificar que Todo Funciona

1. **Ejecuta Azul**: `python jarvis_funcional.py`
2. **Di o escribe**: "Tengo reunión en 1 hora"
3. **Verifica**: 
   - Azul debería confirmar
   - Se crea `data/calendario.json`
   - En ~1 hora recibirás notificaciones

---

## 📞 Próximos Pasos

Una vez que pruebes el calendario, podemos agregar:
- ✅ Control de dispositivos
- ✅ Gestión de tareas con prioridades
- ✅ Análisis de productividad
- ✅ Integración con Google Calendar
- ✅ Recordatorios recurrentes

---

## 💡 Consejos

1. **Sé específico con las horas**: "3pm" mejor que "tarde"
2. **Usa días relativos**: "mañana", "pasado mañana" funciona bien
3. **Perfiles importan**: Si mencionas que tardas en alistarte, Azul lo usará
4. **Conversa natural**: No necesitas comandos especiales

---

## 🎓 Arquitectura

```
Usuario habla/escribe
    ↓
jarvis_funcional.py detecta palabras clave
    ↓
analizador_calendario.py interpreta con Llama3
    ↓
calendario.py crea y guarda el evento
    ↓
Monitor revisa eventos cada 30 segundos
    ↓
Cuando es tiempo, genera notificación inteligente
    ↓
Azul te habla el recordatorio personalizado
```

**Principio**: Todo es modular. Cada pieza funciona independiente.

---

*¿Listo? Ejecuta `python jarvis_funcional.py` y empieza a usar tu nuevo calendario inteligente!* 🚀
