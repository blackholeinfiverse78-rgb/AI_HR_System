# AI Brain Microservice 🧠

**Plug-and-Play AI Brain with Active Reinforcement Learning**

Ready for integration with **Shashank's Platform** and any HR system.

## 🚀 Quick Start

### One-Command Install
```bash
python install.py
```

### Manual Install
```bash
pip install -r requirements.txt
python ai_brain_service.py
```

### Docker Install
```bash
docker-compose up --build
```

## 🌐 Access Points

- **Service**: http://localhost:8080
- **API Docs**: http://localhost:8080/docs
- **Health Check**: http://localhost:8080/health

## 🔗 Shashank Platform Integration

### Ready-to-Use Endpoints

#### 1. Process Candidate
```bash
POST /integration/shashank/candidate
{
  "full_name": "John Doe",
  "email_address": "john@example.com", 
  "phone_number": "+91-9876543210",
  "skills": ["Python", "AI", "Machine Learning"]
}
```

#### 2. Submit Feedback (RL Learning)
```bash
POST /integration/shashank/feedback?score=4.5&outcome=hired
{
  "full_name": "John Doe",
  "skills": ["Python", "AI"]
}
```

#### 3. Get Insights
```bash
GET /integration/shashank/insights
```

## 🧠 Active RL Features

### ✅ FULLY IMPLEMENTED
- **Real-time Learning**: Weights update with each feedback
- **Decision Making**: AI-powered candidate evaluation
- **Skill Discovery**: Automatically learns new important skills
- **Performance Analytics**: Track learning progress
- **Integration Ready**: Plug into any HR platform

### 📊 RL Analytics Available
- Reward evolution graphs
- Decision accuracy tracking
- Learning velocity metrics
- Skill importance weights

## 🔧 Core API Endpoints

### Decision Making
```bash
POST /ai/decide
{
  "candidate": {
    "name": "John Doe",
    "skills": ["Python", "FastAPI"],
    "email": "john@example.com"
  }
}
```

**Response:**
```json
{
  "decision": "recommend",
  "success_probability": 0.75,
  "confidence": "high",
  "recommendations": ["Strong Python skills", "Good API experience"],
  "rl_analysis": {
    "skills_matched": 2,
    "total_skills": 2,
    "brain_weights": 15
  }
}
```

### Feedback Processing (RL Learning)
```bash
POST /ai/feedback
{
  "candidate": {
    "name": "John Doe", 
    "skills": ["Python", "FastAPI"]
  },
  "feedback_score": 4.5,
  "outcome": "hired"
}
```

### Brain State
```bash
GET /ai/brain-state
```

**Response:**
```json
{
  "total_skills": 15,
  "top_skills": {
    "python": 1.45,
    "ai": 1.32,
    "machine learning": 1.28
  },
  "brain_status": "FULLY_ACTIVE"
}
```

## 🐳 Docker Deployment

### Build and Run
```bash
docker-compose up --build
```

### Production Deployment
```bash
docker-compose -f docker-compose.yml up -d
```

## 🧪 Testing Integration

### Test Endpoint
```bash
GET /integration/test
```

### Health Check
```bash
GET /health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "rl_status": "FULLY_ACTIVE",
  "skills_learned": 15,
  "service": "AI Brain Microservice"
}
```

## 📈 Performance Monitoring

### Analytics Endpoint
```bash
GET /analytics/performance
```

### Real-time Metrics
- Total decisions made
- Success rate percentage  
- Skills learned count
- Brain health status

## 🔧 Configuration

### Environment Variables
```bash
# Optional - defaults work out of the box
AI_BRAIN_PORT=8080
AI_BRAIN_HOST=0.0.0.0
RL_LEARNING_RATE=0.15
```

### Integration Settings
- **Platform Name**: Configure in `/integration/generic/setup`
- **API Keys**: Optional for enhanced security
- **Webhooks**: For real-time notifications

## 🚀 Production Ready Features

### ✅ Implemented
- **Active RL Learning**: Real-time weight updates
- **Decision API**: Fast candidate evaluation
- **Analytics**: Performance tracking
- **Health Monitoring**: Service status checks
- **Docker Support**: Container deployment
- **API Documentation**: Auto-generated docs

### 🔒 Security
- Input validation with Pydantic
- Error handling and logging
- Health checks and monitoring
- Optional API key authentication

## 📞 Integration Support

### For Shashank's Team
1. **Start Service**: `python ai_brain_service.py`
2. **Test Connection**: `curl http://localhost:8080/health`
3. **Check Docs**: Visit `http://localhost:8080/docs`
4. **Use Endpoints**: `/integration/shashank/*`

### Sample Integration Code
```python
import requests

# Initialize connection
base_url = "http://localhost:8080"

# Test health
health = requests.get(f"{base_url}/health").json()
print(f"RL Status: {health['rl_status']}")

# Process candidate
candidate = {
    "full_name": "Test User",
    "skills": ["Python", "AI"]
}
result = requests.post(f"{base_url}/integration/shashank/candidate", json=candidate)
print(f"Decision: {result.json()}")
```

## 🎯 Next Steps

1. **Start the microservice**
2. **Test with sample data**
3. **Integrate with your platform**
4. **Monitor RL learning progress**
5. **Scale as needed**

---

**Status**: ✅ PRODUCTION READY  
**RL Learning**: ✅ FULLY ACTIVE  
**Shashank Integration**: ✅ READY  
**Documentation**: ✅ COMPLETE