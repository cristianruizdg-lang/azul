# ✅ Checklist de Verificación - Azul v3.0

## Pre-vuelo: Verificar antes de despegar

### 📋 Requisitos del Sistema

- [ ] Python 3.8+ instalado
  ```bash
  python --version
  ```

- [ ] Ollama instalado
  ```bash
  ollama --version
  ```

- [ ] Llama3 descargado
  ```bash
  ollama list
  # Debe aparecer llama3 en la lista
  ```

- [ ] Librerías Python instaladas
  ```bash
  pip list | findstr "ollama pyttsx3 customtkinter"
  ```

---

## 🏗️ Verificar Estructura de Archivos

### Archivos Principales

- [ ] `jarvis_funcional.py` existe
- [ ] `modules/` directorio existe
- [ ] `modules/__init__.py` existe
- [ ] `modules/calendario.py` existe
- [ ] `modules/analizador_calendario.py` existe
- [ ] `data/` directorio existe

### Archivos de Documentación

- [ ] `README.md`
- [ ] `INICIO_RAPIDO.md`
- [ ] `README_CALENDARIO.md`
- [ ] `EJEMPLOS_USO.md`
- [ ] `ESTRUCTURA.md`
- [ ] `test_calendario.py`
- [ ] `config_calendario.py`

---

## 🧪 Pruebas Básicas

### Prueba 1: Importar Módulos

```bash
python -c "from modules import GestorCalendario; print('✅ Imports OK')"
```

- [ ] No hay errores de importación

### Prueba 2: Crear Evento de Prueba

```bash
python -c "
from modules import GestorCalendario
from datetime import datetime, timedelta
g = GestorCalendario('data/test.json')
e = g.agregar_evento('Test', datetime.now() + timedelta(hours=1))
print(f'✅ Evento creado: {e.titulo}')
"
```

- [ ] Se crea el evento sin errores
- [ ] Se genera `data/test.json`

### Prueba 3: Ejecutar Test Suite

```bash
python test_calendario.py
```

- [ ] El menú se muestra correctamente
- [ ] Opción 1 funciona (crear eventos)
- [ ] No hay errores en la ejecución

### Prueba 4: Ejecutar Azul

```bash
python jarvis_funcional.py
```

- [ ] La ventana se abre
- [ ] La esfera azul se anima
- [ ] El campo de texto está visible
- [ ] No hay errores en la consola

---

## 🎯 Pruebas Funcionales

### Test de Entrada de Texto

1. Ejecuta Azul
2. Escribe en el chat: "Hola Azul"
3. Presiona Enter

- [ ] Azul responde
- [ ] La esfera cambia de color al hablar
- [ ] El audio se reproduce

### Test de Calendario - Texto

1. En el chat, escribe: "Tengo reunión mañana a las 10am"
2. Espera la respuesta

- [ ] Azul confirma que anotó el evento
- [ ] Se crea/actualiza `data/calendario.json`
- [ ] No hay errores en consola

### Test de Calendario - Consulta

1. Escribe: "¿Qué tengo mañana?"

- [ ] Azul menciona la reunión de las 10am
- [ ] La respuesta es coherente

### Test de Voz (si tienes micrófono)

1. Di claramente: "Azul"
2. Espera que se active
3. Di: "Tengo dentista en 2 horas"

- [ ] Azul reconoce la activación
- [ ] Interpreta el comando
- [ ] Crea el evento

---

## 🔔 Prueba de Notificaciones

### Test Rápido (5 minutos)

1. Ejecuta este código:
```bash
python -c "
from modules import GestorCalendario
from datetime import datetime, timedelta

g = GestorCalendario('data/test_notif.json')

# Crear evento en 2 minutos
e = g.agregar_evento(
    'Prueba de notificación',
    datetime.now() + timedelta(minutes=2),
    tipo='alarma',
    notificaciones=[1, 0.5]  # 1 min y 30 seg antes
)

def callback(evt, mins):
    print(f'🔔 NOTIFICACIÓN: {evt.titulo} en {mins} minutos')

g.registrar_callback_notificacion(callback)
g.iniciar_monitor()

print(f'✅ Evento creado para {e.fecha_hora.strftime(\"%H:%M:%S\")}')
print('⏳ Esperando notificaciones... (Ctrl+C para salir)')

import time
while True:
    time.sleep(1)
"
```

- [ ] El evento se crea
- [ ] Después de ~1 minuto aparece notificación
- [ ] Después de ~1.5 minutos aparece otra notificación

---

## 🧠 Prueba de IA (Llama3)

### Test de Interpretación

```bash
python -c "
from modules import AnalizadorCalendario

a = AnalizadorCalendario('llama3')
resultado = a.interpretar_comando('Tengo cita con el doctor mañana a las 3pm')

if resultado.get('valido'):
    print('✅ IA funciona')
    print(f'   Tipo: {resultado[\"tipo\"]}')
    print(f'   Título: {resultado[\"titulo\"]}')
else:
    print('❌ IA no interpretó correctamente')
"
```

- [ ] Llama3 responde
- [ ] La interpretación es correcta
- [ ] No hay errores

**Nota**: Esta prueba puede tardar 10-30 segundos según tu hardware.

---

## 📊 Verificar Datos

### Revisar Archivo de Calendario

```bash
type data\calendario.json
```

- [ ] El archivo existe
- [ ] Contiene JSON válido
- [ ] Los eventos están correctamente formateados

### Ejemplo de Estructura Correcta:

```json
[
  {
    "id": "evt_1234567890",
    "titulo": "Reunión",
    "fecha_hora": "2026-01-26T10:00:00",
    "tipo": "cita",
    "descripcion": "",
    "notificaciones": [30, 10, 5],
    "notificaciones_enviadas": [],
    "completado": false,
    "creado_en": "2026-01-25T15:00:00"
  }
]
```

---

## 🎨 Verificar Interfaz Gráfica

### Al Ejecutar Azul

- [ ] Ventana 900x750 se abre
- [ ] Título: "AZUL v2.5 - Adaptive Intelligence"
- [ ] Botón "📜 Historial" visible
- [ ] Canvas con esfera azul visible
- [ ] Canvas de espectro (barras) visible
- [ ] Campo de texto con placeholder visible
- [ ] Tema oscuro aplicado

### Durante Uso

- [ ] Esfera rota suavemente
- [ ] Al hablar, esfera se hace más grande y color cyan
- [ ] Espectro reacciona a sonido del micrófono
- [ ] Texto se puede escribir en el campo

---

## 🔊 Verificar Sistema de Voz

### Síntesis de Voz (Azul habla)

1. Escribe en el chat: "Hola"
2. Espera respuesta

- [ ] Se escucha la voz
- [ ] La voz está en español
- [ ] La velocidad es natural (~185 wpm)
- [ ] El volumen es adecuado

### Reconocimiento de Voz (Tú hablas)

1. Di: "Azul"
2. Observa si se activa

- [ ] El micrófono detecta la palabra
- [ ] El espectro reacciona
- [ ] Azul se activa

**Troubleshooting**:
- Si no funciona, verifica los permisos del micrófono
- Habla más fuerte o más cerca del mic
- Reduce el ruido de fondo

---

## 🔗 Verificar Integración

### Azul + Calendario

1. Ejecuta Azul
2. Escribe: "Tengo cita en 1 hora"
3. Después escribe: "¿Qué tengo?"

- [ ] Primer mensaje crea el evento
- [ ] Segundo mensaje lista el evento
- [ ] Azul menciona la cita correctamente

### Aprendizaje + Calendario

1. Conversa con Azul y menciona algo personal
   - "Sabes, yo siempre llego tarde"
2. Luego crea un evento
   - "Tengo reunión importante mañana"
3. Al día siguiente (o simula), revisa la notificación

- [ ] Azul recuerda tu tendencia a llegar tarde
- [ ] La notificación incluye ese contexto
- [ ] El mensaje es personalizado

---

## 🚨 Checklist de Errores Comunes

### Error: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'modules'
```

**Solución**:
- [ ] Verifica que estás en la carpeta correcta
- [ ] Verifica que `modules/__init__.py` existe

### Error: Ollama no responde

```
Error: Could not connect to Ollama
```

**Solución**:
- [ ] Ollama está corriendo: `ollama list`
- [ ] Llama3 está instalado: `ollama pull llama3`

### Error: No se crea calendario.json

**Solución**:
- [ ] La carpeta `data/` existe
- [ ] Tienes permisos de escritura
- [ ] No hay errores de sintaxis en JSON

### Error: Voz no funciona

**Solución**:
- [ ] pyttsx3 instalado: `pip install pyttsx3`
- [ ] Drivers de audio funcionando
- [ ] Volumen del sistema no está en mute

---

## ✅ Checklist Final

### Antes de Usar en Producción

- [ ] Todas las pruebas básicas pasan
- [ ] Prueba de notificación funciona
- [ ] IA de Llama3 responde correctamente
- [ ] Voz funciona (síntesis y reconocimiento)
- [ ] Datos se guardan correctamente
- [ ] No hay errores en consola
- [ ] Interfaz se ve correctamente

### Configuración Personalizada

- [ ] Editado `config_calendario.py` si es necesario
- [ ] Ajustados tiempos de notificación
- [ ] Configurado nivel de formalidad
- [ ] Definido nombre de usuario

### Documentación Leída

- [ ] Leído `README.md`
- [ ] Revisado `INICIO_RAPIDO.md`
- [ ] Consultado `EJEMPLOS_USO.md`
- [ ] Entendido `ESTRUCTURA.md`

---

## 🎉 ¡Todo Listo!

Si todos los checks anteriores están ✅, entonces:

### 🚀 Azul v3.0 está 100% funcional

Puedes:
1. Usar Azul como tu asistente personal diario
2. Crear eventos y recibir notificaciones
3. Conversar y que Azul aprenda de ti
4. Agregar nuevas funcionalidades al sistema modular

---

## 📝 Reporte de Estado

Completa esto después de las pruebas:

```
Fecha: ___/___/______
Estado General: [ ] ✅ Todo funciona  [ ] ⚠️ Algunos problemas  [ ] ❌ No funciona

Pruebas que pasaron:  ___ / 30
Pruebas que fallaron: ___ / 30

Problemas encontrados:
1. ________________________________
2. ________________________________
3. ________________________________

Notas adicionales:
________________________________________
________________________________________
________________________________________
```

---

## 🆘 Si Algo No Funciona

1. **Revisa la consola** para ver el error específico
2. **Consulta la documentación** correspondiente
3. **Verifica requisitos** del sistema
4. **Prueba cada módulo** por separado con `test_calendario.py`

---

## 📞 Próximos Pasos

Una vez que todo funcione:

1. **Usa Azul diariamente** para ver cómo aprende
2. **Prueba diferentes tipos** de eventos
3. **Experimenta con voz** para mejor interacción
4. **Personaliza** en `config_calendario.py`
5. **Piensa en nuevas funcionalidades** para agregar

---

*Checklist completado = Azul lista para usar* ✨

**¡Disfruta tu asistente personal!** 🤖
