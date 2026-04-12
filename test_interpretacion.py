"""
Script de prueba rápida para verificar la interpretación de comandos
Úsalo para probar si Llama3 está interpretando correctamente
"""

from modules import AnalizadorCalendario
from datetime import datetime

def probar_comando(texto):
    """Prueba un comando y muestra el resultado"""
    print("\n" + "="*70)
    print(f"📝 COMANDO: {texto}")
    print("="*70)
    
    analizador = AnalizadorCalendario('llama3')
    resultado = analizador.interpretar_comando(texto)
    
    print(f"\n📊 RESULTADO:")
    print(f"   Válido: {resultado.get('valido')}")
    
    if resultado.get('valido'):
        print(f"   ✅ Tipo: {resultado['tipo']}")
        print(f"   ✅ Título: {resultado['titulo']}")
        print(f"   ✅ Fecha/Hora: {resultado['fecha_hora'].strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"   ✅ Descripción: {resultado['descripcion']}")
        
        # Calcular tiempo hasta el evento
        ahora = datetime.now()
        diferencia = resultado['fecha_hora'] - ahora
        minutos = int(diferencia.total_seconds() / 60)
        
        if minutos > 0:
            print(f"   ⏰ Tiempo hasta evento: {minutos} minutos")
        else:
            print(f"   ⚠️  ¡EVENTO EN EL PASADO! ({abs(minutos)} minutos atrás)")
    else:
        print(f"   ❌ No se pudo interpretar el comando")
    
    return resultado

if __name__ == "__main__":
    print("🧪 PRUEBA DE INTERPRETACIÓN DE COMANDOS")
    print("Probando diferentes formas de expresar eventos...")
    print("\n⚠️  NOTA: Este test usa análisis directo (regex) primero.")
    print("   Solo usa IA si el análisis directo falla.")
    
    # Obtener hora actual para los tests
    ahora = datetime.now()
    print(f"\n⏰ Hora actual: {ahora.strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Comandos de prueba
    comandos_prueba = [
        "oye recuerdame que voy a jugar con mis amigos orita a las 3:30pm",
        "tengo dentista mañana a las 4pm",
        "recordar comprar leche en 2 horas",
        "alarma para las 7am mañana",
        "cita con el doctor hoy a las 5pm",
    ]
    
    resultados = []
    for cmd in comandos_prueba:
        resultado = probar_comando(cmd)
        resultados.append((cmd, resultado.get('valido')))
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*70)
    
    exitosas = sum(1 for _, valido in resultados if valido)
    total = len(resultados)
    
    print(f"\n✅ Comandos exitosos: {exitosas}/{total}")
    print(f"❌ Comandos fallidos: {total - exitosas}/{total}")
    
    if exitosas == total:
        print("\n🎉 ¡Todas las pruebas pasaron! El sistema funciona correctamente.")
    elif exitosas > 0:
        print("\n⚠️  Algunas pruebas fallaron. Verifica los logs arriba.")
    else:
        print("\n❌ Todas las pruebas fallaron. Verifica que:")
        print("   1. Ollama esté corriendo (ollama serve)")
        print("   2. Llama3 esté instalado (ollama list)")
        print("   3. No haya errores en la consola")
    
    print("\n" + "="*70)
