[app]

# Nombre de la app (interno)
title = Azul Mobile

# Nombre del paquete
package.name = azulmobile

# Dominio del paquete (inverso)
package.domain = com.azul

# Archivo de código fuente principal
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# Versión de la app
version = 0.1

# Requerimientos de Python
requirements = python3==3.11,kivy==2.3.0,kivymd==1.2.0,requests,pyjnius,android,pillow

# Icono de la aplicación (512x512 px recomendado)
# icon.filename = assets/icon.png

# Splash screen opcional
# presplash.filename = assets/splash.png

# Orientación (landscape, portrait o all)
orientation = portrait

# Permisos de Android
android.permissions = INTERNET,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# Arquitecturas de Android (arm64-v8a para dispositivos modernos)
android.archs = arm64-v8a

# API de Android
android.api = 33
android.minapi = 21
android.ndk = 25b

# Aceptar licencias automáticamente
android.accept_sdk_license = True

# SDK path (buildozer lo descarga automáticamente)
# android.sdk_path = 
# android.ndk_path = 

# Características Android
android.features = android.hardware.microphone

# Logs
log_level = 2

# Buildozer settings
[buildozer]

# Log de buildozer
log_level = 2

# Directorio de salida de archivos compilados
# bin_dir = ./bin

# Advertencias a ignorar
warn_on_root = 1

# Actualizar automáticamente buildozer
auto_update = 1
