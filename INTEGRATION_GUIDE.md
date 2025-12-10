# 🧠 HR Intelligence Brain - Integration Guide

## 🚀 **Plug-and-Play Integration for Shashank's HR Platform**

The system includes an **ACTIVE Reinforcement Learning (RL) Brain** that learns from HR feedback in real-time.

## 📡 **Core API Endpoints**

### **1. AI Decision Making**
```bash
POST /ai/decide
{
  "candidate_data": {
    "name": "Jane Doe",
    "skills": ["Python", "FastAPI", "RL"]
  }
}

# Response:
{
  "decision": "recommend_hire",
  "success_probability": 0.85,
  "confidence": 0.9,
  "rl_status": "FULLY_ACTIVE"
}
```

### **2. Feedback Loop (Critical for Learning)**
```bash
POST /ai/feedback
{
  "candidate_data": { ... },
  "feedback_score": 5.0,
  "outcome": "hired"
}

# Result: Brain updates weights immediately
```

### **3. RL Analytics**
```bash
GET /ai/rl-state        # Current brain weights
GET /ai/rl-analytics    # Learning performance
GET /ai/rl-history      # Feedback history
GET /ai/status          # System status
```

## 🔌 **Integration Methods**

### **Method 1: Direct API Integration**
```python
import requests

# Get Decision
response = requests.post("http://localhost:5000/ai/decide", 
                        json={"candidate_data": candidate_data})
decision = response.json()

# Send Feedback (Critical for Learning)
requests.post("http://localhost:5000/ai/feedback", 
              json={
                  "candidate_data": candidate_data,
                  "feedback_score": 5, 
                  "outcome": "hired"
              })
```

### **Method 2: Python SDK**
```python
from hr_intelligence_brain import HRIntelligenceBrain

brain = HRIntelligenceBrain()
prob = brain.predict_success(candidate_data)
brain.reward_log(candidate_data, 5.0, "hired")
```

## 🛠️ **Setup Instructions**

### **Quick Start**
```bash
# Windows
run_production.bat

# Linux/Mac
chmod +x run_production.sh
./run_production.sh

# Docker
docker build -t hr-ai-system .
docker run -p 5000:5000 -p 8501:8501 hr-ai-system
```

### **Verification**
```bash
# Test integration
python test_shashank_integration.py

# Check system health
curl http://localhost:5000/health

# Verify RL is active
curl http://localhost:5000/ai/status
```

## 📊 **Dashboard Access**
- **URL**: http://localhost:8501
- **RL Analytics**: Real-time learning visualization
- **Performance Metrics**: Success rates, learning trends

## 🔄 **5 Integration Flows (Tested)**

1. **Candidate → AI Decision → Store**
2. **HR Feedback → AI Learning Loop**
3. **Decision Change After Feedback**
4. **Automation Trigger Confirmation**
5. **Logs Verification**

## 🤝 **Shashank Platform Adapter**

```python
from hr_intelligence_brain import create_hr_brain_for_shashank

# Initialize for Shashank's platform
adapter = create_hr_brain_for_shashank("https://shashank-platform.com/api")

# Process candidate
result = adapter.process_shashank_candidate(candidate_data)

# Feedback loop
adapter.feedback_loop(candidate_data, score, outcome)
```

## 📞 **Support**
- **API Docs**: http://localhost:5000/docs
- **Health Check**: http://localhost:5000/health
- **Integration Tests**: `python test_shashank_integration.py`

**🧠 The RL Brain is FULLY ACTIVE and ready for production integration!**