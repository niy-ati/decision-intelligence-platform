<<<<<<< HEAD
# Decision Intelligence Platform

A production-grade Decision Comparison Platform for AWS Builder Center that compares multiple technical options using AI-powered analysis.

## 🎯 Overview

The Decision Intelligence Platform helps technical teams make informed decisions by:
- Comparing multiple technical options (APIs, cloud services, stacks, architectures)
- Accepting constraints (budget, latency, scale, region, compliance, team skills)
- Scoring each option with transparent methodology
- Generating explicit trade-offs between options
- Providing AI-powered explanations and recommendations
- Never giving only one answer — always comparing multiple options

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Kiro Agent    │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (AI Analysis) │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   (SQLite)      │
                       └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### 1. Clone and Start
```bash
git clone <repository-url>
cd decision-intelligence-platform
docker-compose up --build
```

### 2. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 3. Try the Examples
The platform includes pre-loaded examples:
- **API Gateway Selection**: Compare AWS API Gateway, Kong, and Nginx Plus
- **Database Selection**: Compare RDS PostgreSQL, DynamoDB, and MongoDB Atlas

## 📊 How It Works

### 1. Input Your Decision
- **Use Case**: Describe what you're building
- **Constraints**: Set your budget, latency, scale, compliance, and team skill requirements
- **Options**: Add 2+ technical options to compare

### 2. AI Analysis
The Kiro agent analyzes your options using:
- **Weighted Scoring**: Each option scored across 6 dimensions
- **Trade-off Analysis**: Identifies where options win/lose against each other
- **Risk Assessment**: Highlights potential risks for each choice
- **Scenario Mapping**: Shows which option is best for different situations

### 3. Get Results
- **Score Table**: Transparent scoring across all dimensions
- **Trade-off Matrix**: Visual comparison of strengths/weaknesses
- **AI Insights**: Key findings and patterns
- **Multiple Recommendations**: Context-dependent suggestions
- **Risk Factors**: Potential issues to consider

## 🔧 Configuration

### Scoring Weights
Default weights (can be customized in `backend/scoring.py`):
- Cost: 25%
- Latency: 20%
- Scalability: 20%
- Compliance: 15%
- Cloud Preference: 10%
- Team Skills: 10%

### Kiro Agent Settings
Configure the AI agent in `.kiro/decision_agent.yaml`:
- Model parameters
- Analysis prompts
- Decision rules
- Integration settings

## 🛠️ Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Database Management
The SQLite database is automatically created. To reset:
```bash
docker-compose down -v
docker-compose up --build
```

## 📁 Project Structure

```
decision-intelligence-platform/
├── backend/                 # FastAPI backend
│   ├── main.py             # API endpoints
│   ├── decision_engine.py  # Core decision logic
│   ├── scoring.py          # Scoring algorithms
│   ├── tradeoffs.py        # Trade-off analysis
│   ├── kiro_agent.py       # AI agent integration
│   ├── models.py           # Data models
│   ├── db.py               # Database operations
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/               # Next.js frontend
│   ├── pages/index.tsx     # Main page
│   ├── components/         # React components
│   ├── styles.css          # Global styles
│   ├── package.json        # Node dependencies
│   └── Dockerfile          # Frontend container
├── .kiro/                  # Kiro agent configuration
│   └── decision_agent.yaml # Agent settings
├── docker-compose.yml      # Container orchestration
└── README.md              # This file
```

## 🔍 API Endpoints

### Core Endpoints
- `POST /compare` - Submit comparison request
- `GET /comparisons/{id}` - Retrieve specific comparison
- `GET /comparisons` - List recent comparisons
- `GET /health` - Health check

### Example API Usage
```bash
curl -X POST "http://localhost:8000/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "use_case": "API Gateway Selection",
    "options": [...],
    "constraints": {...}
  }'
```

## 🎨 Customization

### Adding New Scoring Dimensions
1. Update `models.py` to add new fields
2. Modify `scoring.py` to include new scoring logic
3. Update frontend forms in `CompareForm.tsx`

### Custom Decision Rules
Add rules in `.kiro/decision_agent.yaml`:
```yaml
decision_rules:
  - name: "custom_rule"
    condition: "custom_condition"
    action: "custom_action"
```

### Styling
- Global styles: `frontend/styles.css`
- Component styles: Inline JSX styles in components
- Theme colors: Update CSS variables

## 🔒 Security

- Input validation on all API endpoints
- CORS configuration for cross-origin requests
- SQL injection protection via parameterized queries
- Rate limiting (configurable)
- Health checks for all services

## 📈 Monitoring

### Health Checks
All services include health endpoints:
- Backend: `/health`
- Frontend: Built-in Next.js health
- Database: Connection validation

### Logging
- Backend: FastAPI automatic logging
- Frontend: Console logging for errors
- Agent: Configurable log levels

## 🚀 Production Deployment

### Environment Variables
```bash
# Backend
DATABASE_URL=sqlite:///app/data/decisions.db
CORS_ORIGINS=https://yourdomain.com

# Frontend  
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NODE_ENV=production
```

### Production Profile
```bash
docker-compose --profile production up -d
```

This includes:
- Nginx reverse proxy
- SSL termination (configure certificates)
- Production optimizations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the [Issues](../../issues) page
2. Review the API documentation at `/docs`
3. Check Docker logs: `docker-compose logs`

## 🔄 Updates

The platform is designed for easy updates:
- Backend: Update Python packages in `requirements.txt`
- Frontend: Update Node packages in `package.json`
- Agent: Modify `.kiro/decision_agent.yaml`
- Infrastructure: Update `docker-compose.yml`

---

**Built for AWS Builder Center** - Empowering technical teams to make better decisions through AI-powered analysis.
=======
# decision-intelligence-platform
>>>>>>> 018f462924f5c88daddadbe13eb658b5282f5ecb
