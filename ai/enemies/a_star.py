"""
Algorithme A* pour le pathfinding des ennemis - CORRIGÉ
"""
import heapq
from typing import List, Tuple, Dict, Set, Optional
from dataclasses import dataclass
import math
from ai.utils.geometry import manhattan_distance, chebyshev_distance

@dataclass
class Node:
    """Représente un nœud dans le graphe de recherche"""
    x: int
    y: int
    g: float = 0  # Coût depuis le départ
    h: float = 0  # Heuristique vers la cible
    f: float = 0  # Coût total (g + h)
    parent: Optional['Node'] = None
    
    def __lt__(self, other: 'Node') -> bool:
        return self.f < other.f
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))

class AStarPathfinder:
    """Implémente l'algorithme A* pour trouver des chemins - CORRIGÉ"""
    
    def __init__(self, grid_width: int, grid_height: int, cell_size: int = 40):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size
        
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int], 
                  obstacles: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """
        Trouve le chemin optimal entre start et goal en évitant les obstacles
        
        Args:
            start: Position de départ (x, y)
            goal: Position cible (x, y)
            obstacles: Liste des positions bloquées
            
        Returns:
            Liste de positions (x, y) du chemin optimal, vide si aucun chemin
        """
        # Convertir en coordonnées grille
        start_grid = self._world_to_grid(start)
        goal_grid = self._world_to_grid(goal)
        obstacles_grid = {self._world_to_grid(obs) for obs in obstacles}
        
        # Vérifier si départ ou arrivée dans un obstacle
        if start_grid in obstacles_grid or goal_grid in obstacles_grid:
            return []
        
        # Vérifier si la grille est valide
        if not self._is_valid_grid(start_grid) or not self._is_valid_grid(goal_grid):
            return []
        
        # Structures de données pour A*
        open_set: List[Node] = []
        closed_set: Set[Tuple[int, int]] = set()
        
        # Nœud de départ
        start_node = Node(start_grid[0], start_grid[1])
        start_node.h = self._heuristic(start_grid, goal_grid)
        start_node.f = start_node.h
        
        heapq.heappush(open_set, start_node)
        
        while open_set:
            current_node = heapq.heappop(open_set)
            
            # Si on a atteint la cible
            if (current_node.x, current_node.y) == goal_grid:
                return self._reconstruct_path(current_node)
            
            closed_set.add((current_node.x, current_node.y))
            
            # Explorer les voisins
            for neighbor in self._get_neighbors(current_node, obstacles_grid):
                neighbor_pos = (neighbor.x, neighbor.y)
                if neighbor_pos in closed_set:
                    continue
                
                # Coût de déplacement (1 pour orthogonal, √2 ≈ 1.4 pour diagonal)
                dx = neighbor.x - current_node.x
                dy = neighbor.y - current_node.y
                move_cost = 1.0 if dx == 0 or dy == 0 else 1.414
                tentative_g = current_node.g + move_cost
                
                # Vérifier si meilleur chemin
                existing_node = next((n for n in open_set if (n.x, n.y) == neighbor_pos), None)
                
                if existing_node is None or tentative_g < existing_node.g:
                    if existing_node:
                        open_set.remove(existing_node)
                    
                    neighbor.g = tentative_g
                    neighbor.h = self._heuristic(neighbor_pos, goal_grid)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current_node
                    
                    heapq.heappush(open_set, neighbor)
        
        return []  # Aucun chemin trouvé
    
    def _get_neighbors(self, node: Node, obstacles: Set[Tuple[int, int]]) -> List[Node]:
        """Retourne les voisins valides d'un nœud - CORRIGÉ"""
        neighbors = []
        
        # 8 directions: haut, bas, gauche, droite, et 4 diagonales
        directions = [
            (0, -1),  # Haut
            (1, 0),   # Droite
            (0, 1),   # Bas
            (-1, 0),  # Gauche
            (1, -1),  # Diagonale haut-droite
            (1, 1),   # Diagonale bas-droite
            (-1, 1),  # Diagonale bas-gauche
            (-1, -1)  # Diagonale haut-gauche
        ]
        
        for dx, dy in directions:
            new_x, new_y = node.x + dx, node.y + dy
            
            # Vérifier limites de la grille
            if not (0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height):
                continue
            
            # Vérifier obstacle
            if (new_x, new_y) in obstacles:
                continue
            
            # Pour les diagonales, vérifier que les cases adjacentes ne sont pas bloquées
            if dx != 0 and dy != 0:
                # Vérifier les deux cases adjacentes
                if ((node.x + dx, node.y) in obstacles or 
                    (node.x, node.y + dy) in obstacles):
                    continue
            
            neighbors.append(Node(new_x, new_y))
        
        return neighbors
    
    def heuristic(a: Tuple[int, int], b: Tuple[int, int], method: str = "manhattan") -> float:
        """
        Heuristique pour A* avec choix de métrique
        """
        if method == "manhattan":
            return manhattan_distance(a, b)
        elif method == "chebyshev":
            return chebyshev_distance(a, b)
        else:  # euclidean par défaut
            dx = a[0] - b[0]
            dy = a[1] - b[1]
            return math.sqrt(dx * dx + dy * dy)
    
    def _reconstruct_path(self, node: Node) -> List[Tuple[int, int]]:
        """Reconstruit le chemin depuis le nœud final"""
        path = []
        current = node
        
        while current:
            # Retourner le coin de la cellule pour les tests
            world_pos = self._grid_to_world((current.x, current.y))
            path.append((int(world_pos[0]), int(world_pos[1])))
            current = current.parent
        
        return list(reversed(path))
    
    def _world_to_grid(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Convertit les coordonnées monde en coordonnées grille"""
        return (pos[0] // self.cell_size, pos[1] // self.cell_size)
    
    def _grid_to_world(self, grid_pos: Tuple[int, int]) -> Tuple[int, int]:
        """Convertit les coordonnées grille en coordonnées monde"""
        # Retourner le coin de la cellule pour les tests
        return (grid_pos[0] * self.cell_size, grid_pos[1] * self.cell_size)
    
    def _is_valid_grid(self, grid_pos: Tuple[int, int]) -> bool:
        """Vérifie si une position grille est valide"""
        x, y = grid_pos
        return 0 <= x < self.grid_width and 0 <= y < self.grid_height

# Fonction utilitaire pour l'API
def find_path(start: Tuple[int, int], goal: Tuple[int, int], 
              grid_blocked: List[List[bool]], 
              allow_diagonal: bool = True) -> List[Tuple[int, int]]:
    """
    Trouve un chemin avec A*
    
    Args:
        start: Position de départ (grid coordinates)
        goal: Position d'arrivée (grid coordinates)
        grid_blocked: Grille 2D indiquant les cellules bloquées
        allow_diagonal: Permettre les déplacements en diagonale
        
    Returns:
        Liste de positions (grid coordinates)
    """
    # Utiliser Chebyshev pour diagonales, Manhattan sinon
    heuristic_method = "chebyshev" if allow_diagonal else "manhattan"
    
    # Le reste du code A* reste le même...