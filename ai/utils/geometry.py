"""
Utilitaires géométriques pour le système d'IA
Fonctions réutilisables pour les calculs de position, distance, collision, etc.
"""
import math
from typing import Tuple, List, Optional, Union
from dataclasses import dataclass

@dataclass
class Point:
    """Point 2D"""
    x: float
    y: float
    
    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)
    
    def distance_to(self, other: 'Point') -> float:
        """Distance euclidienne entre deux points"""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def manhattan_distance(self, other: 'Point') -> float:
        """Distance de Manhattan (somme des différences absolues)"""
        return abs(self.x - other.x) + abs(self.y - other.y)

@dataclass
class Rectangle:
    """Rectangle axis-aligned"""
    x: float
    y: float
    width: float
    height: float
    
    @property
    def left(self) -> float:
        return self.x
    
    @property
    def right(self) -> float:
        return self.x + self.width
    
    @property
    def top(self) -> float:
        return self.y
    
    @property
    def bottom(self) -> float:
        return self.y + self.height
    
    @property
    def center(self) -> Point:
        return Point(self.x + self.width / 2, self.y + self.height / 2)
    
    def contains_point(self, point: Union[Point, Tuple[float, float]]) -> bool:
        """Vérifie si le rectangle contient un point"""
        if isinstance(point, tuple):
            x, y = point
        else:
            x, y = point.x, point.y
            
        return (self.left <= x <= self.right and 
                self.top <= y <= self.bottom)
    
    def intersects(self, other: 'Rectangle') -> bool:
        """Vérifie si deux rectangles s'intersectent"""
        return not (self.right < other.left or 
                   self.left > other.right or 
                   self.bottom < other.top or 
                   self.top > other.bottom)

@dataclass
class Circle:
    """Cercle"""
    center: Point
    radius: float
    
    def contains_point(self, point: Union[Point, Tuple[float, float]]) -> bool:
        """Vérifie si le cercle contient un point"""
        if isinstance(point, tuple):
            point_obj = Point(*point)
        else:
            point_obj = point
        
        return self.center.distance_to(point_obj) <= self.radius
    
    def intersects_circle(self, other: 'Circle') -> bool:
        """Vérifie si deux cercles s'intersectent"""
        return self.center.distance_to(other.center) <= (self.radius + other.radius)

# Fonctions utilitaires
def distance_between(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Distance euclidienne entre deux tuples (x, y)"""
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def manhattan_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Distance de Manhattan entre deux points"""
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

def chebyshev_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Distance de Chebyshev (pour les déplacements en diagonale)"""
    return max(abs(p2[0] - p1[0]), abs(p2[1] - p1[1]))

def angle_between_points(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """Calcule l'angle (en radians) entre deux points"""
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.atan2(dy, dx)

def normalize_angle(angle: float) -> float:
    """Normalise un angle entre -π et π"""
    while angle > math.pi:
        angle -= 2 * math.pi
    while angle < -math.pi:
        angle += 2 * math.pi
    return angle

def point_in_polygon(point: Tuple[float, float], polygon: List[Tuple[float, float]]) -> bool:
    """
    Test du point dans un polygone (algorithme ray casting)
    
    Args:
        point: Point à tester (x, y)
        polygon: Liste de points définissant le polygone
    
    Returns:
        True si le point est à l'intérieur du polygone
    """
    if len(polygon) < 3:
        return False
    
    x, y = point
    inside = False
    
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]
        
        # Vérifier si le point est sur un sommet
        if (x, y) == (x1, y1) or (x, y) == (x2, y2):
            return True
        
        # Vérifier si le rayon horizontal traverse l'arête
        if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1) + x1):
            inside = not inside
    
    return inside

def line_intersection(line1: Tuple[Tuple[float, float], Tuple[float, float]],
                     line2: Tuple[Tuple[float, float], Tuple[float, float]]) -> Optional[Tuple[float, float]]:
    """
    Trouve le point d'intersection de deux segments de ligne
    
    Args:
        line1: ((x1, y1), (x2, y2))
        line2: ((x3, y3), (x4, y4))
    
    Returns:
        Point d'intersection ou None si pas d'intersection
    """
    (x1, y1), (x2, y2) = line1
    (x3, y3), (x4, y4) = line2
    
    # Calcul des dénominateurs
    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    
    if denom == 0:  # Lignes parallèles
        return None
    
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denom
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denom
    
    # Vérifier si l'intersection est dans les segments
    if 0 <= ua <= 1 and 0 <= ub <= 1:
        x = x1 + ua * (x2 - x1)
        y = y1 + ua * (y2 - y1)
        return (x, y)
    
    return None

def closest_point_on_segment(point: Tuple[float, float], 
                           segment: Tuple[Tuple[float, float], Tuple[float, float]]) -> Tuple[float, float]:
    """
    Trouve le point le plus proche sur un segment de ligne
    
    Args:
        point: Point de référence
        segment: ((x1, y1), (x2, y2))
    
    Returns:
        Point le plus proche sur le segment
    """
    x, y = point
    (x1, y1), (x2, y2) = segment
    
    # Vecteur du segment
    dx = x2 - x1
    dy = y2 - y1
    
    # Vecteur du point au début du segment
    vx = x - x1
    vy = y - y1
    
    # Produit scalaire
    dot = vx * dx + vy * dy
    length_squared = dx * dx + dy * dy
    
    if length_squared == 0:
        return (x1, y1)
    
    # Paramètre t
    t = dot / length_squared
    
    # Limiter au segment
    t = max(0, min(1, t))
    
    return (x1 + t * dx, y1 + t * dy)

def grid_to_world(grid_pos: Tuple[int, int], cell_size: int = 40) -> Tuple[float, float]:
    """Convertit une position de grille en coordonnées monde"""
    return (grid_pos[0] * cell_size + cell_size / 2, 
            grid_pos[1] * cell_size + cell_size / 2)

def world_to_grid(world_pos: Tuple[float, float], cell_size: int = 40) -> Tuple[int, int]:
    """Convertit des coordonnées monde en position de grille"""
    return (int(world_pos[0] // cell_size), int(world_pos[1] // cell_size))

def get_direction_vector(direction: str) -> Tuple[float, float]:
    """Retourne le vecteur direction à partir d'une direction textuelle"""
    direction_map = {
        'up': (0, -1),
        'down': (0, 1),
        'left': (-1, 0),
        'right': (1, 0),
        'up_left': (-0.707, -0.707),  # √2/2
        'up_right': (0.707, -0.707),
        'down_left': (-0.707, 0.707),
        'down_right': (0.707, 0.707)
    }
    return direction_map.get(direction.lower(), (0, 0))

def calculate_bounding_box(points: List[Tuple[float, float]]) -> Tuple[float, float, float, float]:
    """
    Calcule la boîte englobante d'un ensemble de points
    
    Returns:
        (x_min, y_min, x_max, y_max)
    """
    if not points:
        return (0, 0, 0, 0)
    
    x_min = min(p[0] for p in points)
    x_max = max(p[0] for p in points)
    y_min = min(p[1] for p in points)
    y_max = max(p[1] for p in points)
    
    return (x_min, y_min, x_max, y_max)

def point_in_rect(point: Tuple[float, float], rect: Tuple[float, float, float, float]) -> bool:
    """Vérifie si un point est dans un rectangle"""
    x, y = point
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh

def rectangles_overlap(rect1: Tuple[float, float, float, float], 
                      rect2: Tuple[float, float, float, float]) -> bool:
    """Vérifie si deux rectangles se chevauchent"""
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2
    
    return not (x1 + w1 < x2 or x2 + w2 < x1 or y1 + h1 < y2 or y2 + h2 < y1)

def lerp(start: float, end: float, t: float) -> float:
    """Interpolation linéaire entre deux valeurs"""
    return start + (end - start) * t

def lerp_point(p1: Tuple[float, float], p2: Tuple[float, float], t: float) -> Tuple[float, float]:
    """Interpolation linéaire entre deux points"""
    return (lerp(p1[0], p2[0], t), lerp(p1[1], p2[1], t))

def smooth_step(t: float) -> float:
    """Fonction de lissage sigmoïde"""
    return t * t * (3 - 2 * t)

def calculate_centroid(polygon: List[Tuple[float, float]]) -> Tuple[float, float]:
    """Calcule le centroïde d'un polygone"""
    if not polygon:
        return (0, 0)
    
    x_sum = sum(p[0] for p in polygon)
    y_sum = sum(p[1] for p in polygon)
    
    return (x_sum / len(polygon), y_sum / len(polygon))

def is_point_visible(viewer_pos: Tuple[float, float], target_pos: Tuple[float, float],
                    obstacles: List[Tuple[Tuple[float, float], Tuple[float, float]]]) -> bool:
    """
    Vérifie si le point cible est visible depuis le point de vue
    
    Args:
        viewer_pos: Position de l'observateur
        target_pos: Position de la cible
        obstacles: Liste de segments de ligne représentant les obstacles
    
    Returns:
        True si la cible est visible
    """
    # Créer un segment de ligne entre l'observateur et la cible
    line_of_sight = (viewer_pos, target_pos)
    
    # Vérifier chaque obstacle
    for obstacle in obstacles:
        if line_intersection(line_of_sight, obstacle):
            return False
    
    return True

# Tests unitaires intégrés
if __name__ == "__main__":
    print("🧪 Tests des fonctions géométriques...")
    
    # Test distance
    assert distance_between((0, 0), (3, 4)) == 5.0
    print("✅ Distance euclidienne")
    
    # Test manhattan distance
    assert manhattan_distance((0, 0), (3, 4)) == 7
    print("✅ Distance de Manhattan")
    
    # Test point in rect
    assert point_in_rect((5, 5), (0, 0, 10, 10)) == True
    assert point_in_rect((15, 5), (0, 0, 10, 10)) == False
    print("✅ Point dans rectangle")
    
    # Test rectangles overlap
    assert rectangles_overlap((0, 0, 10, 10), (5, 5, 10, 10)) == True
    assert rectangles_overlap((0, 0, 10, 10), (20, 20, 10, 10)) == False
    print("✅ Chevauchement de rectangles")
    
    # Test line intersection
    intersection = line_intersection(((0, 0), (10, 10)), ((0, 10), (10, 0)))
    assert intersection == (5.0, 5.0)
    print("✅ Intersection de lignes")
    
    # Test closest point on segment
    closest = closest_point_on_segment((5, 5), ((0, 0), (10, 0)))
    assert closest == (5.0, 0.0)
    print("✅ Point le plus proche sur segment")
    
    print("🎉 Tous les tests passent!")