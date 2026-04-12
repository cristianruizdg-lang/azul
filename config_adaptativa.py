"""
Configuración adaptativa de Azul
Detecta automáticamente el entorno y ajusta configuración
"""

import os
import platform
import psutil

# ===========================
# DETECCIÓN DE ENTORNO
# ===========================

def detectar_entorno():
    """Detecta si está en PC, Android, o servidor"""
    
    sistema = platform.system()
    
    # Detectar Android (Termux)
    if 'ANDROID_ROOT' in os.environ or 'TERMUX_VERSION' in os.environ:
        return {
            'tipo': 'android',
            'nombre': 'Tablet Android',
            'modelo_ia': 'phi3',
            'interfaz': 'kivy',
            'notificaciones': 'android',
            'recursos_limitados': True
        }
    
    # Detectar Windows/Linux/Mac normal
    elif sistema in ['Windows', 'Linux', 'Darwin']:
        # Verificar RAM disponible
        ram_gb = psutil.virtual_memory().total / (1024**3)
        
        if ram_gb >= 16:
            tipo_pc = 'potente'
            modelo = 'llama3'
        elif ram_gb >= 8:
            tipo_pc = 'medio'
            modelo = 'llama3'  # Puede con 8B
        else:
            tipo_pc = 'ligero'
            modelo = 'phi3'  # Mejor para PCs con poca RAM
        
        return {
            'tipo': 'pc',
            'nombre': f'PC {sistema} ({tipo_pc})',
            'modelo_ia': modelo,
            'interfaz': 'customtkinter',
            'notificaciones': 'win10toast' if sistema == 'Windows' else 'native',
            'recursos_limitados': ram_gb < 8
        }
    
    # Raspberry Pi o servidor
    else:
        return {
            'tipo': 'servidor',
            'nombre': 'Servidor/Raspberry Pi',
            'modelo_ia': 'phi3',
            'interfaz': 'web',
            'notificaciones': 'none',
            'recursos_limitados': True
        }


# ===========================
# CONFIGURACIÓN GLOBAL
# ===========================

ENTORNO = detectar_entorno()

# Modelo de IA a usar
MODELO_IA = ENTORNO['modelo_ia']

# Tipo de interfaz
TIPO_INTERFAZ = ENTORNO['interfaz']

# Sistema de notificaciones
SISTEMA_NOTIFICACIONES = ENTORNO['notificaciones']

# Optimizaciones para recursos limitados
RECURSOS_LIMITADOS = ENTORNO['recursos_limitados']

if RECURSOS_LIMITADOS:
    # Reducir frecuencia de monitoreo
    INTERVALO_MONITOR = 60  # segundos
    
    # Desactivar animaciones complejas
    ANIMACIONES_3D = False
    
    # Limitar historial en memoria
    MAX_HISTORIAL_MEMORIA = 50  # mensajes
    
    # Temperatura de IA (menos creativo = más rápido)
    TEMPERATURA = 0.5
else:
    INTERVALO_MONITOR = 30
    ANIMACIONES_3D = True
    MAX_HISTORIAL_MEMORIA = 200
    TEMPERATURA = 0.7


# ===========================
# CONFIGURACIÓN DE RED
# ===========================

# Modo servidor (para conectar tablet a PC)
MODO_SERVIDOR = False  # Cambiar a True en PC si quieres modo cliente-servidor
SERVIDOR_IP = "0.0.0.0"  # Escuchar en todas las interfaces
SERVIDOR_PUERTO = 8000

# Modo cliente (para tablet que se conecta a PC)
MODO_CLIENTE = False  # Cambiar a True en tablet si quieres conectar a PC
SERVIDOR_REMOTO = "192.168.1.100"  # Cambiar por IP de tu PC


# ===========================
# CONFIGURACIÓN DE SUPABASE
# ===========================

# Usar Supabase solo si hay conexión
USAR_SUPABASE = True
SUPABASE_URL = "https://lovcwnqviaovthtcxjjr.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxvdmN3bnF2aWFvdnRodGN4ampyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjcwNjI0MDMsImV4cCI6MjA4MjYzODQwM30.33OPrkBMRnFPJRW98SNJCkx6fG1x4Ffx4MKxfBmbbWE"


# ===========================
# IMPRIMIR CONFIGURACIÓN
# ===========================

def mostrar_configuracion():
    """Muestra la configuración detectada"""
    print("=" * 60)
    print("🤖 AZUL - CONFIGURACIÓN ADAPTATIVA")
    print("=" * 60)
    print(f"📱 Entorno: {ENTORNO['nombre']}")
    print(f"🧠 Modelo IA: {MODELO_IA}")
    print(f"🎨 Interfaz: {TIPO_INTERFAZ}")
    print(f"🔔 Notificaciones: {SISTEMA_NOTIFICACIONES}")
    print(f"⚡ Recursos limitados: {'Sí' if RECURSOS_LIMITADOS else 'No'}")
    print(f"📊 Intervalo monitor: {INTERVALO_MONITOR}s")
    print(f"🌡️  Temperatura IA: {TEMPERATURA}")
    
    if MODO_SERVIDOR:
        print(f"🖥️  Modo servidor activo en {SERVIDOR_IP}:{SERVIDOR_PUERTO}")
    
    if MODO_CLIENTE:
        print(f"📱 Modo cliente apuntando a {SERVIDOR_REMOTO}:{SERVIDOR_PUERTO}")
    
    print("=" * 60)


if __name__ == "__main__":
    mostrar_configuracion()
