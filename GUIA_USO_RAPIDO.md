# 🚀 Guía de Uso Rápido - Calendario de Azul

## 💬 Cómo Pedirle a Azul que Agende o Recuerde

Azul detecta automáticamente cuando le pides que agende algo o te recuerde algo.

---

## ✅ Formas de Pedir Eventos

### 🗓️ **Agendar Citas:**

```
"Azul, agéndame cita con el doctor mañana a las 3pm"
"Tengo reunión hoy a las 5pm"
"Agenda dentista para mañana a las 10am"
```

### 📝 **Crear Recordatorios:**

```
"Azul, recuérdame comprar leche en 2 horas"
"Recuérdame llamar a mamá hoy a las 8pm"
"Oye, recuérdame que voy a jugar con mis amigos orita a las 3:30pm"
```

### ⏰ **Poner Alarmas:**

```
"Azul, alarma para las 7am mañana"
"Pon alarma para las 6:30am"
"Alarma en 30 minutos"
```

---

## 🎯 Lo Que Azul Detecta Automáticamente

### Palabras Clave:
- **"recuérdame"** / **"recordar"** → Crea recordatorio
- **"cita"** / **"reunión"** → Crea cita
- **"alarma"** → Crea alarma
- **"agenda"** / **"agendar"** → Crea evento

### Tiempo:
- **"hoy"** / **"orita"** / **"ahorita"** → Hoy
- **"mañana"** → Mañana
- **"en X horas"** / **"en X minutos"** → Tiempo desde ahora

### Hora:
- **"3pm"** / **"15:00"** → Hora específica
- **"3:30pm"** / **"15:30"** → Hora con minutos

---

## 💡 Ejemplos Completos

### Ejemplo 1: Recordatorio Simple
```
Tú: "Azul, recuérdame comprar pan en 1 hora"

[Azul detecta → Crea evento]

Azul: "¡Listo! Te recordaré comprar pan en 1 hora. Te avisaré antes."

[60 minutos después]
Azul: "¡Hey! Es hora de comprar pan."
```

### Ejemplo 2: Cita Programada
```
Tú: "Azul, tengo dentista mañana a las 4pm"

[Azul detecta → Crea evento]

Azul: "Perfecto, te he agendado dentista para mañana a las 4:00 PM. 
       Te recordaré 30, 10 y 5 minutos antes, y en el momento exacto."

[Mañana a las 3:30pm]
Azul: "Cristian, en 30 minutos tienes dentista. ¿Ya estás listo?"

[Mañana a las 3:50pm]
Azul: "Dentista en 10 minutos. Mejor ve saliendo."

[Mañana a las 3:55pm]
Azul: "¡5 minutos para el dentista!"

[Mañana a las 4:00pm - MOMENTO EXACTO]
Azul: "¡ES HORA! ¡Tu cita con el dentista es AHORA!"
```

### Ejemplo 3: Alarma Matutina
```
Tú: "Azul, alarma para las 7am mañana"

[Azul detecta → Crea evento]

Azul: "Alarma configurada para mañana a las 7:00 AM. ¡Que duermas bien!"

[Mañana a las 6:55am]
Azul: "5 minutos para tu alarma. Prepárate para levantarte."

[Mañana a las 7:00am - MOMENTO EXACTO]
Azul: "¡DESPIERTA! ¡Son las 7:00 AM! ¡Es hora de levantarse!"
```

### Ejemplo 4: Evento Hoy (Expresión Mexicana)
```
Tú: "Oye Azul, recuérdame que voy a jugar con mis amigos orita a las 3:30pm"

[Azul detecta → Crea evento]

Azul: "¡Listo! Te recordaré que vas a jugar con tus amigos hoy a las 3:30 PM.
       Te avisaré antes para que no se te olvide."

[Hoy a las 3:00pm]
Azul: "En 30 minutos vas a jugar con tus amigos. ¡No llegues tarde!"
```

---

## 🔔 Sistema de Notificaciones

### Notificaciones Automáticas (por defecto):
- ⏰ **30 minutos antes** → "En 30 minutos tienes..."
- ⏰ **10 minutos antes** → "En 10 minutos..."
- ⏰ **5 minutos antes** → "¡En 5 minutos!"
- 🔥 **Momento exacto (0 min)** → "¡ES HORA! ¡AHORA!"

### Notificaciones Personalizadas:
Azul adapta el mensaje según:
- Tu personalidad (seria, graciosa, etc.)
- Tus hábitos (si tardas en alistarte, te avisa antes)
- El tipo de evento (urgente, importante, casual)

---

## 📊 Consultar tus Eventos

```
"Azul, ¿qué tengo hoy?"
"¿Cuáles son mis citas de mañana?"
"¿Tengo algo programado?"
"¿Qué eventos tengo?"
```

Azul te dirá todos tus eventos próximos.

---

## ✨ Consejos para Mejores Resultados

### ✅ SÍ Funciona Bien:
```
✅ "recuérdame X hoy a las 3pm"
✅ "cita con Y mañana a las 10am"
✅ "alarma en 30 minutos"
✅ "agenda reunión para las 5pm hoy"
```

### ⚠️ Requiere Ser Más Específico:
```
⚠️ "recuérdame algo" → ¿Qué y cuándo?
⚠️ "tengo cita" → ¿Cuándo exactamente?
⚠️ "alarma temprano" → ¿A qué hora?
```

### 💡 Mejor Práctica:
Siempre incluye:
1. **Qué**: comprar pan, cita doctor, etc.
2. **Cuándo**: hoy, mañana, en X horas
3. **Hora**: 3pm, 10am, 15:30

---

## 🎨 Personalización de Azul

Azul aprende de ti y personaliza las notificaciones:

### Si le dices:
```
"Sabes Azul, yo siempre llego tarde"
"Tardo mucho en alistarme"
"Soy muy olvidadizo"
```

### Azul lo recordará:
```
[Notificación personalizada]
"Cristian, son las 2pm. Tienes cita a las 6pm y tú sabes que 
tardas mucho en alistarte. Mejor empieza a prepararte ya."
```

---

## 🔍 Verificar que Funcionó

### En la Consola Verás:
```
🔍 Detectando comando de calendario: recuérdame comprar leche en 1 hora
✅ Análisis directo exitoso
   Tipo: recordatorio
   Título: comprar leche
   Fecha/Hora: 2026-01-25 15:30:00

✅ Evento creado exitosamente:
   ID: evt_1234567890
   Título: comprar leche
   Fecha/Hora: 2026-01-25 15:30:00
   Tipo: recordatorio
   Notificaciones programadas para: [30, 10, 5] minutos antes
```

### En el Archivo JSON:
```bash
type data\calendario.json
```

Debes ver tu evento guardado.

### Azul Confirmará:
```
"¡Listo! Te recordaré comprar leche en 1 hora. Te avisaré antes."
```

---

## 🆘 Si No Funciona

### 1. Azul No Detecta el Comando

**Problema:** Dices "recuérdame X" pero Azul no lo detecta

**Solución:**
- Usa palabras clave: "recuérdame", "cita", "alarma", "agenda"
- Especifica hora: "a las 3pm"
- Especifica cuándo: "hoy", "mañana", "en X horas"

### 2. Azul Dice que Anotó Pero No Hay Evento

**Problema:** Azul dice "¡Listo!" pero no se creó el evento

**Revisa la consola:**
- ¿Aparece "✅ Evento creado exitosamente"?
- Si NO aparece → El análisis falló
- Verifica que incluiste hora y tiempo

**Solución:**
```bash
# Prueba comando más explícito
"recordar comprar leche hoy a las 5pm"
```

### 3. No Llegan Notificaciones

**Problema:** Se creó el evento pero no notifica

**Verifica:**
1. El evento NO está en el pasado
2. data\calendario.json existe y tiene el evento
3. La hora del evento es correcta (formato 24h)

**Revisa:**
```bash
type data\calendario.json
```

---

## 📱 Uso por Voz vs Texto

### Por Voz:
```
1. Di: "Azul"
2. Espera que se active
3. Di: "recuérdame comprar pan en 2 horas"
4. Azul confirmará
```

### Por Texto:
```
1. Escribe en el chat: "recuérdame comprar pan en 2 horas"
2. Presiona Enter
3. Azul confirmará
```

**Ambos funcionan igual** 🎯

---

## 🎉 Casos de Uso Reales

### Trabajo:
```
"Azul, reunión con el equipo mañana a las 9am"
"Recordar enviar reporte hoy a las 5pm"
"Cita con cliente el lunes a las 2pm"
```

### Personal:
```
"Alarma para las 6:30am mañana"
"Recuérdame llamar a mamá hoy a las 8pm"
"Tengo dentista pasado mañana a las 3pm"
```

### Tareas:
```
"Recuérdame sacar la basura en 1 hora"
"Recordar regar las plantas mañana a las 7am"
"Recuérdame estudiar hoy a las 4pm"
```

### Social:
```
"Juego con amigos hoy a las 8pm"
"Cita con María mañana a las 6pm"
"Fiesta el sábado a las 9pm"
```

---

## 📈 Flujo Completo

```
Tú le pides a Azul
        ↓
Azul detecta palabras clave
        ↓
Analiza el comando (regex)
        ↓
Extrae: qué, cuándo, hora
        ↓
Crea evento en calendario
        ↓
Guarda en data/calendario.json
        ↓
Azul confirma "¡Listo! Te he agendado..."
        ↓
Monitor revisa cada 30 segundos
        ↓
Cuando es tiempo → Notifica
        ↓
Azul te habla el recordatorio
```

---

## 🎯 Resumen Rápido

| Acción | Comando | Resultado |
|--------|---------|-----------|
| Recordatorio | "recuérdame X en Y" | ✅ Crea y notifica |
| Cita | "cita/reunión con X mañana" | ✅ Crea y notifica |
| Alarma | "alarma para las Xam" | ✅ Crea y notifica |
| Consultar | "¿qué tengo hoy?" | 📋 Lista eventos |

---

## 💪 ¡Empieza a Usar Azul!

Simplemente dile:

```
"Azul, recuérdame [algo] [cuando] a las [hora]"
```

Y Azul se encargará del resto. 

**Es así de simple** ✨

---

*Azul v3.1 - Tu asistente que nunca olvida* 🤖
