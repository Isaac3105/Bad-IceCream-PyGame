"""
Rôles intelligents pour les ennemis - Version corrigée
"""
from enum import Enum
from typing import List, Tuple, Optional, Dict, Any
import random
import math
from dataclasses import dataclass
from .a_star import AStarPathfinder
from ai.utils.game_api import GameState
from ai.utils.geometry import distance_between, angle_between_points, get_direction_vector


class EnemyRole(Enum):
    """Types de rôles pour les ennemis"""
    HUNTER = "hunter"      # Chasse le joueur
    PATROLLER = "patroller" # Patrouille des waypoints
    BLOCKER = "blocker"    # Bloque les passages stratégiques

@dataclass
class Waypoint:
    """Point de patrouille pour les patrouilleurs"""
    x: int
    y: int
    wait_time: float = 0.0

class EnemyAI:
    """Classe unique pour l'IA des ennemis avec différents rôles"""
    
    def __init__(self, role: EnemyRole, enemy_id: int, **kwargs):
        """
        Initialise l'IA pour un ennemi
        
        Args:
            role: Rôle de l'ennemi (hunter, patroller, blocker)
            enemy_id: Identifiant unique de l'ennemi
            **kwargs: Paramètres spécifiques au rôle
        """
        self.role = role
        self.enemy_id = enemy_id
        self.pathfinder = AStarPathfinder(20, 15)  # Grille 20x15
        
        # État commun
        self.current_path: List[Tuple[int, int]] = []
        self.state: Dict[str, Any] = {}
        
        # Initialisation spécifique au rôle
        if role == EnemyRole.HUNTER:
            self._init_hunter(kwargs)
        elif role == EnemyRole.PATROLLER:
            self._init_patroller(kwargs)
        elif role == EnemyRole.BLOCKER:
            self._init_blocker(kwargs)
        else:
            raise ValueError(f"Rôle inconnu: {role}")
    
    def _init_hunter(self, kwargs):
        """Initialise les paramètres du chasseur"""
        self.aggression = kwargs.get('aggression', 0.8)
        self.last_player_pos = None
        self.patience = 0
        self.view_distance = 300
        self.attack_distance = 50
        self.state.update({
            'mode': 'patrol',  # 'hunt', 'patrol', 'wait'
            'last_seen_player': None,
            'hunting_duration': 0
        })
    
    def _init_patroller(self, kwargs):
        """Initialise les paramètres du patrouilleur"""
        self.waypoints = kwargs.get('waypoints', [])
        if not self.waypoints:
            # Générer des waypoints par défaut
            self.waypoints = self._generate_default_waypoints()
        
        self.current_waypoint_index = 0
        self.wait_timer = 0.0
        self.patrol_speed = kwargs.get('patrol_speed', 1.0)
        self.state.update({
            'patrol_direction': 1,  # 1 = forward, -1 = backward
            'waiting': False
        })
    
    def _init_blocker(self, kwargs):
        """Initialise les paramètres du bloqueur"""
        self.strategic_points = kwargs.get('strategic_points', [])
        if not self.strategic_points:
            # Points stratégiques par défaut (entrées, sorties)
            self.strategic_points = [(100, 100), (700, 100), (100, 500), (700, 500)]
        
        self.current_strategic_index = 0
        self.blocking_timer = 0.0
        self.block_duration = kwargs.get('block_duration', 5.0)
        self.state.update({
            'blocking': False,
            'next_move_time': 0
        })
    
    def _generate_default_waypoints(self) -> List[Waypoint]:
        """Génère des waypoints par défaut en forme de carré"""
        return [
            Waypoint(100, 100, 1.0),
            Waypoint(700, 100, 1.0),
            Waypoint(700, 500, 1.0),
            Waypoint(100, 500, 1.0)
        ]
    
    def update(self, enemy_pos: Tuple[int, int], game_state: GameState) -> Dict:
        """
        Met à jour l'IA et retourne une action
        
        Returns:
            Dictionnaire d'action à effectuer
        """
        if self.role == EnemyRole.HUNTER:
            return self._update_hunter(enemy_pos, game_state)
        elif self.role == EnemyRole.PATROLLER:
            return self._update_patroller(enemy_pos, game_state)
        elif self.role == EnemyRole.BLOCKER:
            return self._update_blocker(enemy_pos, game_state)
        else:
            return {'type': 'wait', 'direction': 'none'}
    
    def _update_hunter(self, enemy_pos: Tuple[int, int], game_state: GameState) -> Dict:
        """Logique du chasseur"""
        player_pos = game_state.player_pos
        
        # Si joueur mort ou invulnérable, patrouiller
        if not game_state.player_alive:
            return self._patrol_action(enemy_pos, game_state)
        
        # Calculer la distance au joueur
        dist = distance_between(enemy_pos, player_pos)
        
        # Si joueur visible et proche
        if dist < self.view_distance and self._has_line_of_sight(enemy_pos, player_pos, game_state):
            self.state['mode'] = 'hunt'
            self.state['last_seen_player'] = player_pos
            self.state['hunting_duration'] += 1
            
            # Déterminer l'action
            if dist < self.attack_distance:
                # Attaquer
                direction = self._get_direction_to_target(enemy_pos, player_pos)
                return {
                    'type': 'attack',
                    'direction': direction,
                    'target': player_pos
                }
            else:
                # Poursuivre
                direction = self._get_direction_to_target(enemy_pos, player_pos)
                return {
                    'type': 'chase',
                    'direction': direction,
                    'target': player_pos,
                    'aggression': self.aggression
                }
        else:
            # Joueur non visible
            if self.state['mode'] == 'hunt' and self.state['last_seen_player']:
                # Chercher à la dernière position connue
                if distance_between(enemy_pos, self.state['last_seen_player']) < 50:
                    # Passer en mode patrouille après recherche
                    self.state['mode'] = 'patrol'
                    return self._patrol_action(enemy_pos, game_state)
                else:
                    direction = self._get_direction_to_target(enemy_pos, self.state['last_seen_player'])
                    return {
                        'type': 'search',
                        'direction': direction,
                        'last_known_pos': self.state['last_seen_player']
                    }
            else:
                # Mode patrouille
                return self._patrol_action(enemy_pos, game_state)
    
    def _update_patroller(self, enemy_pos: Tuple[int, int], game_state: GameState) -> Dict:
        """Logique du patrouilleur"""
        current_waypoint = self.waypoints[self.current_waypoint_index]
        
        # Vérifier si on est arrivé au waypoint
        dist = distance_between(enemy_pos, (current_waypoint.x, current_waypoint.y))
        
        if dist < 20:  # Arrivé au waypoint
            if not self.state['waiting']:
                # Commencer à attendre
                self.state['waiting'] = True
                self.wait_timer = 0.0
            
            # Vérifier le temps d'attente
            if self.wait_timer < current_waypoint.wait_time:
                self.wait_timer += 1.0 / 60.0  # Incrémenter par frame
                return {
                    'type': 'wait',
                    'direction': self._get_random_look_direction(),
                    'remaining_time': current_waypoint.wait_time - self.wait_timer
                }
            else:
                # Passer au waypoint suivant
                self.state['waiting'] = False
                self.wait_timer = 0.0
                
                # Déterminer le prochain waypoint
                if random.random() < 0.1:  # 10% de chance de changer de direction
                    self.state['patrol_direction'] *= -1
                
                next_index = self.current_waypoint_index + self.state['patrol_direction']
                if next_index >= len(self.waypoints):
                    next_index = 0
                elif next_index < 0:
                    next_index = len(self.waypoints) - 1
                
                self.current_waypoint_index = next_index
                current_waypoint = self.waypoints[self.current_waypoint_index]
        
        # Se déplacer vers le waypoint
        direction = self._get_direction_to_target(enemy_pos, (current_waypoint.x, current_waypoint.y))
        
        return {
            'type': 'patrol',
            'direction': direction,
            'waypoint_index': self.current_waypoint_index,
            'speed': self.patrol_speed
        }
    
    def _update_blocker(self, enemy_pos: Tuple[int, int], game_state: GameState) -> Dict:
        """Logique du bloqueur"""
        strategic_point = self.strategic_points[self.current_strategic_index]
        
        # Vérifier si on est sur le point stratégique
        dist = distance_between(enemy_pos, strategic_point)
        
        if dist < 30:  # Positionné sur le point
            if not self.state['blocking']:
                # Commencer à bloquer
                self.state['blocking'] = True
                self.blocking_timer = 0.0
            
            # Vérifier la durée du blocage
            if self.blocking_timer < self.block_duration:
                self.blocking_timer += 1.0 / 60.0
                
                # Surveiller les alentours
                if random.random() < 0.2:  # 20% de chance de changer de direction
                    direction = self._get_random_look_direction()
                else:
                    direction = self.state.get('last_direction', 'down')
                
                self.state['last_direction'] = direction
                
                return {
                    'type': 'block',
                    'direction': direction,
                    'strategic_point': strategic_point,
                    'remaining_time': self.block_duration - self.blocking_timer
                }
            else:
                # Changer de point stratégique
                self.state['blocking'] = False
                self.blocking_timer = 0.0
                
                # Choisir un nouveau point (pas forcément le suivant)
                available_indices = list(range(len(self.strategic_points)))
                available_indices.remove(self.current_strategic_index)
                self.current_strategic_index = random.choice(available_indices)
                strategic_point = self.strategic_points[self.current_strategic_index]
        
        # Se déplacer vers le point stratégique
        direction = self._get_direction_to_target(enemy_pos, strategic_point)
        
        return {
            'type': 'move_to_block',
            'direction': direction,
            'target': strategic_point
        }
    
    def _patrol_action(self, enemy_pos: Tuple[int, int], game_state: GameState) -> Dict:
        """Action de patrouille générique"""
        # Patrouille aléatoire
        if random.random() < 0.1:  # 10% de chance de changer de direction
            directions = ['up', 'down', 'left', 'right']
            direction = random.choice(directions)
            
            return {
                'type': 'patrol',
                'direction': direction,
                'random': True
            }
        else:
            # Continuer dans la même direction
            last_direction = self.state.get('last_direction', 'right')
            return {
                'type': 'patrol',
                'direction': last_direction,
                'random': False
            }
    
    def _has_line_of_sight(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], 
                          game_state: GameState) -> bool:
        """Vérifie la ligne de vue entre deux positions"""
        # Simplifié: vérifier si pas d'obstacles entre les deux points
        # En réalité, il faudrait utiliser un raycast
        
        # Pour l'instant, on vérifie juste si la distance est petite
        # et s'il n'y a pas trop d'obstacles proches
        obstacles = game_state.iceblocks_pos
        if not obstacles:
            return True
        
        # Vérifier si un obstacle est sur la ligne
        for obstacle in obstacles:
            # Distance point-ligne simplifiée
            if self._distance_point_to_line(obstacle, from_pos, to_pos) < 30:
                return False
        
        return True
    
    def _distance_point_to_line(self, point: Tuple[int, int], 
                               line_start: Tuple[int, int], 
                               line_end: Tuple[int, int]) -> float:
        """Distance d'un point à une ligne"""
        x, y = point
        x1, y1 = line_start
        x2, y2 = line_end
        
        # Formule de distance point-ligne
        numerator = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
        denominator = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
        
        return numerator / denominator if denominator != 0 else float('inf')
    
    def _get_direction_to_target(self, from_pos: Tuple[int, int], 
                                to_pos: Tuple[int, int]) -> str:
        """Retourne la direction vers la cible"""
        dx = to_pos[0] - from_pos[0]
        dy = to_pos[1] - from_pos[1]
        
        # Priorité aux déplacements horizontaux/verticaux
        if abs(dx) > abs(dy):
            return 'right' if dx > 0 else 'left'
        else:
            return 'down' if dy > 0 else 'up'
    
    def _get_random_look_direction(self) -> str:
        """Retourne une direction aléatoire pour regarder autour"""
        return random.choice(['up', 'down', 'left', 'right'])

# Factory pour créer des IA selon le rôle
def create_enemy_ai(role: EnemyRole, enemy_id: int, **kwargs) -> EnemyAI:
    """Crée une instance d'IA selon le rôle spécifié"""
    return EnemyAI(role, enemy_id, **kwargs)

# Coordinateur pour gérer plusieurs ennemis
class EnemyCoordinator:
    """Coordonne les actions de plusieurs ennemis"""
    
    def __init__(self):
        self.enemies: Dict[int, EnemyAI] = {}
        self.communication: Dict[str, Any] = {}
    
    def add_enemy(self, enemy_id: int, role: EnemyRole, **kwargs):
        """Ajoute un ennemi au coordinateur"""
        self.enemies[enemy_id] = create_enemy_ai(role, enemy_id, **kwargs)
    
    def update_all(self, enemies_data: List[Dict], game_state: GameState) -> Dict[int, Dict]:
        """
        Met à jour tous les ennemis
        
        Returns:
            Dictionnaire {enemy_id: action}
        """
        actions = {}
        
        for enemy_data in enemies_data:
            enemy_id = enemy_data['id']
            enemy_pos = enemy_data['pos']
            
            if enemy_id in self.enemies:
                ai = self.enemies[enemy_id]
                action = ai.update(enemy_pos, game_state)
                actions[enemy_id] = action
                
                # Communication entre ennemis
                if action.get('type') == 'chase' and ai.role == EnemyRole.HUNTER:
                    # Informer les autres ennemis de la position du joueur
                    self.communication['player_last_seen'] = action.get('target')
                    self.communication['reported_by'] = enemy_id
        
        return actions
    
    def remove_enemy(self, enemy_id: int):
        """Retire un ennemi"""
        if enemy_id in self.enemies:
            del self.enemies[enemy_id]