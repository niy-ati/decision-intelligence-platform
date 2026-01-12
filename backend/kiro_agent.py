from typing import List, Dict
import json
import asyncio
from models import TechOption, Constraints, OptionScore, TradeOff, KiroAnalysis

class KiroAgent:
    """
    Kiro AI Agent that provides intelligent analysis of technical decisions
    """
    
    def __init__(self):
        self.analysis_templates = {
            "cost_focused": "For cost-sensitive projects, consider the long-term TCO including operational overhead.",
            "performance_focused": "Performance-critical applications should prioritize latency and scalability over cost.",
            "compliance_focused": "Regulatory requirements are non-negotiable and should drive the decision.",
            "team_focused": "Team expertise and learning curve significantly impact project success."
        }
    
    async def analyze(self, options: List[TechOption], constraints: Constraints, 
                     scores: List[OptionScore], tradeoffs: List[TradeOff], 
                     use_case: str) -> KiroAnalysis:
        """
        Generate comprehensive AI analysis of the decision
        """
        
        # Analyze the decision context
        context = self._analyze_context(constraints, use_case)
        
        # Generate insights from scores and trade-offs
        insights = self._generate_insights(options, scores, tradeoffs)
        
        # Create recommendations (multiple, not single)
        recommendations = self._generate_recommendations(options, scores, tradeoffs, context)
        
        # Identify risk factors
        risks = self._identify_risks(options, scores, tradeoffs)
        
        # Map best scenarios for each option
        scenarios = self._map_scenarios(options, scores, tradeoffs)
        
        # Generate summary
        summary = self._generate_summary(options, scores, context)
        
        return KiroAnalysis(
            summary=summary,
            key_insights=insights,
            recommendations=recommendations,
            risk_factors=risks,
            best_for_scenarios=scenarios
        )
    
    def _analyze_context(self, constraints: Constraints, use_case: str) -> Dict[str, any]:
        """Analyze the decision context to understand priorities"""
        context = {
            "primary_concern": "balanced",
            "risk_tolerance": "medium",
            "decision_type": "technical"
        }
        
        # Determine primary concern based on constraints
        if constraints.budget <= 3:
            context["primary_concern"] = "cost"
        elif constraints.max_latency <= 3:
            context["primary_concern"] = "performance"
        elif constraints.compliance.value in ["hipaa", "pci", "gdpr"]:
            context["primary_concern"] = "compliance"
        elif constraints.team_skill.value in ["beginner", "intermediate"]:
            context["primary_concern"] = "team_capability"
        
        # Analyze use case for additional context
        use_case_lower = use_case.lower()
        if any(word in use_case_lower for word in ["startup", "mvp", "prototype"]):
            context["risk_tolerance"] = "high"
        elif any(word in use_case_lower for word in ["enterprise", "production", "critical"]):
            context["risk_tolerance"] = "low"
        
        return context
    
    def _generate_insights(self, options: List[TechOption], scores: List[OptionScore], 
                          tradeoffs: List[TradeOff]) -> List[str]:
        """Generate key insights from the analysis"""
        insights = []
        
        # Score distribution insight
        top_score = scores[0].weighted_score
        bottom_score = scores[-1].weighted_score
        score_gap = top_score - bottom_score
        
        if score_gap < 1.0:
            insights.append("All options are very close in overall scoring - decision factors beyond metrics may be important")
        elif score_gap > 4.0:
            insights.append(f"Clear winner: {scores[0].option_name} significantly outperforms other options")
        
        # Trade-off insights
        high_impact_tradeoffs = [t for t in tradeoffs if t.impact == "high"]
        if high_impact_tradeoffs:
            dimensions = set(t.dimension for t in high_impact_tradeoffs)
            insights.append(f"Critical trade-offs exist in: {', '.join(dimensions)}")
        
        # Cost vs performance insight
        cost_leaders = sorted(scores, key=lambda x: x.cost_score, reverse=True)[:2]
        perf_leaders = sorted(scores, key=lambda x: (x.latency_score + x.scalability_score)/2, reverse=True)[:2]
        
        if set(s.option_name for s in cost_leaders) != set(s.option_name for s in perf_leaders):
            insights.append("Classic cost vs performance trade-off - no option excels at both")
        
        # Compliance insight
        compliance_scores = [s.compliance_score for s in scores]
        if max(compliance_scores) - min(compliance_scores) > 3:
            insights.append("Significant compliance differences between options - regulatory requirements are decisive")
        
        return insights
    
    def _generate_recommendations(self, options: List[TechOption], scores: List[OptionScore], 
                                tradeoffs: List[TradeOff], context: Dict) -> List[str]:
        """Generate multiple recommendations based on different scenarios"""
        recommendations = []
        
        # Always provide multiple recommendations, never just one
        top_3_options = scores[:3] if len(scores) >= 3 else scores
        
        # Context-based recommendations
        if context["primary_concern"] == "cost":
            cost_leader = max(scores, key=lambda x: x.cost_score)
            recommendations.append(f"For cost optimization: Choose {cost_leader.option_name} - best cost efficiency")
            
            if len(scores) > 1:
                balanced_option = scores[1] if scores[0] != cost_leader else scores[0]
                recommendations.append(f"For balanced approach: Consider {balanced_option.option_name} - good cost with better features")
        
        elif context["primary_concern"] == "performance":
            perf_scores = [(s.latency_score + s.scalability_score)/2 for s in scores]
            perf_leader = scores[perf_scores.index(max(perf_scores))]
            recommendations.append(f"For maximum performance: Choose {perf_leader.option_name} - superior speed and scale")
            
            if len(scores) > 1:
                cost_conscious = max(scores, key=lambda x: x.cost_score)
                if cost_conscious != perf_leader:
                    recommendations.append(f"For performance on budget: Consider {cost_conscious.option_name} - acceptable performance, lower cost")
        
        elif context["primary_concern"] == "compliance":
            compliance_leader = max(scores, key=lambda x: x.compliance_score)
            recommendations.append(f"For regulatory compliance: Choose {compliance_leader.option_name} - meets all requirements")
        
        # Risk-based recommendations
        if context["risk_tolerance"] == "low":
            established_options = [s for s in scores if any(opt.name == s.option_name and "enterprise" in opt.description.lower() for opt in options)]
            if established_options:
                recommendations.append(f"For low-risk deployment: {established_options[0].option_name} - proven enterprise solution")
        
        # Always include a "depends on priorities" recommendation
        recommendations.append(f"Choice depends on priorities: {scores[0].option_name} for overall balance, {max(scores, key=lambda x: x.cost_score).option_name} for cost, {max(scores, key=lambda x: x.latency_score).option_name} for performance")
        
        return recommendations
    
    def _identify_risks(self, options: List[TechOption], scores: List[OptionScore], 
                       tradeoffs: List[TradeOff]) -> List[str]:
        """Identify potential risks in each option"""
        risks = []
        
        # Low score risks
        for score in scores:
            if score.cost_score < 4:
                risks.append(f"{score.option_name}: High cost risk - may exceed budget")
            if score.latency_score < 4:
                risks.append(f"{score.option_name}: Performance risk - may not meet latency requirements")
            if score.scalability_score < 4:
                risks.append(f"{score.option_name}: Scalability risk - may not handle growth")
            if score.compliance_score < 6:
                risks.append(f"{score.option_name}: Compliance risk - may not meet regulatory requirements")
            if score.skill_score < 5:
                risks.append(f"{score.option_name}: Team capability risk - may require additional training")
        
        # Trade-off risks
        high_impact_tradeoffs = [t for t in tradeoffs if t.impact == "high"]
        for tradeoff in high_impact_tradeoffs:
            risks.append(f"Choosing {tradeoff.winner} over alternatives sacrifices {tradeoff.dimension} performance")
        
        return risks
    
    def _map_scenarios(self, options: List[TechOption], scores: List[OptionScore], 
                      tradeoffs: List[TradeOff]) -> Dict[str, str]:
        """Map which option is best for which scenario"""
        scenarios = {}
        
        # Cost-constrained scenario
        cost_leader = max(scores, key=lambda x: x.cost_score)
        scenarios["tight_budget"] = f"{cost_leader.option_name} - most cost-effective option"
        
        # Performance-critical scenario
        perf_scores = [(s.latency_score + s.scalability_score)/2 for s in scores]
        perf_leader = scores[perf_scores.index(max(perf_scores))]
        scenarios["high_performance"] = f"{perf_leader.option_name} - best performance characteristics"
        
        # Rapid deployment scenario
        skill_leader = max(scores, key=lambda x: x.skill_score)
        scenarios["quick_deployment"] = f"{skill_leader.option_name} - matches current team skills"
        
        # Enterprise scenario
        compliance_leader = max(scores, key=lambda x: x.compliance_score)
        scenarios["enterprise_deployment"] = f"{compliance_leader.option_name} - strongest compliance and governance"
        
        # Startup scenario
        balanced_leader = max(scores, key=lambda x: x.weighted_score)
        scenarios["startup_mvp"] = f"{balanced_leader.option_name} - best overall balance for rapid iteration"
        
        return scenarios
    
    def _generate_summary(self, options: List[TechOption], scores: List[OptionScore], 
                         context: Dict) -> str:
        """Generate executive summary of the analysis"""
        top_option = scores[0]
        option_count = len(options)
        
        summary = f"Analyzed {option_count} technical options for your use case. "
        
        if context["primary_concern"] == "cost":
            summary += f"With cost as the primary concern, the analysis reveals significant trade-offs between price and capabilities. "
        elif context["primary_concern"] == "performance":
            summary += f"Performance requirements drive this decision, with clear winners in latency and scalability. "
        elif context["primary_concern"] == "compliance":
            summary += f"Regulatory compliance is the decisive factor, limiting viable options. "
        
        summary += f"{top_option.option_name} leads in overall scoring (weighted score: {top_option.weighted_score}), "
        summary += f"but each option has distinct advantages depending on your specific priorities and constraints. "
        summary += f"The decision should align with your risk tolerance and long-term technical strategy."
        
        return summary