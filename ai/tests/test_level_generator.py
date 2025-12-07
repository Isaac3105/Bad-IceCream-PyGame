"""
Tests unitaires pour le générateur de niveaux
"""
import sys
import os
from pathlib import Path

# Ajouter le chemin du projet
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

import pytest
from ai.design.level_generator import LevelGenerator, LevelTheme, generate_level
from ai.design.maze_generator import MazeGenerator, generate_ice_maze
from ai.design.difficulty_balancer import DifficultyBalancer, DifficultyMetrics

class TestLevelGenerator:
    """Tests pour le générateur de niveaux BSP"""
    
    def test_generator_initialization(self):
        """Test l'initialisation du générateur"""
        generator = LevelGenerator()
        assert generator.width == 820
        assert generator.height == 622
        assert generator.min_room_size > 0
        assert generator.max_room_size > generator.min_room_size
    
    def test_level_generation(self):
        """Test la génération d'un niveau basique"""
        generator = LevelGenerator(width=400, height=300)  # Taille réduite pour les tests
        level = generator.generate(theme=LevelTheme.CAVE, difficulty=0.5)
        
        # Vérifier la présence des clés essentielles
        assert 'trolls' in level
        assert 'fruits' in level
        assert 'iceblocks' in level
        assert 'player_start' in level
        
        # Vérifier les types
        assert isinstance(level['trolls'], list)
        assert isinstance(level['fruits'], list)
        assert isinstance(level['iceblocks'], list)
        assert isinstance(level['player_start'], tuple)

class TestMazeGenerator:
    """Tests pour le générateur de labyrinthes"""
    
    def test_maze_generator_initialization(self):
        """Test l'initialisation du générateur de labyrinthes"""
        generator = MazeGenerator(width=10, height=10)
        assert generator.width == 10
        assert generator.height == 10
        assert generator.cell_size == 40
    
    def test_maze_generation(self):
        """Test la génération d'un labyrinthe"""
        generator = MazeGenerator(width=5, height=5)
        maze_data = generator.generate()
        
        assert 'walls' in maze_data
        assert 'paths' in maze_data
        assert 'width' in maze_data
        assert 'height' in maze_data
        
        # Un labyrinthe 5x5 doit avoir des chemins
        assert len(maze_data['paths']) == 25

class TestDifficultyBalancer:
    """Tests pour le système d'équilibrage de difficulté"""
    
    def test_balancer_initialization(self):
        """Test l'initialisation du balancer"""
        balancer = DifficultyBalancer(target_difficulty=0.6)
        assert balancer.target_difficulty == 0.6
        assert len(balancer.player_history) == 0
    
    def test_difficulty_metrics(self):
        """Test la classe DifficultyMetrics"""
        metrics = DifficultyMetrics(
            enemy_density=0.5,
            obstacle_density=0.3,
            path_complexity=0.4,
            resource_availability=0.7,
            navigation_difficulty=0.2
        )
        
        overall = metrics.overall_difficulty
        assert 0.0 <= overall <= 1.0

def test_simple_integration():
    """Test d'intégration simple"""
    # Test de la fonction generate_level
    level = generate_level(theme="cave", difficulty=0.5)
    assert level is not None
    assert 'trolls' in level
    print("✅ Test d'intégration réussi")

if __name__ == "__main__":
    # Exécuter les tests manuellement
    print("🧪 Exécution des tests...")
    
    try:
        test_generator = TestLevelGenerator()
        test_generator.test_generator_initialization()
        print("✅ test_generator_initialization")
        
        test_generator.test_level_generation()
        print("✅ test_level_generation")
        
        test_balancer = TestDifficultyBalancer()
        test_balancer.test_balancer_initialization()
        print("✅ test_balancer_initialization")
        
        test_balancer.test_difficulty_metrics()
        print("✅ test_difficulty_metrics")
        
        test_simple_integration()
        print("✅ test_simple_integration")
        
        print("\n🎉 Tous les tests de base passent!")
    except Exception as e:
        print(f"❌ Erreur pendant les tests: {e}")
        import traceback
        traceback.print_exc()