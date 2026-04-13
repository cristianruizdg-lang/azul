# ====================================================================
# AZUL v3.0 - CLOUD EDITION
# Asistente Personal con IA en la Nube (Groq + Supabase + Render)
# ====================================================================
# Autor: Cristian Ruiz
# Fecha: Abril 2026
# Backend: https://azul-4xsp.onrender.com
# ====================================================================

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
from modules import GestorCalendario, AnalizadorCalendario, GeneradorNotificacionesInteligentes
import pygame
import os
import asyncio
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
print(f"🌐 Conectando a backend: {API_URL}")

# --- CONFIGURACIÓN DE SUPABASE (directo para UI, API la usa para chat) ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- CONFIGURACIÓN DE VOZ NATURAL ---
esta_hablando = False
usuario_interrumpiendo = False
nombre_asistente = "azul"
VOZ_AZUL = "es-MX-DaliaNeural"

cola_voz = queue.Queue()

# === CLIENTE DE API ===
class AzulApiClient:
    """Cliente para comunicarse con el backend de Azul en la nube"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.timeout = 30
        
        # Verificar conectividad al iniciar
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                health = response.json()
                print(f"✅ Backend conectado: v{health['version']} - {health['status']}")
            else:
                print(f"⚠️  Backend respondió con código {response.status_code}")
        except Exception as e:
            print(f"⚠️  No se pudo conectar al backend: {e}")
    
    def enviar_mensaje(self, texto: str, user_id: str = "desktop_user", stream: bool = False) -> dict:
        """Envía un mensaje al chat y recibe respuesta con audio"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/chat/message",
                json={
                    "message": texto,
                    "user_id": user_id,
                    "stream": stream
                },
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error al enviar mensaje: {e}")
            return {"text": "Lo siento, no pude conectarme al servidor.", "audio_urls": [], "frases": []}
    
    def descargar_audio(self, audio_url: str) -> Optional[str]:
        """Descarga un archivo de audio y lo guarda temporalmente"""
        try:
            # Construir URL completa
            if audio_url.startswith('/'):
                full_url = f"{self.base_url}{audio_url}"
            else:
                full_url = audio_url
            
            # Descargar audio
            response = self.session.get(full_url, timeout=10)
            response.raise_for_status()
            
            # Guardar en archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
                temp_audio.write(response.content)
                return temp_audio.name
        except Exception as e:
            print(f"⚠️  Error descargando audio: {e}")
            return None

# Instancia global del cliente API
api_client = AzulApiClient(API_URL)

# === FUNCIONES DE AUDIO ===
def reproducir_audio_descargado(audio_path: str):
    """Reproduce un archivo de audio descargado"""
    global esta_hablando, usuario_interrumpiendo
    try:
        esta_hablando = True
        usuario_interrumpiendo = False
        
        # Reproducir audio con pygame
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        
        # Esperar a que termine O detectar interrupción
        while pygame.mixer.music.get_busy() and not usuario_interrumpiendo:
            time.sleep(0.1)
        
        # Si hubo interrupción, detener inmediatamente
        if usuario_interrumpiendo:
            pygame.mixer.music.stop()
            print("🛑 Azul interrumpida por usuario")
        
        # Limpiar archivo temporal
        try:
            os.unlink(audio_path)
        except:
            pass
            
        esta_hablando = False
    except Exception as e:
        print(f"⚠️  Error reproduciendo audio: {e}")
        esta_hablando = False

def procesar_audio_desde_api(audio_urls: list):
    """Descarga y reproduce los audios desde la API"""
    for audio_url in audio_urls:
        if usuario_interrumpiendo:
            break
        
        # Descargar audio
        audio_path = api_client.descargar_audio(audio_url)
        if audio_path:
            # Reproducir
            reproducir_audio_descargado(audio_path)

def hilo_hablar():
    """Hilo que procesa la cola de reproducción de audio"""
    while True:
        item = cola_voz.get()
        if item is None:
            break
        try:
            if isinstance(item, list):  # Lista de URLs de audio
                procesar_audio_desde_api(item)
            elif isinstance(item, str):  # Ignorar (legacy)
                pass
        except Exception as e:
            print(f"⚠️  Error en hilo de voz: {e}")
        cola_voz.task_done()

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
            print(f"⚠️  No se pudo reproducir sonido: {e}")
    
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
        print(f"⚠️  No se pudo obtener clima: {e}")
    return None

# === CLASE PRINCIPAL GUI ===
class AzulCloudGUI(ctk.CTk):
    """Interfaz gráfica para Azul Cloud Edition"""
    
    def __init__(self):
        super().__init__()
        
        self.title("AZUL v3.0 - Cloud Edition")
        self.geometry("900x600")
        ctk.set_appearance_mode("light")
        
        # User ID para el backend
        self.user_id = "desktop_user"
        
        # Reconocedor de voz
        self.reconocedor = sr.Recognizer()
        self.escuchando = False
        
        # === LAYOUT PRINCIPAL ===
        self.configure(fg_color="#ffffff")
        
        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=1)  # Chat area
        self.grid_rowconfigure(2, weight=0)  # Input area
        
        # === HEADER ===
        header = ctk.CTkFrame(self, fg_color="#000000", height=60)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(header, text="AZUL - Cloud Edition", 
                            font=("Arial", 24, "bold"), text_color="#ffffff")
        title.grid(row=0, column=0, pady=15)
        
        status = ctk.CTkLabel(header, text=f"🌐 {API_URL}", 
                             font=("Arial", 10), text_color="#888888")
        status.grid(row=0, column=1, padx=20)
        
        # === CHAT AREA ===
        self.chat_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color="#fafafa",
            corner_radius=0
        )
        self.chat_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        
        # Mensaje de bienvenida
        self.agregar_mensaje_sistema("Hola! Soy Azul. Escríbeme o presiona el micrófono para hablarme.")
        
        # === INPUT AREA ===
        input_frame = ctk.CTkFrame(self, fg_color="#ffffff", height=80)
        input_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Botón de voz
        self.btn_voz = ctk.CTkButton(
            input_frame,
            text="🎤",
            width=60,
            height=50,
            font=("Arial", 24),
            fg_color="#000000",
            hover_color="#333333",
            command=self.toggle_escuchar
        )
        self.btn_voz.grid(row=0, column=0, padx=(0, 10))
        
        # Entry de texto
        self.entry_texto = ctk.CTkEntry(
            input_frame,
            placeholder_text="Escribe tu mensaje aquí...",
            height=50,
            font=("Arial", 13),
            border_color="#e0e0e0",
            border_width=1
        )
        self.entry_texto.grid(row=0, column=1, sticky="ew", padx=10)
        self.entry_texto.bind("<Return>", lambda e: self.enviar_mensaje())
        
        # Botón enviar
        self.btn_enviar = ctk.CTkButton(
            input_frame,
            text="Enviar",
            width=100,
            height=50,
            font=("Arial", 13),
            fg_color="#000000",
            hover_color="#333333",
            command=self.enviar_mensaje
        )
        self.btn_enviar.grid(row=0, column=2, padx=(10, 0))
        
        print("✅ Interfaz inicializada")
    
    def agregar_mensaje_sistema(self, texto: str):
        """Agrega un mensaje del sistema al chat"""
        msg_frame = ctk.CTkFrame(self.chat_frame, fg_color="#e8e8e8", corner_radius=10)
        msg_frame.grid(sticky="ew", pady=5, padx=50)
        
        msg_label = ctk.CTkLabel(
            msg_frame,
            text=texto,
            font=("Arial", 12),
            text_color="#666666",
            wraplength=700,
            justify="center"
        )
        msg_label.pack(padx=15, pady=10)
    
    def agregar_mensaje_usuario(self, texto: str):
        """Agrega un mensaje del usuario al chat"""
        msg_frame = ctk.CTkFrame(self.chat_frame, fg_color="#000000", corner_radius=15)
        msg_frame.grid(sticky="e", pady=5, padx=(100, 0))
        
        msg_label = ctk.CTkLabel(
            msg_frame,
            text=texto,
            font=("Arial", 13),
            text_color="#ffffff",
            wraplength=500,
            justify="left"
        )
        msg_label.pack(padx=20, pady=12)
    
    def agregar_mensaje_azul(self, texto: str):
        """Agrega un mensaje de Azul al chat"""
        msg_frame = ctk.CTkFrame(self.chat_frame, fg_color="#f0f0f0", corner_radius=15)
        msg_frame.grid(sticky="w", pady=5, padx=(0, 100))
        
        # Icono y texto
        content_frame = ctk.CTkFrame(msg_frame, fg_color="transparent")
        content_frame.pack(padx=15, pady=10)
        
        icon_label = ctk.CTkLabel(
            content_frame,
            text="🔵",
            font=("Arial", 16)
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        msg_label = ctk.CTkLabel(
            content_frame,
            text=texto,
            font=("Arial", 13),
            text_color="#1a1a1a",
            wraplength=500,
            justify="left"
        )
        msg_label.pack(side="left")
    
    def toggle_escuchar(self):
        """Activa/desactiva el reconocimiento de voz"""
        if self.escuchando:
            self.escuchando = False
            self.btn_voz.configure(text="🎤", fg_color="#000000")
        else:
            self.escuchando = True
            self.btn_voz.configure(text="⏸️", fg_color="#ff0000")
            threading.Thread(target=self.escuchar_voz, daemon=True).start()
    
    def escuchar_voz(self):
        """Escucha voz del usuario"""
        try:
            with sr.Microphone() as source:
                print("🎤 Escuchando...")
                self.agregar_mensaje_sistema("Escuchando...")
                
                self.reconocedor.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.reconocedor.listen(source, timeout=5, phrase_time_limit=10)
                
                print("🔄 Procesando audio...")
                self.agregar_mensaje_sistema("Procesando...")
                
                texto = self.reconocedor.recognize_google(audio, language="es-MX")
                print(f"📝 Reconocido: {texto}")
                
                self.entry_texto.delete(0, "end")
                self.entry_texto.insert(0, texto)
                self.enviar_mensaje()
                
        except sr.WaitTimeoutError:
            self.agregar_mensaje_sistema("No escuché nada. Intenta de nuevo.")
        except sr.UnknownValueError:
            self.agregar_mensaje_sistema("No pude entender. Intenta de nuevo.")
        except Exception as e:
            self.agregar_mensaje_sistema(f"Error: {e}")
        finally:
            self.escuchando = False
            self.btn_voz.configure(text="🎤", fg_color="#000000")
    
    def enviar_mensaje(self):
        """Envía mensaje a la API y procesa respuesta"""
        texto = self.entry_texto.get().strip()
        if not texto:
            return
        
        # Limpiar input
        self.entry_texto.delete(0, "end")
        
        # Mostrar mensaje del usuario
        self.agregar_mensaje_usuario(texto)
        
        # Deshabilitar botones mientras procesa
        self.btn_enviar.configure(state="disabled", text="Enviando...")
        self.btn_voz.configure(state="disabled")
        
        # Procesar en hilo separado
        threading.Thread(
            target=self.procesar_respuesta_api,
            args=(texto,),
            daemon=True
        ).start()
    
    def procesar_respuesta_api(self, texto: str):
        """Procesa la respuesta de la API en un hilo separado"""
        try:
            # Enviar a API
            print(f"📤 Enviando a API: {texto}")
            response = api_client.enviar_mensaje(texto, self.user_id, stream=False)
            
            # Obtener texto de respuesta
            respuesta_texto = response.get("text", "Sin respuesta")
            print(f"📥 Respuesta: {respuesta_texto}")
            
            # Mostrar respuesta en UI
            self.after(0, self.agregar_mensaje_azul, respuesta_texto)
            
            # Procesar audio si está disponible
            audio_urls = response.get("audio_urls", [])
            if audio_urls:
                print(f"🎵 Audio recibido: {len(audio_urls)} fragmentos")
                cola_voz.put(audio_urls)
            
        except Exception as e:
            print(f"❌ Error procesando respuesta: {e}")
            self.after(0, self.agregar_mensaje_sistema, f"Error: {e}")
        
        finally:
            # Rehabilitar botones
            self.after(0, self.btn_enviar.configure, {"state": "normal", "text": "Enviar"})
            self.after(0, self.btn_voz.configure, {"state": "normal"})

# === MAIN ===
if __name__ == "__main__":
    print("=" * 60)
    print("AZUL v3.0 - CLOUD EDITION")
    print("Backend:", API_URL)
    print("=" * 60)
    
    app = AzulCloudGUI()
    app.mainloop()

