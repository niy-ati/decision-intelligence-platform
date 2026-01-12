from typing import List, Dict
from models import TechOption, Constraints, OptionScore, ComplianceLevel, CloudProvider, SkillLevel

class ScoringEngine:
    def __init__(self):
        # Scoring weights - can be adjusted based on requirements
        self.weights = {
            'cost': 0.25,
            'latency': 0.20,
            'scalability': 0.20,
            'compliance': 0.15,
            'cloud': 0.10,
            'skill': 0.10
        }
    
    def score_options(self, options: List[TechOption], constraints: Constraints) -> List[OptionScore]:
        """Score all options against constraints"""
        scores = []
        
        for option in options:
            score = self._score_single_option(option, constraints)
            scores.append(score)
        
        return sorted(scores, key=lambda x: x.weighted_score, reverse=True)
    
    def _score_single_option(self, option: TechOption, constraints: Constraints) -> OptionScore:
        """Score a single option against constraints"""
        
        # Cost scoring (lower cost is better, so invert)
        cost_score = self._score_cost(option.cost, constraints.budget)
        
        # Latency scoring (lower latency is better, so invert)
        latency_score = self._score_latency(option.latency, constraints.max_latency)
        
        # Scalability scoring (higher scalability is better)
        scalability_score = self._score_scalability(option.scalability, constraints.required_scale)
        
        # Compliance scoring
        compliance_score = self._score_compliance(option.compliance, constraints.compliance)
        
        # Cloud preference scoring
        cloud_score = self._score_cloud(option.cloud, constraints.preferred_cloud)
        
        # Team skill scoring
        skill_score = self._score_skill(option.team_skill_required, constraints.team_skill)
        
        # Calculate weighted total
        weighted_score = (
            cost_score * self.weights['cost'] +
            latency_score * self.weights['latency'] +
            scalability_score * self.weights['scalability'] +
            compliance_score * self.weights['compliance'] +
            cloud_score * self.weights['cloud'] +
            skill_score * self.weights['skill']
        )
        
        total_score = (cost_score + latency_score + scalability_score + 
                      compliance_score + cloud_score + skill_score) / 6
        
        return OptionScore(
            option_name=option.name,
            total_score=round(total_score, 2),
            cost_score=round(cost_score, 2),
            latency_score=round(latency_score, 2),
            scalability_score=round(scalability_score, 2),
            compliance_score=round(compliance_score, 2),
            cloud_score=round(cloud_score, 2),
            skill_score=round(skill_score, 2),
            weighted_score=round(weighted_score, 2)
        )
    
    def _score_cost(self, option_cost: float, budget_constraint: float) -> float:
        """Score cost - higher budget tolerance allows higher costs"""
        if budget_constraint >= option_cost:
            return 10.0  # Perfect match
        else:
            # Penalty for exceeding budget
            penalty = (option_cost - budget_constraint) / budget_constraint
            return max(0, 10 - penalty * 5)
    
    def _score_latency(self, option_latency: float, latency_constraint: float) -> float:
        """Score latency - lower latency is better"""
        if option_latency <= latency_constraint:
            return 10.0  # Meets requirement
        else:
            # Penalty for exceeding latency requirement
            penalty = (option_latency - latency_constraint) / latency_constraint
            return max(0, 10 - penalty * 5)
    
    def _score_scalability(self, option_scalability: float, required_scale: float) -> float:
        """Score scalability - must meet minimum requirement"""
        if option_scalability >= required_scale:
            # Bonus for exceeding requirement
            bonus = min(2, (option_scalability - required_scale) / required_scale)
            return min(10, 8 + bonus)
        else:
            # Penalty for not meeting requirement
            penalty = (required_scale - option_scalability) / required_scale
            return max(0, 8 - penalty * 8)
    
    def _score_compliance(self, option_compliance: ComplianceLevel, required_compliance: ComplianceLevel) -> float:
        """Score compliance - must meet or exceed requirement"""
        compliance_levels = {
            ComplianceLevel.NONE: 0,
            ComplianceLevel.BASIC: 1,
            ComplianceLevel.SOC2: 2,
            ComplianceLevel.HIPAA: 3,
            ComplianceLevel.PCI: 3,
            ComplianceLevel.GDPR: 4
        }
        
        option_level = compliance_levels.get(option_compliance, 0)
        required_level = compliance_levels.get(required_compliance, 0)
        
        if option_level >= required_level:
            return 10.0
        else:
            return max(0, 10 - (required_level - option_level) * 3)
    
    def _score_cloud(self, option_cloud: CloudProvider, preferred_cloud: CloudProvider) -> float:
        """Score cloud preference"""
        if not preferred_cloud:
            return 8.0  # Neutral if no preference
        
        if option_cloud == preferred_cloud:
            return 10.0
        elif option_cloud == CloudProvider.MULTI:
            return 9.0  # Multi-cloud is flexible
        else:
            return 6.0  # Different cloud provider
    
    def _score_skill(self, required_skill: SkillLevel, team_skill: SkillLevel) -> float:
        """Score skill requirement vs team capability"""
        skill_levels = {
            SkillLevel.BEGINNER: 1,
            SkillLevel.INTERMEDIATE: 2,
            SkillLevel.ADVANCED: 3,
            SkillLevel.EXPERT: 4
        }
        
        required_level = skill_levels.get(required_skill, 1)
        team_level = skill_levels.get(team_skill, 1)
        
        if team_level >= required_level:
            return 10.0
        else:
            # Penalty for skill gap
            gap = required_level - team_level
            return max(0, 10 - gap * 3)