import { useState } from 'react';
import { ComparisonRequest, TechOption, Constraints } from '../types';

interface CompareFormProps {
  onSubmit: (request: ComparisonRequest) => void;
  loading: boolean;
  error: string | null;
}

export default function CompareForm({ onSubmit, loading, error }: CompareFormProps) {
  const [useCase, setUseCase] = useState('');
  const [description, setDescription] = useState('');
  const [options, setOptions] = useState<TechOption[]>([
    {
      name: '',
      description: '',
      cost: 5,
      latency: 5,
      scalability: 5,
      compliance: 'basic',
      cloud: 'aws',
      team_skill_required: 'intermediate',
      pros: [],
      cons: []
    },
    {
      name: '',
      description: '',
      cost: 5,
      latency: 5,
      scalability: 5,
      compliance: 'basic',
      cloud: 'aws',
      team_skill_required: 'intermediate',
      pros: [],
      cons: []
    }
  ]);
  
  const [constraints, setConstraints] = useState<Constraints>({
    budget: 5,
    max_latency: 5,
    required_scale: 5,
    compliance: 'basic',
    preferred_cloud: 'aws',
    team_skill: 'intermediate'
  });

  const addOption = () => {
    setOptions([...options, {
      name: '',
      description: '',
      cost: 5,
      latency: 5,
      scalability: 5,
      compliance: 'basic',
      cloud: 'aws',
      team_skill_required: 'intermediate',
      pros: [],
      cons: []
    }]);
  };

  const removeOption = (index: number) => {
    if (options.length > 2) {
      setOptions(options.filter((_, i) => i !== index));
    }
  };

  const updateOption = (index: number, field: keyof TechOption, value: any) => {
    const newOptions = [...options];
    newOptions[index] = { ...newOptions[index], [field]: value };
    setOptions(newOptions);
  };

  const updateConstraints = (field: keyof Constraints, value: any) => {
    setConstraints({ ...constraints, [field]: value });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate form
    if (!useCase.trim()) {
      alert('Please enter a use case');
      return;
    }
    
    if (options.some(opt => !opt.name.trim())) {
      alert('Please fill in all option names');
      return;
    }

    const request: ComparisonRequest = {
      options,
      constraints,
      use_case: useCase,
      description: description || undefined
    };

    onSubmit(request);
  };

  const loadPreset = (preset: string) => {
    switch (preset) {
      case 'api_gateway':
        setUseCase('API Gateway Selection');
        setOptions([
          {
            name: 'AWS API Gateway',
            description: 'Fully managed API gateway service',
            cost: 6,
            latency: 4,
            scalability: 9,
            compliance: 'soc2',
            cloud: 'aws',
            team_skill_required: 'intermediate',
            pros: ['Fully managed', 'Auto-scaling', 'AWS integration'],
            cons: ['Vendor lock-in', 'Cost at scale', 'Cold starts']
          },
          {
            name: 'Kong Gateway',
            description: 'Open-source API gateway',
            cost: 4,
            latency: 6,
            scalability: 8,
            compliance: 'basic',
            cloud: 'multi',
            team_skill_required: 'advanced',
            pros: ['Open source', 'Flexible', 'Multi-cloud'],
            cons: ['Self-managed', 'Complex setup', 'Operational overhead']
          },
          {
            name: 'Nginx Plus',
            description: 'Commercial web server and load balancer',
            cost: 5,
            latency: 8,
            scalability: 7,
            compliance: 'soc2',
            cloud: 'multi',
            team_skill_required: 'expert',
            pros: ['High performance', 'Proven', 'Flexible'],
            cons: ['Complex config', 'Limited API features', 'Manual scaling']
          }
        ]);
        break;
      case 'database':
        setUseCase('Database Selection for E-commerce');
        setOptions([
          {
            name: 'Amazon RDS PostgreSQL',
            description: 'Managed relational database',
            cost: 7,
            latency: 6,
            scalability: 7,
            compliance: 'soc2',
            cloud: 'aws',
            team_skill_required: 'intermediate',
            pros: ['ACID compliance', 'SQL support', 'Managed service'],
            cons: ['Higher cost', 'Vertical scaling limits', 'Complex queries']
          },
          {
            name: 'Amazon DynamoDB',
            description: 'NoSQL database service',
            cost: 5,
            latency: 9,
            scalability: 10,
            compliance: 'soc2',
            cloud: 'aws',
            team_skill_required: 'intermediate',
            pros: ['Serverless', 'Auto-scaling', 'Low latency'],
            cons: ['No SQL', 'Query limitations', 'Data modeling complexity']
          },
          {
            name: 'MongoDB Atlas',
            description: 'Cloud document database',
            cost: 6,
            latency: 7,
            scalability: 8,
            compliance: 'soc2',
            cloud: 'multi',
            team_skill_required: 'intermediate',
            pros: ['Flexible schema', 'Rich queries', 'Multi-cloud'],
            cons: ['Memory usage', 'Consistency model', 'Cost at scale']
          }
        ]);
        break;
    }
  };

  return (
    <div className="form-container">
      <form onSubmit={handleSubmit} className="compare-form">
        <div className="section">
          <h2>Use Case</h2>
          <div className="presets">
            <button type="button" onClick={() => loadPreset('api_gateway')}>
              Load API Gateway Example
            </button>
            <button type="button" onClick={() => loadPreset('database')}>
              Load Database Example
            </button>
          </div>
          
          <input
            type="text"
            placeholder="Enter your use case (e.g., 'API Gateway for microservices')"
            value={useCase}
            onChange={(e) => setUseCase(e.target.value)}
            required
          />
          
          <textarea
            placeholder="Additional description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={3}
          />
        </div>

        <div className="section">
          <h2>Your Constraints</h2>
          <div className="constraints-grid">
            <div className="constraint">
              <label>Budget (1=tight, 10=unlimited): {constraints.budget}</label>
              <input
                type="range"
                min="1"
                max="10"
                value={constraints.budget}
                onChange={(e) => updateConstraints('budget', parseInt(e.target.value))}
              />
            </div>
            
            <div className="constraint">
              <label>Max Latency (1=must be fastest, 10=latency ok): {constraints.max_latency}</label>
              <input
                type="range"
                min="1"
                max="10"
                value={constraints.max_latency}
                onChange={(e) => updateConstraints('max_latency', parseInt(e.target.value))}
              />
            </div>
            
            <div className="constraint">
              <label>Required Scale (1=small, 10=massive): {constraints.required_scale}</label>
              <input
                type="range"
                min="1"
                max="10"
                value={constraints.required_scale}
                onChange={(e) => updateConstraints('required_scale', parseInt(e.target.value))}
              />
            </div>
            
            <div className="constraint">
              <label>Compliance Requirement:</label>
              <select
                value={constraints.compliance}
                onChange={(e) => updateConstraints('compliance', e.target.value)}
              >
                <option value="none">None</option>
                <option value="basic">Basic</option>
                <option value="soc2">SOC 2</option>
                <option value="hipaa">HIPAA</option>
                <option value="pci">PCI DSS</option>
                <option value="gdpr">GDPR</option>
              </select>
            </div>
            
            <div className="constraint">
              <label>Preferred Cloud:</label>
              <select
                value={constraints.preferred_cloud || ''}
                onChange={(e) => updateConstraints('preferred_cloud', e.target.value || null)}
              >
                <option value="">No preference</option>
                <option value="aws">AWS</option>
                <option value="azure">Azure</option>
                <option value="gcp">Google Cloud</option>
                <option value="multi">Multi-cloud</option>
              </select>
            </div>
            
            <div className="constraint">
              <label>Team Skill Level:</label>
              <select
                value={constraints.team_skill}
                onChange={(e) => updateConstraints('team_skill', e.target.value)}
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
                <option value="expert">Expert</option>
              </select>
            </div>
          </div>
        </div>

        <div className="section">
          <h2>Options to Compare</h2>
          {options.map((option, index) => (
            <div key={index} className="option-card">
              <div className="option-header">
                <h3>Option {index + 1}</h3>
                {options.length > 2 && (
                  <button type="button" onClick={() => removeOption(index)} className="remove-btn">
                    Remove
                  </button>
                )}
              </div>
              
              <div className="option-fields">
                <input
                  type="text"
                  placeholder="Option name (e.g., 'AWS API Gateway')"
                  value={option.name}
                  onChange={(e) => updateOption(index, 'name', e.target.value)}
                  required
                />
                
                <textarea
                  placeholder="Description"
                  value={option.description}
                  onChange={(e) => updateOption(index, 'description', e.target.value)}
                  rows={2}
                />
                
                <div className="metrics-grid">
                  <div className="metric">
                    <label>Cost (1=cheap, 10=expensive): {option.cost}</label>
                    <input
                      type="range"
                      min="1"
                      max="10"
                      value={option.cost}
                      onChange={(e) => updateOption(index, 'cost', parseInt(e.target.value))}
                    />
                  </div>
                  
                  <div className="metric">
                    <label>Latency (1=fast, 10=slow): {option.latency}</label>
                    <input
                      type="range"
                      min="1"
                      max="10"
                      value={option.latency}
                      onChange={(e) => updateOption(index, 'latency', parseInt(e.target.value))}
                    />
                  </div>
                  
                  <div className="metric">
                    <label>Scalability (1=limited, 10=unlimited): {option.scalability}</label>
                    <input
                      type="range"
                      min="1"
                      max="10"
                      value={option.scalability}
                      onChange={(e) => updateOption(index, 'scalability', parseInt(e.target.value))}
                    />
                  </div>
                </div>
                
                <div className="selects-grid">
                  <div>
                    <label>Compliance Level:</label>
                    <select
                      value={option.compliance}
                      onChange={(e) => updateOption(index, 'compliance', e.target.value)}
                    >
                      <option value="none">None</option>
                      <option value="basic">Basic</option>
                      <option value="soc2">SOC 2</option>
                      <option value="hipaa">HIPAA</option>
                      <option value="pci">PCI DSS</option>
                      <option value="gdpr">GDPR</option>
                    </select>
                  </div>
                  
                  <div>
                    <label>Cloud Provider:</label>
                    <select
                      value={option.cloud}
                      onChange={(e) => updateOption(index, 'cloud', e.target.value)}
                    >
                      <option value="aws">AWS</option>
                      <option value="azure">Azure</option>
                      <option value="gcp">Google Cloud</option>
                      <option value="multi">Multi-cloud</option>
                    </select>
                  </div>
                  
                  <div>
                    <label>Skill Required:</label>
                    <select
                      value={option.team_skill_required}
                      onChange={(e) => updateOption(index, 'team_skill_required', e.target.value)}
                    >
                      <option value="beginner">Beginner</option>
                      <option value="intermediate">Intermediate</option>
                      <option value="advanced">Advanced</option>
                      <option value="expert">Expert</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
          ))}
          
          <button type="button" onClick={addOption} className="add-option-btn">
            Add Another Option
          </button>
        </div>

        {error && <div className="error">{error}</div>}

        <button type="submit" disabled={loading} className="submit-btn">
          {loading ? 'Analyzing...' : 'Compare Options'}
        </button>
      </form>

      <style jsx>{`
        .form-container {
          background: white;
          border-radius: 12px;
          padding: 2rem;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }

        .compare-form {
          max-width: 800px;
          margin: 0 auto;
        }

        .section {
          margin-bottom: 2rem;
        }

        .section h2 {
          color: #333;
          margin-bottom: 1rem;
          font-size: 1.5rem;
        }

        .presets {
          margin-bottom: 1rem;
        }

        .presets button {
          margin-right: 1rem;
          padding: 0.5rem 1rem;
          background: #f0f0f0;
          border: 1px solid #ddd;
          border-radius: 4px;
          cursor: pointer;
        }

        .presets button:hover {
          background: #e0e0e0;
        }

        input[type="text"], textarea, select {
          width: 100%;
          padding: 0.75rem;
          border: 1px solid #ddd;
          border-radius: 4px;
          margin-bottom: 1rem;
          font-size: 1rem;
        }

        .constraints-grid, .metrics-grid, .selects-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 1rem;
          margin-bottom: 1rem;
        }

        .constraint, .metric {
          display: flex;
          flex-direction: column;
        }

        .constraint label, .metric label {
          margin-bottom: 0.5rem;
          font-weight: 500;
          color: #555;
        }

        input[type="range"] {
          width: 100%;
          margin-bottom: 0.5rem;
        }

        .option-card {
          border: 1px solid #ddd;
          border-radius: 8px;
          padding: 1.5rem;
          margin-bottom: 1rem;
          background: #f9f9f9;
        }

        .option-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
        }

        .option-header h3 {
          margin: 0;
          color: #333;
        }

        .remove-btn {
          background: #ff4757;
          color: white;
          border: none;
          padding: 0.5rem 1rem;
          border-radius: 4px;
          cursor: pointer;
        }

        .remove-btn:hover {
          background: #ff3742;
        }

        .add-option-btn {
          background: #2ed573;
          color: white;
          border: none;
          padding: 1rem 2rem;
          border-radius: 4px;
          cursor: pointer;
          font-size: 1rem;
          width: 100%;
        }

        .add-option-btn:hover {
          background: #26d065;
        }

        .submit-btn {
          background: #667eea;
          color: white;
          border: none;
          padding: 1rem 2rem;
          border-radius: 4px;
          cursor: pointer;
          font-size: 1.1rem;
          width: 100%;
          margin-top: 1rem;
        }

        .submit-btn:hover:not(:disabled) {
          background: #5a6fd8;
        }

        .submit-btn:disabled {
          background: #ccc;
          cursor: not-allowed;
        }

        .error {
          background: #ff4757;
          color: white;
          padding: 1rem;
          border-radius: 4px;
          margin: 1rem 0;
        }

        @media (max-width: 768px) {
          .form-container {
            padding: 1rem;
          }
          
          .constraints-grid, .metrics-grid, .selects-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
}