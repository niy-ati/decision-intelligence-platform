from typing import List, Dict
from models import TechOption, OptionScore, TradeOff

class TradeOffGenerator:
    def __init__(self):
        self.dimensions = ['cost', 'latency', 'scalability', 'compliance', 'cloud', 'skill']
    
    def generate_tradeoffs(self, options: List[TechOption], scores: List[OptionScore]) -> List[TradeOff]:
        """Generate trade-offs between all pairs of options"""
        tradeoffs = []
        
        # Create option lookup for easy access
        option_lookup = {opt.name: opt for opt in options}
        score_lookup = {score.option_name: score for score in scores}
        
        # Compare each pair of options
        for i in range(len(options)):
            for j in range(i + 1, len(options)):
                option_a = options[i]
                option_b = options[j]
                
                score_a = score_lookup[option_a.name]
                score_b = score_lookup[option_b.name]
                
                # Generate trade-offs for each dimension
                pair_tradeoffs = self._compare_options(option_a, option_b, score_a, score_b)
                tradeoffs.extend(pair_tradeoffs)
        
        return tradeoffs
    
    def _compare_options(self, option_a: TechOption, option_b: TechOption, 
                        score_a: OptionScore, score_b: OptionScore) -> List[TradeOff]:
        """Compare two options across all dimensions"""
        tradeoffs = []
        
        # Cost comparison
        if abs(score_a.cost_score - score_b.cost_score) > 1.0:
            winner = option_a.name if score_a.cost_score > score_b.cost_score else option_b.name
            loser = option_b.name if winner == option_a.name else option_a.name
            
            tradeoffs.append(TradeOff(
                option_a=option_a.name,
                option_b=option_b.name,
                dimension="cost",
                winner=winner,
                explanation=f"{winner} is more cost-effective than {loser}",
                impact=self._calculate_impact(abs(score_a.cost_score - score_b.cost_score))
            ))
        
        # Latency comparison
        if abs(score_a.latency_score - score_b.latency_score) > 1.0:
            winner = option_a.name if score_a.latency_score > score_b.latency_score else option_b.name
            loser = option_b.name if winner == option_a.name else option_a.name
            
            tradeoffs.append(TradeOff(
                option_a=option_a.name,
                option_b=option_b.name,
                dimension="latency",
                winner=winner,
                explanation=f"{winner} offers better latency performance than {loser}",
                impact=self._calculate_impact(abs(score_a.latency_score - score_b.latency_score))
            ))
        
        # Scalability comparison
        if abs(score_a.scalability_score - score_b.scalability_score) > 1.0:
            winner = option_a.name if score_a.scalability_score > score_b.scalability_score else option_b.name
            loser = option_b.name if winner == option_a.name else option_a.name
            
            tradeoffs.append(TradeOff(
                option_a=option_a.name,
                option_b=option_b.name,
                dimension="scalability",
                winner=winner,
                explanation=f"{winner} scales better than {loser}",
                impact=self._calculate_impact(abs(score_a.scalability_score - score_b.scalability_score))
            ))
        
        # Compliance comparison
        if abs(score_a.compliance_score - score_b.compliance_score) > 1.0:
            winner = option_a.name if score_a.compliance_score > score_b.compliance_score else option_b.name
            loser = option_b.name if winner == option_a.name else option_a.name
            
            tradeoffs.append(TradeOff(
                option_a=option_a.name,
                option_b=option_b.name,
                dimension="compliance",
                winner=winner,
                explanation=f"{winner} better meets compliance requirements than {loser}",
                impact=self._calculate_impact(abs(score_a.compliance_score - score_b.compliance_score))
            ))
        
        # Cloud preference comparison
        if abs(score_a.cloud_score - score_b.cloud_score) > 1.0:
            winner = option_a.name if score_a.cloud_score > score_b.cloud_score else option_b.name
            loser = option_b.name if winner == option_a.name else option_a.name
            
            tradeoffs.append(TradeOff(
                option_a=option_a.name,
                option_b=option_b.name,
                dimension="cloud",
                winner=winner,
                explanation=f"{winner} better aligns with cloud preferences than {loser}",
                impact=self._calculate_impact(abs(score_a.cloud_score - score_b.cloud_score))
            ))
        
        # Skill requirement comparison
        if abs(score_a.skill_score - score_b.skill_score) > 1.0:
            winner = option_a.name if score_a.skill_score > score_b.skill_score else option_b.name
            loser = option_b.name if winner == option_a.name else option_a.name
            
            tradeoffs.append(TradeOff(
                option_a=option_a.name,
                option_b=option_b.name,
                dimension="skill",
                winner=winner,
                explanation=f"{winner} better matches team skill level than {loser}",
                impact=self._calculate_impact(abs(score_a.skill_score - score_b.skill_score))
            ))
        
        return tradeoffs
    
    def _calculate_impact(self, score_difference: float) -> str:
        """Calculate impact level based on score difference"""
        if score_difference >= 4.0:
            return "high"
        elif score_difference >= 2.0:
            return "medium"
        else:
            return "low"