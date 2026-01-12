import { ComparisonResult } from '../types';

interface ResultsProps {
  result: ComparisonResult;
  onReset: () => void;
}

export default function Results({ result, onReset }: ResultsProps) {
  const getScoreColor = (score: number) => {
    if (score >= 8) return '#2ed573';
    if (score >= 6) return '#ffa502';
    if (score >= 4) return '#ff6348';
    return '#ff4757';
  };

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high': return '#ff4757';
      case 'medium': return '#ffa502';
      case 'low': return '#2ed573';
      default: return '#747d8c';
    }
  };

  return (
    <div className="results-container">
      <div className="results-header">
        <h2>Decision Analysis Results</h2>
        <button onClick={onReset} className="reset-btn">
          New Comparison
        </button>
      </div>

      {/* Kiro AI Analysis Summary */}
      <div className="section kiro-summary">
        <h3>🤖 Kiro AI Analysis</h3>
        <div className="summary-card">
          <p className="summary-text">{result.kiro_analysis.summary}</p>
        </div>
      </div>

      {/* Scores Table */}
      <div className="section">
        <h3>📊 Option Scores</h3>
        <div className="scores-table">
          <div className="table-header">
            <div>Option</div>
            <div>Overall</div>
            <div>Cost</div>
            <div>Latency</div>
            <div>Scale</div>
            <div>Compliance</div>
            <div>Cloud</div>
            <div>Skills</div>
            <div>Weighted</div>
          </div>
          {result.scores.map((score, index) => (
            <div key={index} className="table-row">
              <div className="option-name">{score.option_name}</div>
              <div className="score" style={{ color: getScoreColor(score.total_score) }}>
                {score.total_score}
              </div>
              <div className="score" style={{ color: getScoreColor(score.cost_score) }}>
                {score.cost_score}
              </div>
              <div className="score" style={{ color: getScoreColor(score.latency_score) }}>
                {score.latency_score}
              </div>
              <div className="score" style={{ color: getScoreColor(score.scalability_score) }}>
                {score.scalability_score}
              </div>
              <div className="score" style={{ color: getScoreColor(score.compliance_score) }}>
                {score.compliance_score}
              </div>
              <div className="score" style={{ color: getScoreColor(score.cloud_score) }}>
                {score.cloud_score}
              </div>
              <div className="score" style={{ color: getScoreColor(score.skill_score) }}>
                {score.skill_score}
              </div>
              <div className="score weighted" style={{ color: getScoreColor(score.weighted_score) }}>
                {score.weighted_score}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Trade-offs */}
      <div className="section">
        <h3>⚖️ Key Trade-offs</h3>
        <div className="tradeoffs-grid">
          {result.tradeoffs.map((tradeoff, index) => (
            <div key={index} className="tradeoff-card">
              <div className="tradeoff-header">
                <span className="dimension">{tradeoff.dimension.toUpperCase()}</span>
                <span 
                  className="impact-badge" 
                  style={{ backgroundColor: getImpactColor(tradeoff.impact) }}
                >
                  {tradeoff.impact} impact
                </span>
              </div>
              <div className="tradeoff-comparison">
                <span className="winner">{tradeoff.winner}</span>
                <span className="vs">vs</span>
                <span className="loser">
                  {tradeoff.option_a === tradeoff.winner ? tradeoff.option_b : tradeoff.option_a}
                </span>
              </div>
              <p className="tradeoff-explanation">{tradeoff.explanation}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Kiro Insights */}
      <div className="section">
        <h3>💡 Key Insights</h3>
        <div className="insights-list">
          {result.kiro_analysis.key_insights.map((insight, index) => (
            <div key={index} className="insight-item">
              <span className="insight-bullet">•</span>
              <span>{insight}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Recommendations */}
      <div className="section">
        <h3>🎯 Recommendations</h3>
        <div className="recommendations-list">
          {result.kiro_analysis.recommendations.map((rec, index) => (
            <div key={index} className="recommendation-item">
              <span className="rec-number">{index + 1}</span>
              <span>{rec}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Best For Scenarios */}
      <div className="section">
        <h3>🎭 Best for Different Scenarios</h3>
        <div className="scenarios-grid">
          {Object.entries(result.kiro_analysis.best_for_scenarios).map(([scenario, recommendation]) => (
            <div key={scenario} className="scenario-card">
              <h4>{scenario.replace(/_/g, ' ').toUpperCase()}</h4>
              <p>{recommendation}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Risk Factors */}
      {result.kiro_analysis.risk_factors.length > 0 && (
        <div className="section">
          <h3>⚠️ Risk Factors</h3>
          <div className="risks-list">
            {result.kiro_analysis.risk_factors.map((risk, index) => (
              <div key={index} className="risk-item">
                <span className="risk-icon">⚠️</span>
                <span>{risk}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      <style jsx>{`
        .results-container {
          background: white;
          border-radius: 12px;
          padding: 2rem;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }

        .results-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 2rem;
          padding-bottom: 1rem;
          border-bottom: 2px solid #f0f0f0;
        }

        .results-header h2 {
          color: #333;
          margin: 0;
          font-size: 2rem;
        }

        .reset-btn {
          background: #667eea;
          color: white;
          border: none;
          padding: 0.75rem 1.5rem;
          border-radius: 6px;
          cursor: pointer;
          font-size: 1rem;
        }

        .reset-btn:hover {
          background: #5a6fd8;
        }

        .section {
          margin-bottom: 2rem;
        }

        .section h3 {
          color: #333;
          margin-bottom: 1rem;
          font-size: 1.3rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .kiro-summary {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 1.5rem;
          border-radius: 8px;
          margin-bottom: 2rem;
        }

        .kiro-summary h3 {
          color: white;
          margin-bottom: 1rem;
        }

        .summary-card {
          background: rgba(255, 255, 255, 0.1);
          padding: 1rem;
          border-radius: 6px;
        }

        .summary-text {
          font-size: 1.1rem;
          line-height: 1.6;
          margin: 0;
        }

        .scores-table {
          background: #f9f9f9;
          border-radius: 8px;
          overflow: hidden;
          border: 1px solid #e0e0e0;
        }

        .table-header {
          display: grid;
          grid-template-columns: 2fr repeat(7, 1fr) 1.2fr;
          gap: 1rem;
          padding: 1rem;
          background: #333;
          color: white;
          font-weight: 600;
          font-size: 0.9rem;
        }

        .table-row {
          display: grid;
          grid-template-columns: 2fr repeat(7, 1fr) 1.2fr;
          gap: 1rem;
          padding: 1rem;
          border-bottom: 1px solid #e0e0e0;
          align-items: center;
        }

        .table-row:last-child {
          border-bottom: none;
        }

        .option-name {
          font-weight: 600;
          color: #333;
        }

        .score {
          font-weight: 600;
          text-align: center;
        }

        .score.weighted {
          font-size: 1.1rem;
          background: #f0f0f0;
          padding: 0.25rem;
          border-radius: 4px;
        }

        .tradeoffs-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 1rem;
        }

        .tradeoff-card {
          background: #f9f9f9;
          border: 1px solid #e0e0e0;
          border-radius: 8px;
          padding: 1rem;
        }

        .tradeoff-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.5rem;
        }

        .dimension {
          font-weight: 600;
          color: #333;
          font-size: 0.9rem;
        }

        .impact-badge {
          color: white;
          padding: 0.25rem 0.5rem;
          border-radius: 12px;
          font-size: 0.8rem;
          font-weight: 500;
        }

        .tradeoff-comparison {
          margin-bottom: 0.5rem;
          font-size: 1.1rem;
        }

        .winner {
          font-weight: 600;
          color: #2ed573;
        }

        .vs {
          margin: 0 0.5rem;
          color: #666;
        }

        .loser {
          color: #666;
        }

        .tradeoff-explanation {
          color: #555;
          font-size: 0.9rem;
          margin: 0;
        }

        .insights-list, .recommendations-list, .risks-list {
          space-y: 0.5rem;
        }

        .insight-item, .recommendation-item, .risk-item {
          display: flex;
          align-items: flex-start;
          gap: 0.5rem;
          padding: 0.75rem;
          background: #f9f9f9;
          border-radius: 6px;
          margin-bottom: 0.5rem;
        }

        .insight-bullet {
          color: #667eea;
          font-weight: bold;
          font-size: 1.2rem;
        }

        .rec-number {
          background: #667eea;
          color: white;
          width: 24px;
          height: 24px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.8rem;
          font-weight: 600;
          flex-shrink: 0;
        }

        .risk-icon {
          font-size: 1.2rem;
        }

        .scenarios-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 1rem;
        }

        .scenario-card {
          background: #f9f9f9;
          border: 1px solid #e0e0e0;
          border-radius: 8px;
          padding: 1rem;
        }

        .scenario-card h4 {
          color: #333;
          margin: 0 0 0.5rem 0;
          font-size: 0.9rem;
          font-weight: 600;
        }

        .scenario-card p {
          color: #555;
          margin: 0;
          font-size: 0.9rem;
        }

        @media (max-width: 768px) {
          .results-container {
            padding: 1rem;
          }

          .results-header {
            flex-direction: column;
            gap: 1rem;
            align-items: stretch;
          }

          .table-header, .table-row {
            grid-template-columns: 1fr;
            gap: 0.5rem;
          }

          .table-header > div, .table-row > div {
            padding: 0.25rem 0;
          }

          .tradeoffs-grid, .scenarios-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
}