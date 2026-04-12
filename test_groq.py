"""
🧪 TEST DE GROQ API
===================
Este script verifica que tu API key de Groq funciona correctamente.

INSTRUCCIONES:
1. Asegúrate de haber agregado tu API key en el archivo .env
2. Ejecuta: python test_groq.py
3. Deberías ver un mensaje de confirmación

Si ves errores:
- Verifica que copiaste la key completa en .env
- Asegúrate que la key empieza con "gsk_"
- Revisa que no hay espacios extra en .env
"""

import os
from dotenv import load_dotenv
from groq import Groq

# Cargar variables de entorno
load_dotenv()

def test_groq_connection():
    """Prueba la conexión con Groq"""
    print("=" * 60)
    print("🧪 PROBANDO CONEXIÓN CON GROQ API")
    print("=" * 60)
    
    # Obtener API key
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key or api_key == "tu_api_key_aqui_comienza_con_gsk":
        print("\n❌ ERROR: API key no configurada")
        print("\nPasos para solucionar:")
        print("1. Ve a: https://console.groq.com")
        print("2. Crea cuenta o inicia sesión")
        print("3. Click 'API Keys' → 'Create API Key'")
        print("4. Copia la key (empieza con gsk_)")
        print("5. Abre el archivo .env")
        print("6. Reemplaza 'tu_api_key_aqui_comienza_con_gsk' con tu key real")
        print("7. Guarda el archivo .env")
        print("8. Ejecuta este script nuevamente")
        return False
    
    print(f"\n📋 API Key encontrada: {api_key[:20]}...{api_key[-10:]}")
    print("📡 Intentando conectar con Groq...")
    
    try:
        # Crear cliente
        client = Groq(api_key=api_key)
        
        # Test simple con modelo actualizado
        model = os.getenv("AI_MODEL", "llama-3.3-70b-versatile")
        print(f"🤖 Enviando mensaje de prueba con modelo: {model}...")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": "Di exactamente: 'Conexión exitosa con Groq'"
                }
            ],
            temperature=0.5,
            max_tokens=20
        )
        
        respuesta = response.choices[0].message.content
        
        print("\n" + "=" * 60)
        print("✅ ¡GROQ API FUNCIONA PERFECTAMENTE!")
        print("=" * 60)
        print(f"\n🎯 Respuesta de Llama3-70B: {respuesta}")
        print(f"⚡ Tokens usados: {response.usage.total_tokens}")
        print(f"🔥 Modelo: {response.model}")
        
        # Mostrar estadísticas
        print("\n📊 ESTADÍSTICAS:")
        print(f"   - Prompt tokens: {response.usage.prompt_tokens}")
        print(f"   - Completion tokens: {response.usage.completion_tokens}")
        print(f"   - Total tokens: {response.usage.total_tokens}")
        
        print("\n🎉 ¡Tu API key está lista para usarse!")
        print("=" * 60)
        print("\n✨ Siguiente paso: Continuar con Fase 2 (Backend)")
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR AL CONECTAR CON GROQ")
        print("=" * 60)
        print(f"\nDetalle del error: {str(e)}")
        
        if "invalid" in str(e).lower() or "authentication" in str(e).lower():
            print("\n🔑 Problema con la API key:")
            print("   - Verifica que copiaste la key completa")
            print("   - Asegúrate que empieza con 'gsk_'")
            print("   - No debe tener espacios al principio o final")
            print("   - Regenera la key en console.groq.com si es necesario")
        elif "rate" in str(e).lower():
            print("\n⏱️ Límite de requests alcanzado:")
            print("   - Espera unos minutos e intenta de nuevo")
            print("   - Free tier: 14,400 requests/día")
        else:
            print("\n🌐 Problema de conexión:")
            print("   - Verifica tu conexión a internet")
            print("   - Intenta de nuevo en unos segundos")
        
        return False

if __name__ == "__main__":
    test_groq_connection()
    
    input("\n\nPresiona Enter para cerrar...")
