"""
Servicio de Voz
Maneja síntesis (TTS) con Edge TTS (fallback a pyttsx3) y reconocimiento (STT)
"""

import edge_tts
import pyttsx3
import speech_recognition as sr
import tempfile
import os
import asyncio
from typing import Optional
import sys
import hashlib

# Agregar directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import VOICE_MODEL, VOICE_RATE, VOICE_PITCH, TEMP_AUDIO_DIR

class VoiceService:
    """Servicio de síntesis y reconocimiento de voz con fallback"""
    
    def __init__(self):
        """Inicializa el servicio de voz con Edge TTS y fallback a pyttsx3"""
        self.voice_model = VOICE_MODEL
        self.voice_rate = VOICE_RATE
        self.voice_pitch = VOICE_PITCH
        self.recognizer = sr.Recognizer()
        
        # Inicializar pyttsx3 como fallback
        try:
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)  # Velocidad
            self.tts_engine.setProperty('volume', 0.9)  # Volumen
            
            # Configurar voz en español si está disponible
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                if 'es' in voice.languages or 'spanish' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            
            self.tts_fallback_available = True
            print("✅ pyttsx3 inicializado como fallback")
        except Exception as e:
            print(f"⚠️ pyttsx3 no disponible: {e}")
            self.tts_engine = None
            self.tts_fallback_available = False
        
        # Asegurar que existe el directorio de audio temporal
        os.makedirs(TEMP_AUDIO_DIR, exist_ok=True)
        
        # Contador de fallos de Edge TTS
        self.edge_tts_failed = False
        
        print(f"✅ VoiceService inicializado con voz: {self.voice_model}")
        print(f"   Fallback disponible: {'Sí (pyttsx3)' if self.tts_fallback_available else 'No'}")
    
    async def generar_audio(self, texto: str) -> str:
        """
        Genera audio a partir de texto usando Edge TTS (fallback a pyttsx3)
        
        Args:
            texto: Texto a sintetizar
        
        Returns:
            Path al archivo de audio generado
        """
        # Crear nombre único para el archivo
        text_hash = hashlib.md5(texto.encode()).hexdigest()[:12]
        filename = f"{text_hash}.mp3"
        output_path = os.path.join(TEMP_AUDIO_DIR, filename)
        
        # Verificar si ya existe (cache)
        if os.path.exists(output_path):
            print(f"♻️ Audio en cache: {filename}")
            return output_path
        
        # Intentar Edge TTS primero (si no ha fallado antes)
        if not self.edge_tts_failed:
            try:
                communicate = edge_tts.Communicate(
                    texto, 
                    self.voice_model,
                    rate=self.voice_rate,
                    pitch=self.voice_pitch
                )
                
                await communicate.save(output_path)
                
                print(f"🔊 Audio generado con Edge TTS: {filename}")
                return output_path
            
            except Exception as e:
                print(f"⚠️ Edge TTS falló: {str(e)[:100]}")
                self.edge_tts_failed = True  # Marcar como fallido para próximas llamadas
                # Continuar con fallback
        
        # Fallback a pyttsx3
        if self.tts_fallback_available:
            try:
                return await self._generar_audio_pyttsx3(texto, output_path)
            except Exception as e:
                print(f"❌ Error en pyttsx3 fallback: {e}")
                raise
        else:
            raise Exception("TTS no disponible: Edge TTS falló y pyttsx3 no está disponible")
    
    async def _generar_audio_pyttsx3(self, texto: str, output_path: str) -> str:
        """
        Genera audio usando pyttsx3 (TTS local)
        
        Args:
            texto: Texto a sintetizar
            output_path: Path donde guardar el audio
        
        Returns:
            Path al archivo generado
        """
        # pyttsx3 es sincrónico, ejecutar en thread pool
        loop = asyncio.get_event_loop()
        
        def _generar():
            try:
                self.tts_engine.save_to_file(texto, output_path)
                self.tts_engine.runAndWait()
                return output_path
            except Exception as e:
                raise Exception(f"Error generando audio con pyttsx3: {e}")
        
        result = await loop.run_in_executor(None, _generar)
        print(f"🔊 Audio generado con pyttsx3 (fallback): {os.path.basename(output_path)}")
        return result
    
    async def generar_multiples_audios(self, frases: list) -> list:
        """
        Genera múltiples archivos de audio en paralelo
        
        Args:
            frases: Lista de textos a sintetizar
        
        Returns:
            Lista de paths a los archivos generados
        """
        try:
            tasks = [self.generar_audio(frase) for frase in frases]
            audio_paths = await asyncio.gather(*tasks)
            return audio_paths
        
        except Exception as e:
            print(f"❌ Error generando múltiples audios: {e}")
            raise
    
    async def audio_a_texto(self, audio_path: str, idioma: str = "es-ES") -> str:
        """
        Convierte audio a texto usando Google Speech Recognition
        
        Args:
            audio_path: Path al archivo de audio
            idioma: Código de idioma (default: es-ES)
        
        Returns:
            Texto reconocido
        """
        try:
            # Cargar audio
            with sr.AudioFile(audio_path) as source:
                # Ajustar ruido ambiente
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Grabar audio
                audio_data = self.recognizer.record(source)
            
            # Reconocer con Google Speech API
            texto = self.recognizer.recognize_google(audio_data, language=idioma)
            
            print(f"🎤 Texto reconocido: {texto}")
            return texto
        
        except sr.UnknownValueError:
            print("⚠️ No se pudo entender el audio")
            raise ValueError("No se pudo entender el audio")
        
        except sr.RequestError as e:
            print(f"❌ Error en el servicio de reconocimiento: {e}")
            raise
        
        except Exception as e:
            print(f"❌ Error convirtiendo audio a texto: {e}")
            raise
    
    async def limpiar_audios_antiguos(self, max_archivos: int = 100):
        """
        Limpia archivos de audio antiguos para liberar espacio
        
        Args:
            max_archivos: Número máximo de archivos a mantener
        """
        try:
            archivos = []
            
            # Listar todos los archivos de audio
            for filename in os.listdir(TEMP_AUDIO_DIR):
                if filename.endswith('.mp3'):
                    filepath = os.path.join(TEMP_AUDIO_DIR, filename)
                    archivos.append({
                        'path': filepath,
                        'mtime': os.path.getmtime(filepath)
                    })
            
            # Si hay menos archivos que el máximo, no hacer nada
            if len(archivos) <= max_archivos:
                return
            
            # Ordenar por tiempo de modificación (más antiguos primero)
            archivos.sort(key=lambda x: x['mtime'])
            
            # Eliminar los más antiguos
            num_eliminar = len(archivos) - max_archivos
            for i in range(num_eliminar):
                os.unlink(archivos[i]['path'])
            
            print(f"🗑️ Eliminados {num_eliminar} archivos de audio antiguos")
        
        except Exception as e:
            print(f"⚠️ Error limpiando audios antiguos: {e}")
    
    def obtener_url_audio(self, audio_path: str, base_url: str = "") -> str:
        """
        Obtiene la URL pública para un archivo de audio
        
        Args:
            audio_path: Path local del audio
            base_url: URL base del servidor (opcional)
        
        Returns:
            URL pública del audio
        """
        filename = os.path.basename(audio_path)
        
        if base_url:
            return f"{base_url}/audio/{filename}"
        else:
            return f"/audio/{filename}"

# Instancia global
voice_service = VoiceService()
