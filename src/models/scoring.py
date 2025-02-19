from dataclasses import dataclass
from typing import Dict, List, Optional
import numpy as np

@dataclass
class StartupScore:
    team_score: float
    market_score: float
    financial_score: float
    overall_score: float
    
    @classmethod
    def calculate_scores(cls,
                        team_metrics: Dict[str, float],
                        market_metrics: Dict[str, float],
                        financial_metrics: Dict[str, float],
                        weights: Optional[Dict[str, float]] = None) -> 'StartupScore':
        """Calculate weighted scores for a startup"""
        
        if weights is None:
            weights = {
                'team': 0.4,
                'market': 0.3,
                'financial': 0.3
            }
        
        team_score = cls._calculate_component_score(team_metrics)
        market_score = cls._calculate_component_score(market_metrics)
        financial_score = cls._calculate_component_score(financial_metrics)
        
        overall_score = (
            team_score * weights['team'] +
            market_score * weights['market'] +
            financial_score * weights['financial']
        )
        
        return cls(
            team_score=team_score,
            market_score=market_score,
            financial_score=financial_score,
            overall_score=overall_score
        )
    
    @staticmethod
    def _calculate_component_score(metrics: Dict[str, float]) -> float:
        """Calculate score for a single component"""
        if not metrics:
            return 0.0
        return np.mean(list(metrics.values()))
