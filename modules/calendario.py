"""
Módulo de Calendario y Recordatorios para Azul
Gestiona citas, alarmas y recordatorios con notificaciones inteligentes
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import threading
import time

class EventoCalendario:
    """Representa un evento en el calendario de Azul"""
    
    def __init__(self, titulo: str, fecha_hora: datetime, tipo: str = "cita", 
                 descripcion: str = "", notificaciones: List[int] = None):
        """
        Args:
            titulo: Título del evento
            fecha_hora: Fecha y hora del evento
            tipo: Tipo de evento ('cita', 'alarma', 'recordatorio')
            descripcion: Descripción adicional del evento
            notificaciones: Lista de minutos antes del evento para notificar
        """
        self.id = self._generar_id()
        self.titulo = titulo
        self.fecha_hora = fecha_hora
        self.tipo = tipo
        self.descripcion = descripcion
        # Por defecto: 30, 10, 5 minutos antes Y en el momento exacto (0)
        self.notificaciones = notificaciones or [30, 10, 5, 0]
        self.notificaciones_enviadas = []
        self.completado = False
        self.creado_en = datetime.now()
        
    def _generar_id(self) -> str:
        """Genera un ID único para el evento"""
        return f"evt_{int(datetime.now().timestamp() * 1000)}"
    
    def to_dict(self) -> Dict:
        """Convierte el evento a diccionario para guardar"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'fecha_hora': self.fecha_hora.isoformat(),
            'tipo': self.tipo,
            'descripcion': self.descripcion,
            'notificaciones': self.notificaciones,
            'notificaciones_enviadas': self.notificaciones_enviadas,
            'completado': self.completado,
            'creado_en': self.creado_en.isoformat()
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'EventoCalendario':
        """Crea un evento desde un diccionario"""
        evento = EventoCalendario(
            titulo=data['titulo'],
            fecha_hora=datetime.fromisoformat(data['fecha_hora']),
            tipo=data['tipo'],
            descripcion=data.get('descripcion', ''),
            notificaciones=data.get('notificaciones', [30, 10, 5])
        )
        evento.id = data['id']
        evento.notificaciones_enviadas = data.get('notificaciones_enviadas', [])
        evento.completado = data.get('completado', False)
        evento.creado_en = datetime.fromisoformat(data['creado_en'])
        return evento
    
    def tiempo_restante(self) -> timedelta:
        """Calcula el tiempo restante hasta el evento"""
        return self.fecha_hora - datetime.now()
    
    def minutos_restantes(self) -> int:
        """Retorna los minutos restantes hasta el evento"""
        delta = self.tiempo_restante()
        return int(delta.total_seconds() / 60)


class GestorCalendario:
    """Gestor principal del calendario de Azul"""
    
    def __init__(self, archivo_datos: str = "data/calendario.json"):
        self.archivo_datos = archivo_datos
        self.eventos: List[EventoCalendario] = []
        self.callbacks_notificacion = []
        self.monitor_activo = False
        self._cargar_eventos()
        
    def _cargar_eventos(self):
        """Carga eventos desde el archivo JSON"""
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self.eventos = [EventoCalendario.from_dict(e) for e in datos]
                    # Limpiar eventos antiguos completados
                    self._limpiar_eventos_antiguos()
            except Exception as e:
                print(f"Error cargando calendario: {e}")
                self.eventos = []
    
    def _guardar_eventos(self):
        """Guarda eventos en el archivo JSON"""
        try:
            os.makedirs(os.path.dirname(self.archivo_datos), exist_ok=True)
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump([e.to_dict() for e in self.eventos], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando calendario: {e}")
    
    def _limpiar_eventos_antiguos(self):
        """Elimina eventos completados que tienen más de 7 días"""
        ahora = datetime.now()
        self.eventos = [e for e in self.eventos if not (
            e.completado and (ahora - e.fecha_hora).days > 7
        )]
        self._guardar_eventos()
    
    def agregar_evento(self, titulo: str, fecha_hora: datetime, tipo: str = "cita",
                      descripcion: str = "", notificaciones: List[int] = None) -> EventoCalendario:
        """Agrega un nuevo evento al calendario"""
        evento = EventoCalendario(titulo, fecha_hora, tipo, descripcion, notificaciones)
        self.eventos.append(evento)
        self._guardar_eventos()
        return evento
    
    def eliminar_evento(self, evento_id: str) -> bool:
        """Elimina un evento por ID"""
        eventos_filtrados = [e for e in self.eventos if e.id != evento_id]
        if len(eventos_filtrados) < len(self.eventos):
            self.eventos = eventos_filtrados
            self._guardar_eventos()
            return True
        return False
    
    def marcar_completado(self, evento_id: str) -> bool:
        """Marca un evento como completado"""
        for evento in self.eventos:
            if evento.id == evento_id:
                evento.completado = True
                self._guardar_eventos()
                return True
        return False
    
    def obtener_eventos_proximos(self, horas: int = 24) -> List[EventoCalendario]:
        """Obtiene eventos próximos dentro de las siguientes X horas"""
        limite = datetime.now() + timedelta(hours=horas)
        return [e for e in self.eventos 
                if not e.completado and datetime.now() <= e.fecha_hora <= limite]
    
    def obtener_eventos_hoy(self) -> List[EventoCalendario]:
        """Obtiene todos los eventos de hoy"""
        hoy = datetime.now().date()
        return [e for e in self.eventos 
                if not e.completado and e.fecha_hora.date() == hoy]
    
    def obtener_evento_por_id(self, evento_id: str) -> Optional[EventoCalendario]:
        """Busca un evento por ID"""
        for evento in self.eventos:
            if evento.id == evento_id:
                return evento
        return None
    
    def registrar_callback_notificacion(self, callback):
        """Registra una función callback para notificaciones"""
        self.callbacks_notificacion.append(callback)
    
    def _disparar_notificacion(self, evento: EventoCalendario, minutos_antes: int):
        """Dispara notificación para un evento"""
        for callback in self.callbacks_notificacion:
            try:
                callback(evento, minutos_antes)
            except Exception as e:
                print(f"Error en callback de notificación: {e}")
    
    def iniciar_monitor(self):
        """Inicia el monitoreo de eventos para notificaciones"""
        if self.monitor_activo:
            return
        
        self.monitor_activo = True
        threading.Thread(target=self._monitor_eventos, daemon=True).start()
    
    def detener_monitor(self):
        """Detiene el monitoreo de eventos"""
        self.monitor_activo = False
    
    def _monitor_eventos(self):
        """Hilo que monitorea continuamente los eventos"""
        while self.monitor_activo:
            try:
                ahora = datetime.now()
                
                for evento in self.eventos:
                    if evento.completado:
                        continue
                    
                    minutos_restantes = evento.minutos_restantes()
                    
                    # Verificar si es tiempo de notificar
                    for minutos_aviso in evento.notificaciones:
                        # Para el momento exacto (0 minutos), notificar si estamos en el rango de -1 a +1 minuto
                        if minutos_aviso == 0:
                            if (0 not in evento.notificaciones_enviadas and
                                -1 <= minutos_restantes <= 1):
                                # Notificación del momento exacto
                                self._disparar_notificacion(evento, 0)
                                evento.notificaciones_enviadas.append(0)
                                self._guardar_eventos()
                        
                        # Para otras notificaciones, usar lógica normal
                        elif (minutos_aviso not in evento.notificaciones_enviadas and
                              0 <= minutos_restantes <= minutos_aviso):
                            # Enviar notificación
                            self._disparar_notificacion(evento, minutos_aviso)
                            evento.notificaciones_enviadas.append(minutos_aviso)
                            self._guardar_eventos()
                    
                    # Marcar como completado si ya pasó hace más de 1 hora
                    if minutos_restantes < -60 and not evento.completado:
                        evento.completado = True
                        self._guardar_eventos()
                
                # Revisar cada 30 segundos
                time.sleep(30)
                
            except Exception as e:
                print(f"Error en monitor de eventos: {e}")
                time.sleep(60)
    
    def obtener_contexto_para_ia(self) -> str:
        """
        Genera un contexto sobre eventos próximos para que Azul pueda 
        hacer comentarios inteligentes
        """
        ahora = datetime.now()
        eventos_proximos = self.obtener_eventos_proximos(24)
        
        if not eventos_proximos:
            return "No hay eventos programados para las próximas 24 horas."
        
        contexto = "Eventos próximos:\n"
        for evento in eventos_proximos:
            minutos = evento.minutos_restantes()
            horas = minutos // 60
            mins_restantes = minutos % 60
            
            tiempo_str = ""
            if horas > 0:
                tiempo_str = f"{horas}h {mins_restantes}min"
            else:
                tiempo_str = f"{mins_restantes}min"
            
            contexto += f"- {evento.tipo.upper()}: '{evento.titulo}' en {tiempo_str} ({evento.fecha_hora.strftime('%H:%M')})\n"
        
        return contexto
