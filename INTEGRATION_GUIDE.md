## 🧠 HR Intelligence Brain - Integration Guide

### 🚀 **Plug-and-Play Integration for Shashank's HR Platform**

The system now includes an active **Reinforcement Learning (RL) Brain** that learns from HR feedback.

### **Quick Integration (Standard)**

```python
# 1. Import HR Intelligence Brain
from hr_intelligence_brain import create_hr_brain_for_shashank

# 2. Initialize for Shashank's platform
hr_brain = create_hr_brain_for_shashank("https://shashank-platform.com/api")

# 3. Start using AI features
result = hr_brain.process_shashank_candidate(candidate_data)
# returns "success_probability" based on real-time RL weights
```

## 📡 **API Endpoints (New RL Features)**

### **Reinforcement Learning Core**
```bash
# 1. DECIDE: Get AI Decision with RL Probability
POST /ai/decide
{
  "candidate_data": {
    "name": "Jane Doe",
    "skills": ["Python", "FastAPI", "RL"]
  }
}
# Response:
# {
#   "decision": "recommend_hire",
#   "success_probability": 0.85,
#   "confidence": 0.9,
#   "rl_factors_used": ["python", "rl"]
# }

# 2. FEEDBACK: Close the Loop (Train the Brain)
POST /ai/feedback
{
  "candidate_data": { ... },
  "feedback_score": 5.0,  # 1-5 Scale
  "outcome": "hired"      # hired/rejected
}
# Result: Brain updates weights immediately. next /decide will be smarter.

# 3. INSPECT: See the Brain State
GET /ai/rl-state
# Returns current weights and learning rate
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

### **Method 2: Python SDK (Recommended)**
```python
from hr_intelligence_brain import HRIntelligenceBrain

# Initialize
brain = HRIntelligenceBrain("http://localhost:5000")

# Use AI features
prob = brain.predict_success(candidate_data)

# Log Reward
brain.reward_log(candidate_data, 5.0, "hired")
```

## 🛠️ **Setup Instructions (Production)**

### **1. One-Click Startup (Recommended)**
```bash
# Windows
run_production.bat

# Linux/Mac
python start_enhanced_system.py
```
This starts both the **FastAPI Backend (Port 5000)** and **Streamlit Dashboard (Port 8501)**.

### **2. Docker Deployment**
```bash
docker build -t hr-ai-system .
docker run -p 5000:5000 -p 8501:8501 hr-ai-system
```

## 📊 **Dashboard & Analytics**
Access the real-time AI dashboard to see the Brain in action:
*   URL: http://localhost:8501
*   **RL Performance Chart**: Watch cumulative rewards grow.
*   **Active Brain State**: See which skills the AI currently values.

## 🤝 **Support & Integration Help**

- **API Documentation**: http://localhost:5000/docs
- **Health Check**: http://localhost:5000/health
- **RL History**: http://localhost:5000/ai/rl-history

**The HR Intelligence Brain is ready. Just Plug, Play, and Train!** 🧠⚡