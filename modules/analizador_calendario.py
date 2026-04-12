"""
Módulo de Análisis Inteligente para Calendario
Interpreta comandos de usuario y genera notificaciones contextuales
"""

import ollama
from datetime import datetime, timedelta
import re
import json
from typing import Optional, Dict


class AnalizadorCalendario:
    """Analiza texto del usuario para extraer información de eventos"""
    
    def __init__(self, modelo: str = "llama3"):
        self.modelo = modelo
    
    def es_consulta(self, texto: str) -> bool:
        """
        Detecta si el texto es una consulta (pregunta) sobre eventos
        en lugar de un comando para crear un evento
        """
        texto_lower = texto.lower()
        
        # Palabras clave que indican consulta/pregunta
        palabras_consulta = [
            'tengo', 'hay', 'existe', 'qué', 'que', 'cuál', 'cual', 
            'cuándo', 'cuando', 'cuántos', 'cuantos', 'lista', 'listar',
            'mostrar', 'ver', 'dime', 'muestra', 'muéstrame', 'muestrame'
        ]
        
        # Signos de interrogación
        if '?' in texto:
            return True
        
        # Verificar palabras clave de consulta
        for palabra in palabras_consulta:
            if palabra in texto_lower:
                return True
        
        return False
    
    def analizar_consulta(self, texto: str) -> Dict:
        """
        Analiza una consulta sobre eventos y devuelve el tipo de consulta
        """
        texto_lower = texto.lower()
        
        resultado = {
            'tipo_consulta': 'general',  # 'hoy', 'mañana', 'semana', 'general'
            'valido': True
        }
        
        # Detectar ámbito temporal de la consulta
        if any(palabra in texto_lower for palabra in ['hoy', 'día', 'dia']):
            resultado['tipo_consulta'] = 'hoy'
        elif 'mañana' in texto_lower or 'manana' in texto_lower:
            resultado['tipo_consulta'] = 'mañana'
        elif any(palabra in texto_lower for palabra in ['semana', 'próximos', 'proximos']):
            resultado['tipo_consulta'] = 'semana'
        
        return resultado
    
    @staticmethod
    def formatear_eventos(eventos: list, tipo_consulta: str = 'general') -> str:
        """
        Formatea una lista de eventos en texto legible para el usuario
        """
        if not eventos:
            if tipo_consulta == 'hoy':
                return "No tienes eventos programados para hoy. Tu agenda está libre."
            elif tipo_consulta == 'mañana':
                return "No tienes eventos para mañana. Puedes planificar tu día libremente."
            else:
                return "No tienes eventos próximos en tu calendario."
        
        # Construir respuesta
        if tipo_consulta == 'hoy':
            encabezado = f"Tienes {len(eventos)} evento{'s' if len(eventos) > 1 else ''} para hoy:\n\n"
        elif tipo_consulta == 'mañana':
            encabezado = f"Tienes {len(eventos)} evento{'s' if len(eventos) > 1 else ''} para mañana:\n\n"
        else:
            encabezado = f"Tienes {len(eventos)} evento{'s' if len(eventos) > 1 else ''} próximos:\n\n"
        
        lineas = []
        for i, evento in enumerate(eventos, 1):
            # Formatear hora
            hora_str = evento.fecha_hora.strftime("%I:%M %p").lstrip("0")
            
            # Calcular tiempo restante
            ahora = datetime.now()
            delta = evento.fecha_hora - ahora
            
            if delta.days > 0:
                fecha_str = evento.fecha_hora.strftime("%d/%m/%Y")
                tiempo_restante = f"en {delta.days} día{'s' if delta.days > 1 else ''}"
            else:
                fecha_str = "Hoy"
                horas = int(delta.total_seconds() // 3600)
                minutos = int((delta.total_seconds() % 3600) // 60)
                
                if horas > 0:
                    tiempo_restante = f"en {horas}h {minutos}m"
                else:
                    tiempo_restante = f"en {minutos}m"
            
            # Emoji según tipo
            emoji = "📅" if evento.tipo == "cita" else "⏰" if evento.tipo == "alarma" else "📝"
            
            lineas.append(f"{emoji} {evento.titulo}")
            lineas.append(f"   🕒 {hora_str}")
            
            if delta.days > 0:
                lineas.append(f"   📆 {fecha_str}")
            
            lineas.append(f"   ⏳ {tiempo_restante}\n")
        
        return encabezado + "\n".join(lineas)
    
    def _analisis_directo(self, texto: str) -> Optional[Dict]:
        """
        Análisis directo con regex - más rápido y confiable
        Detecta patrones comunes sin usar IA
        """
        texto_lower = texto.lower()
        ahora = datetime.now()
        
        # Detectar tipo de evento
        tipo = "recordatorio"
        if any(palabra in texto_lower for palabra in ['cita', 'reunión', 'reunión']):
            tipo = "cita"
        elif 'alarma' in texto_lower:
            tipo = "alarma"
        
        # Extraer hora (formatos: 3pm, 3:30pm, 15:00, 15:30)
        hora_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm|a\.m\.|p\.m\.)?', texto_lower)
        
        if not hora_match:
            return None
        
        hora = int(hora_match.group(1))
        minutos = int(hora_match.group(2)) if hora_match.group(2) else 0
        periodo = hora_match.group(3)
        
        # Convertir a formato 24h
        if periodo and 'pm' in periodo and hora != 12:
            hora += 12
        elif periodo and 'am' in periodo and hora == 12:
            hora = 0
        
        # Detectar cuándo (hoy, mañana, en X horas, etc.)
        fecha_evento = None
        
        if any(palabra in texto_lower for palabra in ['orita', 'ahorita', 'hoy']):
            # Hoy a la hora especificada
            fecha_evento = ahora.replace(hour=hora, minute=minutos, second=0, microsecond=0)
            if fecha_evento <= ahora:
                # Si ya pasó, programar para mañana
                fecha_evento += timedelta(days=1)
        
        elif 'mañana' in texto_lower:
            # Mañana a la hora especificada
            fecha_evento = (ahora + timedelta(days=1)).replace(
                hour=hora, minute=minutos, second=0, microsecond=0
            )
        
        elif 'pasado mañana' in texto_lower or 'pasado manana' in texto_lower:
            # Pasado mañana
            fecha_evento = (ahora + timedelta(days=2)).replace(
                hour=hora, minute=minutos, second=0, microsecond=0
            )
        
        # Detectar "en X horas/minutos"
        tiempo_match = re.search(r'en\s+(\d+)\s*(hora|minuto)', texto_lower)
        if tiempo_match:
            cantidad = int(tiempo_match.group(1))
            unidad = tiempo_match.group(2)
            
            if 'hora' in unidad:
                fecha_evento = ahora + timedelta(hours=cantidad)
            else:  # minutos
                fecha_evento = ahora + timedelta(minutes=cantidad)
        
        if not fecha_evento:
            return None
        
        # Extraer título (todo el texto menos las palabras de control)
        titulo = texto
        # Remover palabras comunes
        for palabra in ['oye', 'hey', 'recuerdame', 'recuérdame', 'recordar', 
                       'que', 'tengo', 'voy a', 'a las', 'hoy', 'mañana',
                       'orita', 'ahorita', 'en', 'hora', 'horas', 'minuto', 'minutos']:
            titulo = re.sub(r'\b' + palabra + r'\b', '', titulo, flags=re.IGNORECASE)
        
        # Remover la hora del título
        titulo = re.sub(r'\d{1,2}(?::\d{2})?\s*(?:am|pm|a\.m\.|p\.m\.)?', '', titulo, flags=re.IGNORECASE)
        
        # Limpiar espacios extra
        titulo = ' '.join(titulo.split()).strip()
        
        if not titulo:
            titulo = "Recordatorio"
        
        return {
            'valido': True,
            'tipo': tipo,
            'titulo': titulo,
            'fecha_hora': fecha_evento,
            'descripcion': ''
        }
    
    def interpretar_comando(self, texto: str) -> dict:
        """
        Interpreta un comando del usuario relacionado con calendario
        Primero intenta análisis directo, luego IA si falla
        """
        print(f"🔍 Analizando: {texto}")
        
        # Intentar análisis directo primero
        resultado = self._analisis_directo(texto)
        
        if resultado:
            print(f"✅ Análisis directo exitoso")
            print(f"   Tipo: {resultado['tipo']}")
            print(f"   Título: {resultado['titulo']}")
            print(f"   Fecha/Hora: {resultado['fecha_hora']}")
            return resultado
        
        # Si falla, intentar con IA
        print(f"⚠️  Análisis directo falló, usando IA...")
        return self._analisis_con_ia(texto)
        
    def _analisis_con_ia(self, texto: str) -> dict:
        """Análisis con IA (respaldo)"""
        prompt = f"""Analiza este comando de calendario y responde SOLO con JSON válido, sin comentarios.

Texto: "{texto}"

Responde exactamente en este formato:
{{"tiene_evento": true, "tipo": "cita", "titulo": "texto", "hora": "HH:MM", "cuando": "hoy"}}

Reglas:
- cuando puede ser: "hoy", "mañana", "pasado_mañana"
- hora en formato 24h (ej: "15:30" para 3:30pm)
- NO agregues comentarios
- NO agregues campos extra"""

        try:
            response = ollama.generate(model=self.modelo, prompt=prompt)
            respuesta = response['response'].strip()
            
            # Limpiar comentarios y texto extra
            respuesta = re.sub(r'//.*', '', respuesta)  # Quitar comentarios //
            respuesta = re.sub(r'/\*.*?\*/', '', respuesta, flags=re.DOTALL)  # Quitar /* */
            
            print(f"🤖 Respuesta IA limpia: {respuesta}")
            
            # Extraer solo el JSON
            json_match = re.search(r'\{[^}]+\}', respuesta)
            if json_match:
                datos = json.loads(json_match.group())
                
                if datos.get('tiene_evento'):
                    fecha_hora = self._procesar_fecha_hora_simple(datos)
                    if fecha_hora:
                        return {
                            'valido': True,
                            'tipo': datos.get('tipo', 'recordatorio'),
                            'titulo': datos.get('titulo', 'Sin título'),
                            'fecha_hora': fecha_hora,
                            'descripcion': ''
                        }
        except Exception as e:
            print(f"❌ Error con IA: {e}")
        
        return {'valido': False}
    
    def _procesar_fecha_hora_simple(self, datos: dict) -> Optional[datetime]:
        """Procesa fecha/hora de forma simplificada"""
        try:
            ahora = datetime.now()
            cuando = datos.get('cuando', '').lower()
            hora_str = datos.get('hora', '')
            
            if not hora_str:
                return None
            
            # Parsear hora
            hora, minutos = map(int, hora_str.split(':'))
            
            # Determinar fecha
            if cuando == 'hoy':
                fecha_evento = ahora.replace(hour=hora, minute=minutos, second=0, microsecond=0)
                if fecha_evento <= ahora:
                    fecha_evento += timedelta(days=1)
                return fecha_evento
            
            elif cuando == 'mañana':
                return (ahora + timedelta(days=1)).replace(
                    hour=hora, minute=minutos, second=0, microsecond=0
                )
            
            elif cuando == 'pasado_mañana':
                return (ahora + timedelta(days=2)).replace(
                    hour=hora, minute=minutos, second=0, microsecond=0
                )
        
        except Exception as e:
            print(f"❌ Error procesando fecha/hora: {e}")
        
        return None


class GeneradorNotificacionesInteligentes:
    """Genera notificaciones contextuales e inteligentes"""
    
    def __init__(self, modelo: str = "llama3", perfil_usuario: str = ""):
        self.modelo = modelo
        self.perfil_usuario = perfil_usuario
        
    def actualizar_perfil(self, perfil: str):
        """Actualiza el perfil del usuario para personalizar notificaciones"""
        self.perfil_usuario = perfil
    
    def generar_notificacion(self, evento, minutos_antes: int) -> str:
        """
        Genera una notificación inteligente y personalizada para un evento
        """
        ahora = datetime.now()
        hora_evento = evento.fecha_hora.strftime("%H:%M")
        
        # Determinar contexto temporal
        if minutos_antes == 0:
            # Es el momento exacto del evento
            tiempo_antes_str = "ahora"
            es_momento_exacto = True
        elif minutos_antes >= 60:
            tiempo_antes_str = f"{minutos_antes // 60} horas"
            es_momento_exacto = False
        else:
            tiempo_antes_str = f"{minutos_antes} minutos"
            es_momento_exacto = False
        
        # Construir prompt para Llama3
        if es_momento_exacto:
            prompt = f"""Eres Azul, una asistente con voz de amiga cercana.
ES EL MOMENTO EXACTO del evento. Genera un recordatorio URGENTE pero natural.

PERSONALIDAD: Amiga directa, amable, va al grano
PERFIL: {self.perfil_usuario}

EVENTO:
- {evento.tipo}: {evento.titulo}
- Hora: {hora_evento}
- ES AHORA

ESTILO:
- URGENTE pero amigable
- MUY breve (máximo 1 frase corta)
- Como amiga recordándote: "¡Oye! Es hora de [evento]"
- Ejemplos:
  * Alarma → "¡Arriba! Son las {hora_evento}"
  * Cita → "¡Oye! Tu cita es ahora"
  * Recordatorio → "Es momento: {evento.titulo}"
- Directo, sin rodeos

Genera SOLO el mensaje (sin "Recordatorio:" ni prefijos)."""
        else:
            prompt = f"""Eres Azul, una amiga que le recuerda cosas a su amigo de forma natural.

PERSONALIDAD: Amiga cercana, directa, amable, concisa
PERFIL: {self.perfil_usuario}

EVENTO:
- {evento.tipo}: {evento.titulo}
- Hora: {hora_evento}
- Falta: {tiempo_antes_str}

ESTILO:
- Natural y conversacional
- BREVE (1 frase, máximo 2)
- Como amiga recordándole: "Oye, en [tiempo] tienes [evento]"
- Si falta poco (menos de 10 min) → urgente pero amable
- Si la persona suele tardar → menciónalo con humor ligero
- Ejemplos:
  * "En 30 min tienes {evento.titulo}, ve preparándote"
  * "Oye, tu reunión es en 10 minutos"
  * "En 5 minutos: {evento.titulo}. ¡Apúrate!"
- Directo, sin explicaciones largas

Genera SOLO el mensaje (sin "Recordatorio:" ni prefijos)."""

        try:
            response = ollama.generate(model=self.modelo, prompt=prompt)
            return response['response'].strip()
        except Exception as e:
            # Fallback a notificación simple y amigable
            if minutos_antes == 0:
                return f"¡Oye! Es hora: {evento.titulo}"
            else:
                return f"En {tiempo_antes_str}: {evento.titulo} ({hora_evento})"
    
    def generar_comentario_proactivo(self, eventos_proximos: list) -> str:
        """
        Genera un comentario proactivo sobre eventos próximos
        cuando Azul detecta que puede ser relevante
        """
        if not eventos_proximos:
            return ""
        
        ahora = datetime.now()
        contexto_eventos = "\n".join([
            f"- {e.tipo}: {e.titulo} a las {e.fecha_hora.strftime('%H:%M')} "
            f"(en {e.minutos_restantes()} minutos)"
            for e in eventos_proximos[:3]  # Máximo 3 eventos
        ])
        
        prompt = f"""Eres Azul, una amiga que está conversando y se acuerda de algo.

PERSONALIDAD: Amiga cercana, natural, directa
PERFIL: {self.perfil_usuario}

HORA ACTUAL: {ahora.strftime("%H:%M")}

EVENTOS PRÓXIMOS:
{contexto_eventos}

ESTILO:
- Como amiga que se acuerda: "Oye, por cierto...", "Ah, y recuerda que..."
- MUY breve (1 frase, 2 máximo)
- Natural, como parte de conversación
- Menciona solo el evento más cercano e importante
- Directo, sin rodeos

Genera SOLO el comentario (sin prefijos)."""

        try:
            response = ollama.generate(model=self.modelo, prompt=prompt)
            return response['response'].strip()
        except Exception as e:
            return ""
    
    def debe_comentar_proactivamente(self, eventos_proximos: list, 
                                     ultima_mencion_hace: int = 0) -> bool:
        """
        Determina si Azul debe hacer un comentario proactivo sobre eventos
        
        Args:
            eventos_proximos: Lista de eventos próximos
            ultima_mencion_hace: Minutos desde la última mención de eventos
        
        Returns:
            True si debe comentar, False si no
        """
        if not eventos_proximos:
            return False
        
        evento_mas_cercano = min(eventos_proximos, key=lambda e: e.minutos_restantes())
        minutos_restantes = evento_mas_cercano.minutos_restantes()
        
        # Comentar si:
        # - El evento está en menos de 2 horas y no se ha mencionado en 30 min
        # - El evento está en menos de 30 min y no se ha mencionado en 10 min
        # - El evento está en menos de 10 min siempre
        
        if minutos_restantes <= 10:
            return ultima_mencion_hace >= 5
        elif minutos_restantes <= 30:
            return ultima_mencion_hace >= 10
        elif minutos_restantes <= 120:
            return ultima_mencion_hace >= 30
        
        return False
