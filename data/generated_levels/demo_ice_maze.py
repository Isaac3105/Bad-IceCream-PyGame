"""
Niveau généré automatiquement: demo_ice_maze
Date de génération: 2025-12-07T11:30:52.285494
"""

# Position de départ du joueur
player_start = (25, 25)

# Liste des trolls (position, rôle)
trolls = [
    (25, 25, 'hunter'),
    (25, 125, 'patroller'),
    (25, 225, 'patroller'),
]

# Liste des fruits (position, type)
fruits = [
    Fruits(25, 25, 'apple', fruits, iceblocks),
    Fruits(75, 225, 'apple', fruits, iceblocks),
    Fruits(125, 425, 'grape', fruits, iceblocks),
    Fruits(175, 625, 'grape', fruits, iceblocks),
    Fruits(275, 175, 'banana', fruits, iceblocks),
    Fruits(325, 375, 'banana', fruits, iceblocks),
    Fruits(375, 575, 'orange', fruits, iceblocks),
    Fruits(475, 125, 'banana', fruits, iceblocks),
    Fruits(525, 325, 'orange', fruits, iceblocks),
    Fruits(575, 525, 'apple', fruits, iceblocks),
]

# Liste des blocs de glace (position)
iceblocks = [
    (100, 650),
    (140, 650),
    (100, 300),
    (350, 650),
    (390, 650),
    (350, 400),
    (650, 600),
    (300, 550),
    (150, 600),
    (200, 600),
    (240, 600),
    (400, 150),
    (440, 150),
    (250, 100),
    (600, 0),
    (640, 0),
    (150, 550),
    (190, 550),
    (550, 0),
    (590, 0),
    (150, 400),
    (200, 400),
    (400, 300),
    (50, 350),
    (250, 150),
    (290, 150),
    (0, 0),
    (300, 500),
    (340, 500),
    (500, 600),
    (540, 600),
    (100, 200),
    (300, 400),
    (650, 500),
    (150, 50),
    (190, 50),
    (450, 200),
    (490, 200),
    (100, 250),
    (550, 300),
    (590, 300),
    (400, 600),
    (440, 600),
    (0, 650),
    (40, 650),
    (50, 50),
    (90, 50),
    (250, 450),
    (290, 450),
    (400, 650),
    (440, 650),
    (0, 100),
    (200, 50),
    (240, 50),
    (300, 50),
    (340, 50),
    (350, 100),
    (390, 100),
    (300, 100),
    (340, 100),
    (0, 450),
    (400, 550),
    (50, 150),
    (450, 300),
    (490, 300),
    (100, 300),
    (50, 250),
    (50, 550),
    (90, 550),
    (500, 350),
    (540, 350),
    (500, 600),
    (540, 600),
    (600, 650),
    (640, 650),
    (150, 350),
    (190, 350),
    (650, 350),
    (550, 250),
    (200, 550),
    (400, 600),
    (440, 600),
    (500, 100),
    (540, 100),
    (100, 350),
]

# Niveau complet
demo_ice_maze = [
    trolls,      # Index 0: Trolls
    fruits,      # Index 1: Fruits  
    iceblocks,   # Index 2: Blocs de glace
    [player_start]  # Index 3: Position du joueur
]
