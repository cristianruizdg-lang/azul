"""
Script de prueba para verificar que las notificaciones de Windows funcionan
Ejecuta este script para probar las notificaciones antes de usar Azul
"""

from win10toast import ToastNotifier
import time

print("🔔 Probando notificaciones de Windows...")
print("=" * 50)

toaster = ToastNotifier()

# Notificación de prueba 1
print("\n1️⃣ Mostrando notificación de prueba básica...")
toaster.show_toast(
    "Azul Assistant - Prueba",
    "Si ves esto, las notificaciones funcionan correctamente!",
    duration=5,
    threaded=False
)

print("✅ Primera notificación completada")
time.sleep(2)

# Notificación de prueba 2 - Recordatorio
print("\n2️⃣ Simulando recordatorio urgente...")
toaster.show_toast(
    "⚠️ RECORDATORIO URGENTE",
    "Prueba de evento - Hora: 10:05 PM (En 5 minutos)",
    duration=10,
    threaded=False
)

print("✅ Segunda notificación completada")
print("\n" + "=" * 50)
print("✨ Si viste ambas notificaciones, todo funciona bien!")
print("🚀 Ahora puedes usar Azul con confianza.")
print("\nEjecuta: python jarvis_funcional.py")
