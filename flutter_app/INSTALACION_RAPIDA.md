# 🚀 Guía Rápida: Instalar Azul en tu Celular

## Opción 1: Transferir APK Directo (MÁS RÁPIDO) ⚡

### Paso 1: Compilar APK (en tu PC)

```powershell
# Abrir terminal en la carpeta del proyecto
cd "c:\Users\Chich\OneDrive\Desktop\Proyectos P\jarvis_vista\flutter_app"

# Compilar APK (5-10 minutos la primera vez)
flutter build apk --release --split-per-abi
```

### Paso 2: Encontrar el APK

El archivo estará en:
```
flutter_app\build\app\outputs\flutter-apk\app-arm64-v8a-release.apk
```

**Tamaño:** ~30-40 MB

### Paso 3: Transferir a tu celular

**Opción A - Cable USB:**
1. Conectar celular por USB
2. Copiar el APK a la carpeta "Descargas" del celular

**Opción B - WhatsApp/Telegram:**
1. Enviarte el APK a ti mismo
2. Descargar en el celular

**Opción C - Google Drive/Dropbox:**
1. Subir el APK a la nube
2. Descargar desde el celular

### Paso 4: Instalar en el celular

1. Abrir el archivo `app-arm64-v8a-release.apk`
2. Si aparece advertencia:
   - Presionar "Configuración"
   - Activar "Permitir desde esta fuente"
   - Volver y presionar "Instalar"
3. Presionar "Abrir" cuando termine

### Paso 5: Conceder permisos

Al abrir la app por primera vez:
- ✅ **Permitir acceso al micrófono** (para chat de voz)
- ✅ **Permitir acceso al almacenamiento** (para guardar audios)

### ¡Listo! 🎉

Abre la app "Azul Mobile" y empieza a chatear.

---

## Opción 2: Instalar Directamente con USB (DESARROLLO)

### Requisitos:
- Celular conectado por USB
- Depuración USB activada

### Pasos:

1. **Habilitar modo desarrollador en Android:**
   ```
   Configuración → Acerca del teléfono → 
   Tocar "Número de compilación" 7 veces
   ```

2. **Activar Depuración USB:**
   ```
   Configuración → Sistema → Opciones de desarrollador → 
   Activar "Depuración USB"
   ```

3. **Conectar y verificar:**
   ```powershell
   flutter devices
   # Debería mostrar tu celular
   ```

4. **Instalar directamente:**
   ```powershell
   cd flutter_app
   flutter install
   ```

---

## Solución de Problemas

### ❌ "No se puede instalar la app"
- Verificar que "Fuentes desconocidas" o "Instalar apps desconocidas" esté activado
- Ir a: Configuración → Seguridad → Instalar apps desconocidas

### ❌ "La app se cierra al abrirla"
- Verificar permisos: Configuración → Apps → Azul Mobile → Permisos
- Activar: Micrófono, Almacenamiento

### ❌ "No se conecta al backend"
- Verificar conexión a Internet
- El backend puede tardar ~30 segundos en despertar si estaba inactivo

### ❌ "El micrófono no funciona"
- Ir a: Configuración → Apps → Azul Mobile → Permisos → Micrófono → Permitir

---

## Actualizar la App

Para actualizar a una nueva versión:

1. Compilar nuevo APK con el mismo comando
2. Transferir e instalar sobre la versión anterior
3. Los datos (historial, configuración) se mantienen

---

## Desinstalar

```
Configuración → Apps → Azul Mobile → Desinstalar
```

---

**¿Necesitas ayuda?** Revisa el README.md completo en la carpeta `flutter_app/`
