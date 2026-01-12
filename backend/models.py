from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from enum import Enum

class CloudProvider(str, Enum):
    AWS = "aws"
    AZURE = "azure"
    GCP = "gcp"
    MULTI = "multi"

class ComplianceLevel(str, Enum):
    NONE = "none"
    BASIC = "basic"
    HIPAA = "hipaa"
    SOC2 = "soc2"
    PCI = "pci"
    GDPR = "gdpr"

class SkillLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class TechOption(BaseModel):
    name: str
    description: str
    cost: float  # 1-10 scale (1=cheapest, 10=most expensive)
    latency: float  # 1-10 scale (1=fastest, 10=slowest)
    scalability: float  # 1-10 scale (1=limited, 10=unlimited)
    compliance: ComplianceLevel
    cloud: CloudProvider
    team_skill_required: SkillLevel
    pros: List[str]
    cons: List[str]

class Constraints(BaseModel):
    budget: float  # 1-10 scale (1=very tight, 10=unlimited)
    max_latency: float  # 1-10 scale (1=must be fastest, 10=latency ok)
    required_scale: float  # 1-10 scale (1=small scale, 10=massive scale)
    compliance: ComplianceLevel
    preferred_cloud: Optional[CloudProvider] = None
    team_skill: SkillLevel

class ComparisonRequest(BaseModel):
    options: List[TechOption]
    constraints: Constraints
    use_case: str
    description: Optional[str] = None

class OptionScore(BaseModel):
    option_name: str
    total_score: float
    cost_score: float
    latency_score: float
    scalability_score: float
    compliance_score: float
    cloud_score: float
    skill_score: float
    weighted_score: float

class TradeOff(BaseModel):
    option_a: str
    option_b: str
    dimension: str
    winner: str
    explanation: str
    impact: str  # "high", "medium", "low"

class KiroAnalysis(BaseModel):
    summary: str
    key_insights: List[str]
    recommendations: List[str]
    risk_factors: List[str]
    best_for_scenarios: Dict[str, str]

class ComparisonResult(BaseModel):
    comparison_id: Optional[str] = None
    scores: List[OptionScore]
    tradeoffs: List[TradeOff]
    kiro_analysis: KiroAnalysis
    timestamp: Optional[str] = None