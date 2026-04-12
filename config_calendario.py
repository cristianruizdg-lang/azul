"""
Configuración del Sistema de Calendario de Azul
Puedes modificar estos valores para personalizar el comportamiento
"""

# ===========================
# CONFIGURACIÓN DE NOTIFICACIONES
# ===========================

# Tiempos de notificación por defecto (en minutos antes del evento)
# 0 = momento exacto del evento
NOTIFICACIONES_DEFAULT = [30, 10, 5, 0]

# Puedes personalizar por tipo de evento:
NOTIFICACIONES_POR_TIPO = {
    'cita': [60, 30, 10, 0],      # Citas importantes: aviso con más tiempo + momento exacto
    'alarma': [5, 1, 0],           # Alarmas: notificaciones muy cercanas + momento exacto
    'recordatorio': [30, 10, 0]    # Recordatorios: notificaciones moderadas + momento exacto
}

# Intervalo de revisión del monitor (en segundos)
# Menor = más preciso pero más CPU
# Mayor = menos preciso pero menos CPU
INTERVALO_MONITOR = 30  # segundos


# ===========================
# CONFIGURACIÓN DE LIMPIEZA
# ===========================

# Días que deben pasar para eliminar eventos completados
DIAS_LIMPIEZA = 7

# ¿Limpiar automáticamente al cargar?
LIMPIEZA_AUTOMATICA = True


# ===========================
# CONFIGURACIÓN DE IA
# ===========================

# Modelo de IA a usar (debe estar instalado en Ollama)
MODELO_IA = 'llama3'

# Modelos alternativos (si llama3 no está disponible)
MODELOS_FALLBACK = ['llama2', 'mistral']

# Temperatura para generación de notificaciones (0.0 - 1.0)
# Menor = más consistente y formal
# Mayor = más creativo y variado
TEMPERATURA_NOTIFICACIONES = 0.7


# ===========================
# CONFIGURACIÓN DE COMENTARIOS PROACTIVOS
# ===========================

# ¿Activar comentarios proactivos?
COMENTARIOS_PROACTIVOS_ACTIVOS = True

# Reglas de timing para comentarios proactivos
# (minutos_hasta_evento, minutos_desde_ultima_mencion)
REGLAS_COMENTARIOS = {
    'urgente': (10, 5),      # Evento en menos de 10 min, mencionar cada 5 min
    'cercano': (30, 10),     # Evento en menos de 30 min, mencionar cada 10 min
    'proximo': (120, 30),    # Evento en menos de 2h, mencionar cada 30 min
}


# ===========================
# CONFIGURACIÓN DE ARCHIVOS
# ===========================

# Ubicación del archivo de calendario
RUTA_CALENDARIO = "data/calendario.json"

# Crear backup antes de guardar
CREAR_BACKUP = True

# Ubicación de backups
RUTA_BACKUPS = "data/backups/"

# Máximo de backups a mantener
MAX_BACKUPS = 5


# ===========================
# CONFIGURACIÓN DE FORMATO
# ===========================

# Formato de fecha para mostrar al usuario
FORMATO_FECHA = "%d/%m/%Y"

# Formato de hora para mostrar al usuario
FORMATO_HORA = "%H:%M"

# Formato de fecha y hora combinados
FORMATO_DATETIME = "%d/%m/%Y %H:%M"


# ===========================
# CONFIGURACIÓN DE PERSONALIZACIÓN
# ===========================

# Nombre del usuario (se puede obtener del perfil)
NOMBRE_USUARIO = "Cristian"  # Cambiar por tu nombre

# Nivel de formalidad en notificaciones (1-5)
# 1 = Muy casual ("Ey!", "Wey")
# 3 = Equilibrado
# 5 = Muy formal ("Estimado", "Le recuerdo")
NIVEL_FORMALIDAD = 3

# ¿Usar emojis en notificaciones?
USAR_EMOJIS = True

# ¿Usar humor en notificaciones? (basado en perfil)
USAR_HUMOR = True


# ===========================
# CONFIGURACIÓN DE CONTEXTO
# ===========================

# Horas a considerar como "eventos próximos" para contexto de IA
HORAS_EVENTOS_PROXIMOS = 24

# ¿Incluir eventos completados en el contexto?
INCLUIR_COMPLETADOS = False

# Máximo de eventos a incluir en el contexto
MAX_EVENTOS_CONTEXTO = 5


# ===========================
# CONFIGURACIÓN AVANZADA
# ===========================

# ¿Habilitar logging detallado?
DEBUG_MODE = False

# Ruta del archivo de log
LOG_FILE = "data/calendario.log"

# ¿Sincronizar con Supabase? (futuro)
SYNC_SUPABASE = False

# ¿Permitir eventos en el pasado?
PERMITIR_PASADO = False

# Zona horaria
TIMEZONE = "America/Mexico_City"  # Cambiar según tu ubicación


# ===========================
# CONFIGURACIÓN DE NOTIFICACIÓN POR VOZ
# ===========================

# Velocidad de habla para notificaciones (palabras por minuto)
# Azul habla más rápido en notificaciones urgentes
VELOCIDAD_VOZ_NORMAL = 185
VELOCIDAD_VOZ_URGENTE = 200

# Volumen de voz para notificaciones (0.0 - 1.0)
VOLUMEN_VOZ = 1.0


# ===========================
# TIPS DE CONFIGURACIÓN
# ===========================

"""
CÓMO USAR ESTA CONFIGURACIÓN:

1. Para eventos muy importantes:
   NOTIFICACIONES_POR_TIPO['cita'] = [120, 60, 30, 10, 5]
   (Te avisará: 2h, 1h, 30min, 10min y 5min antes)

2. Para trabajar de noche:
   INTERVALO_MONITOR = 60
   COMENTARIOS_PROACTIVOS_ACTIVOS = False
   (Menos interrupciones)

3. Para ser más productivo:
   NIVEL_FORMALIDAD = 5
   USAR_HUMOR = False
   (Notificaciones directas y serias)

4. Para diversión:
   NIVEL_FORMALIDAD = 1
   USAR_HUMOR = True
   USAR_EMOJIS = True
   (Notificaciones casuales y divertidas)

5. Para debugging:
   DEBUG_MODE = True
   (Ver todo lo que hace el sistema)
"""


# ===========================
# EXPORTAR CONFIGURACIÓN
# ===========================

def obtener_config():
    """Retorna un diccionario con toda la configuración"""
    return {
        'notificaciones': {
            'default': NOTIFICACIONES_DEFAULT,
            'por_tipo': NOTIFICACIONES_POR_TIPO,
            'intervalo_monitor': INTERVALO_MONITOR,
        },
        'limpieza': {
            'dias': DIAS_LIMPIEZA,
            'automatica': LIMPIEZA_AUTOMATICA,
        },
        'ia': {
            'modelo': MODELO_IA,
            'fallback': MODELOS_FALLBACK,
            'temperatura': TEMPERATURA_NOTIFICACIONES,
        },
        'comentarios_proactivos': {
            'activos': COMENTARIOS_PROACTIVOS_ACTIVOS,
            'reglas': REGLAS_COMENTARIOS,
        },
        'archivos': {
            'calendario': RUTA_CALENDARIO,
            'backup': CREAR_BACKUP,
            'ruta_backups': RUTA_BACKUPS,
            'max_backups': MAX_BACKUPS,
        },
        'formato': {
            'fecha': FORMATO_FECHA,
            'hora': FORMATO_HORA,
            'datetime': FORMATO_DATETIME,
        },
        'personalizacion': {
            'nombre_usuario': NOMBRE_USUARIO,
            'formalidad': NIVEL_FORMALIDAD,
            'emojis': USAR_EMOJIS,
            'humor': USAR_HUMOR,
        },
        'contexto': {
            'horas_proximos': HORAS_EVENTOS_PROXIMOS,
            'incluir_completados': INCLUIR_COMPLETADOS,
            'max_eventos': MAX_EVENTOS_CONTEXTO,
        },
        'avanzado': {
            'debug': DEBUG_MODE,
            'log_file': LOG_FILE,
            'sync_supabase': SYNC_SUPABASE,
            'permitir_pasado': PERMITIR_PASADO,
            'timezone': TIMEZONE,
        },
        'voz': {
            'velocidad_normal': VELOCIDAD_VOZ_NORMAL,
            'velocidad_urgente': VELOCIDAD_VOZ_URGENTE,
            'volumen': VOLUMEN_VOZ,
        }
    }


def aplicar_config(config_dict):
    """
    Aplica una configuración desde un diccionario
    Útil para cargar configuraciones guardadas
    """
    global NOTIFICACIONES_DEFAULT, INTERVALO_MONITOR, MODELO_IA
    # Implementar según necesidad
    pass
