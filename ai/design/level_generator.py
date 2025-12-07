"""
Générateur de niveaux basé sur BSP (Binary Space Partitioning)
"""
import random
import math
from typing import List, Tuple, Dict, Optional, Set
from dataclasses import dataclass
from enum import Enum
from ai.utils.geometry import distance_between, rectangles_overlap, calculate_centroid

@dataclass
class Room:
    """Représente une salle dans le niveau"""
    x: int
    y: int
    width: int
    height: int
    center: Tuple[int, int] = None
    
    def __post_init__(self):
        self.center = (self.x + self.width // 2, self.y + self.height // 2)
    
    def intersects(self, other: 'Room') -> bool:
        """Vérifie si deux salles se chevauchent"""
        return (self.x < other.x + other.width and
                self.x + self.width > other.x and
                self.y < other.y + other.height and
                self.y + self.height > other.y)

@dataclass
class Corridor:
    """Représente un couloir entre deux salles"""
    start: Tuple[int, int]
    end: Tuple[int, int]
    path: List[Tuple[int, int]] = None
    
    def __post_init__(self):
        if self.path is None:
            self.path = self._generate_path()
    
    def _generate_path(self) -> List[Tuple[int, int]]:
        """Génère un chemin L-shaped entre deux points"""
        path = []
        x1, y1 = self.start
        x2, y2 = self.end
        
        # Chemin horizontal d'abord, puis vertical
        if random.random() > 0.5:
            # Horizontal puis vertical
            mid_x = x2
            mid_y = y1
            path.extend(self._line(x1, y1, mid_x, mid_y))
            path.extend(self._line(mid_x, mid_y, x2, y2)[1:])  # Éviter le doublon
        else:
            # Vertical puis horizontal
            mid_x = x1
            mid_y = y2
            path.extend(self._line(x1, y1, mid_x, mid_y))
            path.extend(self._line(mid_x, mid_y, x2, y2)[1:])
        
        return path
    
    def _line(self, x1: int, y1: int, x2: int, y2: int) -> List[Tuple[int, int]]:
        """Algorithme de Bresenham pour les lignes"""
        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        while True:
            points.append((x1, y1))
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
        
        return points

class LevelTheme(Enum):
    """Thèmes visuels pour les niveaux"""
    FOREST = "forest"      # Beaucoup d'obstacles naturels
    ICE = "ice"           # Beaucoup de glace
    CAVE = "cave"         # Salles connectées par tunnels
    MAZE = "maze"         # Labyrinthe complexe
    OPEN = "open"         # Espaces ouverts

class LevelGenerator:
    """Générateur de niveaux procédural basé sur BSP"""
    
    def __init__(self, width: int = 820, height: int = 622, 
                 min_room_size: int = 60, max_room_size: int = 150):
        self.width = width
        self.height = height
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size
        
        # Paramètres de génération
        self.max_depth = 4
        self.room_padding = 5
        
        # Éléments générés
        self.rooms: List[Room] = []
        self.corridors: List[Corridor] = []
        self.walls: Set[Tuple[int, int]] = set()
        self.free_cells: Set[Tuple[int, int]] = set()
        
    def generate(self, theme: LevelTheme = LevelTheme.CAVE, 
                 difficulty: float = 0.5) -> Dict:
        """
        Génère un niveau complet
        
        Args:
            theme: Thème visuel du niveau
            difficulty: Niveau de difficulté (0.0 à 1.0)
            
        Returns:
            Dictionnaire contenant tous les éléments du niveau
        """
        print(f"🎮 Génération d'un niveau {theme.value} (difficulté: {difficulty:.1f})")
        
        # Réinitialiser
        self.rooms = []
        self.corridors = []
        self.walls = set()
        self.free_cells = set()
        
        # Étape 1: Générer l'arbre BSP
        root_rect = (50, 50, self.width - 100, self.height - 100)  # Marge pour les bords
        bsp_tree = self._generate_bsp(root_rect, depth=0)
        
        # Étape 2: Créer des salles dans les feuilles de l'arbre BSP
        self._create_rooms_in_leaves(bsp_tree)
        
        # Étape 3: Connecter les salles avec des couloirs
        self._connect_rooms()
        
        # Étape 4: Générer les murs
        self._generate_walls()
        
        # Étape 5: Placer les éléments selon le thème et la difficulté
        elements = self._place_elements(theme, difficulty)
        
        print(f"✅ Niveau généré: {len(self.rooms)} salles, {len(self.corridors)} couloirs")
        return elements
    
    def _generate_bsp(self, rect: Tuple[int, int, int, int], depth: int = 0) -> Dict:
        """
        Génère récursivement un arbre BSP
        """
        x, y, width, height = rect
        
        # Condition d'arrêt
        if (depth >= self.max_depth or 
            width < self.min_room_size * 2 or 
            height < self.min_room_size * 2):
            return {
                'rect': rect,
                'left': None,
                'right': None,
                'room': None,
                'is_leaf': True
            }
        
        # Décider de la direction de coupe
        if width > height * 1.25:  # Couper verticalement
            split = random.randint(int(width * 0.4), int(width * 0.6))
            left_rect = (x, y, split, height)
            right_rect = (x + split, y, width - split, height)
        else:  # Couper horizontalement
            split = random.randint(int(height * 0.4), int(height * 0.6))
            left_rect = (x, y, width, split)
            right_rect = (x, y + split, width, height - split)
        
        # Récursion
        return {
            'rect': rect,
            'left': self._generate_bsp(left_rect, depth + 1),
            'right': self._generate_bsp(right_rect, depth + 1),
            'room': None,
            'is_leaf': False
        }
    
    def _create_rooms_in_leaves(self, node: Dict):
        """Crée des salles dans les feuilles de l'arbre BSP"""
        if node['is_leaf']:
            x, y, width, height = node['rect']
    
        # Créer une salle plus petite que la cellule
            room_width = random.randint(self.min_room_size, min(width - self.room_padding * 2, self.max_room_size))
            room_height = random.randint(self.min_room_size, min(height - self.room_padding * 2, self.max_room_size))
            room_x = x + random.randint(self.room_padding, width - room_width - self.room_padding)
            room_y = y + random.randint(self.room_padding, height - room_height - self.room_padding)
    
        # Vérifier les chevauchements avec les salles existantes  <-- ERREUR ICI
            new_room_rect = (room_x, room_y, room_width, room_height)
            overlapping = False
        
            for  existing_room in self.rooms:
                existing_rect = (existing_room.x, existing_room.y, 
                               existing_room.width, existing_room.height)
                if rectangles_overlap(new_room_rect, existing_rect):
                    overlapping = True
                    break
        
            if not overlapping:
                room = Room(room_x, room_y, room_width, room_height)
                node['room'] = room
                self.rooms.append(room)
            
            # Ajouter les cellules libres
                for rx in range(room.x, room.x + room.width):
                    for ry in range(room.y, room.y + room.height):
                        self.free_cells.add((rx, ry))
        else:
            if node['left']:
                self._create_rooms_in_leaves(node['left'])
            if node['right']:
                self._create_rooms_in_leaves(node['right'])

    def _connect_rooms(self):
        """Connecte les salles avec des couloirs"""
        # Récupérer toutes les salles de l'arbre
        all_rooms = self._get_all_rooms(self._generate_bsp((50, 50, self.width - 100, self.height - 100)))
        
        # Connecter les salles voisines dans l'arbre
        self._connect_tree(all_rooms)
        
        # Ajouter quelques connections supplémentaires aléatoires
        self._add_random_connections()
    
    def _get_all_rooms(self, node: Dict) -> List[Room]:
        """Récupère toutes les salles de l'arbre"""
        rooms = []
        if node['room']:
            rooms.append(node['room'])
        if node['left']:
            rooms.extend(self._get_all_rooms(node['left']))
        if node['right']:
            rooms.extend(self._get_all_rooms(node['right']))
        return rooms
    
    def _connect_tree(self, rooms: List[Room]):
        """Connecte les salles suivant la structure de l'arbre"""
        for i in range(len(rooms) - 1):
            for j in range(i + 1, len(rooms)):
                # Connecter seulement si les salles sont proches
                dist = self._distance(rooms[i].center, rooms[j].center)
                if dist < 300:  # Seuil de proximité
                    corridor = Corridor(rooms[i].center, rooms[j].center)
                    self.corridors.append(corridor)
                    
                    # Ajouter les cellules des couloirs
                    for point in corridor.path:
                        self.free_cells.add(point)
    
    def _add_random_connections(self):
        """Ajoute des connections aléatoires pour éviter les impasses"""
        if len(self.rooms) < 3:
            return
        
        num_extra = random.randint(1, len(self.rooms) // 2)
        for _ in range(num_extra):
            room1 = random.choice(self.rooms)
            room2 = random.choice([r for r in self.rooms if r != room1])
            
            # Vérifier qu'elles ne sont pas déjà connectées
            already_connected = False
            for corridor in self.corridors:
                if (corridor.start == room1.center and corridor.end == room2.center) or \
                   (corridor.start == room2.center and corridor.end == room1.center):
                    already_connected = True
                    break
            
            if not already_connected:
                corridor = Corridor(room1.center, room2.center)
                self.corridors.append(corridor)
                
                for point in corridor.path:
                    self.free_cells.add(point)
    
    def _generate_walls(self):
        """Génère les murs autour des salles et couloirs"""
        # Pour chaque cellule libre, vérifier ses voisins
        for x, y in self.free_cells:
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)
                if neighbor not in self.free_cells:
                    self.walls.add(neighbor)
    
    def _place_elements(self, theme: LevelTheme, difficulty: float) -> Dict:
        """Place les éléments (fruits, ennemis, blocs) selon le thème"""
        elements = {
            'trolls': [],
            'fruits': [],
            'iceblocks': [],
            'walls': list(self.walls),
            'player_start': None
        }
        
        # Déterminer les nombres selon la difficulté
        num_fruits = int(5 + difficulty * 10)  # 5 à 15 fruits
        num_trolls = int(2 + difficulty * 4)   # 2 à 6 trolls
        num_iceblocks = self._get_iceblock_count(theme, difficulty)
        
        # Choisir une salle de départ pour le joueur (la plus éloignée des autres)
        if self.rooms:
            elements['player_start'] = self._find_best_start_position()
        
        # Placer les fruits dans les salles
        fruit_positions = self._distribute_points_in_rooms(num_fruits, min_distance=80)
        elements['fruits'] = [{'pos': pos, 'type': self._random_fruit_type()} 
                             for pos in fruit_positions]
        
        # Placer les ennemis
        enemy_positions = self._distribute_points_in_rooms(num_trolls, min_distance=100)
        elements['trolls'] = [{'pos': pos, 'role': self._random_enemy_role(difficulty)} 
                             for pos in enemy_positions]
        
        # Placer les blocs de glace selon le thème
        if theme == LevelTheme.ICE:
            # Beaucoup de glace pour le thème glace
            ice_positions = self._place_ice_blocks_pattern(num_iceblocks)
        elif theme == LevelTheme.MAZE:
            # Murs de glace pour créer un labyrinthe
            ice_positions = self._place_maze_blocks(num_iceblocks)
        else:
            # Placement aléatoire
            ice_positions = self._place_random_blocks(num_iceblocks)
        
        elements['iceblocks'] = ice_positions
        
        return elements
    
    def _find_best_start_position(self) -> Tuple[int, int]:
        """Trouve la meilleure position de départ pour le joueur"""
        if not self.rooms:
            return (self.width // 2, self.height // 2)
        
        # Prendre le centre de la première salle
        return self.rooms[0].center
    
    def _distribute_points_in_rooms(self, count: int, min_distance: int = 50):
        """Distribue des points dans les salles en respectant une distance minimale"""
        points = []
        attempts = 0

    # Vérifier si self.rooms est vide
        if not self.rooms:
            print("⚠️ Avertissement: Aucune salle disponible, création d'une salle par défaut")
        # Créer une salle par défaut au centre
            default_room = Room(
                self.width // 2 - 100, 
                self.height // 2 - 75,
                200, 150
            )
            self.rooms = [default_room]
    
        while len(points) < count and attempts < count * 10:
            attempts += 1
            room = random.choice(self.rooms)
        
        # Point aléatoire dans la salle (avec marge)
            margin = 20
            x = random.randint(room.x + margin, room.x + room.width - margin)
            y = random.randint(room.y + margin, room.y + room.height - margin)
            point = (x, y)
        
        # Vérifier la distance avec les points existants
            too_close = False
            for existing in points:
                if distance_between(point, existing) < min_distance:
                    too_close = True
                    break
        
            if not too_close:
                points.append(point)
    
    # Si on n'a pas assez de points, ajouter des points aléatoires dans la carte
        if len(points) < count:
            print(f"⚠️ Impossible de placer {count} points avec la distance requise, placement aléatoire")
            for _ in range(count - len(points)):
                x = random.randint(50, self.width - 50)
                y = random.randint(50, self.height - 50)
                points.append((x, y))
    
        return points
    
    def _get_iceblock_count(self, theme: LevelTheme, difficulty: float) -> int:
        """Retourne le nombre de blocs de glace selon le thème"""
        base_count = int(10 + difficulty * 20)
        
        if theme == LevelTheme.ICE:
            return base_count * 2
        elif theme == LevelTheme.MAZE:
            return base_count * 3
        elif theme == LevelTheme.OPEN:
            return base_count // 2
        else:
            return base_count
    
    def _place_ice_blocks_pattern(self, count: int) -> List[Tuple[int, int]]:
        """Place des blocs de glace en motifs réguliers"""
        blocks = []
        
        for room in self.rooms:
            # Créer un motif en damier dans chaque salle
            cell_size = 40
            for x in range(room.x + cell_size, room.x + room.width - cell_size, cell_size * 2):
                for y in range(room.y + cell_size, room.y + room.height - cell_size, cell_size * 2):
                    if len(blocks) < count:
                        blocks.append((x, y))
        
        return blocks
    
    def _place_maze_blocks(self, count: int) -> List[Tuple[int, int]]:
        """Crée des murs de glace pour former un labyrinthe"""
        blocks = []
        
        # Utiliser les murs existants comme base
        for wall in random.sample(list(self.walls), min(count, len(self.walls))):
            blocks.append(wall)
        
        return blocks
    
    def _place_random_blocks(self, count: int) -> List[Tuple[int, int]]:
        """Place des blocs de glace aléatoirement"""
        blocks = []
        
        for _ in range(count):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            blocks.append((x, y))
        
        return blocks
    
    def _random_fruit_type(self) -> str:
        """Retourne un type de fruit aléatoire"""
        fruits = ['apple', 'banana', 'grape', 'orange', 'strawberry', 
                 'peach', 'pear', 'pepper', 'kiwi', 'lemon']
        return random.choice(fruits)
    
    def _random_enemy_role(self, difficulty: float) -> str:
        """Retourne un rôle d'ennemi selon la difficulté"""
        if difficulty < 0.3:
            return 'patroller'  # Facile
        elif difficulty < 0.7:
            return random.choice(['hunter', 'patroller'])  # Moyen
        else:
            # Difficile: plus de chasseurs
            return 'hunter' if random.random() > 0.3 else 'blocker'
    
    def _distance(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> float:
        """Calcule la distance euclidienne"""
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# Interface simplifiée
def generate(self, theme: LevelTheme = LevelTheme.CAVE, 
             difficulty: float = 0.5) -> Dict:
    """
    Génère un niveau complet
    
    Args:
        theme: Thème visuel du niveau
        difficulty: Niveau de difficulté (0.0 à 1.0)
        
    Returns:
        Dictionnaire contenant tous les éléments du niveau
    """
    print(f"🎮 Génération d'un niveau {theme.value} (difficulté: {difficulty:.1f})")
    
    # Réinitialiser
    self.rooms = []
    self.corridors = []
    self.walls = set()
    self.free_cells = set()
    
    try:
        # Étape 1: Générer l'arbre BSP
        print("  Étape 1: Génération de l'arbre BSP")
        root_rect = (50, 50, self.width - 100, self.height - 100)  # Marge pour les bords
        bsp_tree = self._generate_bsp(root_rect, depth=0)
        
        # Étape 2: Créer des salles dans les feuilles de l'arbre BSP
        print("  Étape 2: Création des salles")
        self._create_rooms_in_leaves(bsp_tree)
        print(f"    {len(self.rooms)} salles créées")
        
        if not self.rooms:
            print("  ⚠️ Aucune salle créée, création d'une salle par défaut")
            self._create_default_room()
        
        # Étape 3: Connecter les salles avec des couloirs
        print("  Étape 3: Connexion des salles")
        self._connect_rooms()
        print(f"    {len(self.corridors)} couloirs créés")
        
        # Étape 4: Générer les murs
        print("  Étape 4: Génération des murs")
        self._generate_walls()
        
        # Étape 5: Placer les éléments selon le thème et la difficulté
        print("  Étape 5: Placement des éléments")
        elements = self._place_elements(theme, difficulty)
        
        print(f"✅ Niveau généré: {len(self.rooms)} salles, {len(self.corridors)} couloirs")
        return elements
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération: {e}")
        import traceback
        traceback.print_exc()
        
        # En cas d'erreur, créer un niveau minimal
        return self._create_minimal_level(theme, difficulty)
    
    def _create_default_room(self):
        """Crée une salle par défaut au centre de la map"""
        room_width = min(200, self.width - 100)
        room_height = min(150, self.height - 100)
        default_room = Room(
            (self.width - room_width) // 2,
            (self.height - room_height) // 2,
            room_width,
            room_height
        )
        self.rooms = [default_room]
    
        # Ajouter les cellules libres
        for rx in range(default_room.x, default_room.x + default_room.width):
            for ry in range(default_room.y, default_room.y + default_room.height):
                self.free_cells.add((rx, ry))

def _create_minimal_level(self, theme: LevelTheme, difficulty: float) -> Dict:
    """Crée un niveau minimal en cas d'erreur"""
    print("⚡ Création d'un niveau minimal de secours")
    
    # Créer une salle par défaut
    self._create_default_room()
    
    # Créer des éléments basiques
    return {
        'trolls': [{'pos': (self.width // 2 + 100, self.height // 2), 'role': 'patroller'}],
        'fruits': [{'pos': (self.width // 2 - 100, self.height // 2), 'type': 'apple'}],
        'iceblocks': [],
        'walls': [],
        'player_start': (self.width // 2, self.height // 2)
    }