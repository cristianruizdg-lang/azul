# 📱 FASE 5: APLICACIÓN MÓVIL ANDROID CON KIVY

**Estado**: ✅ EN DESARROLLO  
**Plataforma**: Android (Kivy/KivyMD)  
**Backend**: https://azul-4xsp.onrender.com  
**Objetivo**: App móvil funcional conectada al mismo backend cloud

---

## 🎯 RESUMEN

Creación de una aplicación móvil Android para Azul que:
- ✅ Se conecta al mismo backend en Render
- ✅ Comparte la misma memoria con la app desktop (Supabase)
- ✅ Interfaz moderna con Material Design (KivyMD)
- ✅ Grabación y reproducción de audio
- ✅ Chat conversacional con historial
- ✅ Sincronización en tiempo real

---

## 📁 ESTRUCTURA DE ARCHIVOS

```
jarvis_vista/
│
├── mobile/                          # Nueva carpeta para móvil
│   ├── azul_mobile.py              # App móvil principal
│   ├── requirements_mobile.txt      # Dependencias para móvil
│   ├── buildozer.spec              # Config para compilar APK
│   └── assets/                     # Recursos de la app
│       ├── icon.png                # Icono de la app (512x512)
│       └── splash.png              # Pantalla de carga
│
└── FASE_5_APP_MOVIL.md (este archivo)
```

---

## 🏗️ ARQUITECTURA

### Cliente-Servidor Cloud

```
┌─────────────────────────────────────────────┐
│  📱 APP MÓVIL ANDROID                       │
│  ├─ Kivy/KivyMD (Interfaz Material)        │
│  ├─ Grabación de audio                     │
│  ├─ Reproducción de audio                  │
│  ├─ Chat UI con historial                  │
│  └─ HTTP Client → Backend API              │
└─────────────────────────────────────────────┘
                    ↕️ HTTPS
┌─────────────────────────────────────────────┐
│  ☁️ BACKEND EN RENDER                      │
│  URL: https://azul-4xsp.onrender.com       │
│  ├─ FastAPI                                │
│  ├─ Groq API (llama-3.3-70b)              │
│  ├─ Supabase (memoria compartida)          │
│  └─ Edge TTS (síntesis de voz)            │
└─────────────────────────────────────────────┘
```

### Flujo de Comunicación

```
1. Usuario escribe/habla en app móvil
   ├─ Texto → POST /api/chat/message
   └─ Audio → POST /api/chat/voice

2. Backend procesa:
   ├─ STT (si es audio) → texto
   ├─ Groq IA → genera respuesta
   ├─ TTS → genera audio
   └─ Guarda en Supabase

3. App móvil recibe:
   ├─ Texto de respuesta
   ├─ URLs de audio
   └─ Metadata

4. App reproduce audio y muestra en chat
```

---

## 🚀 INSTALACIÓN Y USO

### Opción 1: Ejecutar en PC con Python (Testing)

```bash
# Navegar a carpeta mobile
cd mobile

# Instalar dependencias
pip install -r requirements_mobile.txt

# Ejecutar app (ventana simulada en PC)
python azul_mobile.py
```

### Opción 2: Compilar APK para Android

**Requisitos:**
- Linux o WSL2 (Windows Subsystem for Linux)
- Buildozer instalado

```bash
# En WSL2/Linux, instalar buildozer
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
pip3 install buildozer cython

# Navegar a carpeta mobile
cd mobile

# Primera compilación (puede tomar 30-60 min)
buildozer -v android debug

# El APK estará en:
mobile/bin/azulmobile-0.1-armeabi-v7a-debug.apk
```

### Opción 3: Instalar APK en Android

```bash
# Transferir APK al teléfono
adb install bin/azulmobile-0.1-armeabi-v7a-debug.apk

# O usar cable USB y copiar manualmente
# Habilitar "Instalar apps desconocidas" en Android
```

---

## 📱 CARACTERÍSTICAS DE LA APP

### Interfaz Principal
- **Tema oscuro** con colores azul/cyan (brand Azul)
- **Chat conversacional** con burbujas
- **Botón de voz** flotante (FAB - Floating Action Button)
- **Input de texto** en la parte inferior
- **Historial de conversación** sincronizado con desktop

### Funcionalidades
1. ✅ **Chat por texto**
   - Escribir mensaje
   - Enviar a backend
   - Mostrar respuesta

2. ✅ **Chat por voz**
   - Grabar audio al presionar botón
   - Enviar audio a backend
   - Reproducir respuesta de Azul

3. ✅ **Historial compartido**
   - Carga últimos 50 mensajes de Supabase
   - Misma conversación que en desktop
   - Scroll infinito

4. ✅ **Notificaciones**
   - Respuesta recibida
   - Estado de conexión

5. ✅ **Sincronización**
   - Memoria compartida
   - Perfil de usuario sincronizado
   - Contexto conversacional persistente

---

## 🔧 CONFIGURACIÓN

### Variables de Entorno

Editar `mobile/azul_mobile.py` línea ~15:

```python
API_URL = "https://azul-4xsp.onrender.com"  # Backend en Render
USER_ID = "default"  # ID de usuario (sincronizado con desktop)
```

### Permisos Android (buildozer.spec)

```ini
android.permissions = INTERNET, RECORD_AUDIO, WRITE_EXTERNAL_STORAGE
```

---

## 🎨 PERSONALIZACIÓN

### Cambiar Colores del Tema

Editar `azul_mobile.py`:

```python
self.theme_cls.primary_palette = "Blue"  # Azul, Cyan, Indigo, etc.
self.theme_cls.theme_style = "Dark"      # Dark o Light
```

### Cambiar Icono y Splash

Reemplazar archivos en `mobile/assets/`:
- `icon.png` - 512x512 px, PNG
- `splash.png` - 1920x1080 px, PNG

Rebuild APK con buildozer.

---

## 🧪 TESTING

### Probar Localmente

```bash
cd mobile
python azul_mobile.py
```

Ventana de Kivy se abrirá simulando un móvil.

### Logs en Android

```bash
# Ver logs de la app en tiempo real
adb logcat | grep python
```

---

## 🐛 TROUBLESHOOTING

### Error: "No module named 'kivymd'"

```bash
pip install kivymd
```

### Error: "Permission denied" en Android

Asegúrate de habilitar permisos en:
- Ajustes → Apps → Azul → Permisos → Micrófono ✅

### Backend no responde

1. Verifica que backend esté activo:
   ```bash
   curl https://azul-4xsp.onrender.com/health
   ```

2. Si está "dormido", espera 30 segundos (cold start de Render)

3. Configura UptimeRobot para evitar sleep

### Compilación APK falla

```bash
# Limpiar buildozer cache
buildozer android clean

# Intentar de nuevo
buildozer -v android debug
```

---

## 📊 COMPARACIÓN: DESKTOP VS MÓVIL

| Característica | Desktop (jarvis_cloud.py) | Móvil (azul_mobile.py) |
|---------------|--------------------------|------------------------|
| Framework UI | CustomTkinter | Kivy/KivyMD |
| Esfera 3D | ✅ Sí | ❌ No (más ligero) |
| Animaciones | ✅ Complejas | ✅ Material Design |
| Espectro Audio | ✅ 20 barras | ❌ No |
| Chat por Texto | ✅ Sí | ✅ Sí |
| Chat por Voz | ✅ Sí | ✅ Sí |
| Historial | ✅ Supabase | ✅ Supabase (mismo) |
| Backend | API Cloud | API Cloud (mismo) |
| Sincronización | ✅ Supabase | ✅ Supabase |
| Peso App | ~50 MB | ~25 MB APK |

---

## 🔄 SINCRONIZACIÓN ENTRE DISPOSITIVOS

**Ambas apps comparten:**
- ✅ Mismo `user_id` → misma memoria
- ✅ Misma tabla `mensajes_chat` en Supabase
- ✅ Mismo perfil de usuario
- ✅ Mismo contexto conversacional

**Ejemplo:**
1. Hablas con Azul en desktop: "Me gusta Rocket League"
2. Azul guarda en Supabase: `gustos_juegos = "Rocket League"`
3. Abres app móvil → Azul recuerda: "Sé que te gusta Rocket League"

---

## 🚀 ROADMAP FUTURO

### Versión 1.0 (Actual)
- ✅ Chat texto y voz
- ✅ Historial sincronizado
- ✅ Conexión a backend cloud

### Versión 1.1 (Próximo)
- 🔜 Notificaciones push
- 🔜 Widget en pantalla principal
- 🔜 Modo offline (cache local)

### Versión 2.0 (Futuro)
- 🔜 iOS (Swift/React Native)
- 🔜 Tema claro/oscuro dinámico
- 🔜 Calendario integrado
- 🔜 Recordatorios por voz

---

## 📚 RECURSOS ADICIONALES

### Documentación
- [Kivy Docs](https://kivy.org/doc/stable/)
- [KivyMD Components](https://kivymd.readthedocs.io/)
- [Buildozer Docs](https://buildozer.readthedocs.io/)

### Tutoriales
- [Kivy Android Tutorial](https://www.youtube.com/watch?v=F7UKmK9eQLY)
- [KivyMD Design System](https://kivymd.readthedocs.io/en/latest/getting-started/)

---

## ✅ CHECKLIST DE DEPLOYMENT

### Pre-Compilación
- [ ] Backend funcionando en Render
- [ ] WSL2 o Linux configurado
- [ ] Buildozer instalado
- [ ] Icon y splash creados

### Compilación
- [ ] `buildozer.spec` configurado
- [ ] `requirements_mobile.txt` completo
- [ ] `buildozer -v android debug` ejecutado
- [ ] APK generado en `bin/`

### Testing
- [ ] APK instalado en Android
- [ ] Permisos habilitados (micrófono, internet)
- [ ] Chat por texto funciona
- [ ] Chat por voz funciona
- [ ] Historial sincroniza con desktop

### Publicación (Opcional)
- [ ] Firmar APK con keystore
- [ ] Crear cuenta Google Play Developer
- [ ] Subir APK a Play Store
- [ ] Llenar metadata (descripción, screenshots)

---

**Última actualización**: 13 de Abril, 2026  
**Versión de la App**: 0.1 (alpha)  
**Estado**: ✅ Funcional en desarrollo
