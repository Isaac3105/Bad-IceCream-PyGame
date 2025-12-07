"""
Démonstration du générateur de niveaux
"""
import sys
import os
from pathlib import Path

# Configuration du chemin
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Importation correcte
from ai.design.level_generator import LevelGenerator, LevelTheme
from ai.design.maze_generator import generate_ice_maze
from ai.design.difficulty_balancer import get_difficulty_balancer
from ai.design.level_exporter import export_level

def demo_level_generation():
    """Démonstration complète de la génération de niveaux"""
    print("=" * 60)
    print("🗺️  DÉMONSTRATION - GÉNÉRATEUR DE NIVEAUX")
    print("=" * 60)
    
    # 1. Génération avec BSP
    print("\n1. Génération de niveau avec BSP (Binary Space Partitioning)")
    generator = LevelGenerator()
    
    for theme in LevelTheme:
        print(f"\n  🎨 Thème: {theme.value}")
        level = generator.generate(theme=theme, difficulty=0.5)
        print(f"    • Salles: {len(generator.rooms)}")
        print(f"    • Couloirs: {len(generator.corridors)}")
        print(f"    • Ennemis: {len(level['trolls'])}")
        print(f"    • Fruits: {len(level['fruits'])}")
        print(f"    • Blocs de glace: {len(level['iceblocks'])}")
    
    # 2. Génération de labyrinthe
    print("\n2. Génération de labyrinthe de glace")
    maze = generate_ice_maze(theme="ice", difficulty=0.7)
    print(f"  • Blocs de glace: {len(maze['iceblocks'])}")
    print(f"  • Fruits dans le labyrinthe: {len(maze['fruits'])}")
    print(f"  • Ennemis patrouilleurs: {len([t for t in maze['trolls'] if t['role'] == 'patroller'])}")
    
    # 3. Équilibrage de difficulté
    print("\n3. Équilibrage automatique de difficulté")
    balancer = get_difficulty_balancer()
    
    # Simuler des performances de joueurs
    test_level = generator.generate(theme=LevelTheme.CAVE, difficulty=0.5)
    
    # Joueur débutant
    balancer.record_player_performance(test_level, {
        'completed': True,
        'score': 450,
        'completion_time': 180,
        'deaths': 3
    }, player_id="debutant")
    
    # Joueur expert
    balancer.record_player_performance(test_level, {
        'completed': True,
        'score': 1200,
        'completion_time': 90,
        'deaths': 0
    }, player_id="expert")
    
    print(f"  • Niveau débutant estimé: {balancer.get_player_skill_level('debutant'):.2f}")
    print(f"  • Niveau expert estimé: {balancer.get_player_skill_level('expert'):.2f}")
    
    # 4. Export des niveaux
    print("\n4. Export des niveaux générés")
    
    # Exporter un niveau au format JSON
    json_file = export_level(test_level, format="json", name="demo_cave_level")
    print(f"  ✅ JSON exporté: {Path(json_file).name}")
    
    # Exporter un labyrinthe en Python
    python_file = export_level(maze, format="python", name="demo_ice_maze")
    print(f"  ✅ Python exporté: {Path(python_file).name}")
    
    print("\n" + "=" * 60)
    print("🎉 DÉMONSTRATION TERMINÉE!")
    print("=" * 60)
    
    return test_level, maze

if __name__ == "__main__":
    demo_level_generation()