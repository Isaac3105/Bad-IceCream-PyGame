# ai/coach/hints.py
from enum import Enum
from typing import List, Dict, Optional, Tuple
import time
from dataclasses import dataclass
import math

from ai.utils.game_api import GameState

class HintPriority(Enum):
    """Priorité des conseils"""
    LOW = 1      # Suggestions générales
    MEDIUM = 2   # Conseils stratégiques  
    HIGH = 3     # Alertes importantes
    CRITICAL = 4 # Danger immédiat

@dataclass
class Hint:
    """Représentation d'un conseil"""
    message: str
    priority: HintPriority
    category: str
    duration: float  # Durée d'affichage en secondes
    cooldown: float  # Temps avant réaffichage
    last_displayed: float = 0  # Timestamp dernier affichage
    
    def is_ready(self, current_time: float) -> bool:
        """Vérifie si le conseil peut être affiché"""
        return current_time - self.last_displayed >= self.cooldown
    
    def mark_displayed(self, current_time: float):
        """Marque le conseil comme affiché"""
        self.last_displayed = current_time

class HintGenerator:
    """Générateur de conseils intelligents basé sur les métriques"""
    
    def __init__(self):
        self.last_hint_time = 0
        self.min_hint_interval = 3.0  # Secondes entre conseils
    
    def generate_hints(self, metrics: Dict, game_state: GameState) -> List[Hint]:
        """Génère des conseils basés sur métriques et état jeu"""
        current_time = time.time()
        
        # Cooldown global
        if current_time - self.last_hint_time < self.min_hint_interval:
            return []
        
        hints = []
        
        # 1. Conseils PERFORMANCE (vos métriques semaine 1)
        hints.extend(self._generate_performance_hints(metrics, current_time))
        
        # 2. Conseils SITUATIONNELS (état actuel)
        hints.extend(self._generate_situational_hints(game_state, current_time))
        
        # 3. Conseils STRATÉGIQUES
        hints.extend(self._generate_strategic_hints(metrics, game_state, current_time))
        
        # Trier par priorité
        hints.sort(key=lambda h: h.priority.value, reverse=True)
        
        if hints:
            self.last_hint_time = current_time
            
        return hints[:2]  # Maximum 2 conseils à la fois
    
    def _generate_performance_hints(self, metrics: Dict, current_time: float) -> List[Hint]:
        """Conseils basés sur les performances"""
        hints = []
        
        # Mort rapide
        if metrics.get('death_count', 0) > 0:
            death_times = metrics.get('time_between_deaths', [])
            if death_times and death_times[-1] < 10:
                hints.append(Hint(
                    message="⚡ Tu meurs trop vite! Anticipe mieux les ennemis.",
                    priority=HintPriority.HIGH,
                    category="survie",
                    duration=5.0,
                    cooldown=30.0
                ))
        
        # Temps par fruit élevé
        if metrics.get('average_fruit_time', 0) > 8.0:
            hints.append(Hint(
                message="🎯 Tu peux collecter plus rapidement! Planifie ton chemin.",
                priority=HintPriority.LOW,
                category="efficacité",
                duration=4.0,
                cooldown=60.0
            ))
        
        # Beaucoup de zones à risque
        if metrics.get('high_risk_zones', 0) > 5:
            hints.append(Hint(
                message="🗺️ Tu fréquentes trop de zones dangereuses. Sois prudent!",
                priority=HintPriority.MEDIUM,
                category="navigation",
                duration=5.0,
                cooldown=50.0
            ))
        
        return hints
    
    def _generate_situational_hints(self, game_state: GameState, current_time: float) -> List[Hint]:
        """Conseils basés sur la situation actuelle - CORRIGÉ"""
        hints = []
    
        # Vérifier le danger pour chaque ennemi
        player_pos = game_state.player_pos
        for troll_pos in game_state.trolls_pos:
            distance = self._calculate_distance(player_pos, troll_pos)
        
            if distance < 60:  # TRÈS proche - CRITICAL
                # Déterminer la direction
                dx = troll_pos[0] - player_pos[0]
                dy = troll_pos[1] - player_pos[1]
            
                if abs(dx) > abs(dy):
                    direction = "DROITE" if dx > 0 else "GAUCHE"
                else:
                    direction = "BAS" if dy > 0 else "HAUT"
            
                hints.append(Hint(
                    message=f"🚨 Ennemi TRÈS PROCHE à ta {direction}! FUIS IMMÉDIATEMENT!",
                    priority=HintPriority.CRITICAL,
                    category="danger",
                    duration=3.0,
                    cooldown=10.0
                ))
                break  # Un seul conseil CRITICAL suffit
        
            elif distance < 120:  # Proche - HIGH
                # Déterminer la direction
                dx = troll_pos[0] - player_pos[0]
                dy = troll_pos[1] - player_pos[1]
            
                if abs(dx) > abs(dy):
                    direction = "DROITE" if dx > 0 else "GAUCHE"
                else:
                    direction = "BAS" if dy > 0 else "HAUT"
            
                hints.append(Hint(
                    message=f"⚠️ Ennemi proche à ta {direction}! Attention!",
                    priority=HintPriority.HIGH,
                    category="danger",
                    duration=4.0,
                    cooldown=15.0
                ))
                break
    
        # Ennemis multiples proches
        nearby_enemies = self._find_nearby_enemies(game_state.player_pos, game_state.trolls_pos, 150)
        if len(nearby_enemies) >= 2:
            hints.append(Hint(
                message="👥 Deux ennemis ou plus proches! Utilise F pour créer des barrières.",
                priority=HintPriority.HIGH,
                category="défense",
                duration=4.0,
                cooldown=25.0
            ))
    
        # Joueur coincé
        if self._is_player_cornered(game_state.player_pos, game_state):
            hints.append(Hint(
                message="🚧 Tu es coincé! Utilise ESPACE pour détruire les blocs.",
                priority=HintPriority.HIGH,
                category="évasion",
                duration=4.0,
                cooldown=20.0
            ))
    
        return hints
    
    def _generate_strategic_hints(self, metrics: Dict, game_state: GameState, current_time: float) -> List[Hint]:
        """Conseils stratégiques avancés"""
        hints = []
        
        fruits_remaining = len(game_state.fruits_pos)
        total_fruits = metrics.get('total_fruits_collected', 0)
        
        # Fin de niveau
        if fruits_remaining == 1 and total_fruits > 0:
            hints.append(Hint(
                message="🎉 Plus qu'un fruit! Attention aux derniers ennemis.",
                priority=HintPriority.MEDIUM,
                category="objectif",
                duration=4.0,
                cooldown=15.0
            ))
        
        # Pattern répétitif
        fruit_order = metrics.get('fruit_order', [])
        if self._has_repetitive_pattern(fruit_order):
            hints.append(Hint(
                message="🔄 Tu suis toujours le même chemin. Varie ta stratégie!",
                priority=HintPriority.LOW,
                category="stratégie",
                duration=5.0,
                cooldown=90.0
            ))
        
        # Tutoriel début de partie
        if game_state.level == 1 and metrics.get('tick_count', 0) < 50:
            hints.append(Hint(
                message="🎮 Astuce: ZQSD/Flèches pour bouger, F pour glace, ESPACE pour casser.",
                priority=HintPriority.LOW,
                category="tutoriel",
                duration=8.0,
                cooldown=300.0
            ))
        
        return hints
    
    def _check_immediate_danger(self, game_state: GameState) -> Optional[str]:
        """Détecte danger immédiat"""
        player_pos = game_state.player_pos
    
        for troll_pos in game_state.trolls_pos:
            distance = self._calculate_distance(player_pos, troll_pos)
            if distance < 100:  # Augmenté à 100px pour être plus réaliste
                dx = troll_pos[0] - player_pos[0]
                dy = troll_pos[1] - player_pos[1]
            
                # Seuil pour éviter les micro-mouvements
                if abs(dx) > abs(dy) + 10:  # +10 pour biais horizontal
                    direction = "DROITE" if dx > 0 else "GAUCHE"
                elif abs(dy) > abs(dx) + 10:  # +10 pour biais vertical
                    direction = "BAS" if dy > 0 else "HAUT"
                else:
                    # Diagonale - choisir la direction dominante
                    if abs(dx) > abs(dy):
                        direction = "DROITE" if dx > 0 else "GAUCHE"
                    else:
                        direction = "BAS" if dy > 0 else "HAUT"

                return f"Ennemi proche à ta {direction}! Sois prudent!"
        return None
    def _find_nearby_enemies(self, player_pos: Tuple[int, int], 
                           enemies_pos: List[Tuple[int, int]], 
                           radius: int = 150) -> List[Tuple[int, int]]:
        """Trouve ennemis proches"""
        nearby = []
        for enemy_pos in enemies_pos:
            if self._calculate_distance(player_pos, enemy_pos) <= radius:
                nearby.append(enemy_pos)
        return nearby
    
    def _is_player_cornered(self, player_pos: Tuple[int, int], game_state: GameState) -> bool:
        """Vérifie si joueur coincé"""
        directions = [
            (player_pos[0] + 40, player_pos[1]),  # droite
            (player_pos[0] - 40, player_pos[1]),  # gauche
            (player_pos[0], player_pos[1] + 58),  # bas
            (player_pos[0], player_pos[1] - 58)   # haut
        ]
        
        blocked = 0
        for direction in directions:
            if not self._is_valid_position(direction, game_state):
                blocked += 1
        
        return blocked >= 3
    
    def _has_repetitive_pattern(self, fruit_order: List[str]) -> bool:
        """Détecte patterns répétitifs"""
        if len(fruit_order) < 4:
            return False
        
        for pattern_len in range(2, min(3, len(fruit_order) // 2) + 1):
            for i in range(len(fruit_order) - pattern_len * 2 + 1):
                if fruit_order[i:i+pattern_len] == fruit_order[i+pattern_len:i+pattern_len*2]:
                    return True
        
        return False
    
    def _calculate_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """Calcule distance entre points"""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    def _is_valid_position(self, pos: Tuple[int, int], game_state: GameState) -> bool:
        """Vérifie si position valide"""
        if pos[0] < 50 or pos[0] >= 770 or pos[1] < 50 or pos[1] >= 572:
            return False
        
        for ice_pos in game_state.iceblocks_pos:
            if self._calculate_distance(pos, ice_pos) < 30:
                return False
        
        return True