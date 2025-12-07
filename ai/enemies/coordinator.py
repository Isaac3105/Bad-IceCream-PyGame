"""
Coordinateur pour la communication entre ennemis
"""
from typing import List, Dict, Tuple, Optional
from enum import Enum
from dataclasses import dataclass
from ai.utils.game_api import GameState

class CommunicationType(Enum):
    """Types de communication entre ennemis"""
    PLAYER_LOCATION = "player_location"
    STRATEGIC_POINT = "strategic_point"
    TRAP_SET = "trap_set"
    COORDINATED_ATTACK = "coordinated_attack"

@dataclass
class Message:
    """Message entre ennemis"""
    sender_id: int
    message_type: CommunicationType
    data: Dict
    timestamp: float
    range_limit: float = 300.0  # Portée du message

class AICoordinator:
    """Gère la communication et coordination entre ennemis"""
    
    def __init__(self, communication_range: float = 300.0):
        self.communication_range = communication_range
        self.messages: List[Message] = []
        self.shared_knowledge: Dict = {
            "last_player_positions": [],
            "strategic_points_controlled": [],
            "traps_active": [],
            "attack_phases": {}
        }
        self.message_history: List[Message] = []
        self.max_messages = 50
        
    def update(self, enemies_positions: List[Tuple[int, int, int]], 
               game_state: GameState) -> List[Message]:
        """
        Met à jour le coordinateur et retourne les messages à diffuser
        
        Args:
            enemies_positions: Liste de (enemy_id, x, y)
            game_state: État actuel du jeu
            
        Returns:
            Liste des messages à envoyer
        """
        self._clean_old_messages()
        
        new_messages = []
        
        # Détection automatique de situations à communiquer
        if game_state.player_alive:
            # Si joueur détecté par plusieurs ennemis
            player_pos = game_state.player_pos
            detecting_enemies = []
            
            for enemy_id, x, y in enemies_positions:
                distance = self._calculate_distance((x, y), player_pos)
                if distance < 200:  # Détection à 200 pixels
                    detecting_enemies.append(enemy_id)
            
            if len(detecting_enemies) >= 2:
                # Coordonner une attaque
                message = Message(
                    sender_id=-1,  # -1 pour le coordinateur
                    message_type=CommunicationType.COORDINATED_ATTACK,
                    data={
                        "player_position": player_pos,
                        "detecting_enemies": detecting_enemies,
                        "suggested_strategy": "pincer_movement"
                    },
                    timestamp=game_state.timer
                )
                new_messages.append(message)
                self.messages.append(message)
        
        # Propagation des messages existants
        for message in self.messages[:]:
            if game_state.timer - message.timestamp < 5.0:  # Messages valides 5 secondes
                new_messages.append(message)
        
        return new_messages
    
    def send_message(self, sender_id: int, message_type: CommunicationType, 
                    data: Dict, timestamp: float) -> Message:
        """Crée et enregistre un nouveau message"""
        message = Message(
            sender_id=sender_id,
            message_type=message_type,
            data=data,
            timestamp=timestamp,
            range_limit=self.communication_range
        )
        
        self.messages.append(message)
        self.message_history.append(message)
        
        # Garder l'historique limité
        if len(self.message_history) > self.max_messages:
            self.message_history.pop(0)
        
        return message
    
    def get_messages_for_enemy(self, enemy_id: int, enemy_pos: Tuple[int, int], 
                              current_time: float) -> List[Message]:
        """
        Récupère les messages pertinents pour un ennemi spécifique
        
        Args:
            enemy_id: ID de l'ennemi
            enemy_pos: Position de l'ennemi
            current_time: Temps actuel
            
        Returns:
            Liste des messages pertinents
        """
        relevant_messages = []
        
        for message in self.messages:
            # Vérifier la portée
            if message.sender_id >= 0:  # Pas un message système
                sender_pos = self._get_enemy_position(message.sender_id)
                if sender_pos:
                    distance = self._calculate_distance(enemy_pos, sender_pos)
                    if distance > message.range_limit:
                        continue
            
            # Vérifier l'âge
            if current_time - message.timestamp > 5.0:  # 5 secondes max
                continue
            
            # Éviter les messages de soi-même
            if message.sender_id == enemy_id:
                continue
            
            relevant_messages.append(message)
        
        return relevant_messages
    
    def update_shared_knowledge(self, key: str, value, max_items: int = 10):
        """Met à jour la connaissance partagée"""
        if key not in self.shared_knowledge:
            self.shared_knowledge[key] = []
        
        self.shared_knowledge[key].append(value)
        
        # Limiter la taille
        if len(self.shared_knowledge[key]) > max_items:
            self.shared_knowledge[key].pop(0)
    
    def get_shared_knowledge(self, key: str, default=None):
        """Récupère une connaissance partagée"""
        return self.shared_knowledge.get(key, default)
    
    def _clean_old_messages(self):
        """Nettoie les messages trop anciens"""
        current_time = self.messages[-1].timestamp if self.messages else 0
        self.messages = [m for m in self.messages 
                        if current_time - m.timestamp < 10.0]  # Garder 10 secondes
    
    def _calculate_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
    
    def _get_enemy_position(self, enemy_id: int) -> Optional[Tuple[int, int]]:
        """Récupère la position d'un ennemi (à implémenter selon votre jeu)"""
        # Cette méthode dépend de votre implémentation spécifique
        return None

# Singleton pour le coordinateur global
_global_coordinator: Optional[AICoordinator] = None

def get_global_coordinator() -> AICoordinator:
    """Retourne le coordinateur global (singleton)"""
    global _global_coordinator
    if _global_coordinator is None:
        _global_coordinator = AICoordinator()
    return _global_coordinator

def reset_global_coordinator():
    """Réinitialise le coordinateur global"""
    global _global_coordinator
    _global_coordinator = None