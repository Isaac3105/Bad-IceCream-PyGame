"""
Exporte les niveaux générés dans le format du jeu
"""
import json
import os
from typing import Dict, List, Tuple
from pathlib import Path
from datetime import datetime

class LevelExporter:
    """Exporte les niveaux générés vers différents formats"""
    
    def __init__(self, output_dir: str = "data/generated_levels"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_to_json(self, level_data: Dict, name: str = None) -> str:
        """
        Exporte un niveau au format JSON
        
        Args:
            level_data: Données du niveau
            name: Nom du fichier (sans extension)
            
        Returns:
            Chemin du fichier généré
        """
        if name is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"level_{timestamp}"
        
        filename = self.output_dir / f"{name}.json"
        
        # Formater les données pour l'export
        export_data = {
            'metadata': {
                'name': name,
                'generation_date': datetime.now().isoformat(),
                'version': '1.0',
                'difficulty': level_data.get('difficulty', 0.5)
            },
            'level_data': level_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Niveau exporté: {filename}")
        return str(filename)
    
    def export_to_python(self, level_data: Dict, name: str = None) -> str:
        """
        Exporte un niveau en code Python compatible avec le jeu
        
        Args:
            level_data: Données du niveau
            name: Nom du niveau
            
        Returns:
            Code Python généré
        """
        if name is None:
            name = "generated_level"
        
        # Générer le code Python
        code = self._generate_python_code(level_data, name)
        
        filename = self.output_dir / f"{name}.py"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(code)
        
        print(f"✅ Code Python généré: {filename}")
        return str(filename)
    
    def _generate_python_code(self, level_data: Dict, name: str) -> str:
        """Génère le code Python pour un niveau"""
        # Formater les listes de positions
        trolls_code = self._format_positions_list(level_data.get('trolls', []), 'trolls')
        fruits_code = self._format_fruits_list(level_data.get('fruits', []))
        iceblocks_code = self._format_positions_list(level_data.get('iceblocks', []), 'iceblocks')
        
        player_start = level_data.get('player_start', (400, 300))
        
        code = f'''"""
Niveau généré automatiquement: {name}
Date de génération: {datetime.now().isoformat()}
"""

# Position de départ du joueur
player_start = {player_start}

# Liste des trolls (position, rôle)
{trolls_code}

# Liste des fruits (position, type)
{fruits_code}

# Liste des blocs de glace (position)
{iceblocks_code}

# Niveau complet
{name} = [
    trolls,      # Index 0: Trolls
    fruits,      # Index 1: Fruits  
    iceblocks,   # Index 2: Blocs de glace
    [player_start]  # Index 3: Position du joueur
]
'''
        return code
    
    def _format_positions_list(self, items: List, var_name: str) -> str:
        """Formate une liste de positions pour l'export Python"""
        if not items:
            return f"{var_name} = []"
        
        lines = [f"{var_name} = ["]
        for item in items:
            if isinstance(item, dict) and 'pos' in item:
                pos = item['pos']
                if 'role' in item:
                    lines.append(f"    ({pos[0]}, {pos[1]}, '{item['role']}'),")
                else:
                    lines.append(f"    ({pos[0]}, {pos[1]}),")
            else:
                lines.append(f"    {item},")
        lines.append("]")
        
        return '\n'.join(lines)
    
    def _format_fruits_list(self, fruits: List[Dict]) -> str:
        """Formate la liste des fruits pour l'export Python"""
        if not fruits:
            return "fruits = []"
        
        lines = ["fruits = ["]
        for fruit in fruits:
            pos = fruit['pos']
            fruit_type = fruit.get('type', 'apple')
            lines.append(f"    Fruits({pos[0]}, {pos[1]}, '{fruit_type}', fruits, iceblocks),")
        lines.append("]")
        
        return '\n'.join(lines)
    
    def convert_to_game_format(self, level_data: Dict) -> List:
        """
        Convertit les données générées au format du jeu (liste de listes)
        
        Format attendu par Bad Ice Cream:
        [
            [trolls...],      # Troll objects
            [fruits...],      # Fruit objects  
            [iceblocks...],   # IceBlock objects
            [player...]       # Player object
        ]
        """
        # Cette fonction nécessite les classes du jeu
        # C'est un placeholder pour l'intégration future
        game_format = [
            level_data.get('trolls', []),
            level_data.get('fruits', []),
            level_data.get('iceblocks', []),
            [level_data.get('player_start', (400, 300))]
        ]
        
        return game_format

# Interface simplifiée
def export_level(level_data: Dict, format: str = "json", name: str = None) -> str:
    """
    Exporte un niveau dans le format spécifié
    
    Args:
        level_data: Données du niveau
        format: Format d'export ('json' ou 'python')
        name: Nom du niveau
        
    Returns:
        Chemin du fichier généré
    """
    exporter = LevelExporter()
    
    if format.lower() == 'python':
        return exporter.export_to_python(level_data, name)
    else:  # JSON par défaut
        return exporter.export_to_json(level_data, name)