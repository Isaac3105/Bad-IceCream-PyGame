"""
Démonstration du système d'analyse de performance
"""
import sys
from pathlib import Path
import time

# Ajouter le chemin du projet
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from ai.coach.analyzer import PerformanceAnalyzer
from ai.utils.game_api import GameAPI, GameState, create_game_state_for_analyzer

def demo_analyzer():
    """Démonstration complète de l'analyzer"""
    print("=" * 60)
    print("📊 DÉMONSTRATION - ANALYSEUR DE PERFORMANCE")
    print("=" * 60)
    
    # Créer un analyseur
    analyzer = PerformanceAnalyzer()
    
    # Créer des données de test
    test_fruits = [
        {'pos': (100, 100), 'type': 'apple'},
        {'pos': (200, 200), 'type': 'banana'},
        {'pos': (300, 300), 'type': 'grape'},
        {'pos': (400, 400), 'type': 'orange'}
    ]
    
    test_trolls = [
        {'pos': (150, 150), 'role': 'hunter', 'id': 1},
        {'pos': (250, 250), 'role': 'patroller', 'id': 2}
    ]
    
    # Simulation de plusieurs ticks
    for tick in range(5):
        print(f"\n🎮 Tick {tick + 1}:")
        
        # Créer un état de jeu
        game_state = create_game_state_for_analyzer(
            player_pos=(50 + tick * 20, 50 + tick * 20),
            player_alive=True,
            trolls_info=test_trolls,
            fruits=test_fruits[tick:] if tick < 4 else [],  # Moins de fruits à chaque tick
            iceblocks=[(300, 300), (350, 350)],
            timer=tick * 10.0,
            score=tick * 100,
            player_has_block=(tick == 2)  # A un bloc au tick 2
        )
        
        # Analyser
        metrics = analyzer.analyze_snapshot(game_state)
        
        print(f"  • Fruits restants: {len(game_state.fruits_pos)}")
        print(f"  • Score: {game_state.score}")
        print(f"  • Fruits collectés: {analyzer.metrics.fruits_collected_this_session}")
    
    # Afficher les résultats finaux
    print("\n" + "=" * 60)
    print("📈 RÉSULTATS FINAUX")
    print("=" * 60)
    
    final_metrics = analyzer._get_current_metrics(game_state)
    for key, value in final_metrics.items():
        print(f"  {key}: {value}")
    
    # Score de performance
    score = analyzer.get_performance_score()
    print(f"\n🎯 Score de performance: {score:.1f}/100")
    
    # Recommandations
    recommendations = analyzer.get_recommendations()
    if recommendations:
        print("\n💡 Recommandations:")
        for rec in recommendations:
            print(f"  • {rec['message']} ({rec['priority']})")
    
    # Export
    export_file = analyzer.export_metrics()
    print(f"\n📁 Fichier exporté: {Path(export_file).name}")
    
    print("\n" + "=" * 60)
    print("✅ DÉMONSTRATION TERMINÉE!")
    print("=" * 60)

if __name__ == "__main__":
    demo_analyzer()