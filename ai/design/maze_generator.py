"""
Générateur de labyrinthes par backtracking récursif
"""
import random
from typing import List, Tuple, Set, Dict
from enum import Enum

class MazeCell:
    """Représente une cellule dans le labyrinthe"""
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False
    
    def remove_wall(self, other: 'MazeCell'):
        """Enlève le mur entre deux cellules adjacentes"""
        dx = self.x - other.x
        dy = self.y - other.y
        
        if dx == 1:  # other est à gauche
            self.walls['W'] = False
            other.walls['E'] = False
        elif dx == -1:  # other est à droite
            self.walls['E'] = False
            other.walls['W'] = False
        elif dy == 1:  # other est en haut
            self.walls['N'] = False
            other.walls['S'] = False
        elif dy == -1:  # other est en bas
            self.walls['S'] = False
            other.walls['N'] = False

class MazeGenerator:
    """Génère des labyrinthes par backtracking récursif"""
    
    def __init__(self, width: int = 20, height: int = 15, cell_size: int = 40):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid: List[List[MazeCell]] = []
        self.paths: Set[Tuple[int, int]] = set()
        
    def generate(self) -> Dict:
        """Génère un labyrinthe complet"""
        # Initialiser la grille
        self.grid = [[MazeCell(x, y) for y in range(self.height)] 
                     for x in range(self.width)]
        
        # Backtracking récursif à partir d'un point aléatoire
        start_x, start_y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
        self._recursive_backtrack(self.grid[start_x][start_y])
        
        # Convertir en positions monde
        return self._to_world_coordinates()
    
    def _recursive_backtrack(self, cell: MazeCell):
        """Algorithme de backtracking récursif"""
        cell.visited = True
        
        # Voisins non visités
        neighbors = self._get_unvisited_neighbors(cell)
        random.shuffle(neighbors)
        
        for neighbor in neighbors:
            if not neighbor.visited:
                # Enlever le mur entre les cellules
                cell.remove_wall(neighbor)
                # Continuer récursivement
                self._recursive_backtrack(neighbor)
    
    def _get_unvisited_neighbors(self, cell: MazeCell) -> List[MazeCell]:
        """Retourne les voisins non visités d'une cellule"""
        neighbors = []
        x, y = cell.x, cell.y
        
        # Directions: (dx, dy)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbor = self.grid[nx][ny]
                if not neighbor.visited:
                    neighbors.append(neighbor)
        
        return neighbors
    
    def _to_world_coordinates(self) -> Dict:
        """Convertit le labyrinthe en coordonnées monde"""
        walls = []
        paths = []
    
    # Pour chaque cellule
        for x in range(self.width):
            for y in range(self.height):
                cell = self.grid[x][y]
                world_x = x * self.cell_size
                world_y = y * self.cell_size
            
                # MODIFIER : Ne générer que les murs extérieurs et quelques murs intérieurs
                if random.random() > 0.3:  # 70% de chance d'avoir un mur
                    if cell.walls['N'] and (y == 0 or random.random() > 0.5):
                        walls.append((world_x, world_y, world_x + self.cell_size, world_y))
                    if cell.walls['S'] and (y == self.height-1 or random.random() > 0.5):
                        walls.append((world_x, world_y + self.cell_size, 
                                 world_x + self.cell_size, world_y + self.cell_size))
                    if cell.walls['W'] and (x == 0 or random.random() > 0.5):
                        walls.append((world_x, world_y, world_x, world_y + self.cell_size))
                    if cell.walls['E'] and (x == self.width-1 or random.random() > 0.5):
                        walls.append((world_x + self.cell_size, world_y,
                                    world_x + self.cell_size, world_y + self.cell_size))
            
                # Ajouter le chemin (centre de la cellule)
                paths.append((world_x + self.cell_size // 2, world_y + self.cell_size // 2))
    
        return {
            'walls': walls,
            'paths': paths,
            'width': self.width * self.cell_size,
            'height': self.height * self.cell_size,
            'cell_size': self.cell_size
        }

# Interface pour générer des labyrinthes pour Bad Ice Cream
def generate_ice_maze(theme: str = "ice", difficulty: float = 0.5) -> Dict:
    """
    Génère un labyrinthe spécial pour Bad Ice Cream
    
    Args:
        theme: Thème du labyrinthe (ice, forest, cave)
        difficulty: Difficulté (0.0 à 1.0)
    
    Returns:
        Dictionnaire avec les éléments du niveau
    """
    # Ajuster la taille selon la difficulté
    base_size = 10  # Réduit de 15 à 10
    size_increase = int(difficulty * 5)  # Réduit de 10 à 5
    width = height = base_size + size_increase
    
    generator = MazeGenerator(width=width, height=height, cell_size=50)  # Taille de cellule augmentée
    
    maze_data = generator.generate()
    
    # Placer les éléments spécifiques au jeu
    elements = {
        'iceblocks': [],
        'fruits': [],
        'trolls': [],
        'player_start': maze_data['paths'][0] if maze_data['paths'] else (300, 300)
    }
    
    # Convertir les murs en blocs de glace (avec limite)
    max_blocks = int(50 + difficulty * 50)  # Maximum 100 blocs
    walls = maze_data['walls']
    
    # Prendre un échantillon limité de murs
    if len(walls) > max_blocks:
        walls = random.sample(walls, max_blocks)
    
    for wall in walls:
        x1, y1, x2, y2 = wall
        # Pour les murs horizontaux
        if y1 == y2:
            step = max(40, abs(x2 - x1) // 3)  # Limiter le nombre de blocs
            for x in range(x1, x2, step):
                if len(elements['iceblocks']) < max_blocks:
                    elements['iceblocks'].append((x, y1))
        # Pour les murs verticaux
        else:
            step = max(58, abs(y2 - y1) // 3)  # Limiter le nombre de blocs
            for y in range(y1, y2, step):
                if len(elements['iceblocks']) < max_blocks:
                    elements['iceblocks'].append((x1, y))
    
    # Placer des fruits le long des chemins
    num_fruits = int(5 + difficulty * 8)  # 5 à 13 fruits
    for i, path in enumerate(maze_data['paths']):
        if i % (len(maze_data['paths']) // num_fruits + 1) == 0 and len(elements['fruits']) < num_fruits:
            elements['fruits'].append({
                'pos': path,
                'type': random.choice(['apple', 'banana', 'grape', 'orange'])
            })
    
    # Placer des ennemis (corriger le rôle)
    num_trolls = int(1 + difficulty * 4)  # 1 à 5 trolls
    for i in range(num_trolls):
        if i * 2 < len(maze_data['paths']):
            troll_pos = maze_data['paths'][i * 2]
            # Changer la logique pour avoir plus de patrouilleurs
            if difficulty < 0.5:
                role = 'patroller'
            elif difficulty < 0.8:
                role = random.choice(['patroller', 'hunter'])
            else:
                role = 'hunter' if random.random() > 0.4 else 'blocker'
                
            elements['trolls'].append({
                'pos': troll_pos,
                'role': role
            })
    
    return elements