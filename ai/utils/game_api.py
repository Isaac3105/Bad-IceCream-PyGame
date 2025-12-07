"""
Interface pour communiquer avec le jeu - Version intégrée avec l'analyzer
"""
import json
import time
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum

class FruitType(Enum):
    """Types de fruits disponibles"""
    APPLE = "apple"
    BANANA = "banana"
    GRAPE = "grape"
    ORANGE = "orange"
    STRAWBERRY = "strawberry"
    PEACH = "peach"
    PEAR = "pear"
    PEPPER = "pepper"
    KIWI = "kiwi"
    LEMON = "lemon"

@dataclass
class GameState:
    """Représentation de l'état du jeu pour l'IA"""
    player_pos: Tuple[int, int]
    player_alive: bool
    trolls_pos: List[Tuple[int, int]]
    iceblocks_pos: List[Tuple[int, int]]
    fruits_pos: List[Tuple[int, int]]
    fruits_collected: List[Tuple[int, int]]
    level: int
    round: int
    timer: float
    score: int
    
    # Nouveaux champs pour l'analyzer amélioré
    player_has_block: bool = False
    fruit_types: Dict[Tuple[int, int], str] = field(default_factory=dict)
    trolls_info: List[Dict] = field(default_factory=list)
    
    @property
    def total_fruits(self) -> int:
        """Nombre total de fruits (collectés + restants)"""
        return len(self.fruits_pos) + len(self.fruits_collected)

class GameAPI:
    """Interface pour communiquer avec le jeu"""
    
    SCHEMA_VERSION = 1
    
    @classmethod
    def load_snapshot(cls, json_file: str) -> GameState:
        """Charge un snapshot JSON du jeu"""
        file_path = Path(json_file)
        if not file_path.exists():
            # Retourner un état mock pour les tests
            return cls._create_mock_state()
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        return cls._parse_game_state(data)
    
    @classmethod
    def get_current_state(cls) -> GameState:
        """Récupère l'état actuel du jeu (pour intégration future)"""
        # Pour l'instant, retourne un état mock
        return cls._create_mock_state()
    
    @staticmethod
    def _create_mock_state() -> GameState:
        """Crée un état de jeu mock pour les tests"""
        # Créer des fruits avec types
        fruits = [
            (120, 120), (180, 180), (220, 220),
            (300, 150), (350, 250), (400, 300)
        ]
        
        # Associer des types aux fruits
        fruit_types = {}
        fruit_type_list = list(FruitType)
        for i, pos in enumerate(fruits):
            fruit_types[pos] = fruit_type_list[i % len(fruit_type_list)].value
        
        # Créer des infos sur les trolls
        trolls_info = [
            {'pos': (200, 150), 'role': 'hunter', 'id': 1},
            {'pos': (300, 200), 'role': 'patroller', 'id': 2},
            {'pos': (400, 250), 'role': 'blocker', 'id': 3}
        ]
        
        return GameState(
            player_pos=(100, 100),
            player_alive=True,
            trolls_pos=[(200, 150), (300, 200), (400, 250)],
            iceblocks_pos=[(150, 100), (250, 150), (350, 200)],
            fruits_pos=fruits,
            fruits_collected=[],
            level=1,
            round=1,
            timer=0.0,
            score=0,
            player_has_block=False,
            fruit_types=fruit_types,
            trolls_info=trolls_info
        )
    
    @staticmethod
    def _parse_game_state(data: Dict[str, Any]) -> GameState:
        """Parse les données JSON en GameState"""
        # Créer un dictionnaire des types de fruits
        fruit_types = {}
        if 'fruit_types' in data:
            for pos_str, fruit_type in data['fruit_types'].items():
                pos = tuple(map(int, pos_str.strip('()').split(',')))
                fruit_types[pos] = fruit_type
        
        # Trolls avec informations complètes
        trolls_info = data.get('trolls_info', [])
        if not trolls_info and 'trolls_pos' in data:
            # Convertir les positions en info de trolls basiques
            trolls_info = [
                {'pos': tuple(pos), 'role': 'hunter', 'id': i}
                for i, pos in enumerate(data['trolls_pos'])
            ]
        
        return GameState(
            player_pos=tuple(data['player_pos']),
            player_alive=data['player_alive'],
            trolls_pos=[tuple(pos) for pos in data['trolls_pos']],
            iceblocks_pos=[tuple(pos) for pos in data['iceblocks_pos']],
            fruits_pos=[tuple(pos) for pos in data['fruits_pos']],
            fruits_collected=[tuple(pos) for pos in data.get('fruits_collected', [])],
            level=data['level'],
            round=data['round'],
            timer=data['timer'],
            score=data['score'],
            player_has_block=data.get('player_has_block', False),
            fruit_types=fruit_types,
            trolls_info=trolls_info
        )
    
    @staticmethod
    def export_metrics(metrics: Dict, filename: str):
        """Exporte les métriques en JSON"""
        output_dir = Path("data/logs")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = output_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2, default=str)
        
        print(f"📊 Métriques exportées: {file_path}")
    
    @staticmethod
    def create_test_snapshot(filename: str = "data/snapshots/test_snapshot.json"):
        """Crée un snapshot de test pour l'analyzer"""
        snapshot_dir = Path("data/snapshots")
        snapshot_dir.mkdir(parents=True, exist_ok=True)
        
        state = GameAPI._create_mock_state()
        
        snapshot_data = {
            "player_pos": list(state.player_pos),
            "player_alive": state.player_alive,
            "trolls_pos": [list(pos) for pos in state.trolls_pos],
            "iceblocks_pos": [list(pos) for pos in state.iceblocks_pos],
            "fruits_pos": [list(pos) for pos in state.fruits_pos],
            "fruits_collected": [list(pos) for pos in state.fruits_collected],
            "fruit_types": {str(pos): fruit_type for pos, fruit_type in state.fruit_types.items()},
            "trolls_info": state.trolls_info,
            "level": state.level,
            "round": state.round,
            "timer": state.timer,
            "score": state.score,
            "player_has_block": state.player_has_block,
            "timestamp": time.time()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(snapshot_data, f, indent=2)
        
        print(f"✅ Snapshot de test créé: {filename}")
        return filename

# Fonctions utilitaires pour l'analyzer
def create_game_state_for_analyzer(
    player_pos: Tuple[int, int],
    player_alive: bool,
    trolls_info: List[Dict],
    fruits: List[Dict],
    iceblocks: List[Tuple[int, int]],
    timer: float,
    score: int,
    player_has_block: bool = False
) -> GameState:
    """
    Crée un GameState à partir des données pour l'analyzer
    """
    # Séparer les fruits en positions et types
    fruits_pos = []
    fruit_types = {}
    
    for fruit in fruits:
        pos = fruit.get('pos')
        fruit_type = fruit.get('type', 'apple')
        if pos:
            fruits_pos.append(pos)
            fruit_types[pos] = fruit_type
    
    # Extraire les positions des trolls
    trolls_pos = [troll.get('pos', (0, 0)) for troll in trolls_info]
    
    return GameState(
        player_pos=player_pos,
        player_alive=player_alive,
        trolls_pos=trolls_pos,
        iceblocks_pos=iceblocks,
        fruits_pos=fruits_pos,
        fruits_collected=[],  # À déterminer par l'analyzer
        level=1,
        round=1,
        timer=timer,
        score=score,
        player_has_block=player_has_block,
        fruit_types=fruit_types,
        trolls_info=trolls_info
    )

# Test
if __name__ == "__main__":
    # Créer un snapshot de test
    GameAPI.create_test_snapshot()
    
    # Charger le snapshot
    state = GameAPI.load_snapshot("data/snapshots/test_snapshot.json")
    print(f"✅ État chargé: {state.player_pos}, {len(state.fruits_pos)} fruits")