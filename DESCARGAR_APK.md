# 📱 CÓMO DESCARGAR AZUL EN TU CELULAR

## 🚀 PASOS PARA OBTENER EL APK

### 1️⃣ Hacer Push al Repositorio

Primero, sube los archivos a GitHub:

```bash
git add .
git commit -m "Mobile: Agregar app móvil con GitHub Actions para compilación automática"
git push
```

### 2️⃣ GitHub Compila Automáticamente

GitHub Actions compilará el APK automáticamente (toma ~15-30 minutos la primera vez).

Puedes ver el progreso en:
```
https://github.com/cristianruizdg-lang/azul/actions
```

### 3️⃣ Descargar APK en Tu Celular

**Opción A: Desde Actions (Artifact)**

1. Ve a: `https://github.com/cristianruizdg-lang/azul/actions`
2. Click en el workflow más reciente (verde ✅)
3. Baja hasta "Artifacts"
4. Click en `azul-mobile-apk`
5. Descarga el ZIP
6. Extrae el APK del ZIP

**Opción B: Desde Releases (Más Fácil)**

1. Ve a: `https://github.com/cristianruizdg-lang/azul/releases`
2. Click en la release más reciente
3. Descarga directamente el APK

### 4️⃣ Instalar en Android

1. Abre el APK descargado en tu celular
2. Android dirá "App no verificada" o similar
3. Click en "Instalar de todas formas" o "Más detalles" → "Instalar"
4. Habilita "Instalar apps de fuentes desconocidas" si te lo pide
5. ¡Listo! Azul estará instalado

### 5️⃣ Configurar Permisos

Al abrir Azul por primera vez:
1. Permitir acceso a Internet ✅
2. Permitir acceso al Micrófono ✅ (para chat por voz)
3. Permitir acceso al Almacenamiento ✅

---

## 🔄 ACTUALIZACIONES

Cada vez que modifiques el código de `mobile/` y hagas push, GitHub compilará un nuevo APK automáticamente.

Para actualizar la app en tu celular:
1. Descarga el nuevo APK
2. Instálalo sobre la versión anterior (mantendrá tus datos)

---

## 🐛 PROBLEMAS COMUNES

### "No puedo instalar la app"
- Habilita "Fuentes desconocidas" en Ajustes → Seguridad
- Asegúrate de descargar el archivo .apk (no el .zip)

### "La app no se conecta"
- Verifica que tengas internet
- El backend debe estar activo: https://azul-4xsp.onrender.com/health

### "No tengo micrófono"
- Verifica permisos en Ajustes → Apps → Azul → Permisos
- Permite "Micrófono"

---

## 📊 ESTADO DEL BUILD

Puedes ver si la compilación fue exitosa aquí:

[![Build APK](https://github.com/cristianruizdg-lang/azul/actions/workflows/build-apk.yml/badge.svg)](https://github.com/cristianruizdg-lang/azul/actions/workflows/build-apk.yml)

Verde ✅ = APK listo para descargar  
Rojo ❌ = Error en compilación (revisa los logs)

---

## ⚡ COMPILACIÓN MANUAL (Opcional)

Si prefieres ejecutar manualmente:

1. Ve a: `https://github.com/cristianruizdg-lang/azul/actions`
2. Click en "Compilar APK Android" (izquierda)
3. Click en "Run workflow" (derecha)
4. Click en "Run workflow" verde
5. Espera 15-30 min
6. Descarga el APK

---

**Última actualización**: Abril 13, 2026  
**Versión**: 0.1 (Alpha)
