"""
Script de prueba para el módulo de calendario de Azul
Prueba las funcionalidades sin necesidad de la interfaz completa
"""

from datetime import datetime, timedelta
from modules import GestorCalendario, AnalizadorCalendario, GeneradorNotificacionesInteligentes
import time

def prueba_basica():
    """Prueba básica de creación y listado de eventos"""
    print("=" * 50)
    print("🧪 PRUEBA 1: Creación de Eventos")
    print("=" * 50)
    
    gestor = GestorCalendario(archivo_datos="data/calendario_test.json")
    
    # Crear algunos eventos de prueba
    evento1 = gestor.agregar_evento(
        titulo="Cita con el doctor",
        fecha_hora=datetime.now() + timedelta(hours=2),
        tipo="cita",
        descripcion="Consulta general"
    )
    print(f"✅ Creado: {evento1.titulo} - {evento1.fecha_hora}")
    
    evento2 = gestor.agregar_evento(
        titulo="Comprar leche",
        fecha_hora=datetime.now() + timedelta(minutes=30),
        tipo="recordatorio"
    )
    print(f"✅ Creado: {evento2.titulo} - {evento2.fecha_hora}")
    
    evento3 = gestor.agregar_evento(
        titulo="Llamar a mamá",
        fecha_hora=datetime.now() + timedelta(hours=1),
        tipo="recordatorio"
    )
    print(f"✅ Creado: {evento3.titulo} - {evento3.fecha_hora}")
    
    print("\n" + "=" * 50)
    print("📅 EVENTOS PRÓXIMOS (24 horas):")
    print("=" * 50)
    eventos_proximos = gestor.obtener_eventos_proximos(24)
    for evento in eventos_proximos:
        print(f"- {evento.tipo.upper()}: {evento.titulo}")
        print(f"  ⏰ {evento.fecha_hora.strftime('%d/%m/%Y %H:%M')}")
        print(f"  ⏳ En {evento.minutos_restantes()} minutos\n")
    
    return gestor

def prueba_analizador():
    """Prueba el analizador de lenguaje natural"""
    print("\n" + "=" * 50)
    print("🧪 PRUEBA 2: Analizador de Lenguaje Natural")
    print("=" * 50)
    
    analizador = AnalizadorCalendario(modelo='llama3')
    
    frases_test = [
        "Tengo una cita con el dentista mañana a las 3pm",
        "Recuérdame llamar a Juan en 2 horas",
        "Alarma para las 7 de la mañana",
        "Agenda una reunión pasado mañana a las 10:30am"
    ]
    
    for frase in frases_test:
        print(f"\n📝 Frase: '{frase}'")
        resultado = analizador.interpretar_comando(frase)
        if resultado.get('valido'):
            print(f"   ✅ Detectado: {resultado['tipo']}")
            print(f"   📋 Título: {resultado['titulo']}")
            print(f"   📅 Fecha/Hora: {resultado['fecha_hora']}")
        else:
            print(f"   ❌ No se pudo interpretar")

def prueba_notificaciones():
    """Prueba el generador de notificaciones inteligentes"""
    print("\n" + "=" * 50)
    print("🧪 PRUEBA 3: Generador de Notificaciones")
    print("=" * 50)
    
    gestor = GestorCalendario(archivo_datos="data/calendario_test.json")
    generador = GeneradorNotificacionesInteligentes(
        modelo='llama3',
        perfil_usuario="nombre: Cristian; tarda mucho en alistarse; le gusta el humor"
    )
    
    # Crear un evento de prueba
    evento = gestor.agregar_evento(
        titulo="Cita importante",
        fecha_hora=datetime.now() + timedelta(hours=1),
        tipo="cita"
    )
    
    print(f"\n📅 Evento: {evento.titulo}")
    print(f"⏰ Hora: {evento.fecha_hora.strftime('%H:%M')}")
    
    # Generar notificaciones para diferentes tiempos
    tiempos = [60, 30, 10, 5]
    for tiempo in tiempos:
        print(f"\n🔔 Notificación ({tiempo} minutos antes):")
        mensaje = generador.generar_notificacion(evento, tiempo)
        print(f"   '{mensaje}'")

def prueba_monitor():
    """Prueba el monitor de eventos en tiempo real"""
    print("\n" + "=" * 50)
    print("🧪 PRUEBA 4: Monitor de Eventos")
    print("=" * 50)
    print("⚠️  Esta prueba requiere esperar. Creando evento en 1 minuto...")
    
    gestor = GestorCalendario(archivo_datos="data/calendario_test.json")
    
    # Crear evento que notifique en 1 minuto
    evento = gestor.agregar_evento(
        titulo="Prueba de notificación",
        fecha_hora=datetime.now() + timedelta(minutes=2),
        tipo="alarma",
        notificaciones=[1, 0.5]  # Notificar 1 min y 30 seg antes
    )
    
    print(f"✅ Evento creado: {evento.titulo}")
    print(f"⏰ Programado para: {evento.fecha_hora.strftime('%H:%M:%S')}")
    
    # Callback de notificación
    def callback_test(evt, mins_antes):
        print(f"\n🔔 ¡NOTIFICACIÓN RECIBIDA!")
        print(f"   Evento: {evt.titulo}")
        print(f"   Tiempo de aviso: {mins_antes} minutos antes")
    
    gestor.registrar_callback_notificacion(callback_test)
    gestor.iniciar_monitor()
    
    print("\n⏳ Esperando notificaciones (presiona Ctrl+C para salir)...")
    print("   El monitor revisará cada 30 segundos.")
    
    try:
        for i in range(10):  # Esperar hasta 5 minutos
            time.sleep(30)
            mins_restantes = evento.minutos_restantes()
            print(f"   ⏱️  {mins_restantes:.1f} minutos para el evento...")
            if mins_restantes < 0:
                break
    except KeyboardInterrupt:
        print("\n\n⚠️  Prueba interrumpida por el usuario")
    
    gestor.detener_monitor()
    print("✅ Monitor detenido")

def prueba_contexto_ia():
    """Prueba el contexto generado para la IA"""
    print("\n" + "=" * 50)
    print("🧪 PRUEBA 5: Contexto para IA")
    print("=" * 50)
    
    gestor = GestorCalendario(archivo_datos="data/calendario_test.json")
    
    # Crear varios eventos
    gestor.agregar_evento(
        "Reunión con equipo",
        datetime.now() + timedelta(hours=3),
        "cita"
    )
    gestor.agregar_evento(
        "Llamar al banco",
        datetime.now() + timedelta(hours=5),
        "recordatorio"
    )
    
    contexto = gestor.obtener_contexto_para_ia()
    print("\n📄 Contexto generado para Azul:")
    print("-" * 50)
    print(contexto)
    print("-" * 50)

def menu_principal():
    """Menú principal de pruebas"""
    print("\n")
    print("╔════════════════════════════════════════════╗")
    print("║   🤖 PRUEBAS DE CALENDARIO DE AZUL 🤖    ║")
    print("╚════════════════════════════════════════════╝")
    print("\nElige una prueba:")
    print("1. Prueba básica (crear y listar eventos)")
    print("2. Analizador de lenguaje natural")
    print("3. Generador de notificaciones inteligentes")
    print("4. Monitor de eventos en tiempo real")
    print("5. Contexto para IA")
    print("6. Ejecutar todas las pruebas (excepto monitor)")
    print("0. Salir")
    
    opcion = input("\n🔢 Opción: ").strip()
    
    if opcion == "1":
        prueba_basica()
    elif opcion == "2":
        prueba_analizador()
    elif opcion == "3":
        prueba_notificaciones()
    elif opcion == "4":
        prueba_monitor()
    elif opcion == "5":
        prueba_contexto_ia()
    elif opcion == "6":
        prueba_basica()
        prueba_analizador()
        prueba_notificaciones()
        prueba_contexto_ia()
    elif opcion == "0":
        print("\n👋 ¡Hasta luego!")
        return False
    else:
        print("\n❌ Opción inválida")
    
    return True

if __name__ == "__main__":
    print("\n⚠️  NOTA: Estas pruebas requieren que Llama3 esté instalado y funcionando.")
    print("          Algunas pruebas pueden tardar debido al procesamiento de IA.\n")
    
    continuar = True
    while continuar:
        continuar = menu_principal()
        if continuar:
            input("\n✅ Presiona Enter para volver al menú...")
