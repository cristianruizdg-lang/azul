# 📱 AZUL MOBILE - Aplicación Android

Aplicación móvil de Azul construida con Kivy/KivyMD.

## 🚀 INICIO RÁPIDO

### Testing en PC (Desarrollo)

```bash
# Instalar dependencias
pip install -r requirements_mobile.txt

# Ejecutar app
python azul_mobile.py
```

### Compilar APK para Android

**Requisitos:**
- Linux o WSL2 (Windows Subsystem for Linux)
- Buildozer instalado

```bash
# En WSL2/Linux

# 1. Instalar dependencias del sistema
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 2. Instalar buildozer
pip3 install buildozer cython

# 3. Compilar APK (primera vez: 30-60 min)
buildozer -v android debug

# 4. El APK estará en:
# bin/azulmobile-0.1-armeabi-v7a-debug.apk
```

### Instalar en Android

```bash
# Conectar dispositivo por USB y habilitar "Depuración USB"
adb install bin/azulmobile-0.1-armeabi-v7a-debug.apk

# O copiar APK manualmente y habilitar "Fuentes desconocidas"
```

## 📋 CARACTERÍSTICAS

- ✅ Chat conversacional con texto
- ✅ Chat por voz (grabar y reproducir)
- ✅ Historial sincronizado con Supabase
- ✅ Memoria compartida con app desktop
- ✅ Interfaz Material Design moderna
- ✅ Tema oscuro

## 🔧 CONFIGURACIÓN

Editar `azul_mobile.py` línea ~41:

```python
API_URL = "https://azul-4xsp.onrender.com"  # Backend
USER_ID = "default"  # Mismo ID que desktop
```

## 📝 ESTRUCTURA

```
mobile/
├── azul_mobile.py           # App principal
├── requirements_mobile.txt   # Dependencias Python
├── buildozer.spec           # Config para compilar APK
├── assets/
│   ├── icon.png            # Icono 512x512 px (opcional)
│   └── splash.png          # Splash 1920x1080 px (opcional)
└── README.md               # Este archivo
```

## 🐛 TROUBLESHOOTING

### Error: "No module named 'kivymd'"
```bash
pip install kivymd
```

### Buildozer falla
```bash
# Limpiar cache
buildozer android clean

# Reintentar
buildozer -v android debug
```

### Permisos denegados en Android
1. Ajustes → Apps → Azul → Permisos
2. Habilitar: Micrófono, Almacenamiento

## 📚 MÁS INFO

Ver `../FASE_5_APP_MOVIL.md` para documentación completa.
