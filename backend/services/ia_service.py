"""
Servicio de IA con Groq
Maneja toda la lógica de conversación con Llama3 en la nube
"""

from groq import Groq
from typing import List, Dict, Optional
import sys
import os

# Agregar directorio padre al path para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GROQ_API_KEY, AI_MODEL, AI_TEMPERATURE, AI_MAX_TOKENS

class IAService:
    """Servicio de IA conversacional con Groq"""
    
    def __init__(self):
        """Inicializa el cliente de Groq"""
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = AI_MODEL
        self.temperature = AI_TEMPERATURE
        self.max_tokens = AI_MAX_TOKENS
        print(f"✅ IAService inicializado con modelo: {self.model}")
    
    def crear_prompt_sistema(self, contexto_usuario: str = "", contexto_calendario: str = "") -> str:
        """
        Crea el prompt del sistema con el contexto del usuario
        
        Args:
            contexto_usuario: Perfil y preferencias del usuario
            contexto_calendario: Información de eventos próximos
        
        Returns:
            Prompt del sistema formateado
        """
        prompt = f"""Eres Azul, amiga cercana del usuario. Natural, directa, concisa.

REGLAS BÁSICAS:
- MÁXIMO 2-3 frases cortas
- Tono cálido y cercano
- Nunca formal/robótica

PERFIL DEL USUARIO:
{contexto_usuario if contexto_usuario else "Aún aprendiendo sobre el usuario"}

IMPORTANTE - USO DEL PERFIL:
- USA este conocimiento para personalizar respuestas
- Menciona gustos/hobbies SOLO cuando:
  1. El usuario los mencione primero
  2. Sean directamente relevantes
  3. Haya pasado suficiente tiempo desde última mención
- NO fuerces temas ni bromas repetitivas
- La información está para PERSONALIZAR, no para MENCIONAR constantemente"""

        if contexto_calendario:
            prompt += f"\n\nEVENTOS PRÓXIMOS:\n{contexto_calendario}"
            prompt += "\n\nSi te preguntan por eventos, responde basándote en esta información."
        
        return prompt
    
    async def obtener_respuesta(
        self, 
        mensaje: str, 
        historial: List[Dict[str, str]],
        stream: bool = False
    ) -> Dict:
        """
        Obtiene respuesta de Groq
        
        Args:
            mensaje: Mensaje del usuario
            historial: Lista de mensajes previos [{"role": "...", "content": "..."}]
            stream: Si True, retorna generador para streaming
        
        Returns:
            Dict con 'text' (respuesta completa) y 'frases' (lista de frases)
        """
        try:
            # Agregar mensaje del usuario al historial
            messages = historial + [{"role": "user", "content": mensaje}]
            
            if stream:
                # Streaming para respuestas en tiempo real
                return self._obtener_respuesta_streaming(messages)
            else:
                # Respuesta completa
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                
                respuesta_completa = response.choices[0].message.content
                
                # Dividir en frases para TTS
                frases = self._dividir_en_frases(respuesta_completa)
                
                return {
                    "text": respuesta_completa,
                    "frases": frases,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    }
                }
        
        except Exception as e:
            print(f"❌ Error en IAService.obtener_respuesta: {e}")
            raise
    
    def _obtener_respuesta_streaming(self, messages: List[Dict[str, str]]):
        """
        Generador para respuestas en streaming
        
        Args:
            messages: Lista de mensajes
        
        Yields:
            Chunks de texto
        """
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            print(f"❌ Error en streaming: {e}")
            raise
    
    def _dividir_en_frases(self, texto: str) -> List[str]:
        """
        Divide el texto en frases para síntesis de voz
        
        Args:
            texto: Texto completo
        
        Returns:
            Lista de frases
        """
        frases = []
        frase_actual = ""
        
        for char in texto:
            frase_actual += char
            
            # Detectar final de frase
            if char in ['.', '!', '?', '\n']:
                if frase_actual.strip():
                    frases.append(frase_actual.strip())
                frase_actual = ""
        
        # Agregar última frase si quedó algo
        if frase_actual.strip():
            frases.append(frase_actual.strip())
        
        return frases
    
    async def extraer_aprendizaje(self, texto: str) -> Optional[Dict[str, str]]:
        """
        Extrae gustos/hábitos del texto del usuario usando IA
        
        Args:
            texto: Texto del usuario
        
        Returns:
            Dict con 'clave' y 'valor' si encuentra algo, None si no
        """
        try:
            prompt = f"""Analiza este mensaje y extrae SOLO un gusto o hábito importante del usuario.
Responde en formato exacto: "clave:valor"
Si NO hay nada que aprender, responde exactamente: "NADA"

Ejemplos válidos:
- Usuario: "Me encanta el café" → gusto_bebidas:café
- Usuario: "Siempre desayuno a las 7am" → horario_desayuno:7am
- Usuario: "Hola" → NADA

Mensaje del usuario: "{texto}"

Respuesta (solo clave:valor o NADA):"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,  # Más determinista
                max_tokens=50
            )
            
            resultado = response.choices[0].message.content.strip()
            
            if "NADA" in resultado.upper():
                return None
            
            # Parsear clave:valor
            if ":" in resultado:
                partes = resultado.split(":", 1)
                if len(partes) == 2:
                    return {
                        "clave": partes[0].strip(),
                        "valor": partes[1].strip()
                    }
            
            return None
        
        except Exception as e:
            print(f"⚠️ Error extrayendo aprendizaje: {e}")
            return None

# Instancia global
ia_service = IAService()
