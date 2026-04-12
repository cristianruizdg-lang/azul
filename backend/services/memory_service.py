"""
Servicio de Memoria con Supabase
Maneja historial de chat y perfil del usuario
"""

from supabase import create_client, Client
from typing import List, Dict, Optional, Tuple
import sys
import os

# Agregar directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import SUPABASE_URL, SUPABASE_KEY

class MemoryService:
    """Servicio de memoria persistente con Supabase"""
    
    def __init__(self):
        """Inicializa la conexión con Supabase"""
        # Limpiar comillas si existen en las variables
        url = SUPABASE_URL.strip('"').strip("'")
        key = SUPABASE_KEY.strip('"').strip("'")
        
        self.client: Client = create_client(url, key)
        print("✅ MemoryService conectado a Supabase")
    
    async def cargar_historial(
        self, 
        user_id: str = "default", 
        limit: int = 50
    ) -> List[Dict[str, str]]:
        """
        Carga el historial de mensajes del usuario
        
        Args:
            user_id: ID del usuario
            limit: Número máximo de mensajes a cargar
        
        Returns:
            Lista de mensajes en orden cronológico
        """
        try:
            response = self.client.table("mensajes_chat")\
                .select("role, content, created_at")\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()
            
            # Invertir para obtener orden cronológico (más antiguo primero)
            mensajes = list(reversed(response.data))
            
            # Formatear como lista de dicts simple
            historial = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in mensajes
            ]
            
            print(f"📚 Cargados {len(historial)} mensajes del historial")
            return historial
        
        except Exception as e:
            print(f"⚠️ Error cargando historial: {e}")
            return []
    
    async def cargar_perfil(self, user_id: str = "default") -> str:
        """
        Carga el perfil del usuario (gustos/hábitos)
        
        Args:
            user_id: ID del usuario
        
        Returns:
            Perfil formateado como string con bullet points
        """
        try:
            response = self.client.table("perfil_usuario")\
                .select("clave, valor")\
                .execute()
            
            if not response.data:
                print("📝 No hay perfil de usuario aún")
                return ""
            
            # Formatear como bullet list
            perfil = "\n".join([
                f"- {item['clave']}: {item['valor']}"
                for item in response.data
            ])
            
            print(f"✅ Perfil cargado: {len(response.data)} items")
            return perfil
        
        except Exception as e:
            print(f"⚠️ Error cargando perfil: {e}")
            return ""
    
    async def cargar_contexto_completo(
        self, 
        user_id: str = "default"
    ) -> Tuple[List[Dict[str, str]], str]:
        """
        Carga historial y perfil en una sola llamada
        
        Args:
            user_id: ID del usuario
        
        Returns:
            Tupla de (historial, perfil)
        """
        historial = await self.cargar_historial(user_id)
        perfil = await self.cargar_perfil(user_id)
        
        return historial, perfil
    
    async def guardar_mensaje(
        self, 
        role: str, 
        content: str, 
        user_id: str = "default"
    ) -> bool:
        """
        Guarda un mensaje en el historial
        
        Args:
            role: 'user' o 'assistant'
            content: Contenido del mensaje
            user_id: ID del usuario
        
        Returns:
            True si se guardó correctamente
        """
        try:
            self.client.table("mensajes_chat").insert({
                "role": role,
                "content": content
            }).execute()
            
            return True
        
        except Exception as e:
            print(f"❌ Error guardando mensaje: {e}")
            return False
    
    async def guardar_aprendizaje(
        self, 
        clave: str, 
        valor: str, 
        user_id: str = "default"
    ) -> bool:
        """
        Guarda o actualiza un item del perfil del usuario
        
        Args:
            clave: Clave del aprendizaje (ej: "gusto_comida")
            valor: Valor del aprendizaje (ej: "pizza")
            user_id: ID del usuario
        
        Returns:
            True si se guardó correctamente
        """
        try:
            # Upsert: inserta o actualiza si ya existe
            self.client.table("perfil_usuario").upsert(
                {"clave": clave, "valor": valor},
                on_conflict="clave"
            ).execute()
            
            print(f"🧠 Aprendizaje guardado: {clave} → {valor}")
            return True
        
        except Exception as e:
            print(f"❌ Error guardando aprendizaje: {e}")
            return False
    
    async def obtener_perfil_completo(self, user_id: str = "default") -> Dict[str, str]:
        """
        Obtiene el perfil del usuario como diccionario
        
        Args:
            user_id: ID del usuario
        
        Returns:
            Dict con clave-valor del perfil
        """
        try:
            response = self.client.table("perfil_usuario")\
                .select("clave, valor")\
                .execute()
            
            perfil = {
                item["clave"]: item["valor"]
                for item in response.data
            }
            
            return perfil
        
        except Exception as e:
            print(f"❌ Error obteniendo perfil: {e}")
            return {}
    
    async def limpiar_historial_antiguo(
        self, 
        user_id: str = "default", 
        mantener_ultimos: int = 100
    ) -> int:
        """
        Limpia mensajes antiguos del historial (optimización)
        
        Args:
            user_id: ID del usuario
            mantener_ultimos: Cantidad de mensajes a mantener
        
        Returns:
            Número de mensajes eliminados
        """
        try:
            # Obtener todos los mensajes
            response = self.client.table("mensajes_chat")\
                .select("id, created_at")\
                .order("created_at", desc=True)\
                .execute()
            
            if len(response.data) <= mantener_ultimos:
                print("✅ No hay mensajes antiguos que limpiar")
                return 0
            
            # IDs de mensajes a eliminar
            ids_eliminar = [
                msg["id"] 
                for msg in response.data[mantener_ultimos:]
            ]
            
            # Eliminar en batch
            for msg_id in ids_eliminar:
                self.client.table("mensajes_chat")\
                    .delete()\
                    .eq("id", msg_id)\
                    .execute()
            
            print(f"🗑️ Eliminados {len(ids_eliminar)} mensajes antiguos")
            return len(ids_eliminar)
        
        except Exception as e:
            print(f"⚠️ Error limpiando historial: {e}")
            return 0

# Instancia global
memory_service = MemoryService()
