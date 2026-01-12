from typing import List, Dict
import asyncio
from models import ComparisonRequest, ComparisonResult, OptionScore, TradeOff, KiroAnalysis
from scoring import ScoringEngine
from tradeoffs import TradeOffGenerator
from kiro_agent import KiroAgent

class DecisionEngine:
    def __init__(self):
        self.scoring_engine = ScoringEngine()
        self.tradeoff_generator = TradeOffGenerator()
        self.kiro_agent = KiroAgent()
    
    async def compare(self, request: ComparisonRequest) -> ComparisonResult:
        """
        Main comparison logic that orchestrates scoring, trade-off analysis, and Kiro insights
        """
        # Step 1: Score all options
        scores = self.scoring_engine.score_options(request.options, request.constraints)
        
        # Step 2: Generate trade-offs between options
        tradeoffs = self.tradeoff_generator.generate_tradeoffs(request.options, scores)
        
        # Step 3: Get Kiro AI analysis
        kiro_analysis = await self.kiro_agent.analyze(
            request.options, 
            request.constraints, 
            scores, 
            tradeoffs,
            request.use_case
        )
        
        return ComparisonResult(
            scores=scores,
            tradeoffs=tradeoffs,
            kiro_analysis=kiro_analysis
        )
    
    def validate_request(self, request: ComparisonRequest) -> bool:
        """Validate that the comparison request is valid"""
        if len(request.options) < 2:
            raise ValueError("At least 2 options are required for comparison")
        
        if not request.use_case.strip():
            raise ValueError("Use case description is required")
        
        return True