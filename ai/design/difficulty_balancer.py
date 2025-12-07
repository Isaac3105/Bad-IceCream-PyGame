"""
Système d'équilibrage automatique de la difficulté
"""
import random
import math
from typing import Dict, List, Tuple
from dataclasses import dataclass
from enum import Enum
from ai.utils.geometry import calculate_bounding_box, point_in_polygon
@dataclass
class DifficultyMetrics:
    """Métriques pour évaluer la difficulté d'un niveau"""
    enemy_density: float  # Nombre d'ennemis par surface
    obstacle_density: float  # Densité d'obstacles
    path_complexity: float  # Complexité des chemins
    resource_availability: float  # Disponibilité des fruits
    navigation_difficulty: float  # Difficulté de navigation
    
    @property
    def overall_difficulty(self) -> float:
        """Calcule la difficulté globale (0.0 à 1.0)"""
        weights = {
            'enemy_density': 0.35,
            'obstacle_density': 0.25,
            'path_complexity': 0.20,
            'navigation_difficulty': 0.15,
            'resource_availability': 0.05  # Inverse (moins de ressources = plus difficile)
        }
        
        score = (
            self.enemy_density * weights['enemy_density'] +
            self.obstacle_density * weights['obstacle_density'] +
            self.path_complexity * weights['path_complexity'] +
            self.navigation_difficulty * weights['navigation_difficulty'] +
            (1 - self.resource_availability) * weights['resource_availability']
        )
        
        return min(max(score, 0.0), 1.0)

class DifficultyBalancer:
    """Ajuste automatiquement la difficulté des niveaux"""
    
    def __init__(self, target_difficulty: float = 0.5):
        self.target_difficulty = target_difficulty
        self.player_history: List[Dict] = []
        self.max_history_size = 100
    
    def analyze_level(self, level_data: Dict, area_size: Tuple[int, int]) -> DifficultyMetrics:
        """Analyse la difficulté d'un niveau généré"""
        width, height = area_size
        total_area = width * height
        
        # Compter les éléments
        num_enemies = len(level_data.get('trolls', []))
        num_obstacles = len(level_data.get('iceblocks', []))
        num_resources = len(level_data.get('fruits', []))
        
        # Calculer les densités
        enemy_density = num_enemies / (total_area / 10000)  # Normalisé
        obstacle_density = num_obstacles / (total_area / 1000)  # Normalisé
        resource_availability = min(num_resources / 10.0, 1.0)  # 10 fruits = 1.0
        
        # Estimer la complexité des chemins (simplifié)
        num_rooms = len(level_data.get('rooms', []))
        num_corridors = len(level_data.get('corridors', []))
        path_complexity = min((num_rooms + num_corridors) / 20.0, 1.0)
        
        # Difficulté de navigation (basée sur la disposition)
        navigation_difficulty = self._estimate_navigation_difficulty(level_data)
        
        return DifficultyMetrics(
            enemy_density=enemy_density,
            obstacle_density=obstacle_density,
            path_complexity=path_complexity,
            resource_availability=resource_availability,
            navigation_difficulty=navigation_difficulty
        )
    
    def _estimate_navigation_difficulty(self, level_data: Dict) -> float:
        """Estime la difficulté de navigation dans le niveau"""
        # Simplifié: plus d'obstacles = plus difficile à naviguer
        iceblocks = level_data.get('iceblocks', [])
        if len(iceblocks) == 0:
            return 0.1
        
        # Estimer combien l'espace est bloqué
        blocked_ratio = min(len(iceblocks) / 50.0, 1.0)  # 50 blocs = maximum
        
        # Ajuster selon la disposition
        if self._has_choke_points(iceblocks):
            blocked_ratio *= 1.3  # 30% plus difficile s'il y a des goulots d'étranglement
        
        return min(blocked_ratio, 1.0)
    
    def _has_choke_points(self, iceblocks: List[Tuple[int, int]]) -> bool:
        """Détecte si le niveau a des goulots d'étranglement"""
        # Simplifié: vérifier si des blocs forment des lignes continues
        # qui pourraient bloquer des passages
        if len(iceblocks) < 10:
            return False
        
        # Regrouper par coordonnées similaires
        x_groups = {}
        y_groups = {}
        
        for x, y in iceblocks:
            x_groups.setdefault(x, []).append(y)
            y_groups.setdefault(y, []).append(x)
        
        # Vérifier les lignes continues
        for x, ys in x_groups.items():
            if len(ys) >= 5:  # Ligne verticale d'au moins 5 blocs
                ys_sorted = sorted(ys)
                for i in range(len(ys_sorted) - 4):
                    if all(ys_sorted[i + j] + 58 == ys_sorted[i + j + 1] 
                          for j in range(4)):
                        return True
        
        for y, xs in y_groups.items():
            if len(xs) >= 5:  # Ligne horizontale d'au moins 5 blocs
                xs_sorted = sorted(xs)
                for i in range(len(xs_sorted) - 4):
                    if all(xs_sorted[i + j] + 40 == xs_sorted[i + j + 1] 
                          for j in range(4)):
                        return True
        
        return False
    
    def adjust_difficulty(self, level_data: Dict, player_skill: float = 0.5) -> Dict:
        """
        Ajuste la difficulté d'un niveau selon l'habileté du joueur
        
        Args:
            level_data: Données du niveau à ajuster
            player_skill: Habileté du joueur (0.0 à 1.0)
            
        Returns:
            Niveau ajusté
        """
        adjusted_data = level_data.copy()
        
        # Facteur d'ajustement basé sur l'habileté
        # Si player_skill = 1.0 (expert), on augmente la difficulté de 50%
        # Si player_skill = 0.0 (débutant), on réduit la difficulté de 50%
        difficulty_factor = 0.5 + player_skill  # 0.5 à 1.5
        
        # Ajuster le nombre d'ennemis
        trolls = adjusted_data.get('trolls', [])
        if trolls:
            target_count = max(1, int(len(trolls) * difficulty_factor))
            if target_count != len(trolls):
                if target_count > len(trolls):
                    # Ajouter des ennemis
                    self._add_enemies(adjusted_data, target_count - len(trolls))
                else:
                    # Retirer des ennemis
                    adjusted_data['trolls'] = trolls[:target_count]
        
        # Ajuster le nombre d'obstacles
        iceblocks = adjusted_data.get('iceblocks', [])
        if iceblocks:
            target_blocks = max(5, int(len(iceblocks) * difficulty_factor))
            if target_blocks != len(iceblocks):
                if target_blocks > len(iceblocks):
                    # Ajouter des blocs
                    self._add_iceblocks(adjusted_data, target_blocks - len(iceblocks))
                else:
                    # Retirer des blocs
                    adjusted_data['iceblocks'] = random.sample(iceblocks, target_blocks)
        
        # Ajuster les ressources (fruits)
        fruits = adjusted_data.get('fruits', [])
        if fruits:
            # Plus de compétence = moins de ressources (plus difficile)
            resource_factor = 1.5 - player_skill  # 1.5 à 0.5
            target_fruits = max(3, int(len(fruits) * resource_factor))
            if target_fruits != len(fruits):
                adjusted_data['fruits'] = fruits[:target_fruits]
        
        return adjusted_data
    
    def _add_enemies(self, level_data: Dict, count: int):
        """Ajoute des ennemis au niveau"""
        if 'trolls' not in level_data:
            level_data['trolls'] = []
        
        # Positions existantes pour éviter les doublons
        existing_positions = {tuple(troll['pos']) for troll in level_data['trolls']}
        
        # Chercher des positions libres
        free_positions = self._find_free_positions(level_data, count, existing_positions)
        
        for pos in free_positions:
            level_data['trolls'].append({
                'pos': pos,
                'role': 'hunter' if random.random() > 0.5 else 'patroller'
            })
    
    def _add_iceblocks(self, level_data: Dict, count: int):
        """Ajoute des blocs de glace au niveau"""
        if 'iceblocks' not in level_data:
            level_data['iceblocks'] = []
        
        existing_positions = set(level_data['iceblocks'])
        free_positions = self._find_free_positions(level_data, count, existing_positions)
        
        level_data['iceblocks'].extend(free_positions)
    
    def _find_free_positions(self, level_data: Dict, count: int, 
                           existing: set) -> List[Tuple[int, int]]:
        """Trouve des positions libres dans le niveau"""
        positions = []
        attempts = 0
        max_attempts = count * 10
        
        while len(positions) < count and attempts < max_attempts:
            attempts += 1
            x = random.randint(50, 770)  # Dans les limites du jeu
            y = random.randint(50, 572)
            pos = (x, y)
            
            # Éviter les positions existantes
            if pos not in existing and pos not in positions:
                # Éviter de bloquer le joueur au départ
                player_start = level_data.get('player_start', (400, 300))
                if math.dist(pos, player_start) > 100:  # Au moins 100 pixels du départ
                    positions.append(pos)
        
        return positions
    
    def record_player_performance(self, level_data: Dict, 
                                performance: Dict, player_id: str = "default"):
        """
        Enregistre la performance d'un joueur pour ajuster la difficulté future
        
        Args:
            level_data: Données du niveau joué
            performance: Métriques de performance (temps, morts, score, etc.)
            player_id: Identifiant du joueur
        """
        record = {
            'player_id': player_id,
            'level_difficulty': self.analyze_level(level_data, (820, 622)).overall_difficulty,
            'performance': performance,
            'timestamp': self._get_current_timestamp()
        }
        
        self.player_history.append(record)
        
        # Garder l'historique limité
        if len(self.player_history) > self.max_history_size:
            self.player_history.pop(0)
    
    def get_player_skill_level(self, player_id: str = "default") -> float:
        """Estime le niveau de compétence d'un joueur basé sur l'historique"""
        player_records = [r for r in self.player_history if r['player_id'] == player_id]
        
        if not player_records:
            return 0.5  # Valeur par défaut
        
        # Analyser les performances
        success_rate = self._calculate_success_rate(player_records)
        avg_score = self._calculate_average_score(player_records)
        avg_time = self._calculate_average_time(player_records)
        
        # Combiner les métriques (poids arbitraires)
        skill_score = (
            success_rate * 0.4 +
            (avg_score / 1000) * 0.3 +  # Normaliser le score
            (1 - min(avg_time / 300, 1)) * 0.3  # Moins de temps = meilleur
        )
        
        return min(max(skill_score, 0.1), 0.9)  # Limiter entre 0.1 et 0.9
    
    def _calculate_success_rate(self, records: List[Dict]) -> float:
        """Calcule le taux de réussite (niveaux complétés)"""
        completions = sum(1 for r in records if r['performance'].get('completed', False))
        return completions / len(records) if records else 0.0
    
    def _calculate_average_score(self, records: List[Dict]) -> float:
        """Calcule le score moyen"""
        scores = [r['performance'].get('score', 0) for r in records]
        return sum(scores) / len(scores) if scores else 0.0
    
    def _calculate_average_time(self, records: List[Dict]) -> float:
        """Calcule le temps moyen de complétion"""
        times = [r['performance'].get('completion_time', 300) for r in records]
        return sum(times) / len(times) if times else 300.0
    
    def _get_current_timestamp(self) -> str:
        """Retourne un timestamp (simplifié)"""
        import time
        return time.strftime("%Y-%m-%d %H:%M:%S")

# Singleton pour le balancer global
_global_balancer = None

def get_difficulty_balancer() -> DifficultyBalancer:
    """Retourne l'instance globale du balancer de difficulté"""
    global _global_balancer
    if _global_balancer is None:
        _global_balancer = DifficultyBalancer()
    return _global_balancer