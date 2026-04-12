"""
Test rápido de la voz natural de Azul
"""
import asyncio
import edge_tts
import pygame
import tempfile
import os

pygame.mixer.init()

async def test_voz():
    print("🎤 Probando voz natural de Azul (Dalia - México)...\n")
    
    texto = "Hola, soy Azul. Esta es mi nueva voz, mucho más natural. ¿Qué te parece?"
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
            temp_path = temp_audio.name
        
        communicate = edge_tts.Communicate(texto, "es-MX-DaliaNeural", rate='+10%')
        await communicate.save(temp_path)
        
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
        
        os.unlink(temp_path)
        print("✅ ¡Prueba completada! Así sonará Azul ahora.\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_voz())
