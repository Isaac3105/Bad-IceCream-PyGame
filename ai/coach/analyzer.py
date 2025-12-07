"""
Analyseur de performance pour le coach IA - Version adaptée
"""
import json
import time
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass
from pathlib import Path
from enum import Enum

from ai.utils.geometry import distance_between, point_in_rect, is_point_visible
from ai.utils.game_api import GameState, GameAPI

@dataclass
class PerformanceMetrics:
    """Conteneur pour toutes les métriques de performance"""
    death_count: int = 0
    fruit_order: List[str] = None  # Types de fruits dans l'ordre de collecte
    time_between_deaths: List[float] = None  # Temps entre chaque mort
    average_fruit_time: float = 0.0  # Temps moyen par fruit
    player_routes: List[List[Tuple[int, int]]] = None  # Trajectoires du joueur
    risk_zones: Dict[Tuple[int, int], int] = None  # Zones à haut risque
    ice_block_usage: int = 0  # Nombre de blocs de glace placés
    session_start_time: float = 0.0
    last_death_time: float = 0.0
    fruits_collected_this_session: int = 0
    
    def __post_init__(self):
        """Initialise les listes si None"""
        if self.fruit_order is None:
            self.fruit_order = []
        if self.time_between_deaths is None:
            self.time_between_deaths = []
        if self.player_routes is None:
            self.player_routes = []
        if self.risk_zones is None:
            self.risk_zones = {}

class PerformanceAnalyzer:
    """
    Analyse les performances du joueur en temps réel
    et génère des métriques pour le coach
    """
    
    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.previous_state: Optional[GameState] = None
        self.current_session_start = time.time()
        self.tick_count = 0
        
        # Route actuelle du joueur
        self.current_route: List[Tuple[int, int]] = []
        
        # Pour suivre les fruits collectés
        self.collected_fruits_this_session: Set[Tuple[int, int]] = set()
        
        # Pour suivre l'usage des blocs de glace
        self.previous_iceblocks: Set[Tuple[int, int]] = set()
        
        # Pour suivre les fruits déjà collectés dans l'état précédent
        self.previous_fruits_collected: Set[Tuple[int, int]] = set()
    
    def analyze_snapshot(self, game_state: GameState) -> Dict:
        """
        Analyse un snapshot du jeu et met à jour les métriques
        
        Args:
            game_state: État actuel du jeu
            
        Returns:
            Dict: Métriques calculées
        """
        self.tick_count += 1
        self.last_game_state = game_state  # Stocker le dernier état pour l'export
        
        if self.tick_count == 1:
            self.current_session_start = game_state.timer
        
        # Détection des événements
        self._detect_death(game_state)
        self._detect_fruit_collection(game_state)
        self._detect_ice_block_usage(game_state)
        self._track_player_movement(game_state)
        self._analyze_risk_zones(game_state)
        
        # Calcul des métriques dérivées
        self._calculate_derived_metrics(game_state)
        
        self.previous_state = game_state
        
        return self._get_current_metrics(game_state)
    
    def _detect_death(self, game_state: GameState):
        """Détecte si le joueur vient de mourir"""
        if self.previous_state and self.previous_state.player_alive and not game_state.player_alive:
            self.metrics.death_count += 1
            
            # Calcul du temps depuis la dernière mort
            current_time = game_state.timer
            if self.metrics.last_death_time > 0:
                time_since_last_death = current_time - self.metrics.last_death_time
                self.metrics.time_between_deaths.append(time_since_last_death)
            
            self.metrics.last_death_time = current_time
            
            # Réinitialiser le compteur de fruits pour la nouvelle session
            self.metrics.fruits_collected_this_session = 0
            self.collected_fruits_this_session.clear()
            self.current_session_start = current_time
    
    def _detect_fruit_collection(self, game_state: GameState):
        """Détecte la collecte de nouveaux fruits"""
        if not self.previous_state:
            return
        
        # Fruits dans l'état précédent
        previous_fruits = set(self.previous_state.fruits_pos)
        current_fruits = set(game_state.fruits_pos)
        
        # Fruits collectés (disparus entre les deux états)
        collected_fruits = previous_fruits - current_fruits
        
        for fruit_pos in collected_fruits:
            # Récupérer le type de fruit
            fruit_type = self._get_fruit_type(fruit_pos, game_state)
            if fruit_type not in self.metrics.fruit_order:
                self.metrics.fruit_order.append(fruit_type)
                self.metrics.fruits_collected_this_session += 1
                self.collected_fruits_this_session.add(fruit_pos)
                
                print(f"🍎 Fruit collecté: {fruit_type} à {fruit_pos}")
    
    def _get_fruit_type(self, fruit_pos: Tuple[int, int], game_state: GameState) -> str:
        """Détermine le type de fruit basé sur la position"""
        # Vérifier dans fruit_types
        if hasattr(game_state, 'fruit_types') and fruit_pos in game_state.fruit_types:
            return game_state.fruit_types[fruit_pos]
        
        # Fallback: déterminer par position
        fruit_types = ["apple", "banana", "grape", "orange", "strawberry"]
        hash_val = hash(fruit_pos) % len(fruit_types)
        return fruit_types[hash_val]
    
    def _detect_ice_block_usage(self, game_state: GameState):
        """Détecte la création de nouveaux blocs de glace"""
        current_iceblocks = set(game_state.iceblocks_pos)
        
        if self.previous_iceblocks:
            new_blocks = current_iceblocks - self.previous_iceblocks
            if new_blocks:
                self.metrics.ice_block_usage += len(new_blocks)
                print(f"🧊 {len(new_blocks)} nouveau(x) bloc(s) de glace créé(s)")
        
        self.previous_iceblocks = current_iceblocks
    
    def _track_player_movement(self, game_state: GameState):
        """Track la trajectoire du joueur"""
        current_pos = game_state.player_pos
        
        if not self.current_route:
            self.current_route.append(current_pos)
        else:
            last_pos = self.current_route[-1]
            # N'ajouter que si le joueur a bougé significativement
            if distance_between(last_pos, current_pos) > 20:  # Seuil de mouvement
                self.current_route.append(current_pos)
        
        # Si la route devient trop longue, enregistrer et recommencer
        if len(self.current_route) > 50:
            self.metrics.player_routes.append(self.current_route.copy())
            self.current_route = [current_pos]
    
    def _analyze_risk_zones(self, game_state: GameState):
        """Identifie les zones à risque (proches des ennemis)"""
        player_pos = game_state.player_pos
        
        for troll_pos in game_state.trolls_pos:
            distance = distance_between(player_pos, troll_pos)
            if distance < 100:  # Zone de risque si ennemi à moins de 100 pixels
                zone_key = self._quantize_position(player_pos)
                self.metrics.risk_zones[zone_key] = self.metrics.risk_zones.get(zone_key, 0) + 1
    
    def _calculate_derived_metrics(self, game_state: GameState):
        """Calcule les métriques dérivées"""
        # Temps moyen par fruit dans cette session
        if self.metrics.fruits_collected_this_session > 0:
            session_duration = game_state.timer - self.current_session_start
            self.metrics.average_fruit_time = session_duration / self.metrics.fruits_collected_this_session
    
    def _quantize_position(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Quantize une position pour regrouper les zones proches"""
        grid_size = 40  # Même que votre grille de jeu
        return (pos[0] // grid_size * grid_size, pos[1] // grid_size * grid_size)
    
    def _get_current_metrics(self, game_state: GameState) -> Dict:
        """Retourne les métriques actuelles sous forme de dict"""
        session_duration = game_state.timer - self.current_session_start
        return {
            "tick_count": self.tick_count,
            "death_count": self.metrics.death_count,
            "fruit_order": self.metrics.fruit_order,
            "time_between_deaths": self.metrics.time_between_deaths,
            "average_fruit_time": self.metrics.average_fruit_time,
            "current_route_length": len(self.current_route),
            "total_routes_recorded": len(self.metrics.player_routes),
            "high_risk_zones": len(self.metrics.risk_zones),
            "ice_block_usage": self.metrics.ice_block_usage,
            "fruits_collected_this_session": self.metrics.fruits_collected_this_session,
            "session_duration": session_duration,
            "total_fruits_collected": len(self.metrics.fruit_order),
            "player_position": game_state.player_pos,
            "player_has_block": getattr(game_state, 'player_has_block', False),
            "active_trolls": len(game_state.trolls_pos),
            "remaining_fruits": len(game_state.fruits_pos),
            "score": game_state.score
        }
    
    def export_metrics(self, filename: str = None, output_dir: str = "data/logs") -> str:
        """
        Exporte les métriques en JSON
        
        Returns:
            Chemin du fichier généré
        """
        if filename is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"metrics_{timestamp}.json"
        
        output_path = Path(output_dir) / filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Créer les métriques
        if hasattr(self, 'last_game_state'):
            current_metrics = self._get_current_metrics(self.last_game_state)
        else:
            # Valeurs par défaut
            current_metrics = self._get_current_metrics(GameState(
                player_pos=(0, 0), player_alive=True,
                trolls_pos=[], iceblocks_pos=[], fruits_pos=[],
                fruits_collected=[], level=1, round=1, timer=0.0, score=0
            ))
        
        metrics_data = {
            "metadata": {
                "export_time": time.time(),
                "tick_count": self.tick_count,
                "version": "1.0",
                "analyzer": "PerformanceAnalyzer"
            },
            "metrics": current_metrics
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(metrics_data, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Métriques exportées: {output_path}")
        return str(output_path)
    
    def get_performance_score(self) -> float:
        """Calcule un score de performance global (0-100)"""
        if self.tick_count == 0:
            return 50.0
        
        score = 100.0
        
        # Pénalités pour les morts
        score -= self.metrics.death_count * 10
        
        # Bonus pour l'efficacité de collecte
        if self.metrics.average_fruit_time > 0 and self.metrics.average_fruit_time < 60:
            score += 20
        elif self.metrics.average_fruit_time < 120:
            score += 10
        
        # Bonus pour l'usage des blocs de glace
        score += min(self.metrics.ice_block_usage * 2, 20)
        
        return max(0.0, min(100.0, score))
    
    def get_recommendations(self) -> List[Dict]:
        """Génère des recommandations basées sur les métriques"""
        recommendations = []
        
        if self.metrics.death_count > 0:
            recommendations.append({
                "type": "warning",
                "message": "Vous mourez trop souvent. Essayez d'éviter les ennemis.",
                "priority": "high"
            })
        
        if self.metrics.ice_block_usage < 2:
            recommendations.append({
                "type": "suggestion",
                "message": "Utilisez les blocs de glace pour bloquer les ennemis!",
                "priority": "medium"
            })
        
        return recommendations
    
    def reset(self):
        """Réinitialise l'analyseur pour une nouvelle session"""
        self.__init__()

# Démonstration
if __name__ == "__main__":
    # Créer un snapshot de test
    GameAPI.create_test_snapshot()
    
    # Charger l'état
    game_state = GameAPI.load_snapshot("data/snapshots/test_snapshot.json")
    
    # Analyser
    analyzer = PerformanceAnalyzer()
    metrics = analyzer.analyze_snapshot(game_state)
    
    print("📈 Métriques initiales:", json.dumps(metrics, indent=2))
    
    # Simuler une collecte de fruit
    game_state.fruits_pos = game_state.fruits_pos[1:]  # Enlever un fruit
    metrics = analyzer.analyze_snapshot(game_state)
    
    print("\n📈 Après collecte:", json.dumps(metrics, indent=2))
    
    # Exporter
    analyzer.export_metrics()