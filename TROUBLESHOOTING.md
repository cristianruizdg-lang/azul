# 🔧 Guía de Solución de Problemas - Azul

## 🐛 Problemas Comunes y Soluciones

### 1. "Azul dice que anotó el evento pero no lo hizo"

#### Síntomas:
- Azul responde: "¡Listo! He anotado..."
- NO aparece mensaje en consola: "✅ Evento creado..."
- NO hay notificaciones

#### Causas Posibles:
1. **La IA no interpretó correctamente el comando**
2. **La fecha/hora no se procesó bien**
3. **Llama3 está tardando mucho**

#### Solución:
1. **Revisa la consola** cuando envíes el comando
2. **Busca estos mensajes:**
   ```
   🔍 Detectando comando de calendario: [tu texto]
   🤖 Respuesta de IA: [JSON]
   📋 Datos extraídos: [datos]
   📅 Fecha/hora procesada: [fecha]
   ✅ Evento creado exitosamente:
   ```

3. **Si NO ves estos mensajes:**
   - Llama3 no está respondiendo
   - Verifica: `ollama list` en terminal
   - Reinicia Ollama: `ollama serve`

4. **Si ves error en procesamiento de fecha:**
   - Usa formato más claro: "hoy a las 3pm" en vez de "orita a las 3"
   - Especifica AM/PM claramente

---

### 2. Expresiones de Tiempo que Funcionan

#### ✅ FUNCIONAN BIEN:
- "**hoy a las 3pm**" 
- "**mañana a las 10am**"
- "**en 2 horas**"
- "**en 30 minutos**"
- "**orita a las 1:30pm**" (ahora con mejora)
- "**ahorita a las 5pm**"

#### ⚠️ PUEDEN FALLAR:
- "esta tarde" (no especifica hora)
- "al rato" (muy ambiguo)
- "luego" (no hay tiempo específico)

#### 💡 MEJOR PRÁCTICA:
Siempre especifica:
1. **Cuándo**: hoy, mañana, en X horas
2. **Hora exacta**: "a las 3pm", "a las 15:00"

---

### 3. Verificar si el Evento se Creó

#### Método 1: Revisar Consola
Cuando envías un comando, debes ver:
```
🔍 Detectando comando de calendario: oye recuerdame que voy a jugar...
🤖 Respuesta de IA: {"tiene_evento": true, ...}
📋 Datos extraídos: {...}
📅 Fecha/hora procesada: 2026-01-25 13:30:00
✅ Evento creado exitosamente:
   ID: evt_1234567890
   Título: Jugar Rocket League con amigos
   Fecha/Hora: 2026-01-25 13:30:00
   Tipo: recordatorio
```

#### Método 2: Revisar Archivo JSON
```bash
type data\calendario.json
```

Debes ver tu evento ahí.

#### Método 3: Preguntarle a Azul
```
"¿Qué tengo hoy?"
"¿Cuáles son mis recordatorios?"
```

---

### 4. Las Notificaciones No Llegan

#### Verificar:
1. **El evento está en el futuro**
   - Si programaste "hoy a las 1:30pm" y ya son las 2pm, no habrá notificación
   - Solución: Programa para más adelante o mañana

2. **El monitor está activo**
   - Debería iniciarse automáticamente
   - Verifica en consola: NO debe haber errores al inicio

3. **La hora es correcta**
   - Revisa `data\calendario.json`
   - La hora debe estar en formato 24h
   - Ejemplo: 13:30 para 1:30pm

4. **Notificaciones programadas**
   - Por defecto: 30, 10, 5 minutos antes
   - Si faltan menos de 5 minutos, puede que no llegue notificación

---

### 5. Debugging Paso a Paso

#### Prueba Manual:

1. **Ejecuta Azul**
   ```bash
   python jarvis_funcional.py
   ```

2. **Escribe comando SIMPLE**
   ```
   "recordar llamar a Juan en 5 minutos"
   ```

3. **Observa la consola**
   - Debe aparecer: "🔍 Detectando comando..."
   - Debe aparecer: "✅ Evento creado..."

4. **Espera 4 minutos**
   - En la consola debe aparecer la notificación

5. **Si NO funciona:**
   ```bash
   # Verifica Ollama
   ollama list
   
   # Prueba Llama3 directamente
   ollama run llama3 "Hola, ¿funcionas?"
   ```

---

### 6. Comando No Se Detecta Como Calendario

#### Si escribes "recordar..." pero NO se detecta:

1. **Palabras clave que activan el sistema:**
   - cita
   - alarma
   - recordatorio
   - recordar
   - agendar
   - mañana
   - hoy
   - agenda
   - orita
   - ahorita

2. **Si usas otras palabras:**
   - "avísame" ❌ (no detecta)
   - "recuérdame" ✅ (detecta)
   - "no olvides" ❌ (no detecta)

3. **Solución:**
   Usa las palabras clave específicas

---

### 7. Error: "Could not connect to Ollama"

```
Error interpretando comando: Could not connect to Ollama
```

#### Solución:
```bash
# Inicia Ollama
ollama serve

# En otra terminal, verifica
ollama list

# Si no está Llama3
ollama pull llama3
```

---

### 8. Azul Tarda Mucho en Responder

#### Si tarda más de 30 segundos:

1. **Llama3 está procesando** (normal en PCs lentas)
2. **Primera ejecución** siempre es más lenta
3. **Modelo muy grande** para tu hardware

#### Solución:
```python
# En modules/analizador_calendario.py
# Cambia la línea:
self.modelo = modelo

# Por:
self.modelo = 'llama2'  # Más rápido, menos preciso
```

---

### 9. Evento se Crea para Mañana en vez de Hoy

#### Si dices "hoy a las 3pm" pero se crea para mañana:

**Causa:** La hora ya pasó

**Lógica actual:**
- Si dices "hoy a las 1:30pm" y ya son las 2pm
- El sistema lo programa para mañana a las 1:30pm
- (Para evitar eventos en el pasado)

**Solución:**
- Especifica "en X minutos" si es inmediato
- O programa para mañana explícitamente

---

### 10. Formato de Hora Incorrecto

#### Ejemplos CORRECTOS:
- "a las 3pm" → 15:00 ✅
- "a las 3:30pm" → 15:30 ✅
- "a las 9am" → 09:00 ✅
- "a las 15:30" → 15:30 ✅

#### Ejemplos INCORRECTOS:
- "a las 3" (¿AM o PM?) ❌
- "tipo 3ish" (muy ambiguo) ❌
- "por la tarde" (no específico) ❌

---

## 🧪 Test Rápido para Verificar Funcionamiento

### Test 1: Evento Simple
```
Comando: "recordar comprar pan en 5 minutos"
Esperar: Mensaje en consola "✅ Evento creado..."
Esperar: En ~4 minutos, notificación por voz
```

### Test 2: Evento con Hora Específica
```bash
# Verifica la hora actual
python -c "from datetime import datetime; print(datetime.now())"

# Programa evento en 10 minutos
# Por ejemplo si son las 14:30, di:
"recordar algo importante hoy a las 2:40pm"

# Verifica en consola
# Verifica en JSON:
type data\calendario.json
```

### Test 3: Consultar Eventos
```
"¿Qué tengo programado?"
"¿Cuáles son mis recordatorios?"
```

---

## 📊 Logs para Reportar Problemas

Si nada funciona, copia estos logs:

1. **Salida de consola completa**
2. **Contenido de data/calendario.json**
3. **Versión de Ollama**: `ollama --version`
4. **Modelos instalados**: `ollama list`
5. **Tu comando exacto**
6. **Hora actual cuando lo enviaste**

---

## ✅ Checklist de Verificación

Antes de reportar un problema:

- [ ] Ollama está corriendo (`ollama list`)
- [ ] Llama3 está instalado
- [ ] Azul se ejecuta sin errores iniciales
- [ ] Usaste una palabra clave (recordar, cita, etc.)
- [ ] Especificaste hora exacta (3pm, 15:30)
- [ ] El evento NO está en el pasado
- [ ] Revisaste la consola por mensajes
- [ ] Revisaste `data/calendario.json`
- [ ] Esperaste el tiempo suficiente para notificación

---

## 🆘 Solución de Emergencia

Si nada funciona, resetea:

```bash
# 1. Cierra Azul
# 2. Borra el calendario
del data\calendario.json

# 3. Reinicia Ollama
# En una terminal:
ollama serve

# 4. Prueba Llama3
ollama run llama3 "responde con un json: {\"test\": true}"

# 5. Ejecuta Azul de nuevo
python jarvis_funcional.py

# 6. Prueba comando simple
"recordar algo en 10 minutos"
```

---

## 📞 Mejoras Aplicadas (v3.1)

### ✅ Detecta más expresiones:
- "orita" / "ahorita" ahora funcionan
- Mejor manejo de "hoy a las X"
- Previene eventos en el pasado

### ✅ Mejor logging:
- Mensajes detallados en consola
- Fácil identificar qué falló
- Tracing completo del proceso

### ✅ Validación mejorada:
- Azul solo confirma si el evento realmente se creó
- Mensaje [EVENTO CREADO] en el sistema
- Detalles específicos en la confirmación

---

*Si sigues teniendo problemas después de revisar esta guía, verifica la consola y el archivo JSON.*
