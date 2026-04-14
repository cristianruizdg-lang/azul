# Azul Mobile - Flutter App

Aplicación móvil nativa de Azul AI Assistant construida con Flutter.

## ✨ Características

- ✅ **Chat de texto** con Azul
- ✅ **Chat de voz** con grabación de audio
- ✅ **Reproducción de respuestas** en audio
- ✅ **Historial sincronizado** con Supabase
- ✅ **Material Design 3** con tema oscuro
- ✅ **Conexión al backend** en la nube
- ⏳ **Background services** (próximamente)

## 🚀 Instalación de Flutter SDK

### Windows

1. **Descargar Flutter SDK:**
   ```powershell
   # Crear carpeta para Flutter
   mkdir C:\src
   cd C:\src
   
   # Descargar Flutter (última versión estable)
   # Ir a: https://docs.flutter.dev/get-started/install/windows
   # Descargar flutter_windows_X.X.X-stable.zip
   ```

2. **Extraer y configurar PATH:**
   ```powershell
   # Extraer el ZIP en C:\src\flutter
   
   # Agregar al PATH del sistema:
   # - Abrir "Editar las variables de entorno del sistema"
   # - Click en "Variables de entorno"
   # - En "Variables del sistema", editar "Path"
   # - Agregar: C:\src\flutter\bin
   ```

3. **Verificar instalación:**
   ```powershell
   flutter doctor
   ```

4. **Instalar Android SDK (para compilar APK):**
   ```powershell
   # Opción 1: Instalar Android Studio (recomendado)
   # Descargar de: https://developer.android.com/studio
   
   # Opción 2: Solo Android SDK Command-Line Tools
   # Descargar de: https://developer.android.com/studio#command-tools
   ```

5. **Aceptar licencias de Android:**
   ```powershell
   flutter doctor --android-licenses
   ```

## 📦 Compilar APK

### Opción 1: APK Debug (Rápido para pruebas)

```powershell
cd flutter_app
flutter build apk --debug
```

El APK estará en: `flutter_app\build\app\outputs\flutter-apk\app-debug.apk`

### Opción 2: APK Release (Optimizado)

```powershell
cd flutter_app
flutter build apk --release
```

El APK estará en: `flutter_app\build\app\outputs\flutter-apk\app-release.apk`

### Opción 3: APK por arquitectura (Más liviano)

```powershell
cd flutter_app
flutter build apk --release --split-per-abi
```

Genera 3 APKs (típicamente arm64 es el que necesitas):
- `app-armeabi-v7a-release.apk` (32-bit)
- `app-arm64-v8a-release.apk` (64-bit) ⭐ **Recomendado**
- `app-x86_64-release.apk` (emuladores)

## 📱 Instalar en tu celular

### Método 1: Cable USB (Rápido)

1. **Habilitar opciones de desarrollador en Android:**
   - Ir a Configuración → Acerca del teléfono
   - Tocar "Número de compilación" 7 veces
   - Volver y entrar a "Opciones de desarrollador"
   - Activar "Depuración USB"

2. **Conectar celular y instalar:**
   ```powershell
   cd flutter_app
   flutter install
   ```

### Método 2: Transferir APK manualmente

1. **Copiar APK al celular:**
   - Conectar por USB y copiar el archivo .apk
   - O enviarlo por WhatsApp/correo

2. **Instalar en el celular:**
   - Abrir el archivo .apk
   - Permitir "Instalar apps desconocidas"
   - Click en "Instalar"

3. **Conceder permisos:**
   - Micrófono (para chat de voz)
   - Almacenamiento (para guardar audios)

## 🛠️ Desarrollo

### Ejecutar en modo desarrollo

```powershell
cd flutter_app
flutter run
```

### Ver logs en tiempo real

```powershell
flutter logs
```

### Limpiar build cache

```powershell
flutter clean
flutter pub get
```

## 📂 Estructura del Proyecto

```
flutter_app/
├── lib/
│   ├── main.dart                    # Punto de entrada
│   ├── models/
│   │   └── message.dart             # Modelo de mensaje
│   ├── screens/
│   │   └── chat_screen.dart         # Pantalla principal de chat
│   ├── services/
│   │   ├── api_service.dart         # Cliente HTTP para backend
│   │   └── audio_service.dart       # Grabación y reproducción
│   └── widgets/
│       └── message_bubble.dart      # Widget de burbuja de mensaje
├── android/
│   └── app/
│       ├── build.gradle             # Configuración Android
│       └── src/main/
│           ├── AndroidManifest.xml  # Permisos y configuración
│           └── kotlin/.../MainActivity.kt
└── pubspec.yaml                     # Dependencias Flutter
```

## 🔧 Configuración del Backend

La app se conecta a: `https://azul-4xsp.onrender.com`

Si necesitas cambiar la URL del backend, edita:
```dart
// lib/services/api_service.dart
static const String baseUrl = 'https://tu-backend.com';
```

## 🐛 Troubleshooting

### Error: "No se encontró Flutter SDK"
```powershell
# Verificar PATH
where flutter

# Debe mostrar: C:\src\flutter\bin\flutter.bat
```

### Error: "Android licenses not accepted"
```powershell
flutter doctor --android-licenses
# Presionar 'y' para aceptar todas
```

### Error: "Unable to locate Android SDK"
```powershell
# Configurar variable de entorno
setx ANDROID_HOME "C:\Users\TU_USUARIO\AppData\Local\Android\Sdk"
```

### Error de permisos en el celular
- Ir a Configuración → Apps → Azul Mobile → Permisos
- Activar: Micrófono, Almacenamiento

## 📝 Próximas Características

- [ ] Background service para respuestas instantáneas
- [ ] Widget de pantalla principal
- [ ] Activación por voz ("Hey Azul")
- [ ] Notificaciones push
- [ ] Modo offline
- [ ] Respuestas rápidas predefinidas

## 🎨 Stack Tecnológico

- **Framework:** Flutter 3.x
- **Lenguaje:** Dart
- **UI:** Material Design 3
- **HTTP Client:** http package
- **Audio:** record + audioplayers
- **State Management:** Provider
- **Storage:** SharedPreferences
- **Backend:** FastAPI (Python) en Render
- **Base de datos:** Supabase (PostgreSQL)

## 📄 Licencia

MIT License - Ver archivo LICENSE para más detalles.

---

**Desarrollado con ❤️ para tener a Azul siempre contigo**
