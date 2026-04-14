"""
AZUL MÓVIL - Aplicación Android con Kivy/KivyMD
Versión: 0.1 (Alpha)
Backend: https://azul-4xsp.onrender.com

Características:
- Chat conversacional con texto
- Chat por voz (grabar y reproducir)
- Historial sincronizado con Supabase
- Memoria compartida con app desktop
- Interfaz Material Design
"""

import os
import json
import requests
from datetime import datetime
from typing import List, Dict
import threading
import tempfile

# Kivy/KivyMD imports
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFloatingActionButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDList
try:
    from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget
except ImportError:
    # KivyMD 1.2.0 compatibility
    OneLineAvatarIconListItem = None
    IconLeftWidget = None
from kivymd.uix.dialog import MDDialog
from kivymd.uix.toolbar import MDTopAppBar

# Audio imports (Android compatible)
try:
    if platform == "android":
        from android.permissions import request_permissions, Permission
        request_permissions([Permission.RECORD_AUDIO, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET])
        from jnius import autoclass
        AudioRecord = autoclass('android.media.AudioRecord')
        MediaRecorder = autoclass('android.media.MediaRecorder')
    else:
        # Desktop testing
        import sounddevice as sd
        import soundfile as sf
except ImportError:
    print("⚠️ Módulos de audio no disponibles")


# ===== CONFIGURACIÓN =====
API_URL = "https://azul-4xsp.onrender.com"
USER_ID = "default"  # Mismo user_id que desktop para sincronización


# ===== KV DESIGN =====
KV = '''
<MessageBubble>:
    size_hint_y: None
    height: self.minimum_height
    padding: dp(10)
    spacing: dp(5)
    orientation: 'vertical'
    
    MDCard:
        size_hint: None, None
        size: self.minimum_width, self.minimum_height
        md_bg_color: root.bg_color
        padding: dp(12)
        radius: [dp(15)]
        pos_hint: {"right": 1} if root.is_user else {"x": 0}
        
        MDBoxLayout:
            adaptive_size: True
            orientation: 'vertical'
            spacing: dp(3)
            
            MDLabel:
                text: root.message_text
                theme_text_color: "Custom"
                text_color: (1, 1, 1, 1) if root.is_user else (0.05, 0.05, 0.05, 1)
                size_hint: None, None
                width: min(dp(250), self.texture_size[0])
                height: self.texture_size[1]
                
            MDLabel:
                text: root.timestamp
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: (0.85, 0.85, 0.85, 1) if root.is_user else (0.3, 0.3, 0.3, 1)
                size_hint: None, None
                size: self.texture_size


ScreenManager:
    ChatScreen:
        name: "chat"


<ChatScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        md_bg_color: app.theme_cls.bg_darkest
        
        # Header
        MDTopAppBar:
            title: "Azul - Asistente Personal"
            md_bg_color: app.theme_cls.primary_color
            left_action_items: [["robot", lambda x: None]]
            right_action_items: [["history", lambda x: app.cargar_historial()]]
        
        # Chat container
        MDBoxLayout:
            orientation: 'vertical'
            
            # Messages scroll
            ScrollView:
                id: scroll_chat
                do_scroll_x: False
                
                MDBoxLayout:
                    id: chat_list
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(8)
                    padding: dp(10)
            
            # Input container
            MDCard:
                size_hint_y: None
                height: dp(70)
                md_bg_color: app.theme_cls.bg_dark
                padding: dp(10)
                
                MDBoxLayout:
                    spacing: dp(10)
                    
                    # Text input
                    MDTextField:
                        id: message_input
                        hint_text: "Escribe un mensaje..."
                        mode: "rectangle"
                        multiline: False
                        on_text_validate: app.enviar_mensaje_texto()
                        
                    # Voice button
                    MDIconButton:
                        icon: "microphone" if not app.is_recording else "stop"
                        md_bg_color: app.theme_cls.accent_color if not app.is_recording else (1, 0.3, 0.3, 1)
                        theme_icon_color: "Custom"
                        icon_color: (1, 1, 1, 1)
                        on_release: app.toggle_recording()
                    
                    # Send button
                    MDIconButton:
                        icon: "send"
                        md_bg_color: app.theme_cls.primary_color
                        theme_icon_color: "Custom"
                        icon_color: (1, 1, 1, 1)
                        on_release: app.enviar_mensaje_texto()
        
        # Status label
        MDLabel:
            id: status_label
            text: app.status_text
            theme_text_color: "Hint"
            halign: "center"
            size_hint_y: None
            height: dp(20)
            padding: dp(5)
'''


# ===== COMPONENTES PERSONALIZADOS =====
class MessageBubble(MDBoxLayout):
    """Burbuja de mensaje en el chat"""
    message_text = StringProperty("")
    timestamp = StringProperty("")
    is_user = BooleanProperty(False)
    bg_color = ListProperty([0.2, 0.6, 1, 1])  # Azul por defecto
    
    def __init__(self, message: str = "", is_user: bool = False, **kwargs):
        super().__init__(**kwargs)
        self.message_text = message
        self.is_user = is_user
        self.timestamp = datetime.now().strftime("%H:%M")
        
        if is_user:
            self.bg_color = [0.2, 0.6, 1, 1]  # Azul para usuario
        else:
            self.bg_color = [0.95, 0.95, 0.95, 1]  # Gris claro para Azul


class ChatScreen(Screen):
    """Pantalla principal del chat"""
    pass


# ===== CLIENTE API =====
class AzulApiClient:
    """Cliente HTTP para comunicarse con el backend"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
    
    def check_health(self) -> Dict:
        """Verificar salud del backend"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error al verificar salud: {e}")
            return {"status": "offline", "error": str(e)}
    
    def enviar_mensaje(self, texto: str, user_id: str = "default") -> Dict:
        """Enviar mensaje de texto a Azul"""
        try:
            payload = {
                "message": texto,
                "user_id": user_id,
                "stream": False
            }
            response = self.session.post(
                f"{self.base_url}/api/chat/message",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"❌ Error al enviar mensaje: {e}")
            return {"error": str(e)}
    
    def enviar_audio(self, audio_path: str, user_id: str = "default") -> Dict:
        """Enviar audio grabado a Azul"""
        try:
            with open(audio_path, "rb") as audio_file:
                files = {"audio": audio_file}
                data = {"user_id": user_id}
                response = self.session.post(
                    f"{self.base_url}/api/chat/voice",
                    files=files,
                    data=data,
                    timeout=60
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"❌ Error al enviar audio: {e}")
            return {"error": str(e)}
    
    def obtener_historial(self, user_id: str = "default", limit: int = 50) -> List[Dict]:
        """Obtener historial de mensajes"""
        try:
            response = self.session.get(
                f"{self.base_url}/api/memory/history",
                params={"user_id": user_id, "limit": limit},
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data.get("messages", [])
        except Exception as e:
            print(f"❌ Error al obtener historial: {e}")
            return []
    
    def descargar_audio(self, audio_url: str) -> str:
        """Descargar audio MP3 del backend"""
        try:
            # Convertir URL relativa a absoluta si es necesario
            if audio_url.startswith('/'):
                audio_url = f"{self.base_url}{audio_url}"
            
            response = self.session.get(audio_url, timeout=15)
            response.raise_for_status()
            
            # Guardar en archivo temporal
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_file.write(response.content)
            temp_file.close()
            
            return temp_file.name
        except Exception as e:
            print(f"❌ Error al descargar audio: {e}")
            return ""


# ===== GRABADOR DE AUDIO =====
class AudioRecorder:
    """Grabador de audio multiplataforma"""
    
    def __init__(self):
        self.is_recording = False
        self.audio_data = []
        self.recording_thread = None
        self.sample_rate = 16000
    
    def start_recording(self):
        """Iniciar grabación"""
        if self.is_recording:
            return
        
        self.is_recording = True
        self.audio_data = []
        
        if platform == "android":
            self._record_android()
        else:
            self._record_desktop()
    
    def stop_recording(self) -> str:
        """Detener grabación y guardar archivo"""
        if not self.is_recording:
            return ""
        
        self.is_recording = False
        
        if self.recording_thread:
            self.recording_thread.join()
        
        # Guardar audio en archivo temporal
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_path = temp_file.name
        temp_file.close()
        
        try:
            if platform != "android":
                import numpy as np
                data = np.concatenate(self.audio_data)
                sf.write(temp_path, data, self.sample_rate)
            
            return temp_path
        except Exception as e:
            print(f"❌ Error al guardar audio: {e}")
            return ""
    
    def _record_android(self):
        """Grabación en Android"""
        # TODO: Implementar grabación con AudioRecord
        print("⚠️ Grabación Android no implementada aún")
    
    def _record_desktop(self):
        """Grabación en desktop (testing)"""
        def record():
            try:
                while self.is_recording:
                    recording = sd.rec(
                        int(0.5 * self.sample_rate),
                        samplerate=self.sample_rate,
                        channels=1
                    )
                    sd.wait()
                    if self.is_recording:
                        self.audio_data.append(recording)
            except Exception as e:
                print(f"❌ Error en grabación: {e}")
        
        self.recording_thread = threading.Thread(target=record, daemon=True)
        self.recording_thread.start()


# ===== APLICACIÓN PRINCIPAL =====
class AzulMobileApp(MDApp):
    """Aplicación principal de Azul Móvil"""
    
    status_text = StringProperty("Conectando...")
    is_recording = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_client = AzulApiClient(API_URL)
        self.audio_recorder = AudioRecorder()
        self.current_audio = None
        
    def build(self):
        """Construir interfaz"""
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.theme_style = "Dark"
        
        return Builder.load_string(KV)
    
    def on_start(self):
        """Inicialización al arrancar"""
        Clock.schedule_once(self._init_app, 0.5)
    
    def _init_app(self, dt):
        """Inicializar aplicación"""
        # Verificar conexión al backend
        threading.Thread(target=self._check_backend, daemon=True).start()
        
        # Cargar historial
        self.cargar_historial()
    
    def _check_backend(self):
        """Verificar estado del backend"""
        health = self.api_client.check_health()
        
        if health.get("status") == "healthy":
            version = health.get("version", "?")
            self.update_status(f"✅ Conectado v{version}", success=True)
        else:
            self.update_status("❌ Backend offline", success=False)
    
    @mainthread
    def update_status(self, message: str, success: bool = True):
        """Actualizar mensaje de estado"""
        self.status_text = message
        print(f"{'✅' if success else '❌'} {message}")
    
    def cargar_historial(self):
        """Cargar historial de conversaciones"""
        def load():
            mensajes = self.api_client.obtener_historial(USER_ID, limit=50)
            
            if mensajes:
                self._mostrar_mensajes(mensajes)
                self.update_status(f"📚 {len(mensajes)} mensajes cargados")
            else:
                self.update_status("📭 Sin historial previo")
        
        threading.Thread(target=load, daemon=True).start()
    
    @mainthread
    def _mostrar_mensajes(self, mensajes: List[Dict]):
        """Mostrar mensajes en el chat"""
        chat_screen = self.root.get_screen('chat')
        chat_list = chat_screen.ids.chat_list
        chat_list.clear_widgets()
        
        for msg in mensajes:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            is_user = (role == "user")
            bubble = MessageBubble(content, is_user)
            chat_list.add_widget(bubble)
        
        # Scroll al final
        Clock.schedule_once(lambda dt: self._scroll_to_end(), 0.1)
    
    def _scroll_to_end(self):
        """Scroll al final del chat"""
        chat_screen = self.root.get_screen('chat')
        scroll = chat_screen.ids.scroll_chat
        scroll.scroll_y = 0
    
    def enviar_mensaje_texto(self):
        """Enviar mensaje de texto"""
        chat_screen = self.root.get_screen('chat')
        message_input = chat_screen.ids.message_input
        texto = message_input.text.strip()
        
        if not texto:
            return
        
        # Limpiar input
        message_input.text = ""
        
        # Agregar mensaje del usuario al chat
        self.agregar_mensaje(texto, is_user=True)
        
        # Enviar al backend
        def send():
            self.update_status("⏳ Enviando...")
            response = self.api_client.enviar_mensaje(texto, USER_ID)
            
            if "error" in response:
                self.update_status(f"❌ Error: {response['error']}", success=False)
                return
            
            # Obtener respuesta
            respuesta_texto = response.get("text", "")
            audio_urls = response.get("audio_urls", [])
            
            # Mostrar respuesta
            self.agregar_mensaje(respuesta_texto, is_user=False)
            self.update_status("✅ Respuesta recibida")
            
            # Reproducir audio si existe
            if audio_urls:
                self._reproducir_audio(audio_urls[0])
        
        threading.Thread(target=send, daemon=True).start()
    
    def toggle_recording(self):
        """Alternar grabación de audio"""
        if not self.is_recording:
            # Iniciar grabación
            self.is_recording = True
            self.audio_recorder.start_recording()
            self.update_status("🎤 Grabando...")
        else:
            # Detener y enviar
            self.is_recording = False
            self.update_status("⏳ Procesando audio...")
            
            def process():
                audio_path = self.audio_recorder.stop_recording()
                
                if not audio_path:
                    self.update_status("❌ Error al grabar audio", success=False)
                    return
                
                # Enviar audio al backend
                response = self.api_client.enviar_audio(audio_path, USER_ID)
                
                # Eliminar archivo temporal
                try:
                    os.unlink(audio_path)
                except:
                    pass
                
                if "error" in response:
                    self.update_status(f"❌ Error: {response['error']}", success=False)
                    return
                
                # Obtener transcripción y respuesta
                transcripcion = response.get("transcription", "")
                respuesta_texto = response.get("text", "")
                audio_urls = response.get("audio_urls", [])
                
                # Mostrar mensajes
                if transcripcion:
                    self.agregar_mensaje(transcripcion, is_user=True)
                
                if respuesta_texto:
                    self.agregar_mensaje(respuesta_texto, is_user=False)
                
                self.update_status("✅ Audio procesado")
                
                # Reproducir respuesta
                if audio_urls:
                    self._reproducir_audio(audio_urls[0])
            
            threading.Thread(target=process, daemon=True).start()
    
    @mainthread
    def agregar_mensaje(self, texto: str, is_user: bool):
        """Agregar mensaje al chat"""
        chat_screen = self.root.get_screen('chat')
        chat_list = chat_screen.ids.chat_list
        bubble = MessageBubble(texto, is_user)
        chat_list.add_widget(bubble)
        
        # Scroll al final
        Clock.schedule_once(lambda dt: self._scroll_to_end(), 0.1)
    
    def _reproducir_audio(self, audio_url: str):
        """Reproducir audio de respuesta"""
        def play():
            # Descargar audio
            audio_path = self.api_client.descargar_audio(audio_url)
            
            if not audio_path:
                return
            
            # Reproducir
            try:
                sound = SoundLoader.load(audio_path)
                if sound:
                    sound.play()
                    self.current_audio = sound
            except Exception as e:
                print(f"❌ Error al reproducir audio: {e}")
            finally:
                # Limpiar archivo temporal después de reproducir
                Clock.schedule_once(lambda dt: self._cleanup_audio(audio_path), 5)
        
        threading.Thread(target=play, daemon=True).start()
    
    def _cleanup_audio(self, path: str):
        """Limpiar archivos de audio"""
        try:
            if os.path.exists(path):
                os.unlink(path)
        except:
            pass


# ===== PUNTO DE ENTRADA =====
if __name__ == "__main__":
    AzulMobileApp().run()
