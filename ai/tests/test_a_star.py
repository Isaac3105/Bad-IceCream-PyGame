"""
Tests unitaires pour l'algorithme A* - VERSION CORRIGÉE
"""
import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from ai.enemies.a_star import AStarPathfinder

class TestAStarPathfinder(unittest.TestCase):
    
    def setUp(self):
        # Pour les tests, utiliser cell_size=10 pour simplifier
        self.pathfinder = AStarPathfinder(grid_width=10, grid_height=10, cell_size=10)
    
    def test_simple_path(self):
        """Test chemin simple sans obstacles"""
        start = (0, 0)
        goal = (90, 90)  # Correspond à la cellule (9, 9) avec cell_size=10
        
        path = self.pathfinder.find_path(start, goal, [])
        
        self.assertGreater(len(path), 0)
        # Le chemin devrait commencer près de start et finir près de goal
        self.assertAlmostEqual(path[0][0], start[0], delta=10)
        self.assertAlmostEqual(path[0][1], start[1], delta=10)
        self.assertAlmostEqual(path[-1][0], goal[0], delta=10)
        self.assertAlmostEqual(path[-1][1], goal[1], delta=10)
    
    def test_path_with_obstacles(self):
        """Test chemin avec obstacles"""
        start = (0, 0)
        goal = (90, 90)
        # Obstacles au centre
        obstacles = [(40, 40), (40, 50), (50, 40), (50, 50)]
        
        path = self.pathfinder.find_path(start, goal, obstacles)
        
        self.assertGreater(len(path), 0)
    
    def test_no_path(self):
        """Test quand aucun chemin n'existe"""
        start = (0, 0)
        goal = (90, 90)
        # Mur complet au milieu
        obstacles = [(50, y) for y in range(0, 100, 10)]
        
        path = self.pathfinder.find_path(start, goal, obstacles)
        
        self.assertEqual(len(path), 0)
    
    def test_diagonal_movement(self):
        """Test mouvement diagonal"""
        start = (0, 0)
        goal = (90, 90)
        
        path = self.pathfinder.find_path(start, goal, [])
        
        # Vérifier qu'il y a des mouvements qui ne sont pas purement horizontaux/verticaux
        non_axis_aligned = False
        for i in range(len(path) - 1):
            dx = path[i+1][0] - path[i][0]
            dy = path[i+1][1] - path[i][1]
            # Si le mouvement a des composantes dans les deux directions, c'est diagonal
            if dx != 0 and dy != 0:
                non_axis_aligned = True
                break
        
        # Dans une grille libre, A* devrait prendre des diagonales
        self.assertTrue(non_axis_aligned, "Le chemin devrait contenir des mouvements diagonaux")

if __name__ == '__main__':
    unittest.main()