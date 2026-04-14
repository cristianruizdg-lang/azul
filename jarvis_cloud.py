import threading
import queue
import customtkinter as ctk
import speech_recognition as sr
import math
import time
import numpy as np
import random
import traceback
from supabase import create_client, Client
from datetime import datetime, timedelta
# from modules import GestorCalendario, AnalizadorCalendario, GeneradorNotificacionesInteligentes  # Deshabilitado en versión cloud (usa Ollama)
import pygame
import os
import asyncio
import edge_tts
import tempfile
import requests
from typing import Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Notificaciones del sistema
try:
    from win10toast import ToastNotifier
    toaster = ToastNotifier()
    NOTIFICACIONES_SISTEMA_DISPONIBLES = True
    print("✅ Sistema de notificaciones de Windows activado")
except ImportError:
    NOTIFICACIONES_SISTEMA_DISPONIBLES = False
    toaster = None
    print("⚠️  win10toast no instalado. Instala con: pip install win10toast")

# --- CONFIGURACIÓN DE API CLOUD ---
API_URL = os.getenv("API_URL", "https://azul-4xsp.onrender.com")
print(f"🌐 Usando backend: {API_URL}")

# --- CONFIGURACIÓN DE SUPABASE CLOUD ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# === CLIENTE DE API ===
class AzulApiClient:
    """Cliente para comunicarse con el backend de Azul en la nube"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.timeout = 30
        self.user_id = "desktop_user"
        
        # Verificar conectividad
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                health = response.json()
                print(f"✅ Backend conectado: v{health['version']} - {health['status']}")
        except Exception as e:
            print(f"⚠️  Error conectando al backend: {e}")
    
    def enviar_mensaje(self, texto: str, stream: bool = False) -> dict:
        """Envía un mensaje al chat y recibe respuesta"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/chat/message",
                json={
                    "message": texto,
                    "user_id": self.user_id,
                    "stream": stream
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error enviando mensaje: {e}")
            return {"text": "Lo siento, hubo un error conectando al servidor.", "audio_urls": []}
    
    def descargar_audio(self, audio_url: str) -> Optional[str]:
        """Descarga un archivo de audio y lo guarda temporalmente"""
        try:
            full_url = f"{self.base_url}{audio_url}" if audio_url.startswith('/') else audio_url
            response = self.session.get(full_url, timeout=10)
            response.raise_for_status()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
                temp_audio.write(response.content)
                return temp_audio.name
        except Exception as e:
            print(f"⚠️  Error descargando audio: {e}")
            return None

# Instancia global del cliente API
api_client = AzulApiClient(API_URL)

# === CLASES DUMMY PARA MÓDULOS DE CALENDARIO (no disponibles en cloud) ===
# Los módulos de calendario requieren Ollama local para análisis de lenguaje natural
class GestorCalendario:
    """Mock para funcionalidad de calendario"""
    def __init__(self, *args, **kwargs):
        self.eventos = []
    def obtener_contexto_para_ia(self): return "No hay eventos programados"
    def obtener_eventos_proximos(self, *args, **kwargs): return []
    def obtener_eventos_hoy(self): return []
    def agregar_evento(self, *args, **kwargs): return None
    def eliminar_evento(self, *args, **kwargs): return False
    def registrar_callback_notificacion(self, *args, **kwargs): pass
    def iniciar_monitor(self): pass

class AnalizadorCalendario:
    """Mock para análisis de calendario"""
    def __init__(self, *args, **kwargs): pass
    def es_consulta(self, texto): return False
    def analizar_consulta(self, texto): return None
    def formatear_eventos(self, *args, **kwargs): return "Calendario no disponible en cloud"
    def interpretar_comando(self, texto): return None

class GeneradorNotificacionesInteligentes:
    """Mock para notificaciones"""
    def __init__(self, *args, **kwargs): pass
    def actualizar_perfil(self, *args, **kwargs): pass
    def generar_notificacion(self, *args, **kwargs): return "Evento próximo"

# --- CONFIGURACIÓN DE VOZ NATURAL ---
esta_hablando = False
usuario_interrumpiendo = False
nombre_asistente = "azul"

# Voz neural de Edge TTS (mucho más natural que pyttsx3)
VOZ_AZUL = "es-MX-DaliaNeural"  # Voz femenina mexicana muy natural
# Alternativas: "es-ES-ElviraNeural" (España), "es-AR-ElenaNeural" (Argentina)

cola_voz = queue.Queue()

async def hablar_async(texto: str):
    """Genera y reproduce audio con Edge TTS (voz neural natural)"""
    global esta_hablando, usuario_interrumpiendo
    try:
        esta_hablando = True
        usuario_interrumpiendo = False
        
        # Crear archivo temporal para el audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
            temp_path = temp_audio.name
        
        # Generar audio con Edge TTS
        communicate = edge_tts.Communicate(texto, VOZ_AZUL, rate='+10%', pitch='+0Hz')
        await communicate.save(temp_path)
        
        # Reproducir audio con pygame
        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        
        # Esperar a que termine O detectar interrupción
        while pygame.mixer.music.get_busy() and not usuario_interrumpiendo:
            await asyncio.sleep(0.1)
        
        # Si hubo interrupción, detener inmediatamente
        if usuario_interrumpiendo:
            pygame.mixer.music.stop()
            print("🛑 Azul interrumpida por usuario")
        
        # Limpiar archivo temporal
        try:
            os.unlink(temp_path)
        except:
            pass
            
        esta_hablando = False
    except Exception as e:
        print(f"⚠️ Error en síntesis de voz: {e}")
        esta_hablando = False

def hilo_hablar():
    """Hilo que procesa la cola de voz"""
    # Crear event loop para este hilo
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    while True:
        texto = cola_voz.get()
        if texto is None:
            break
        try:
            # Ejecutar la función async en el event loop
            loop.run_until_complete(hablar_async(texto))
        except Exception as e:
            print(f"⚠️ Error en hilo de voz: {e}")
        cola_voz.task_done()
    
    loop.close()

threading.Thread(target=hilo_hablar, daemon=True).start()

# --- SISTEMA DE SONIDO ---
pygame.mixer.init()

def reproducir_sonido(archivo):
    """Reproduce un sonido de forma asíncrona"""
    def _reproducir():
        try:
            if os.path.exists(archivo):
                sonido = pygame.mixer.Sound(archivo)
                sonido.play()
        except Exception as e:
            print(f"⚠️ No se pudo reproducir sonido: {e}")
    
    threading.Thread(target=_reproducir, daemon=True).start()

# --- FUNCIÓN PARA OBTENER CLIMA ---
def obtener_clima() -> Optional[dict]:
    """Obtiene información del clima actual"""
    try:
        # API gratuita de wttr.in (no requiere key)
        response = requests.get('https://wttr.in/?format=j1', timeout=3)
        if response.status_code == 200:
            data = response.json()
            current = data['current_condition'][0]
            return {
                'temperatura': current['temp_C'],
                'descripcion': current['lang_es'][0]['value'] if 'lang_es' in current else current['weatherDesc'][0]['value'],
                'ciudad': data['nearest_area'][0]['areaName'][0]['value']
            }
    except Exception as e:
        print(f"⚠️ No se pudo obtener clima: {e}")
    return None

# --- CLASE PRINCIPAL ---
class AzulGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"{nombre_asistente.upper()} v3.0 - Cloud Edition")
        self.geometry("1200x700")
        ctk.set_appearance_mode("light")
        
        # Variables de animación de inicio
        self.animacion_inicio_activa = True
        self.alpha_inicio = 0.0
        self.brillo_esfera_inicio = 0.0
        self.sonido_reproducido = False  # Control para reproducir sonido solo una vez
        
        # Estado de pantalla de bienvenida
        self.en_bienvenida = True
        self.bienvenida_alpha = 0.0
        
        # Empezar invisible
        self.attributes('-alpha', 0.0)
        
        # El sistema ahora incluye instrucciones de aprendizaje
        self.contexto_usuario = "" 
        self.actualizar_instrucciones_sistema()
        
        # --- MÓDULOS DE CALENDARIO (versión dummy en cloud) ---
        # Los módulos usan versiones simplificadas que no requieren Ollama
        self.gestor_calendario = GestorCalendario(archivo_datos="data/calendario.json")
        self.analizador_calendario = AnalizadorCalendario(modelo='cloud')
        self.generador_notificaciones = GeneradorNotificacionesInteligentes(
            modelo='cloud', 
            perfil_usuario=self.contexto_usuario
        )
        self.gestor_calendario.registrar_callback_notificacion(self.manejar_notificacion_evento)
        self.gestor_calendario.iniciar_monitor()
        
        # Control de menciones proactivas
        self.ultima_mencion_eventos = datetime.now()
        
        # Control de menciones de temas/gustos (para evitar spam de humor)
        self.ultimas_menciones_temas = {}  # {tema: timestamp}
        self.cooldown_mencion_tema = 600  # 10 minutos entre menciones del mismo tema
        # --- FIN MÓDULOS DE CALENDARIO ---
        
        self.reconocedor = sr.Recognizer()
        self.datos_espectro = [0] * 20
        
        # Control de modo de conversación
        self.modo_conversacion_activo = False
        self.tiempo_ultima_interaccion = None
        self.timeout_conversacion = 30  # segundos

        # Configuración esfera
        self.puntos_esfera = []
        self.angulo_rotacion = 0
        self.generar_puntos_esfera()
        
        # Control de scrollbar animado
        self.scrollbar_visible = False
        self.scrollbar_alpha = 0.0
        self.scrollbar_timer = None

        # === PANTALLA DE BIENVENIDA ===
        self.crear_pantalla_bienvenida()
        
        # UI LAYOUT - Todo centrado en tareas (se crea pero oculto al inicio)
        self.configure(fg_color="#ffffff")
        
        # Configurar grid principal: diseño centrado
        self.grid_columnconfigure(0, weight=1)  # Centrado
        self.grid_rowconfigure(0, weight=1)  # Contenido principal
        self.grid_rowconfigure(1, weight=0)  # Footer input
        
        # === CONTENEDOR PRINCIPAL CENTRADO ===
        self.main_container = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0)
        self.main_container.grid(row=0, column=0, sticky="nsew")
        self.main_container.grid_rowconfigure(1, weight=1)  # Lista tareas expandible
        self.main_container.grid_columnconfigure(0, weight=1)  # Expandir columna horizontalmente
        
        # Header de tareas - centrado con mínimo padding
        header_tareas = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_tareas.grid(row=0, column=0, sticky="ew", padx=30, pady=(40, 30))
        
        titulo_tareas = ctk.CTkLabel(header_tareas, text="Tareas pendientes", 
                                     font=("Arial", 32, "normal"), text_color="#1a1a1a")
        titulo_tareas.pack(side="left")
        
        self.btn_history = ctk.CTkButton(header_tareas, text="⋯", width=40, height=40,
                                         command=self.mostrar_historial,
                                         fg_color="transparent", hover_color="#f0f0f0", 
                                         corner_radius=20, font=("Arial", 20),
                                         text_color="#666666", border_width=0)
        self.btn_history.pack(side="right")
        
        # Lista de tareas scrollable - máxima extensión horizontal con scrollbar sutil
        self.tareas_frame = ctk.CTkScrollableFrame(
            self.main_container, 
            fg_color="transparent", 
            corner_radius=0,
            scrollbar_button_color="#ffffff",  # Invisible por defecto
            scrollbar_button_hover_color="#d0d0d0"  # Visible solo en hover
        )
        self.tareas_frame.grid(row=1, column=0, sticky="nsew", padx=(30, 220), pady=(0, 20))  # Padding derecho mayor para evitar el icono de Azul
        
        # Botón + fijo en la esquina inferior derecha
        self.btn_add_task = ctk.CTkButton(self.main_container, text="+", 
                                          command=self.mostrar_formulario_tarea,
                                          fg_color="#000000", hover_color="#333333",
                                          corner_radius=30, width=60, height=60, 
                                          font=("Arial", 28, "normal"),
                                          text_color="#ffffff")
        self.btn_add_task.place(relx=0.95, rely=0.90, anchor="se")
        
        # === AZUL FLOTANTE (MARCA DE AGUA) ===
        # Canvas esfera como overlay en esquina superior derecha (más hacia la esquina)
        self.canvas_esfera = ctk.CTkCanvas(self, bg="#ffffff", 
                                           highlightthickness=0, width=180, height=180)
        self.canvas_esfera.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)
        
        # Canvas espectro discreto en la parte inferior del contenedor
        self.canvas_espectro = ctk.CTkCanvas(self.main_container, bg="#ffffff", 
                                             height=40, highlightthickness=0)
        self.canvas_espectro.grid(row=2, column=0, sticky="ew", padx=30, pady=(0, 20))
        
        # === FOOTER: INPUT ===
        self.footer = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0, height=90)
        self.footer.grid(row=1, column=0, sticky="ew")
        self.footer.grid_columnconfigure(0, weight=1)
        self.footer.grid_columnconfigure(1, weight=0)
        self.footer.grid_columnconfigure(2, weight=1)
        
        # Separador sutil
        separator = ctk.CTkFrame(self.footer, fg_color="#f0f0f0", height=1)
        separator.grid(row=0, column=0, columnspan=3, sticky="ew")
        
        # Espaciador izquierdo
        ctk.CTkLabel(self.footer, text="").grid(row=1, column=0)
        
        # Input centrado con ancho máximo
        self.entry_user = ctk.CTkEntry(self.footer, placeholder_text=f"Escribe algo...", 
                                       height=50, border_color="#e0e0e0", border_width=1, 
                                       corner_radius=25, font=("Arial", 13),
                                       fg_color="#fafafa", text_color="#1a1a1a",
                                       width=700)
        self.entry_user.grid(row=1, column=1, pady=20)
        self.entry_user.bind("<Return>", lambda e: self.enviar_mensaje())
        
        # Espaciador derecho
        ctk.CTkLabel(self.footer, text="").grid(row=1, column=2)

        # Cargar tareas inicialmente
        self.actualizar_lista_tareas_main()
        
        # Configurar animación de scrollbar
        self.configurar_scrollbar_animado()
        
        # Ocultar interfaz principal al inicio
        self.main_container.grid_remove()
        self.canvas_esfera.place_forget()
        self.footer.grid_remove()
        
        # Iniciar con pantalla de bienvenida
        self.animar_bienvenida_fade_in()
        self.cargar_datos_aprendizaje()
        threading.Thread(target=self.escucha_pasiva, daemon=True).start()
    
    def crear_pantalla_bienvenida(self):
        """Crea la interfaz de bienvenida elegante con gradiente radial y círculos concéntricos"""
        # Frame principal de bienvenida (cubre toda la ventana)
        self.bienvenida_frame = ctk.CTkFrame(self, fg_color="#0a0a14", corner_radius=0)
        self.bienvenida_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")
        
        # Canvas para fondo con gradiente radial (efecto blur)
        self.canvas_blur = ctk.CTkCanvas(self.bienvenida_frame, bg="#0a0a14", highlightthickness=0)
        self.canvas_blur.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Crear gradiente radial con círculos concéntricos
        def crear_gradiente_radial():
            w = self.winfo_width()
            h = self.winfo_height()
            if w > 1 and h > 1:
                center_x, center_y = w / 2, h / 2
                max_radius = math.sqrt(center_x**2 + center_y**2)
                
                # Dibujar círculos concéntricos desde el centro
                num_circles = 35
                for i in range(num_circles, 0, -1):
                    radius = (i / num_circles) * max_radius
                    
                    # Gradiente de #0a0a14 (centro oscuro) a #16213e (exterior azul)
                    progreso = 1 - (i / num_circles)
                    r = int(10 + (22 - 10) * progreso)
                    g = int(10 + (33 - 10) * progreso)
                    b = int(20 + (62 - 20) * progreso)
                    color = f"#{r:02x}{g:02x}{b:02x}"
                    
                    # Dibujar círculo
                    x0, y0 = center_x - radius, center_y - radius
                    x1, y1 = center_x + radius, center_y + radius
                    self.canvas_blur.create_oval(x0, y0, x1, y1, fill=color, outline="")
        
        # Ejecutar después de que la ventana tenga tamaño
        self.after(100, crear_gradiente_radial)
        
        # Overlay sutil
        self.overlay = ctk.CTkFrame(self.bienvenida_frame, fg_color="transparent", corner_radius=0)
        self.overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Contenedor central para el contenido
        content_container = ctk.CTkFrame(self.overlay, fg_color="transparent")
        content_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Obtener hora actual para saludo
        hora_actual = datetime.now().hour
        if 5 <= hora_actual < 12:
            saludo = "Buenos días"
        elif 12 <= hora_actual < 19:
            saludo = "Buenas tardes"
        else:
            saludo = "Buenas noches"
        
        # === TÍTULO CON EFECTO DE PROFUNDIDAD ===
        titulo_container = ctk.CTkFrame(content_container, fg_color="transparent")
        titulo_container.pack(pady=(0, 15))
        
        # Múltiples capas de sombra para efecto 3D sutil
        for offset in [(0, 4), (0, 3), (0, 2)]:
            sombra = ctk.CTkLabel(titulo_container, text="BIENVENIDO",
                font=("Segoe UI", 72, "bold"), text_color="#050a10")
            sombra.place(relx=0.5, rely=0.5, anchor="center", x=offset[0], y=offset[1])
        
        # Texto principal
        titulo = ctk.CTkLabel(titulo_container, text="BIENVENIDO",
            font=("Segoe UI", 72, "bold"), text_color="#ffffff")
        titulo.place(relx=0.5, rely=0.5, anchor="center")
        
        titulo_container.configure(width=700, height=110)
        
        # Línea de acento cyan ultra-delgada
        linea_acento = ctk.CTkFrame(content_container, fg_color="#00d4ff", height=1, width=180)
        linea_acento.pack(pady=(0, 50))
        
        # === SALUDO ===
        saludo_container = ctk.CTkFrame(content_container, fg_color="transparent")
        saludo_container.pack(pady=(0, 55))
        
        # Sombra doble
        for offset in [(0, 2), (0, 1)]:
            saludo_sombra = ctk.CTkLabel(saludo_container, text=saludo,
                font=("Segoe UI", 26, "normal"), text_color="#0a0f14")
            saludo_sombra.place(relx=0.5, rely=0.5, anchor="center", x=offset[0], y=offset[1])
        
        saludo_label = ctk.CTkLabel(saludo_container, text=saludo,
            font=("Segoe UI", 26, "normal"), text_color="#9ab0c5")
        saludo_label.place(relx=0.5, rely=0.5, anchor="center")
        
        saludo_container.configure(width=420, height=50)
        
        # === HORA CON ACENTO CYAN ===
        hora_str = datetime.now().strftime("%I:%M %p").lstrip("0")
        hora_container = ctk.CTkFrame(content_container, fg_color="transparent")
        hora_container.pack(pady=(0, 40))
        
        # Sombra doble
        for offset in [(0, 3), (0, 2)]:
            hora_sombra = ctk.CTkLabel(hora_container, text=hora_str,
                font=("Segoe UI", 56, "bold"), text_color="#050a10")
            hora_sombra.place(relx=0.5, rely=0.5, anchor="center", x=offset[0], y=offset[1])
        
        hora_label = ctk.CTkLabel(hora_container, text=hora_str,
            font=("Segoe UI", 56, "bold"), text_color="#00d4ff")
        hora_label.place(relx=0.5, rely=0.5, anchor="center")
        
        hora_container.configure(width=360, height=80)
        
        # === CLIMA ===
        clima_container = ctk.CTkFrame(content_container, fg_color="transparent")
        clima_container.pack(pady=(0, 0))
        
        # Sombra
        self.clima_sombra = ctk.CTkLabel(clima_container, text="Obteniendo clima...",
            font=("Segoe UI", 15, "normal"), text_color="#0a0f14")
        self.clima_sombra.place(relx=0.5, rely=0.5, anchor="center", x=0, y=1)
        
        self.clima_label = ctk.CTkLabel(clima_container, text="Obteniendo clima...",
            font=("Segoe UI", 15, "normal"), text_color="#6a7a8a")
        self.clima_label.place(relx=0.5, rely=0.5, anchor="center")
        
        clima_container.configure(width=580, height=45)
        
        # Cargar clima asíncronamente
        threading.Thread(target=self.actualizar_clima_bienvenida, daemon=True).start()
    
    def actualizar_clima_bienvenida(self):
        """Actualiza la información del clima en la pantalla de bienvenida"""
        clima = obtener_clima()
        if clima:
            texto_clima = f"{clima['temperatura']}°C • {clima['descripcion']}"
            if clima['ciudad']:
                texto_clima += f" • {clima['ciudad']}"
            self.after(0, lambda: self.clima_label.configure(text=texto_clima))
            self.after(0, lambda: self.clima_sombra.configure(text=texto_clima))
        else:
            self.after(0, lambda: self.clima_label.configure(text="Clima no disponible"))
            self.after(0, lambda: self.clima_sombra.configure(text="Clima no disponible"))
    
    def animar_bienvenida_fade_in(self):
        """Animación de entrada de la pantalla de bienvenida"""
        # Reproducir sonido al inicio
        if not self.sonido_reproducido:
            reproducir_sonido("assets/sounds/startup.wav")
            self.sonido_reproducido = True
        
        if self.bienvenida_alpha < 1.0:
            self.bienvenida_alpha = min(1.0, self.bienvenida_alpha + 0.02)
            self.attributes('-alpha', self.bienvenida_alpha)
            self.after(30, self.animar_bienvenida_fade_in)
        else:
            # Mantener bienvenida por 5 segundos
            self.after(5000, self.iniciar_transicion_a_principal)
    
    def iniciar_transicion_a_principal(self):
        """Inicia la transición de bienvenida a interfaz principal"""
        self.en_bienvenida = False
        self.animar_bienvenida_fade_out()
    
    def animar_bienvenida_fade_out(self):
        """Animación de salida de la pantalla de bienvenida"""
        if self.bienvenida_alpha > 0.0:
            self.bienvenida_alpha = max(0.0, self.bienvenida_alpha - 0.03)
            self.attributes('-alpha', self.bienvenida_alpha)
            self.after(20, self.animar_bienvenida_fade_out)
        else:
            # Ocultar bienvenida y mostrar interfaz principal
            self.bienvenida_frame.grid_forget()
            self.overlay.place_forget()
            
            # Mostrar interfaz principal
            self.main_container.grid(row=0, column=0, sticky="nsew")
            self.canvas_esfera.place(relx=1.0, rely=0.0, anchor="ne", x=-20, y=20)
            self.footer.grid(row=1, column=0, sticky="ew")
            
            # Iniciar fade in de interfaz principal y animación de esfera
            self.alpha_inicio = 0.0
            self.fade_in_inicio()
            self.animar_todo()
    
    def fade_in_inicio(self):
        """Animación de entrada elegante con fade in de la interfaz principal"""
        if self.alpha_inicio < 1.0:
            # Incrementar opacidad de ventana
            self.alpha_inicio += 0.015  # Más lento y suave
            self.attributes('-alpha', self.alpha_inicio)
            
            # Incrementar brillo de esfera gradualmente
            self.brillo_esfera_inicio = min(1.0, self.brillo_esfera_inicio + 0.02)
            
            self.after(30, self.fade_in_inicio)  # 30ms para suavidad extra
        else:
            # Terminar animación de inicio
            self.animacion_inicio_activa = False
    
    def configurar_scrollbar_animado(self):
        """Configura la animación del scrollbar para aparecer/desaparecer"""
        # Bind para detectar scroll (con rueda del mouse o barra)
        self.tareas_frame.bind("<Enter>", self.on_scroll_area_enter)
        self.tareas_frame.bind("<Leave>", self.on_scroll_area_leave)
        self.tareas_frame.bind_all("<MouseWheel>", self.on_mouse_scroll)
    
    def on_scroll_area_enter(self, event):
        """Cuando el mouse entra en el área de scroll"""
        pass
    
    def on_scroll_area_leave(self, event):
        """Cuando el mouse sale del área de scroll"""
        self.iniciar_fade_out_scrollbar()
    
    def on_mouse_scroll(self, event):
        """Detecta cuando se hace scroll con la rueda del mouse"""
        # Verificar si el mouse está sobre el área de tareas
        x, y = self.winfo_pointerx(), self.winfo_pointery()
        widget_x, widget_y = self.tareas_frame.winfo_rootx(), self.tareas_frame.winfo_rooty()
        widget_width, widget_height = self.tareas_frame.winfo_width(), self.tareas_frame.winfo_height()
        
        if (widget_x <= x <= widget_x + widget_width and 
            widget_y <= y <= widget_y + widget_height):
            self.mostrar_scrollbar()
    
    def mostrar_scrollbar(self):
        """Muestra el scrollbar con fade in"""
        if not self.scrollbar_visible:
            self.scrollbar_visible = True
            self.animar_scrollbar_fade_in()
        
        # Cancelar timer anterior si existe
        if self.scrollbar_timer:
            self.after_cancel(self.scrollbar_timer)
        
        # Programar fade out después de 1 segundo de inactividad
        self.scrollbar_timer = self.after(1000, self.iniciar_fade_out_scrollbar)
    
    def animar_scrollbar_fade_in(self):
        """Animación de aparición del scrollbar"""
        if self.scrollbar_alpha < 1.0:
            self.scrollbar_alpha = min(1.0, self.scrollbar_alpha + 0.15)
            
            # Calcular color interpolado (de #ffffff a #d0d0d0)
            gray_value = int(255 - (self.scrollbar_alpha * (255 - 208)))
            color = f"#{gray_value:02x}{gray_value:02x}{gray_value:02x}"
            
            # Actualizar color del scrollbar
            self.tareas_frame.configure(scrollbar_button_color=color)
            
            self.after(30, self.animar_scrollbar_fade_in)
    
    def iniciar_fade_out_scrollbar(self):
        """Inicia la animación de desaparición del scrollbar"""
        self.scrollbar_visible = False
        self.animar_scrollbar_fade_out()
    
    def animar_scrollbar_fade_out(self):
        """Animación de desaparición del scrollbar"""
        if self.scrollbar_alpha > 0.0:
            self.scrollbar_alpha = max(0.0, self.scrollbar_alpha - 0.1)
            
            # Calcular color interpolado (de #d0d0d0 a #ffffff)
            gray_value = int(255 - (self.scrollbar_alpha * (255 - 208)))
            color = f"#{gray_value:02x}{gray_value:02x}{gray_value:02x}"
            
            # Actualizar color del scrollbar
            self.tareas_frame.configure(scrollbar_button_color=color)
            
            self.after(30, self.animar_scrollbar_fade_out)

    def actualizar_instrucciones_sistema(self):
        # Obtener contexto de eventos del calendario
        contexto_eventos = ""
        if hasattr(self, 'gestor_calendario'):
            contexto_eventos = self.gestor_calendario.obtener_contexto_para_ia()
        
        # Prompt OPTIMIZADO - Más corto = respuestas más rápidas
        instrucciones = f"""Eres Azul, amiga cercana del usuario. Natural, directa, concisa.

REGLAS BÁSICAS:
- MÁXIMO 2-3 frases cortas
- Tono cálido y cercano
- Nunca formal/robótica

PERFIL DEL USUARIO:
{self.contexto_usuario if self.contexto_usuario else "Aún aprendiendo sobre el usuario"}

IMPORTANTE - USO DEL PERFIL:
- USA este conocimiento para personalizar respuestas
- Menciona gustos/hobbies SOLO cuando:
  1. El usuario los mencione primero
  2. Sean directamente relevantes
  3. Haya pasado suficiente tiempo desde última mención
- NO fuerces temas ni bromas repetitivas
- La información está para PERSONALIZAR, no para MENCIONAR constantemente

EVENTOS:
{contexto_eventos}

CALENDARIO:
- [SISTEMA] → Confirma breve
- [CONSULTA CALENDARIO] → Complementa breve
- No inventes eventos

Recuerda: Conoce al usuario, pero no lo acoses con sus gustos. Usa tu conocimiento para adaptar tu tono y respuestas."""
        self.historial = [{"role": "system", "content": instrucciones}]


    
    def _puede_mencionar_tema(self, tema: str) -> bool:
        """Verifica si puede mencionar un tema según el cooldown"""
        if tema not in self.ultimas_menciones_temas:
            return True
        
        tiempo_transcurrido = (datetime.now() - self.ultimas_menciones_temas[tema]).total_seconds()
        return tiempo_transcurrido >= self.cooldown_mencion_tema
    
    def _registrar_mencion_tema(self, texto: str):
        """Registra cuando se menciona un tema para aplicar cooldown"""
        # Detectar menciones de temas conocidos en la respuesta
        texto_lower = texto.lower()
        
        temas_conocidos = ['rocket league', 'videojuegos', 'gaming', 'juegos']
        for tema in temas_conocidos:
            if tema in texto_lower:
                self.ultimas_menciones_temas[tema] = datetime.now()
                print(f"📝 Tema '{tema}' mencionado - cooldown de {self.cooldown_mencion_tema}s activado")
    
    def cargar_datos_aprendizaje(self):
        """Carga gustos y hábitos desde Supabase para personalizar a Azul."""
        try:
            print("📚 Cargando conocimiento del usuario desde Supabase...")
            
            # Cargar historial de chat (últimos 50 mensajes para contexto)
            res_chat = supabase.table("mensajes_chat").select("role, content").order("created_at", desc=True).limit(50).execute()
            
            # Invertir para orden cronológico
            mensajes_ordenados = list(reversed(res_chat.data))
            for msg in mensajes_ordenados:
                self.historial.append(msg)
            
            print(f"   ✅ {len(mensajes_ordenados)} mensajes del historial cargados")
            
            # Cargar perfil (hábitos/gustos)
            res_perfil = supabase.table("perfil_usuario").select("clave, valor").execute()
            if res_perfil.data:
                perfil = "\n".join([f"- {item['clave']}: {item['valor']}" for item in res_perfil.data])
                self.contexto_usuario = perfil
                print(f"   ✅ Perfil del usuario cargado:")
                print(f"      {perfil}")
            else:
                self.contexto_usuario = ""
                print(f"   ⚠️  No hay perfil de usuario aún")
            
            self.actualizar_instrucciones_sistema()
            
            # Actualizar perfil en generador de notificaciones
            if hasattr(self, 'generador_notificaciones'):
                self.generador_notificaciones.actualizar_perfil(self.contexto_usuario)
            
            print("✅ Conocimiento cargado exitosamente\n")
        except Exception as e:
            print(f"⚠️  Error cargando datos: {e}")
            pass

    def aprendizaje_en_tiempo_real(self, texto):
        """Extrae gustos o hábitos del texto del usuario usando el backend."""
        # NOTA: Esta función está simplificada en la versión cloud.
        # El backend ya aprende automáticamente del contexto de la conversación.
        # Aquí solo hacemos aprendizaje básico por patrones simples.
        
        # Detección de patrones simples sin IA (para no sobrecargar la API)
        texto_lower = texto.lower()
        
        # Patrones comunes
        if "me gusta" in texto_lower or "me encanta" in texto_lower:
            palabras = texto.split()
            for i, palabra in enumerate(palabras):
                if palabra.lower() in ["gusta", "encanta"] and i + 1 < len(palabras):
                    tema = palabras[i + 1]
                    clave = "le_gusta"
                    valor = tema
                    print(f"🧠 Aprendizaje simple: {clave} → {valor}")
                    threading.Thread(target=lambda: supabase.table("perfil_usuario").upsert(
                        {"clave": clave, "valor": valor}, on_conflict="clave").execute(), daemon=True).start()
                    break
        
        # El aprendizaje profundo lo hace el backend cloud automáticamente
        # durante las conversaciones con Groq
        
        # Actualizar instrucciones (opcional, para refrescar contexto)
        self.actualizar_instrucciones_sistema()
    
    def agregar_contexto_tiempo_real(self, texto: str) -> bool:
        """
        Responde directamente preguntas comunes (sin IA) - RESPUESTAS INSTANTÁNEAS
        Retorna True si respondió, False si no
        """
        texto_lower = texto.lower()
        ahora = datetime.now()
        respuesta = None
        
        # 1. PREGUNTAS SOBRE HORA
        preguntas_hora = ['qué hora', 'que hora', 'hora es', 'dime la hora', 'cuál es la hora', 
                         'cual es la hora', 'me dices la hora', 'tienes la hora']
        
        if any(pregunta in texto_lower for pregunta in preguntas_hora):
            hora_actual = ahora.strftime("%I:%M %p").lstrip("0")
            respuesta = f"Son las {hora_actual}"
            print(f"⏰ Respuesta directa: {respuesta}")
        
        # 2. PREGUNTAS SOBRE FECHA
        elif any(palabra in texto_lower for palabra in ['qué día', 'que dia', 'qué fecha', 'que fecha', 
                                                         'día es hoy', 'dia es hoy', 'fecha es']):
            dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
            meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 
                    'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
            dia_semana = dias_semana[ahora.weekday()]
            mes = meses[ahora.month - 1]
            respuesta = f"Hoy es {dia_semana} {ahora.day} de {mes}"
            print(f"📅 Respuesta directa: {respuesta}")
        
        # 3. SALUDOS SIMPLES
        elif texto_lower in ['hola', 'hey', 'oye', 'azul']:
            respuestas_saludo = ['¡Hola! ¿Qué necesitas?', 'Aquí estoy', '¿Dime?', 'Te escucho']
            respuesta = respuestas_saludo[ahora.second % len(respuestas_saludo)]
            print(f"👋 Respuesta directa: {respuesta}")
        
        # 4. AGRADECIMIENTOS
        elif any(palabra in texto_lower for palabra in ['gracias', 'graciasgracias', 'grazie', 'thanks']):
            respuestas_gracias = ['De nada 😊', 'Cuando quieras', 'Para eso estoy', '¡Claro!']
            respuesta = respuestas_gracias[ahora.second % len(respuestas_gracias)]
            print(f"💝 Respuesta directa: {respuesta}")
        
        # 5. DESPEDIDAS
        elif any(palabra in texto_lower for palabra in ['adiós', 'adios', 'chao', 'bye', 'nos vemos']):
            respuestas_despedida = ['¡Hasta luego!', 'Nos vemos', 'Cuídate', 'Bye 👋']
            respuesta = respuestas_despedida[ahora.second % len(respuestas_despedida)]
            print(f"👋 Respuesta directa: {respuesta}")
        
        # Si hay respuesta directa, procesarla
        if respuesta:
            self.historial.append({"role": "assistant", "content": respuesta})
            cola_voz.put(respuesta)
            threading.Thread(target=lambda: supabase.table("mensajes_chat").insert(
                {"role": "assistant", "content": respuesta}
            ).execute(), daemon=True).start()
            return True
        
        return False

    def enviar_mensaje(self):
        texto = self.entry_user.get().strip()
        if not texto: return
        
        # Limpiar entry INMEDIATAMENTE y devolver foco
        self.entry_user.delete(0, "end")
        self.entry_user.focus_set()  # Foco inmediato para siguiente mensaje
        
        # Agregar mensaje del usuario al historial
        self.historial.append({"role": "user", "content": texto})
        
        # Responder directamente si pregunta por hora/fecha (sin IA) - SUPER RÁPIDO
        if self.agregar_contexto_tiempo_real(texto):
            # Asegurar que el entry siga con foco después de respuesta rápida
            self.after(100, lambda: self.entry_user.focus_set())
            return  # Ya respondió, no necesita IA
        
        # Procesar calendario PRIMERO (síncronamente) antes de que Azul responda
        evento_creado = self.procesar_calendario(texto)
        
        # TODO en paralelo para máxima velocidad:
        # 1. Aprendizaje (background, no afecta respuesta)
        threading.Thread(target=self.aprendizaje_en_tiempo_real, args=(texto,), daemon=True).start()
        
        # 2. Guardar en Supabase (background, no afecta respuesta)
        threading.Thread(target=lambda: supabase.table("mensajes_chat").insert(
            {"role": "user", "content": texto}
        ).execute(), daemon=True).start()
        
        # 3. Obtener respuesta de Azul (prioritario - respuesta rápida)
        threading.Thread(target=self.obtener_respuesta_ia, daemon=True).start()
        
        # Asegurar que el foco regrese después de iniciar el proceso
        self.after(50, lambda: self.entry_user.focus_set())

    # --- (Funciones de animación y voz se mantienen igual que v2.4) ---
    def generar_puntos_esfera(self):
        for i in range(200):
            phi = math.acos(-1 + (2 * i) / 200)
            theta = math.sqrt(200 * math.pi) * phi
            self.puntos_esfera.append([phi, theta])

    def dibujar_espectro(self):
        self.canvas_espectro.delete("spec")
        w, h = self.canvas_espectro.winfo_width(), self.canvas_espectro.winfo_height()
        n = len(self.datos_espectro)
        for i, v in enumerate(self.datos_espectro):
            alt = (v / 100) * h
            x0, x1 = i * (w/n) + 2, (i+1) * (w/n) - 2
            # Barras muy sutiles
            color = "#e0e0e0" if not esta_hablando else "#00d4ff"
            self.canvas_espectro.create_rectangle(x0, h-alt, x1, h, fill=color, outline="", tags="spec")

    def animar_todo(self):
        # No animar si estamos en la pantalla de bienvenida
        if self.en_bienvenida:
            self.after(20, self.animar_todo)
            return
            
        self.canvas_esfera.delete("all")
        w, h = self.canvas_esfera.winfo_width()/2, self.canvas_esfera.winfo_height()/2
        t = time.time()
        
        # Aplicar brillo gradual durante animación de inicio
        if self.animacion_inicio_activa:
            escala_base = 50 * self.brillo_esfera_inicio  # Muy pequeña para marca de agua
            escala = escala_base * (1 + math.sin(t*2)*0.03)
            # Color azul brillante al inicio
            intensidad = int(212 * self.brillo_esfera_inicio)
            color = f"#{0:02x}{intensidad:02x}{255:02x}"
        else:
            escala = 50 * (1 + ((math.sin(t*10)*0.1 + math.sin(t*25)*0.05) if esta_hablando else math.sin(t*2)*0.03))
            # Muy sutil, casi invisible cuando no habla
            color = "#00d4ff" if esta_hablando else "#e8e8e8"
        
        self.angulo_rotacion += 0.03 if esta_hablando else 0.008
        
        for phi, theta in self.puntos_esfera:
            x, y, z = math.cos(theta+self.angulo_rotacion)*math.sin(phi), math.sin(theta+self.angulo_rotacion)*math.sin(phi), math.cos(phi)
            sx, sy = x*escala+w, y*escala+h
            r = 1.5 + (z+1)*1.5
            
            # Aplicar opacity durante fade in
            if self.animacion_inicio_activa:
                # Crear color con alpha
                alpha_val = int(self.brillo_esfera_inicio * 255)
                color_alpha = f"#{0:02x}{int(212*self.brillo_esfera_inicio):02x}{int(255*self.brillo_esfera_inicio):02x}"
                self.canvas_esfera.create_oval(sx-r, sy-r, sx+r, sy+r, fill=color_alpha, outline="")
            else:
                self.canvas_esfera.create_oval(sx-r, sy-r, sx+r, sy+r, fill=color, outline="")
        
        self.dibujar_espectro()
        self.datos_espectro = [max(0, v - 5) for v in self.datos_espectro]
        self.after(20, self.animar_todo)

    def detener_voz_actual(self):
        """Detiene la voz de Azul inmediatamente (para interrupciones)"""
        global usuario_interrumpiendo, esta_hablando
        
        if esta_hablando:
            usuario_interrumpiendo = True
            # Limpiar cola de voz pendiente
            while not cola_voz.empty():
                try:
                    cola_voz.get_nowait()
                except:
                    break
            print("🛑 Voz de Azul detenida - Usuario interrumpiendo")
    
    def escucha_pasiva(self):
        """Sistema de escucha continua con modo conversación inteligente"""
        print("🎤 Iniciando sistema de escucha pasiva...")
        print("=" * 60)
        
        # Configurar reconocedor con parámetros optimizados
        self.reconocedor.energy_threshold = 4000
        self.reconocedor.dynamic_energy_threshold = True
        self.reconocedor.pause_threshold = 0.8
        self.reconocedor.phrase_threshold = 0.3
        self.reconocedor.non_speaking_duration = 0.5
        
        intentos_reconexion = 0
        max_intentos = 3
        
        while intentos_reconexion < max_intentos:
            try:
                with sr.Microphone() as source:
                    # Ajustar al ruido ambiente
                    print("🔧 Calibrando micrófono al ruido ambiente...")
                    self.reconocedor.adjust_for_ambient_noise(source, duration=2)
                    print(f"✅ Umbral de energía ajustado a: {self.reconocedor.energy_threshold}")
                    print("=" * 60)
                    print("🎧 ESCUCHANDO... Di 'Azul' para activarme")
                    print("=" * 60)
                    
                    intentos_reconexion = 0
                    
                    while True:
                        try:
                            # Verificar timeout de conversación
                            if self.modo_conversacion_activo and self.tiempo_ultima_interaccion:
                                tiempo_transcurrido = time.time() - self.tiempo_ultima_interaccion
                                if tiempo_transcurrido > self.timeout_conversacion:
                                    self.modo_conversacion_activo = False
                                    print("\n💤 Modo conversación desactivado (timeout)")
                                    print("=" * 60)
                                    print("🎧 Di 'Azul' para activarme nuevamente")
                                    print("=" * 60)
                            
                            # Escuchar audio
                            audio = self.reconocedor.listen(source, timeout=None, phrase_time_limit=5)
                            
                            # Actualizar espectro visual
                            try:
                                data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
                                if len(data) > 0:
                                    vol = np.abs(data).mean() / 10
                                    self.datos_espectro = [min(100, vol * (1 + 0.5 * math.sin(i + time.time()))) for i in range(20)]
                            except:
                                pass
                            
                            # Reconocer voz
                            try:
                                texto = self.reconocedor.recognize_google(audio, language="es-ES").lower()
                                print(f"\n👂 Escuché: '{texto}'")
                                
                                # Si Azul está hablando y el usuario habla = INTERRUMPIR
                                if esta_hablando:
                                    print("⚡ Usuario interrumpiendo a Azul...")
                                    self.detener_voz_actual()
                                    time.sleep(0.3)  # Breve pausa para que se detenga la voz
                                
                                # MODO 1: Conversación activa - procesar TODO
                                if self.modo_conversacion_activo:
                                    print(f"💬 [MODO CONVERSACIÓN] Procesando: '{texto}'")
                                    self.datos_espectro = [100] * 20
                                    self.tiempo_ultima_interaccion = time.time()
                                    self.after(0, lambda c=texto: self.procesar_comando_voz(c))
                                    print("=" * 60)
                                    print("💬 Sigo escuchando... (30s timeout)")
                                    print("=" * 60)
                                
                                # MODO 2: Modo pasivo - buscar palabra clave
                                elif nombre_asistente in texto:
                                    print(f"✨ ¡AZUL ACTIVADA! 🎯")
                                    self.datos_espectro = [100] * 20
                                    
                                    # Activar modo conversación
                                    self.modo_conversacion_activo = True
                                    self.tiempo_ultima_interaccion = time.time()
                                    
                                    # Extraer comando si existe
                                    partes = texto.split(nombre_asistente)
                                    cmd = partes[-1].strip() if len(partes) > 1 else ""
                                    
                                    if cmd:
                                        print(f"📝 Comando: '{cmd}'")
                                        print("💬 Modo conversación ACTIVADO (30s)")
                                        self.after(0, lambda c=cmd: self.procesar_comando_voz(c))
                                    else:
                                        print("👋 ¡Hola! ¿En qué puedo ayudarte?")
                                        self.after(0, lambda: self.saludar_activacion())
                                    
                                    print("=" * 60)
                                    print("💬 Ahora puedes hablar normalmente sin decir 'Azul'")
                                    print("=" * 60)
                                
                                else:
                                    # No se detectó "azul" en modo pasivo - ignorar
                                    pass
                            
                            except sr.UnknownValueError:
                                pass
                            
                            except sr.RequestError as e:
                                print(f"\n❌ Error de API de Google Speech: {e}")
                                print("🔄 Reintentando en 2 segundos...")
                                time.sleep(2)
                        
                        except sr.WaitTimeoutError:
                            continue
                        
                        except Exception as e:
                            print(f"\n⚠️ Error durante escucha: {e}")
                            time.sleep(0.5)
                            continue
            
            except OSError as e:
                intentos_reconexion += 1
                print(f"\n❌ Error de micrófono: {e}")
                if intentos_reconexion < max_intentos:
                    print(f"🔄 Reintentando conexión ({intentos_reconexion}/{max_intentos})...")
                    time.sleep(2)
                else:
                    print(f"\n❌ No se pudo conectar al micrófono después de {max_intentos} intentos")
                    print("💡 Verifica que:")
                    print("   1. El micrófono esté conectado")
                    print("   2. Los permisos de micrófono estén habilitados")
                    print("   3. Ninguna otra aplicación esté usando el micrófono")
                    break
            
            except Exception as e:
                print(f"\n❌ Error crítico en escucha pasiva: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(2)
    
    def saludar_activacion(self):
        """Saludo cuando se activa Azul sin comando específico"""
        saludos = [
            "¡Hola! ¿En qué te ayudo?",
            "Aquí estoy, dime",
            "¿Qué necesitas?",
            "Te escucho"
        ]
        saludo = random.choice(saludos)
        cola_voz.put(saludo)
        
        # Actualizar tiempo de interacción
        self.tiempo_ultima_interaccion = time.time()

    def procesar_comando_voz(self, texto):
        """Procesa comando de voz y mantiene modo conversación activo"""
        self.entry_user.insert(0, texto)
        self.enviar_mensaje()
        
        # Actualizar tiempo de interacción para mantener conversación activa
        if self.modo_conversacion_activo:
            self.tiempo_ultima_interaccion = time.time()

    def obtener_respuesta_ia(self):
        # Verificar si debe hacer comentarios proactivos sobre eventos (en paralelo)
        threading.Thread(target=self.verificar_comentarios_proactivos, daemon=True).start()
        
        # Obtener último mensaje del usuario
        ultimo_mensaje = self.historial[-1]['content'] if self.historial else ""
        
        # Enviar a la API Cloud
        try:
            response = api_client.enviar_mensaje(ultimo_mensaje, stream=False)
            
            # Extraer texto de respuesta
            resp_comp = response.get("text", "Lo siento, no pude procesar la respuesta.")
            
            # Agregar al historial local
            self.historial.append({"role": "assistant", "content": resp_comp})
            
            # Registrar menciones de temas para cooldown
            self._registrar_mencion_tema(resp_comp)
            
            # Procesar audio descargado desde la API
            audio_urls = response.get("audio_urls", [])
            if audio_urls:
                # Poner las URLs en la cola para descarga y reproducción
                threading.Thread(
                    target=self._procesar_audio_desde_api, 
                    args=(audio_urls,),
                    daemon=True
                ).start()
            else:
                # Si no hay audio, poner el texto para TTS local (fallback)
                for frase in resp_comp.split('.'):
                    if frase.strip():
                        cola_voz.put(frase.strip())
        
        except Exception as e:
            print(f"❌ Error obteniendo respuesta de IA: {e}")
            resp_comp = "Lo siento, hubo un problema conectando con el servidor."
            self.historial.append({"role": "assistant", "content": resp_comp})
            cola_voz.put(resp_comp)
    
    def _procesar_audio_desde_api(self, audio_urls: list):
        """Descarga y reproduce audios desde la API"""
        global usuario_interrumpiendo
        
        for audio_url in audio_urls:
            if usuario_interrumpiendo:
                break
            
            # Descargar audio
            audio_path = api_client.descargar_audio(audio_url)
            if audio_path:
                # Reproducir directamente (en lugar de usar hablar_async)
                self._reproducir_audio_descargado(audio_path)
    
    def _reproducir_audio_descargado(self, audio_path: str):
        """Reproduce un archivo MP3 descargado de la API"""
        global esta_hablando, usuario_interrumpiendo
        
        try:
            esta_hablando = True
            
            # Reproducir con pygame
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            
            # Esperar a que termine
            while pygame.mixer.music.get_busy() and not usuario_interrumpiendo:
                time.sleep(0.1)
            
            if usuario_interrumpiendo:
                pygame.mixer.music.stop()
                print("🛑 Audio interrumpido por usuario")
            
            # Limpiar archivo temporal
            try:
                os.unlink(audio_path)
            except:
                pass
        
        except Exception as e:
            print(f"⚠️ Error reproduciendo audio: {e}")
        
        finally:
            esta_hablando = False

    def actualizar_lista_tareas_main(self):
        """Actualiza la lista de tareas en el panel principal"""
        # Limpiar frame
        for widget in self.tareas_frame.winfo_children():
            widget.destroy()
        
        # Obtener eventos pendientes
        eventos = self.gestor_calendario.obtener_eventos_proximos(horas=24*365)
        eventos.sort(key=lambda e: e.fecha_hora)
        
        if not eventos:
            no_tareas = ctk.CTkLabel(self.tareas_frame, 
                                     text="No hay tareas pendientes", 
                                     font=("Arial", 14), text_color="#999999",
                                     justify="left")
            no_tareas.pack(pady=40, anchor="w")
            return
        
        # Mostrar cada tarea - máxima extensión horizontal
        for evento in eventos:
            # Frame sin bordes, solo hover
            tarea_item = ctk.CTkFrame(self.tareas_frame, fg_color="transparent", 
                                     corner_radius=0)
            tarea_item.pack(fill="x", pady=10, padx=5)  # Padding lateral mínimo
            
            # Contenedor para hover
            content_frame = ctk.CTkFrame(tarea_item, fg_color="transparent", corner_radius=8)
            content_frame.pack(fill="x")
            
            # Bind hover effects
            def on_enter(e, frame=content_frame):
                frame.configure(fg_color="#f8f8f8")
            
            def on_leave(e, frame=content_frame):
                frame.configure(fg_color="transparent")
            
            content_frame.bind("<Enter>", on_enter)
            content_frame.bind("<Leave>", on_leave)
            
            # Checkbox simple "○"
            checkbox_label = ctk.CTkLabel(content_frame, text="○", font=("Arial", 20), 
                                         text_color="#cccccc", width=30)
            checkbox_label.pack(side="left", padx=(5, 10), pady=8)
            
            # Info de la tarea
            info_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
            info_frame.pack(side="left", fill="both", expand=True, pady=8)
            
            # Título simple
            titulo_label = ctk.CTkLabel(info_frame, text=f"- {evento.titulo}", 
                                        font=("Arial", 15, "normal"), anchor="w",
                                        text_color="#1a1a1a")
            titulo_label.pack(anchor="w")
            
            # Fecha/hora muy sutil
            fecha_str = evento.fecha_hora.strftime("%d/%m a las %I:%M %p").lstrip("0")
            
            detalle_label = ctk.CTkLabel(info_frame, 
                                        text=f"  {fecha_str}",
                                        font=("Arial", 11), anchor="w",
                                        text_color="#999999")
            detalle_label.pack(anchor="w", pady=(2, 0))
            
            # Botón eliminar muy discreto
            def eliminar_tarea(evento_id=evento.id):
                if self.gestor_calendario.eliminar_evento(evento_id):
                    self.actualizar_lista_tareas_main()
            
            btn_eliminar = ctk.CTkButton(content_frame, text="×", width=30, height=30,
                                         command=eliminar_tarea, fg_color="transparent",
                                         hover_color="#ffebee", corner_radius=15,
                                         text_color="#cccccc", font=("Arial", 20),
                                         border_width=0)
            btn_eliminar.pack(side="right", padx=5)
            
            # Hacer hover en todo el widget
            for widget in [checkbox_label, info_frame, titulo_label, detalle_label]:
                widget.bind("<Enter>", on_enter)
                widget.bind("<Leave>", on_leave)
    
    def mostrar_historial(self):
        win = ctk.CTkToplevel(self); win.title("Historial")
        win.geometry("500x600")
        txt = ctk.CTkTextbox(win, width=480, height=580, fg_color="#f8f9fa", 
                            border_color="#e0e0e0", border_width=1, corner_radius=10)
        txt.pack(padx=10, pady=10)
        for m in self.historial:
            if m['role'] != 'system': txt.insert("end", f"{'Tú' if m['role']=='user' else 'Azul'}: {m['content']}\n\n")
        txt.configure(state="disabled")
    
    def mostrar_formulario_tarea(self):
        """Muestra formulario para agregar nueva tarea"""
        # Crear ventana
        win = ctk.CTkToplevel(self)
        win.title("➕ Nueva Tarea - Azul")
        win.geometry("500x550")
        
        # Frame principal
        main_frame = ctk.CTkFrame(win, fg_color="#ffffff")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header = ctk.CTkLabel(main_frame, text="➕ Nueva Tarea", font=("Arial", 22, "bold"), text_color="#2c3e50")
        header.pack(pady=(0, 20))
        
        # --- FORMULARIO ---
        form_frame = ctk.CTkFrame(main_frame, fg_color="#f8f9fa", corner_radius=15, border_width=1, border_color="#e0e0e0")
        form_frame.pack(fill="both", expand=True)
        
        # Título del formulario
        form_title = ctk.CTkLabel(form_frame, text="Nueva Tarea", font=("Arial", 14, "bold"), text_color="#2c3e50")
        form_title.pack(pady=(15, 10))
        
        # Campo: Título de la tarea
        tarea_label = ctk.CTkLabel(form_frame, text="Título:", anchor="w", text_color="#34495e")
        tarea_label.pack(fill="x", padx=20, pady=(5, 0))
        tarea_entry = ctk.CTkEntry(form_frame, placeholder_text="Ej: Comprar leche, Llamar a mamá...",
                                   border_color="#00d4ff", border_width=1, corner_radius=8)
        tarea_entry.pack(fill="x", padx=20, pady=(0, 10))
        
        # Fila: Fecha y Hora
        datetime_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        datetime_frame.pack(fill="x", padx=20, pady=(0, 10))
        datetime_frame.grid_columnconfigure(0, weight=1)
        datetime_frame.grid_columnconfigure(1, weight=1)
        
        # Fecha
        fecha_label = ctk.CTkLabel(datetime_frame, text="Fecha:", anchor="w", text_color="#34495e")
        fecha_label.grid(row=0, column=0, sticky="w", padx=(0, 5))
        fecha_entry = ctk.CTkEntry(datetime_frame, placeholder_text="DD/MM/AAAA",
                                   border_color="#00d4ff", border_width=1, corner_radius=8)
        fecha_entry.grid(row=1, column=0, sticky="ew", padx=(0, 5))
        fecha_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        # Hora
        hora_label = ctk.CTkLabel(datetime_frame, text="Hora:", anchor="w", text_color="#34495e")
        hora_label.grid(row=0, column=1, sticky="w", padx=(5, 0))
        hora_entry = ctk.CTkEntry(datetime_frame, placeholder_text="HH:MM",
                                  border_color="#00d4ff", border_width=1, corner_radius=8)
        hora_entry.grid(row=1, column=1, sticky="ew", padx=(5, 0))
        
        # Recordatorio
        recordatorio_label = ctk.CTkLabel(form_frame, text="Recordatorios (minutos antes):", anchor="w", text_color="#34495e")
        recordatorio_label.pack(fill="x", padx=20, pady=(5, 0))
        
        recordatorio_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        recordatorio_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Checkboxes para recordatorios con estilo moderno
        check_30 = ctk.CTkCheckBox(recordatorio_frame, text="30 min", onvalue=30, offvalue=0,
                                   fg_color="#00d4ff", hover_color="#00a3cc")
        check_30.pack(side="left", padx=5)
        check_30.select()
        
        check_10 = ctk.CTkCheckBox(recordatorio_frame, text="10 min", onvalue=10, offvalue=0,
                                   fg_color="#00d4ff", hover_color="#00a3cc")
        check_10.pack(side="left", padx=5)
        check_10.select()
        
        check_5 = ctk.CTkCheckBox(recordatorio_frame, text="5 min", onvalue=5, offvalue=0,
                                  fg_color="#00d4ff", hover_color="#00a3cc")
        check_5.pack(side="left", padx=5)
        check_5.select()
        
        check_0 = ctk.CTkCheckBox(recordatorio_frame, text="Momento exacto", onvalue=0, offvalue=-1,
                                  fg_color="#00d4ff", hover_color="#00a3cc")
        check_0.pack(side="left", padx=5)
        check_0.select()
        
        def agregar_tarea_manual():
            """Agrega una tarea desde el formulario"""
            titulo = tarea_entry.get().strip()
            fecha_str = fecha_entry.get().strip()
            hora_str = hora_entry.get().strip()
            
            if not titulo:
                error_label.configure(text="⚠️ El título es obligatorio", text_color="red")
                return
            
            if not hora_str:
                error_label.configure(text="⚠️ La hora es obligatoria", text_color="red")
                return
            
            try:
                # Parsear fecha
                dia, mes, anio = map(int, fecha_str.split('/'))
                hora, minuto = map(int, hora_str.split(':'))
                
                fecha_hora = datetime(anio, mes, dia, hora, minuto)
                
                # Validar que sea futura
                if fecha_hora <= datetime.now():
                    error_label.configure(text="⚠️ La fecha/hora debe ser futura", text_color="red")
                    return
                
                # Obtener recordatorios seleccionados
                recordatorios = []
                if check_30.get() == 30: recordatorios.append(30)
                if check_10.get() == 10: recordatorios.append(10)
                if check_5.get() == 5: recordatorios.append(5)
                if check_0.get() == 0: recordatorios.append(0)
                
                # Crear tarea (evento)
                evento = self.gestor_calendario.agregar_evento(
                    titulo=titulo,
                    fecha_hora=fecha_hora,
                    tipo="recordatorio",
                    descripcion="",
                    notificaciones=recordatorios
                )
                
                print(f"✅ Tarea creada: {titulo} - {fecha_hora}")
                
                # Limpiar formulario
                tarea_entry.delete(0, "end")
                hora_entry.delete(0, "end")
                error_label.configure(text="✅ Tarea creada exitosamente!", text_color="#00d4ff")
                
                # Recargar lista de tareas en panel principal
                self.actualizar_lista_tareas_main()
                
                # Cerrar ventana después de 1 segundo
                win.after(1000, win.destroy)
                
            except Exception as e:
                error_label.configure(text=f"⚠️ Error: Verifica el formato de fecha/hora", text_color="red")
                print(f"Error creando tarea: {e}")
        
        # Botón agregar con estilo moderno
        btn_agregar = ctk.CTkButton(form_frame, text="➕ Agregar Tarea", command=agregar_tarea_manual, 
                                     fg_color="#00d4ff", hover_color="#00a3cc", corner_radius=10,
                                     font=("Arial", 13, "bold"))
        btn_agregar.pack(padx=20, pady=(0, 10))
        
        # Label de error/éxito
        error_label = ctk.CTkLabel(form_frame, text="", font=("Arial", 11))
        error_label.pack(pady=(0, 15))
    
    # --- FUNCIONES DE CALENDARIO ---
    
    def procesar_calendario(self, texto: str) -> bool:
        """
        Procesa comandos relacionados con el calendario
        Retorna True si se procesó (evento creado o consulta respondida), False si no
        """
        # Detectar palabras clave de calendario
        palabras_calendario = ['cita', 'alarma', 'recordatorio', 'recordar', 'recuerdame',
                              'agendar', 'agenda', 'mañana', 'hoy', 'orita', 'ahorita',
                              'tengo', 'hay', 'evento', 'eventos', 'qué']
        
        if any(palabra in texto.lower() for palabra in palabras_calendario):
            print(f"🔍 Detectando comando de calendario: {texto}")
            
            # Verificar si es una consulta o un comando de creación
            if self.analizador_calendario.es_consulta(texto):
                print(f"📋 Es una consulta sobre eventos existentes")
                
                # Analizar qué tipo de consulta es
                consulta = self.analizador_calendario.analizar_consulta(texto)
                tipo_consulta = consulta['tipo_consulta']
                
                # Obtener eventos según el tipo de consulta
                if tipo_consulta == 'hoy':
                    eventos = self.gestor_calendario.obtener_eventos_hoy()
                elif tipo_consulta == 'mañana':
                    # Obtener eventos de mañana
                    ahora = datetime.now()
                    manana = ahora + timedelta(days=1)
                    fecha_manana = manana.date()
                    eventos = [e for e in self.gestor_calendario.eventos 
                              if not e.completado and e.fecha_hora.date() == fecha_manana]
                elif tipo_consulta == 'semana':
                    # Eventos de la próxima semana (7 días)
                    eventos = self.gestor_calendario.obtener_eventos_proximos(horas=24*7)
                else:
                    # Próximos 24 horas
                    eventos = self.gestor_calendario.obtener_eventos_proximos(horas=24)
                
                # Ordenar eventos por fecha/hora
                eventos.sort(key=lambda e: e.fecha_hora)
                
                # Formatear respuesta
                respuesta = self.analizador_calendario.formatear_eventos(eventos, tipo_consulta)
                
                print(f"📊 Encontrados {len(eventos)} eventos")
                print(f"📝 Respuesta:\n{respuesta}")
                
                # Agregar la respuesta al historial como mensaje del sistema
                self.historial.append({"role": "system", "content": f"[CONSULTA CALENDARIO] {respuesta}"})
                
                # Hacer que Azul responda de forma natural
                cola_voz.put(respuesta)
                self.historial.append({"role": "assistant", "content": respuesta})
                
                # Guardar en Supabase
                threading.Thread(target=lambda: supabase.table("mensajes_chat").insert(
                    {"role": "assistant", "content": respuesta}
                ).execute()).start()
                
                return True
            
            else:
                # Es un comando para crear evento
                print(f"➕ Es un comando para crear evento")
                resultado = self.analizador_calendario.interpretar_comando(texto)
                
                print(f"📊 Resultado del análisis: {resultado}")
                
                if resultado.get('valido'):
                    # Crear evento
                    evento = self.gestor_calendario.agregar_evento(
                        titulo=resultado['titulo'],
                        fecha_hora=resultado['fecha_hora'],
                        tipo=resultado['tipo'],
                        descripcion=resultado['descripcion']
                    )
                    
                    print(f"✅ Evento creado exitosamente:")
                    print(f"   ID: {evento.id}")
                    print(f"   Título: {evento.titulo}")
                    print(f"   Fecha/Hora: {evento.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"   Tipo: {evento.tipo}")
                    print(f"   Notificaciones programadas para: {evento.notificaciones} minutos antes")
                    
                    # Formatear fecha/hora para mostrar
                    ahora = datetime.now()
                    fecha_evento = evento.fecha_hora
                    
                    # Determinar si es hoy, mañana, etc.
                    if fecha_evento.date() == ahora.date():
                        cuando = "hoy"
                    elif fecha_evento.date() == (ahora + timedelta(days=1)).date():
                        cuando = "mañana"
                    else:
                        cuando = fecha_evento.strftime("%d/%m/%Y")
                    
                    hora_formateada = fecha_evento.strftime("%I:%M %p").lstrip("0")
                    
                    # Agregar información detallada al historial para que Azul confirme
                    info_evento = (
                        f"[SISTEMA] Se ha creado exitosamente un {evento.tipo}: '{evento.titulo}' "
                        f"programado para {cuando} a las {hora_formateada}. "
                        f"Se enviarán recordatorios automáticos antes del evento."
                    )
                    
                    self.historial.append({"role": "system", "content": info_evento})
                    
                    # Actualizar contexto de sistema con eventos actualizados
                    self.actualizar_instrucciones_sistema()
                    
                    # Actualizar lista visual de tareas
                    self.actualizar_lista_tareas_main()
                    
                    return True
                else:
                    print(f"⚠️ No se pudo interpretar como evento de calendario")
                    return False
        
        return False
    
    def manejar_notificacion_evento(self, evento, minutos_antes: int):
        """Maneja las notificaciones de eventos"""
        # Generar notificación inteligente
        mensaje = self.generador_notificaciones.generar_notificacion(evento, minutos_antes)
        
        # Enviar notificación por voz
        cola_voz.put(mensaje)
        
        # Mostrar notificación del sistema de Windows
        if NOTIFICACIONES_SISTEMA_DISPONIBLES:
            def mostrar_notificacion_async():
                try:
                    # Determinar título según el tiempo
                    if minutos_antes == 0:
                        titulo = f"ES HORA! - {evento.tipo.upper()}"
                    elif minutos_antes <= 5:
                        titulo = f"URGENTE - {evento.tipo.upper()} en {minutos_antes} min"
                    else:
                        titulo = f"Recordatorio - {evento.tipo.upper()}"
                    
                    # Formatear mensaje para la notificación
                    hora_evento = evento.fecha_hora.strftime("%I:%M %p").lstrip("0")
                    mensaje_notif = f"{evento.titulo} - Hora: {hora_evento}"
                    
                    if minutos_antes > 0:
                        mensaje_notif += f" (En {minutos_antes} minutos)"
                    
                    print(f"📢 Mostrando notificación del sistema...")
                    print(f"   Título: {titulo}")
                    print(f"   Mensaje: {mensaje_notif}")
                    
                    # Mostrar notificación (bloquea el thread hasta que se cierre)
                    toaster.show_toast(
                        title=titulo,
                        msg=mensaje_notif,
                        duration=15,  # 15 segundos
                        threaded=False,  # No hacer thread dentro de thread
                        icon_path=None
                    )
                    print(f"✅ Notificación mostrada exitosamente")
                    
                except Exception as e:
                    print(f"❌ Error mostrando notificación del sistema: {e}")
                    import traceback
                    traceback.print_exc()
            
            # Ejecutar en thread separado para no bloquear
            threading.Thread(target=mostrar_notificacion_async, daemon=True).start()
        
        # Actualizar timestamp de última mención
        self.ultima_mencion_eventos = datetime.now()
        
        print(f"🔔 Notificación: {mensaje}")
    
    def verificar_comentarios_proactivos(self):
        """Verifica si Azul debe hacer comentarios proactivos sobre eventos"""
        eventos_proximos = self.gestor_calendario.obtener_eventos_proximos(2)  # 2 horas
        
        if eventos_proximos:
            minutos_desde_ultima = (datetime.now() - self.ultima_mencion_eventos).seconds // 60
            
            if self.generador_notificaciones.debe_comentar_proactivamente(
                eventos_proximos, minutos_desde_ultima
            ):
                comentario = self.generador_notificaciones.generar_comentario_proactivo(
                    eventos_proximos
                )
                if comentario:
                    # Agregar comentario al contexto del chat
                    self.historial.append({
                        "role": "assistant", 
                        "content": comentario
                    })
                    cola_voz.put(comentario)
                    self.ultima_mencion_eventos = datetime.now()
                    
                    # Guardar en Supabase
                    threading.Thread(target=lambda: supabase.table("mensajes_chat").insert(
                        {"role": "assistant", "content": comentario}
                    ).execute()).start()
    
    # --- FIN FUNCIONES DE CALENDARIO ---

if __name__ == "__main__":
    # Crear e iniciar Azul con animación de entrada integrada
    app = AzulGUI()
    app.mainloop()