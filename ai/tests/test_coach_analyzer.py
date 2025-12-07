import unittest
import tempfile
import json
from pathlib import Path

from ai.coach.analyzer import PerformanceAnalyzer
from ai.utils.game_api import GameState, GameAPI

class TestPerformanceAnalyzer(unittest.TestCase):
    
    def setUp(self):
        self.analyzer = PerformanceAnalyzer()
        self.sample_state = GameState(
            player_pos=(100, 100),
            player_alive=True,
            trolls_pos=[(200, 150)],
            iceblocks_pos=[(150, 100)],
            fruits_pos=[(120, 120), (180, 180)],
            fruits_collected=[],
            level=1,
            round=1,
            timer=0.0,
            score=0
        )
    
    def test_initial_state(self):
        """Teste l'état initial de l'analyseur"""
        metrics = self.analyzer._get_current_metrics()
        self.assertEqual(metrics['death_count'], 0)
        self.assertEqual(metrics['fruit_order'], [])
        self.assertEqual(metrics['time_between_deaths'], [])
    
    def test_fruit_detection(self):
        """Teste la détection de collecte de fruits"""
        # Premier état avec des fruits
        state1 = self.sample_state
        self.analyzer.analyze_snapshot(state1)
        
        # Deuxième état avec un fruit en moins
        state2 = GameState(
            player_pos=(120, 120),
            player_alive=True,
            trolls_pos=[(200, 150)],
            iceblocks_pos=[(150, 100)],
            fruits_pos=[(180, 180)],  # Un fruit a été collecté
            fruits_collected=[(120, 120)],
            level=1,
            round=1,
            timer=1.0,
            score=50
        )
        
        metrics = self.analyzer.analyze_snapshot(state2)
        self.assertEqual(len(metrics['fruit_order']), 1)
        self.assertEqual(metrics['fruits_collected_this_session'], 1)
    
    def test_death_detection(self):
        """Teste la détection de mort du joueur"""
        # Joueur vivant
        state_alive = self.sample_state
        self.analyzer.analyze_snapshot(state_alive)
        
        # Joueur mort
        state_dead = GameState(
            player_pos=(100, 100),
            player_alive=False,  # Le joueur meurt
            trolls_pos=[(200, 150)],
            iceblocks_pos=[(150, 100)],
            fruits_pos=[(120, 120)],
            fruits_collected=[],
            level=1,
            round=1,
            timer=2.0,
            score=0
        )
        
        metrics = self.analyzer.analyze_snapshot(state_dead)
        self.assertEqual(metrics['death_count'], 1)
        self.assertEqual(len(metrics['time_between_deaths']), 0)  # Première mort
    
    def test_metrics_export(self):
        """Teste l'export des métriques en JSON"""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test_metrics.json"
            
            # Analyser un état
            self.analyzer.analyze_snapshot(self.sample_state)
            
            # Exporter
            metrics = self.analyzer.export_metrics(str(test_file))
            
            # Vérifier que le fichier existe
            self.assertTrue(test_file.exists())
            
            # Vérifier le contenu
            with open(test_file, 'r') as f:
                saved_metrics = json.load(f)
            
            self.assertEqual(saved_metrics['death_count'], 0)
            self.assertEqual(saved_metrics['schema_version'], GameAPI.SCHEMA_VERSION)
    
    def test_risk_zone_detection(self):
        """Teste la détection des zones à risque"""
        # État avec ennemi proche
        risky_state = GameState(
            player_pos=(100, 100),
            player_alive=True,
            trolls_pos=[(110, 110)],  # Très proche du joueur
            iceblocks_pos=[],
            fruits_pos=[],
            fruits_collected=[],
            level=1,
            round=1,
            timer=0.0,
            score=0
        )
        
        metrics = self.analyzer.analyze_snapshot(risky_state)
        self.assertGreater(metrics['high_risk_zones'], 0)

if __name__ == '__main__':
    unittest.main()# ai/tests/test_coach_analyzer.py
import unittest
import tempfile
import json
from pathlib import Path

from ai.coach.analyzer import PerformanceAnalyzer
from ai.utils.game_api import GameState, GameAPI

class TestPerformanceAnalyzer(unittest.TestCase):
    
    def setUp(self):
        self.analyzer = PerformanceAnalyzer()
        self.sample_state = GameState(
            player_pos=(100, 100),
            player_alive=True,
            trolls_pos=[(200, 150)],
            iceblocks_pos=[(150, 100)],
            fruits_pos=[(120, 120), (180, 180)],
            fruits_collected=[],
            level=1,
            round=1,
            timer=0.0,
            score=0
        )
    
    def test_initial_state(self):
        """Teste l'état initial de l'analyseur"""
        metrics = self.analyzer._get_current_metrics()
        self.assertEqual(metrics['death_count'], 0)
        self.assertEqual(metrics['fruit_order'], [])
        self.assertEqual(metrics['time_between_deaths'], [])
    
    def test_fruit_detection(self):
        """Teste la détection de collecte de fruits"""
        # Premier état avec des fruits
        state1 = self.sample_state
        self.analyzer.analyze_snapshot(state1)
        
        # Deuxième état avec un fruit en moins
        state2 = GameState(
            player_pos=(120, 120),
            player_alive=True,
            trolls_pos=[(200, 150)],
            iceblocks_pos=[(150, 100)],
            fruits_pos=[(180, 180)],  # Un fruit a été collecté
            fruits_collected=[(120, 120)],
            level=1,
            round=1,
            timer=1.0,
            score=50
        )
        
        metrics = self.analyzer.analyze_snapshot(state2)
        self.assertEqual(len(metrics['fruit_order']), 1)
        self.assertEqual(metrics['fruits_collected_this_session'], 1)
    
    def test_death_detection(self):
        """Teste la détection de mort du joueur"""
        # Joueur vivant
        state_alive = self.sample_state
        self.analyzer.analyze_snapshot(state_alive)
        
        # Joueur mort
        state_dead = GameState(
            player_pos=(100, 100),
            player_alive=False,  # Le joueur meurt
            trolls_pos=[(200, 150)],
            iceblocks_pos=[(150, 100)],
            fruits_pos=[(120, 120)],
            fruits_collected=[],
            level=1,
            round=1,
            timer=2.0,
            score=0
        )
        
        metrics = self.analyzer.analyze_snapshot(state_dead)
        self.assertEqual(metrics['death_count'], 1)
        self.assertEqual(len(metrics['time_between_deaths']), 0)  # Première mort
    
    def test_metrics_export(self):
        """Teste l'export des métriques en JSON"""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test_metrics.json"
            
            # Analyser un état
            self.analyzer.analyze_snapshot(self.sample_state)
            
            # Exporter
            metrics = self.analyzer.export_metrics(str(test_file))
            
            # Vérifier que le fichier existe
            self.assertTrue(test_file.exists())
            
            # Vérifier le contenu
            with open(test_file, 'r') as f:
                saved_metrics = json.load(f)
            
            self.assertEqual(saved_metrics['death_count'], 0)
            self.assertEqual(saved_metrics['schema_version'], GameAPI.SCHEMA_VERSION)
    
    def test_risk_zone_detection(self):
        """Teste la détection des zones à risque"""
        # État avec ennemi proche
        risky_state = GameState(
            player_pos=(100, 100),
            player_alive=True,
            trolls_pos=[(110, 110)],  # Très proche du joueur
            iceblocks_pos=[],
            fruits_pos=[],
            fruits_collected=[],
            level=1,
            round=1,
            timer=0.0,
            score=0
        )
        
        metrics = self.analyzer.analyze_snapshot(risky_state)
        self.assertGreater(metrics['high_risk_zones'], 0)

if __name__ == '__main__':
    unittest.main()