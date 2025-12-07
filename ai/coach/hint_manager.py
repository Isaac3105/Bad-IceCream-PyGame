# ai/coach/hint_manager.py
import time
from typing import List, Dict
from dataclasses import dataclass

from .hints import Hint, HintGenerator

@dataclass
class DisplayedHint:
    """Conseil actuellement affiché"""
    hint: Hint
    start_time: float
    expires_at: float

class HintManager:
    """Gère l'affichage et priorisation des conseils"""
    
    def __init__(self, max_concurrent_hints: int = 2):
        self.hint_generator = HintGenerator()
        self.max_concurrent_hints = max_concurrent_hints
        self.current_hints: List[DisplayedHint] = []
        self.hint_history: List[Hint] = []
        self.enabled = True
    
    def update(self, metrics: Dict, game_state) -> List[Hint]:
        """Met à jour et retourne conseils à afficher"""
        if not self.enabled:
            return []
        
        current_time = time.time()
        
        # Nettoyer conseils expirés
        self._clean_expired_hints(current_time)
        
        # Générer nouveaux conseils
        new_hints = self.hint_generator.generate_hints(metrics, game_state)
        
        # Sélectionner conseils à afficher
        hints_to_display = self._select_hints_to_display(new_hints, current_time)
        
        # Ajouter à l'affichage
        for hint in hints_to_display:
            if len(self.current_hints) < self.max_concurrent_hints:
                self.current_hints.append(DisplayedHint(
                    hint=hint,
                    start_time=current_time,
                    expires_at=current_time + hint.duration
                ))
                hint.mark_displayed(current_time)
                self.hint_history.append(hint)
        
        return [dh.hint for dh in self.current_hints]
    
    def get_current_hints(self) -> List[Hint]:
        """Retourne conseils actuellement affichés"""
        return [dh.hint for dh in self.current_hints]
    
    def clear_hints(self):
        """Efface tous les conseils"""
        self.current_hints.clear()
    
    def disable(self):
        """Désactive le système"""
        self.enabled = False
        self.clear_hints()
    
    def enable(self):
        """Active le système"""
        self.enabled = True
    
    def _clean_expired_hints(self, current_time: float):
        """Supprime conseils expirés"""
        self.current_hints = [
            dh for dh in self.current_hints 
            if current_time < dh.expires_at
        ]
    
    def _select_hints_to_display(self, new_hints: List[Hint], current_time: float) -> List[Hint]:
        """Sélectionne conseils selon priorité et limitations"""
        available = [h for h in new_hints if h.is_ready(current_time)]
        
        if not available:
            return []
        
        # Trier par priorité
        available.sort(key=lambda h: h.priority.value, reverse=True)
        
        # Prendre les plus prioritaires
        selected = available[:self.max_concurrent_hints]
        
        # Éviter doublons avec ceux déjà affichés
        current_messages = {dh.hint.message for dh in self.current_hints}
        selected = [h for h in selected if h.message not in current_messages]
        
        return selected
    
    def get_stats(self) -> Dict:
        """Retourne statistiques d'utilisation"""
        return {
            "total_hints_generated": len(self.hint_history),
            "currently_displayed": len(self.current_hints),
            "enabled": self.enabled,
            "recent_hints": [
                {"message": h.message, "priority": h.priority.name, "category": h.category}
                for h in self.hint_history[-3:]
            ]
        }