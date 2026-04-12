"""
Test del sistema de detección de hora/fecha
"""
from datetime import datetime

def agregar_contexto_tiempo_real(texto: str):
    """Agrega información de hora/fecha cuando el usuario pregunta por ello"""
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
        hora_24h = ahora.strftime("%H:%M")
        print(f"✅ DETECTADO - Pregunta por hora")
        print(f"   Respuesta: {hora_actual} ({hora_24h} formato 24h)")
        return True
    
    # Si pregunta por la fecha
    if any(pregunta in texto_lower for pregunta in preguntas_fecha):
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
                'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
        
        dia_semana = dias_semana[ahora.weekday()]
        mes = meses[ahora.month - 1]
        
        print(f"✅ DETECTADO - Pregunta por fecha")
        print(f"   Respuesta: {dia_semana} {ahora.day} de {mes} de {ahora.year}")
        return True
    
    return False

# Tests
print("=" * 60)
print("🧪 TEST DE DETECCIÓN DE HORA/FECHA")
print("=" * 60)

tests = [
    "¿Qué hora es?",
    "Dime la hora por favor",
    "¿Me dices que hora es?",
    "Hora",
    "¿Qué día es hoy?",
    "¿En qué fecha estamos?",
    "¿Cuál es la fecha actual?",
    "Hola Azul, ¿cómo estás?"  # No debería detectar
]

for i, test in enumerate(tests, 1):
    print(f"\n[Test {i}] Usuario: '{test}'")
    detectado = agregar_contexto_tiempo_real(test)
    if not detectado:
        print("   ⏭️  No es pregunta de hora/fecha")

print("\n" + "=" * 60)
print("✨ Tests completados")
print("=" * 60)
