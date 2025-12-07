# ai/tests/test_coach_hints.py
import unittest
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from coach.hints import HintGenerator, Hint, HintPriority
from coach.hint_manager import HintManager
from utils.game_api import GameState

class TestCoachHints(unittest.TestCase):
    
    def setUp(self):
        self.hint_generator = HintGenerator()
        self.hint_manager = HintManager()
        
        self.sample_metrics = {
            'death_count': 2,
            'fruit_order': ['apple', 'banana', 'apple'],
            'time_between_deaths': [15.0, 20.0],
            'average_fruit_time': 7.5,
            'high_risk_zones': 4,
            'total_fruits_collected': 3,
            'tick_count': 150,
            'ice_block_usage': 0
        }
        
        self.sample_game_state = GameState(
            player_pos=(400, 300),
            player_alive=True,
            trolls_pos=[(450, 320), (200, 200)],
            iceblocks_pos=[(350, 300), (500, 300)],
            fruits_pos=[(420, 280), (380, 320)],
            fruits_collected=[],
            level=1,
            round=1,
            timer=45.0,
            score=150
        )
    
    def test_hint_creation(self):
        """Test création d'un conseil"""
        hint = Hint(
            message="Test message",
            priority=HintPriority.MEDIUM,
            category="test",
            duration=5.0,
            cooldown=10.0
        )
        
        self.assertEqual(hint.message, "Test message")
        self.assertEqual(hint.priority, HintPriority.MEDIUM)
        self.assertEqual(hint.duration, 5.0)
    
    def test_hint_ready_check(self):
        """Test vérification disponibilité"""
        hint = Hint(
            message="Test",
            priority=HintPriority.LOW,
            category="test",
            duration=5.0,
            cooldown=10.0,
            last_displayed=time.time() - 15.0
        )
        
        self.assertTrue(hint.is_ready(time.time()))
        
        hint.last_displayed = time.time() - 5.0
        self.assertFalse(hint.is_ready(time.time()))
    
    def test_performance_hints(self):
        """Test génération conseils performance"""
        hints = self.hint_generator._generate_performance_hints(
            self.sample_metrics, 
            time.time()
        )
        
        self.assertIsInstance(hints, list)
        for hint in hints:
            self.assertIsInstance(hint, Hint)
    
    def test_danger_detection(self):
        """Test détection danger immédiat"""
        dangerous_state = GameState(
            player_pos=(400, 300),
            player_alive=True,
            trolls_pos=[(410, 310)],  # Très proche
            iceblocks_pos=[],
            fruits_pos=[],
            fruits_collected=[],
            level=1,
            round=1,
            timer=0.0,
            score=0
        )
        
        hints = self.hint_generator._generate_situational_hints(
            dangerous_state, 
            time.time()
        )
        
        critical_hints = [h for h in hints if h.priority == HintPriority.CRITICAL]
        self.assertGreater(len(critical_hints), 0)
    
    def test_pattern_detection(self):
        """Test détection patterns"""
        hint_generator = HintGenerator()
        
        # Pattern répétitif
        repetitive = ['apple', 'banana', 'apple', 'banana', 'apple', 'banana']
        self.assertTrue(hint_generator._has_repetitive_pattern(repetitive))
        
        # Non répétitif
        random = ['apple', 'banana', 'grape', 'apple', 'orange', 'banana']
        self.assertFalse(hint_generator._has_repetitive_pattern(random))
    
    def test_hint_manager(self):
        """Test gestionnaire de conseils"""
        self.assertEqual(self.hint_manager.max_concurrent_hints, 2)
        self.assertTrue(self.hint_manager.enabled)
    
    def test_hint_manager_update(self):
        """Test mise à jour gestionnaire"""
        hints = self.hint_manager.update(self.sample_metrics, self.sample_game_state)
        self.assertIsInstance(hints, list)

if __name__ == '__main__':
    unittest.main()