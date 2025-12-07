"""
Runner de simulation headless pour tester l'IA des ennemis - CORRIGÉ
"""
import json
import time
import sys
import os
from typing import List, Dict, Tuple
from pathlib import Path

# Ajouter le répertoire racine du projet au sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from ai.utils.game_api import GameState, GameAPI
from ai.enemies.a_star import AStarPathfinder
from ai.enemies.roles import create_enemy_ai, EnemyRole, HunterAI, PatrollerAI, BlockerAI, Waypoint
from ai.enemies.coordinator import get_global_coordinator

class SimulationRunner:
    """Runner de simulation sans interface graphique"""
    
    def __init__(self, config_file: str = None):
        self.config = self._load_config(config_file)
        self.pathfinder = AStarPathfinder(grid_width=20, grid_height=15)
        self.coordinator = get_global_coordinator()
        
        # Métriques de performance
        self.metrics = {
            "catch_rate": 0.0,  # Taux de capture du joueur
            "average_path_length": 0.0,  # Longueur moyenne des chemins
            "pathfinding_time": 0.0,  # Temps moyen de pathfinding
            "coordination_events": 0,  # Nombre d'événements de coordination
            "player_escape_time": 0.0  # Temps moyen d'évasion du joueur
        }
        
        self.enemy_ais: List[Dict] = []
        self.simulation_time = 0.0
        self.player_caught = False
        self.player_escape_start = None
        
    def _load_config(self, config_file: str) -> Dict:
        """Charge la configuration de simulation"""
        default_config = {
            "num_hunters": 2,
            "num_patrollers": 1,
            "num_blockers": 1,
            "simulation_duration": 60.0,  # secondes
            "player_strategy": "evasive",  # evasive, random, strategic
            "map_obstacles": "medium",  # low, medium, high
            "log_level": "info"
        }
        
        if config_file and Path(config_file).exists():
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        
        return default_config
    
    def setup_simulation(self, initial_state: GameState = None):
        """Configure la simulation avec un état initial"""
        if initial_state is None:
            initial_state = self._create_default_state()
        
        # Créer les IA selon la configuration
        self.enemy_ais = []
        enemy_id = 0
        
        # Hunters
        for i in range(self.config["num_hunters"]):
            ai = HunterAI(aggression=0.7 + i * 0.1)
            self.enemy_ais.append({
                "id": enemy_id,
                "ai": ai,
                "position": initial_state.trolls_pos[i] if i < len(initial_state.trolls_pos) else (100 + i*100, 100),
                "role": EnemyRole.HUNTER
            })
            enemy_id += 1
        
        # Patrollers
        waypoints = [
            Waypoint(200, 200, wait_time=1.0),
            Waypoint(400, 200, wait_time=0.5),
            Waypoint(400, 400, wait_time=1.0),
            Waypoint(200, 400, wait_time=0.5)
        ]
        
        for i in range(self.config["num_patrollers"]):
            ai = PatrollerAI(waypoints=waypoints)
            start_pos = (300 + i*50, 300) if i < len(initial_state.trolls_pos) else (300, 300)
            self.enemy_ais.append({
                "id": enemy_id,
                "ai": ai,
                "position": start_pos,
                "role": EnemyRole.PATROLLER
            })
            enemy_id += 1
        
        # Blockers
        strategic_points = [(150, 150), (550, 150), (150, 450), (550, 450)]
        
        for i in range(self.config["num_blockers"]):
            ai = BlockerAI(strategic_points=[strategic_points[i % len(strategic_points)]])
            self.enemy_ais.append({
                "id": enemy_id,
                "ai": ai,
                "position": strategic_points[i % len(strategic_points)],
                "role": EnemyRole.BLOCKER
            })
            enemy_id += 1
        
        print(f"✅ Simulation configurée avec {len(self.enemy_ais)} ennemis:")
        print(f"   - {self.config['num_hunters']} chasseurs")
        print(f"   - {self.config['num_patrollers']} patrouilleurs")
        print(f"   - {self.config['num_blockers']} bloqueurs")
    
    def run_simulation(self, steps: int = 1000):
        """Exécute la simulation pour un nombre d'étapes"""
        print(f"🚀 Démarrage de la simulation ({steps} étapes)...")
        
        # État initial mock
        game_state = self._create_default_state()
        
        for step in range(steps):
            if step % 100 == 0:
                print(f"  Step {step}/{steps}...")
            
            self.simulation_time += 1.0 / 60.0  # 60 FPS
            
            # Mettre à jour l'état du jeu (simulé)
            game_state = self._simulate_game_state(game_state, step)
            
            # Mettre à jour chaque IA
            enemies_positions = []
            pathfinding_times = []
            
            for enemy in self.enemy_ais:
                start_time = time.time()
                
                # Mettre à jour l'IA
                new_position = enemy["ai"].update(enemy["position"], game_state)
                enemy["position"] = new_position
                
                # Mesurer le temps de pathfinding
                pathfinding_time = time.time() - start_time
                pathfinding_times.append(pathfinding_time)
                
                # Collecter les positions pour le coordinateur
                enemies_positions.append((enemy["id"], new_position[0], new_position[1]))
                
                # Vérifier si le joueur est attrapé
                distance_to_player = self._calculate_distance(new_position, game_state.player_pos)
                if distance_to_player < 40 and not self.player_caught:  # Distance de capture
                    self.player_caught = True
                    self.metrics["catch_rate"] += 1
                    print(f"🎯 Joueur attrapé à l'étape {step} par l'ennemi {enemy['id']}!")
            
            # Mettre à jour le coordinateur
            coordination_messages = self.coordinator.update(enemies_positions, game_state)
            if coordination_messages:
                self.metrics["coordination_events"] += len(coordination_messages)
            
            # Calculer les métriques
            if pathfinding_times:
                self.metrics["pathfinding_time"] = sum(pathfinding_times) / len(pathfinding_times)
            
            # Vérifier l'évasion du joueur
            if self.player_caught and self.player_escape_start is None:
                self.player_escape_start = self.simulation_time
            elif not self.player_caught and self.player_escape_start:
                escape_duration = self.simulation_time - self.player_escape_start
                self.metrics["player_escape_time"] = escape_duration
                self.player_escape_start = None
            
            # Condition d'arrêt prématurée
            if self.simulation_time >= self.config["simulation_duration"]:
                print(f"⏱️ Durée de simulation atteinte: {self.simulation_time:.1f}s")
                break
        
        self._calculate_final_metrics()
        self._export_results()
        
        print("✅ Simulation terminée!")
        return self.metrics
    
    def _simulate_game_state(self, current_state: GameState, step: int) -> GameState:
        """Simule l'évolution de l'état du jeu"""
        # Simulation simple du joueur
        player_x, player_y = current_state.player_pos
        
        # Stratégie du joueur selon la configuration
        if self.config["player_strategy"] == "evasive":
            # Évite les ennemis
            closest_enemy = min(self.enemy_ais, 
                              key=lambda e: self._calculate_distance(e["position"], (player_x, player_y)))
            enemy_x, enemy_y = closest_enemy["position"]
            
            # Fuir dans la direction opposée
            dx = player_x - enemy_x
            dy = player_y - enemy_y
            
            # Normaliser et déplacer
            norm = (dx**2 + dy**2)**0.5
            if norm > 0:
                player_x += int(dx / norm * 3)
                player_y += int(dy / norm * 3)
        
        elif self.config["player_strategy"] == "strategic":
            # Va vers les fruits
            if current_state.fruits_pos:
                target_fruit = current_state.fruits_pos[0]
                fx, fy = target_fruit
                
                dx = fx - player_x
                dy = fy - player_y
                
                norm = (dx**2 + dy**2)**0.5
                if norm > 0:
                    player_x += int(dx / norm * 2)
                    player_y += int(dy / norm * 2)
        
        else:  # random
            # Mouvement aléatoire
            player_x += (step % 3 - 1) * 2  # -2, 0, ou 2
            player_y += ((step // 3) % 3 - 1) * 2
        
        # Limiter aux bornes
        player_x = max(50, min(player_x, 770))
        player_y = max(50, min(player_y, 572))
        
        # Mettre à jour l'état
        return GameState(
            player_pos=(player_x, player_y),
            player_alive=not self.player_caught,
            trolls_pos=[e["position"] for e in self.enemy_ais],
            iceblocks_pos=current_state.iceblocks_pos,
            fruits_pos=current_state.fruits_pos,
            fruits_collected=current_state.fruits_collected,
            level=current_state.level,
            round=current_state.round,
            timer=self.simulation_time,
            score=current_state.score
        )
    
    def _create_default_state(self) -> GameState:
        """Crée un état de jeu par défaut pour la simulation"""
        # Obstacles selon la configuration
        if self.config["map_obstacles"] == "low":
            iceblocks = [(300, 300), (400, 400)]
        elif self.config["map_obstacles"] == "high":
            iceblocks = [(x, y) for x in range(200, 600, 40) for y in range(200, 400, 58)]
        else:  # medium
            iceblocks = [(200, 200), (400, 200), (600, 200),
                        (200, 400), (400, 400), (600, 400)]
        
        return GameState(
            player_pos=(400, 300),
            player_alive=True,
            trolls_pos=[],
            iceblocks_pos=iceblocks,
            fruits_pos=[(100, 100), (700, 100), (100, 500), (700, 500)],
            fruits_collected=[],
            level=1,
            round=1,
            timer=0.0,
            score=0
        )
    
    def _calculate_final_metrics(self):
        """Calcule les métriques finales de la simulation"""
        # Catch rate en pourcentage
        total_catches = self.metrics["catch_rate"]
        self.metrics["catch_rate_percentage"] = (total_catches / max(1, self.simulation_time / 10)) * 100
        
        # Calculer la longueur moyenne des chemins
        path_lengths = []
        for enemy in self.enemy_ais:
            if hasattr(enemy["ai"], 'current_path'):
                path = enemy["ai"].current_path
                if path and len(path) > 1:
                    total_length = 0
                    for i in range(len(path) - 1):
                        total_length += self._calculate_distance(path[i], path[i+1])
                    if len(path) > 1:
                        path_lengths.append(total_length / (len(path) - 1))
        
        if path_lengths:
            self.metrics["average_path_length"] = sum(path_lengths) / len(path_lengths)
    
    def _export_results(self):
        """Exporte les résultats de la simulation"""
        results_dir = Path("data/simulations")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = results_dir / f"simulation_{timestamp}.json"
        
        results = {
            "timestamp": timestamp,
            "config": self.config,
            "metrics": self.metrics,
            "simulation_duration": self.simulation_time,
            "enemy_count": len(self.enemy_ais),
            "player_caught": self.player_caught,
            "coordination_events": self.metrics["coordination_events"]
        }
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"📊 Résultats exportés: {filename}")
    
    def _calculate_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5

def run_simulation_from_config(config_file: str = None):
    """Fonction principale pour lancer une simulation"""
    print("=" * 60)
    print("🤖 SIMULATION HEADLESS - IA DES ENNEMIS")
    print("=" * 60)
    
    runner = SimulationRunner(config_file)
    runner.setup_simulation()
    metrics = runner.run_simulation(steps=1200)  # 20 secondes à 60 FPS
    
    print("\n📊 RÉSULTATS DE LA SIMULATION:")
    print(f"  • Taux de capture: {metrics.get('catch_rate_percentage', 0):.1f}%")
    print(f"  • Longueur moyenne des chemins: {metrics.get('average_path_length', 0):.1f}px")
    print(f"  • Temps moyen de pathfinding: {metrics.get('pathfinding_time', 0)*1000:.2f}ms")
    print(f"  • Événements de coordination: {metrics.get('coordination_events', 0)}")
    print(f"  • Temps d'évasion moyen: {metrics.get('player_escape_time', 0):.1f}s")
    print(f"  • Durée totale: {runner.simulation_time:.1f}s")
    
    return metrics

if __name__ == "__main__":
    # Exemple d'utilisation
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        run_simulation_from_config(config_file)
    else:
        run_simulation_from_config()