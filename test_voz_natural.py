"""
Prueba de voz natural con Edge TTS
Permite escuchar diferentes voces femeninas en español
"""
import asyncio
import edge_tts
import pygame
import tempfile
import os

# Inicializar pygame mixer
pygame.mixer.init()

VOCES_DISPONIBLES = {
    "1": ("es-MX-DaliaNeural", "Dalia - México (Cálida y natural)"),
    "2": ("es-ES-ElviraNeural", "Elvira - España (Elegante)"),
    "3": ("es-AR-ElenaNeural", "Elena - Argentina (Amigable)"),
    "4": ("es-CO-SalomeNeural", "Salomé - Colombia (Dulce)"),
    "5": ("es-MX-NuriaNeural", "Nuria - México (Profesional)")
}

async def probar_voz(voz_id: str, texto: str):
    """Prueba una voz con el texto dado"""
    print(f"\n🔊 Reproduciendo con {VOCES_DISPONIBLES[voz_id][1]}...")
    
    try:
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
            temp_path = temp_audio.name
        
        # Generar audio con Edge TTS
        # rate: velocidad (+10% = un poco más rápido, natural)
        # pitch: tono (+0Hz = normal)
        communicate = edge_tts.Communicate(
            texto, 
            VOCES_DISPONIBLES[voz_id][0],
            rate='+10%',
            pitch='+0Hz'
        )
        await communicate.save(temp_path)
        
        # Reproducir
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        
        # Esperar a que termine
        while pygame.mixer.music.get_busy():
            await asyncio.sleep(0.1)
        
        # Limpiar
        try:
            os.unlink(temp_path)
        except:
            pass
            
        print("✅ Reproducción completada\n")
        
    except Exception as e:
        print(f"❌ Error: {e}\n")

async def main():
    print("=" * 60)
    print("🎤 PROBADOR DE VOCES NATURALES PARA AZUL")
    print("=" * 60)
    print("\nVoces disponibles:")
    for key, (_, descripcion) in VOCES_DISPONIBLES.items():
        print(f"  {key}. {descripcion}")
    
    print("\n" + "=" * 60)
    
    # Texto de prueba
    texto_prueba = (
        "Hola, soy Azul, tu asistente personal. "
        "Esta es mi nueva voz, mucho más natural y humana. "
        "¿Qué te parece?"
    )
    
    # Probar cada voz
    for voz_id in VOCES_DISPONIBLES.keys():
        input(f"\nPresiona ENTER para escuchar la voz {voz_id}...")
        await probar_voz(voz_id, texto_prueba)
    
    print("\n" + "=" * 60)
    print("✨ Prueba completada")
    print("\nLa voz configurada actualmente en Azul es:")
    print(f"   {VOCES_DISPONIBLES['1'][1]} (Recomendada)")
    print("\nPara cambiarla, modifica VOZ_AZUL en jarvis_funcional.py")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
