# 📝 Sistema de Gestión de Tareas - Azul

## ✨ Nueva Funcionalidad: Interfaz Minimalista de Tareas

### 🎯 Características Principales

**1. Interfaz Visual Elegante**
- Diseño minimalista y limpio
- Colores consistentes con Azul (#00d4ff)
- Ventana organizada y fácil de usar

**2. Agregar Tareas**
- ✍️ Título descriptivo
- 📅 Fecha (formato DD/MM/AAAA)
- ⏰ Hora (formato HH:MM)
- 🔔 Recordatorios configurables:
  * 30 minutos antes
  * 10 minutos antes
  * 5 minutos antes
  * En el momento exacto

**3. Gestión de Tareas**
- 📋 Lista visual de todas las tareas pendientes
- ⏳ Tiempo restante en tiempo real
- 🗑️ Eliminar tareas fácilmente
- 📊 Ordenadas por fecha/hora

**4. Sistema de Notificaciones**
- 🔊 Azul te avisa por voz
- 🖥️ Notificaciones de Windows
- 📢 Recordatorios inteligentes según tu perfil
- ⏰ Múltiples alertas antes del evento

---

## 🚀 Cómo Usar

### Abrir Gestión de Tareas
1. Haz clic en el botón **"📝 Tareas"** (arriba a la izquierda)
2. Se abrirá la ventana de gestión

### Agregar Nueva Tarea
1. Escribe el título (ej: "Comprar leche")
2. Selecciona o edita la fecha
3. Escribe la hora (ej: "15:30")
4. Marca los recordatorios que deseas
5. Haz clic en "➕ Agregar Tarea"

### Ver Tareas Pendientes
- Todas tus tareas aparecen en la lista inferior
- Muestra:
  * 📌 Título
  * 🕒 Fecha y hora exacta
  * ⏳ Tiempo restante

### Eliminar Tarea
- Haz clic en el botón 🗑️ junto a la tarea

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Tarea Simple
```
Título: Llamar a mamá
Fecha: 08/04/2026
Hora: 18:00
Recordatorios: ✅ 30 min, ✅ 10 min, ✅ Momento exacto
```
→ Azul te avisará 30 min antes, 10 min antes y en el momento exacto

### Ejemplo 2: Tarea Urgente
```
Título: Reunión con cliente
Fecha: 07/04/2026
Hora: 20:30
Recordatorios: ✅ 10 min, ✅ 5 min, ✅ Momento exacto
```
→ Recordatorios solo 10 y 5 min antes (para no molestar con antelación)

### Ejemplo 3: Tarea Futura
```
Título: Pagar servicios
Fecha: 15/04/2026
Hora: 09:00
Recordatorios: ✅ 30 min, ✅ Momento exacto
```
→ Azul recordará con 30 min de anticipación

---

## 🎨 Características de Diseño

- **Minimalista**: Sin elementos innecesarios
- **Oscuro**: Consistente con la interfaz de Azul
- **Responsive**: Se adapta al contenido
- **Scrollable**: Lista de tareas con scroll automático
- **Colores**:
  * Azul (#00d4ff): Acciones principales
  * Rojo (#ff4444): Eliminar
  * Gris: Información secundaria

---

## 🔗 Integración con Azul

### Voz + Interfaz Visual
Azul sigue aceptando comandos de voz:
- "Recuérdame comprar leche a las 3pm"
- "Tengo tareas para hoy?"

**NUEVO**: Ahora puedes gestionar visualmente:
- Ver todas las tareas de un vistazo
- Agregar tareas con precisión
- Personalizar recordatorios
- Eliminar fácilmente

### Sistema Unificado
- Las tareas creadas en la interfaz = eventos de calendario
- Aparecen en consultas por voz
- Mismo sistema de notificaciones
- Persistencia en base de datos (data/calendario.json)

---

## 📊 Estado del Sistema

✅ Interfaz minimalista completada
✅ Formulario de nueva tarea funcional
✅ Lista de tareas pendientes
✅ Sistema de recordatorios configurables
✅ Integración con calendario existente
✅ Notificaciones por voz + Windows
✅ Eliminación de tareas
✅ Persistencia en JSON

---

## 🎯 Próximas Mejoras (Opcionales)

- [ ] Editar tareas existentes
- [ ] Categorías de tareas (trabajo, personal, etc.)
- [ ] Estadísticas (tareas completadas, pendientes)
- [ ] Filtros (hoy, semana, mes)
- [ ] Exportar/Importar tareas
- [ ] Tareas recurrentes

---

## 💬 Comandos de Voz Relacionados

```
"Muestra mis tareas"         → Abre la ventana de tareas
"Tengo tareas hoy?"           → Lista tareas del día
"Recuérdame [tarea] [hora]"   → Crea tarea por voz
"Qué tengo pendiente?"        → Consulta tareas próximas
```

---

**✨ ¡Disfruta gestionando tus tareas con Azul!**
