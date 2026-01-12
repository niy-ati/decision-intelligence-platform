export interface TechOption {
  name: string;
  description: string;
  cost: number;
  latency: number;
  scalability: number;
  compliance: string;
  cloud: string;
  team_skill_required: string;
  pros: string[];
  cons: string[];
}

export interface Constraints {
  budget: number;
  max_latency: number;
  required_scale: number;
  compliance: string;
  preferred_cloud?: string;
  team_skill: string;
}

export interface ComparisonRequest {
  options: TechOption[];
  constraints: Constraints;
  use_case: string;
  description?: string;
}

export interface OptionScore {
  option_name: string;
  total_score: number;
  cost_score: number;
  latency_score: number;
  scalability_score: number;
  compliance_score: number;
  cloud_score: number;
  skill_score: number;
  weighted_score: number;
}

export interface TradeOff {
  option_a: string;
  option_b: string;
  dimension: string;
  winner: string;
  explanation: string;
  impact: string;
}

export interface KiroAnalysis {
  summary: string;
  key_insights: string[];
  recommendations: string[];
  risk_factors: string[];
  best_for_scenarios: Record<string, string>;
}

export interface ComparisonResult {
  comparison_id?: string;
  scores: OptionScore[];
  tradeoffs: TradeOff[];
  kiro_analysis: KiroAnalysis;
  timestamp?: string;
}