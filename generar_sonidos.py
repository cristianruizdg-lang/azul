"""
Generador de Sonido de Encendido Premium para Azul
Crea un sonido elegante similar a autos eléctricos de lujo
"""

import numpy as np
from scipy.io import wavfile
import os

def generar_sonido_encendido(duracion=1.0, sample_rate=44100):
    """
    Genera un sonido ultra elegante tipo campana de cristal
    Inspirado en Mac OS - Extremadamente suave, refinado y lujoso
    """
    t = np.linspace(0, duracion, int(sample_rate * duracion))
    
    # TONO 1: Fundamental cristalino (más agudo que antes)
    duracion_tono1 = duracion * 0.4
    t1 = t[t <= duracion_tono1]
    freq1 = 1000  # Hz - Más cristalino
    tono1 = np.sin(2 * np.pi * freq1 * t1)
    
    # Envelope muy suave con decay lento
    env1 = np.exp(-t1 / (duracion_tono1 * 0.6))
    tono1 = tono1 * env1
    
    # TONO 2: Armónico superior (campana elegante)
    tiempo_inicio_tono2 = duracion * 0.2
    t2 = t[t >= tiempo_inicio_tono2]
    t2_rel = t2 - tiempo_inicio_tono2
    freq2 = 1600  # Hz - Quinta perfecta elevada
    tono2 = np.sin(2 * np.pi * freq2 * t2_rel)
    
    # Envelope muy prolongado y suave
    env2 = np.exp(-t2_rel / (duracion * 0.7))
    tono2 = tono2 * env2
    
    # TONO 3: Armónico sutil de profundidad
    tiempo_inicio_tono3 = duracion * 0.3
    t3 = t[t >= tiempo_inicio_tono3]
    t3_rel = t3 - tiempo_inicio_tono3
    freq3 = 2400  # Hz - Octava alta muy sutil
    tono3 = np.sin(2 * np.pi * freq3 * t3_rel)
    env3 = np.exp(-t3_rel / (duracion * 0.4))
    tono3 = tono3 * env3
    
    # Crear array completo con balance elegante
    sonido = np.zeros_like(t)
    
    # Mezcla balanceada (tono principal más presente)
    sonido[:len(tono1)] += tono1 * 0.35
    idx_inicio2 = int(tiempo_inicio_tono2 * sample_rate)
    sonido[idx_inicio2:idx_inicio2 + len(tono2)] += tono2 * 0.30
    idx_inicio3 = int(tiempo_inicio_tono3 * sample_rate)
    sonido[idx_inicio3:idx_inicio3 + len(tono3)] += tono3 * 0.10  # Muy sutil
    
    # Fade in MUY suave y largo (200ms - ultra delicado)
    fade_in_len = int(sample_rate * 0.2)
    fade_in = (np.linspace(0, 1, fade_in_len)) ** 3  # Curva cúbica más suave
    sonido[:fade_in_len] *= fade_in
    
    # Fade out muy gradual (300ms)
    fade_out_len = int(sample_rate * 0.3)
    fade_out = (np.linspace(1, 0, fade_out_len)) ** 3
    sonido[-fade_out_len:] *= fade_out
    
    # Normalizar a volumen ultra suave (18% - muy discreto)
    sonido = sonido / np.max(np.abs(sonido)) * 0.18
    
    # Convertir a 16-bit PCM
    sonido_int = np.int16(sonido * 32767)
    
    return sonido_int, sample_rate


def generar_sonido_click_ui(duracion=0.1, sample_rate=44100):
    """
    Click sutil para interacciones de UI
    """
    t = np.linspace(0, duracion, int(sample_rate * duracion))
    
    # Click suave y elegante
    freq = 1200
    click = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-t * 50)
    click = click * envelope * 0.3
    
    click_int = np.int16(click * 32767)
    return click_int, sample_rate


def generar_sonido_notificacion(duracion=0.8, sample_rate=44100):
    """
    Sonido para notificaciones de eventos
    """
    t = np.linspace(0, duracion, int(sample_rate * duracion))
    
    # Dos tonos armónicos
    nota1 = np.sin(2 * np.pi * 800 * t)
    nota2 = np.sin(2 * np.pi * 1200 * t)
    
    envelope = np.exp(-t * 5) * (1 - np.exp(-t * 20))
    
    sonido = (nota1 + nota2) * envelope * 0.4
    sonido_int = np.int16(sonido * 32767)
    
    return sonido_int, sample_rate


if __name__ == "__main__":
    # Crear carpeta de sonidos
    os.makedirs("assets/sounds", exist_ok=True)
    
    print("🔊 Generando sonidos premium para Azul...")
    
    # Generar sonido de encendido
    print("   ⚡ Creando sonido de encendido...")
    sonido_encendido, sr = generar_sonido_encendido()
    wavfile.write("assets/sounds/startup.wav", sr, sonido_encendido)
    print("   ✅ startup.wav creado")
    
    # Generar click de UI
    print("   🖱️  Creando click de UI...")
    sonido_click, sr = generar_sonido_click_ui()
    wavfile.write("assets/sounds/click.wav", sr, sonido_click)
    print("   ✅ click.wav creado")
    
    # Generar sonido de notificación
    print("   🔔 Creando sonido de notificación...")
    sonido_notif, sr = generar_sonido_notificacion()
    wavfile.write("assets/sounds/notification.wav", sr, sonido_notif)
    print("   ✅ notification.wav creado")
    
    print("\n✨ Todos los sonidos premium generados exitosamente")
    print("📁 Ubicación: assets/sounds/")
