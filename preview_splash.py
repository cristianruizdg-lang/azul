"""
Previsualizador de Sonido de Encendido de Azul
Ejecuta solo el sonido para probar el volumen y elegancia
"""

import pygame
import os
import time

def probar_sonido():
    """Reproduce el sonido de encendido"""
    
    pygame.mixer.init()
    
    print("\n" + "="*60)
    print("🔊 PREVISUALIZADOR DE SONIDO DE AZUL")
    print("="*60)
    
    archivo = "assets/sounds/startup.wav"
    
    if not os.path.exists(archivo):
        print("❌ No se encontró el archivo de sonido.")
        print("📝 Ejecuta: python generar_sonidos.py")
        return
    
    print("\n🎵 Características del sonido:")
    print("   • Duración: ~2 segundos")
    print("   • Volumen: 35% (suave y elegante)")
    print("   • Estilo: Windows/Tesla moderno")
    print("   • Fade in/out: Muy suave")
    
    print("\n▶️  Reproduciendo sonido...")
    print("🔊 Ajusta tu volumen ahora\n")
    
    time.sleep(1)
    
    try:
        sonido = pygame.mixer.Sound(archivo)
        sonido.play()
        
        # Esperar a que termine
        while pygame.mixer.get_busy():
            time.sleep(0.1)
        
        print("✅ Reproducción completada")
        print("\n💡 ¿Cómo sonó?")
        print("   • Demasiado fuerte → Edita generar_sonidos.py (reduce 0.35)")
        print("   • Muy suave → Edita generar_sonidos.py (aumenta 0.35)")
        print("   • Perfecto → ¡Disfruta de Azul!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    probar_sonido()
