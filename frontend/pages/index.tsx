import { useState } from 'react';
import CompareForm from '../components/CompareForm';
import Results from '../components/Results';
import { ComparisonRequest, ComparisonResult } from '../types';

export default function Home() {
  const [result, setResult] = useState<ComparisonResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCompare = async (request: ComparisonRequest) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/compare', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="container">
      <header className="header">
        <h1>Decision Intelligence Platform</h1>
        <p>Compare technical options with AI-powered analysis</p>
      </header>

      <main className="main">
        {!result ? (
          <CompareForm onSubmit={handleCompare} loading={loading} error={error} />
        ) : (
          <Results result={result} onReset={handleReset} />
        )}
      </main>

      <footer className="footer">
        <p>AWS Builder Center - Decision Intelligence Platform</p>
      </footer>

      <style jsx>{`
        .container {
          min-height: 100vh;
          padding: 0 2rem;
          display: flex;
          flex-direction: column;
          justify-content: flex-start;
          align-items: center;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }

        .header {
          text-align: center;
          margin: 2rem 0;
          color: white;
        }

        .header h1 {
          font-size: 3rem;
          margin-bottom: 0.5rem;
          font-weight: 700;
        }

        .header p {
          font-size: 1.2rem;
          opacity: 0.9;
        }

        .main {
          flex: 1;
          width: 100%;
          max-width: 1200px;
          margin-bottom: 2rem;
        }

        .footer {
          text-align: center;
          padding: 1rem 0;
          color: white;
          opacity: 0.8;
        }

        @media (max-width: 768px) {
          .container {
            padding: 0 1rem;
          }
          
          .header h1 {
            font-size: 2rem;
          }
        }
      `}</style>
    </div>
  );
}