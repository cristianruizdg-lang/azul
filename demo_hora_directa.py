"""
Test de respuestas directas de hora y fecha
Simula lo que hace Azul cuando le preguntas la hora
"""
from datetime import datetime

def responder_hora_fecha(texto: str):
    """Simula la respuesta directa de Azul"""
    texto_lower = texto.lower()
    
    # Detectar preguntas sobre hora
    preguntas_hora = ['qué hora', 'que hora', 'hora es', 'dime la hora', 'cuál es la hora', 
                     'cual es la hora', 'me dices la hora', 'tienes la hora']
    
    # Detectar preguntas sobre fecha
    preguntas_fecha = ['qué día', 'que dia', 'qué fecha', 'que fecha', 'día es hoy',
                      'dia es hoy', 'fecha es', 'cuál es la fecha', 'cual es la fecha',
                      'estamos a', 'en qué día', 'en que dia']
    
    ahora = datetime.now()
    
    # Si pregunta por la hora
    if any(pregunta in texto_lower for pregunta in preguntas_hora):
        hora_actual = ahora.strftime("%I:%M %p").lstrip("0")
        return f"Son las {hora_actual}"
    
    # Si pregunta por la fecha
    if any(pregunta in texto_lower for pregunta in preguntas_fecha):
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
                'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        
        dia_semana = dias_semana[ahora.weekday()]
        mes = meses[ahora.month - 1]
        
        return f"Hoy es {dia_semana} {ahora.day} de {mes}"
    
    return None

# Tests
print("=" * 60)
print("🧪 TEST DE RESPUESTAS DIRECTAS (COMO AZUL)")
print("=" * 60)
print(f"\n⏰ Hora actual del sistema: {datetime.now().strftime('%I:%M %p').lstrip('0')}")
print(f"📅 Fecha actual del sistema: {datetime.now().strftime('%A %d de %B, %Y')}")
print("\n" + "=" * 60)

tests = [
    "¿Qué hora es?",
    "Dime la hora",
    "¿Me dices que hora es?",
    "¿Qué día es hoy?",
    "¿En qué fecha estamos?",
]

for test in tests:
    respuesta = responder_hora_fecha(test)
    print(f"\n👤 Usuario: '{test}'")
    print(f"🤖 Azul: '{respuesta}'")

print("\n" + "=" * 60)
print("✅ Ahora Azul responde DIRECTAMENTE del sistema")
print("   (Sin usar IA = Siempre correcto)")
print("=" * 60)
