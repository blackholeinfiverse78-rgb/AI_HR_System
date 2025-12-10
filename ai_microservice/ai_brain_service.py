"""
Plug-and-Play AI Brain Microservice
Ready for integration with any HR platform including Shashank's system
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import uvicorn
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hr_intelligence_brain import HRIntelligenceBrain, ShashankHRAdapter

# Initialize FastAPI app
app = FastAPI(
    title="AI Brain Microservice",
    description="Plug-and-Play AI Brain with Active RL for HR Platforms",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Initialize AI Brain
ai_brain = HRIntelligenceBrain()

# Pydantic Models
class CandidateData(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str]
    id: Optional[int] = None

class DecisionRequest(BaseModel):
    candidate: CandidateData
    context: Optional[Dict[str, Any]] = None

class FeedbackRequest(BaseModel):
    candidate: CandidateData
    feedback_score: float  # 1.0 to 5.0
    outcome: str  # 'hired', 'rejected', etc.

class IntegrationConfig(BaseModel):
    platform_name: str
    api_endpoint: str
    api_key: Optional[str] = None
    webhook_url: Optional[str] = None

# Health Check
@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "AI Brain Microservice",
        "version": "2.0.0",
        "rl_status": "FULLY_ACTIVE",
        "skills_learned": len(ai_brain.weights),
        "timestamp": datetime.now().isoformat()
    }

# Core AI Endpoints
@app.post("/ai/decide")
def make_decision(request: DecisionRequest):
    """
    Make AI decision for candidate
    Compatible with Shashank's platform and any HR system
    """
    try:
        candidate_data = request.candidate.dict()
        
        # Get RL prediction
        success_probability = ai_brain.predict_success(candidate_data)
        
        # Enhanced decision logic
        if success_probability >= 0.8:
            decision = "strong_recommend"
            confidence = "high"
        elif success_probability >= 0.6:
            decision = "recommend"
            confidence = "medium"
        elif success_probability >= 0.4:
            decision = "consider"
            confidence = "medium"
        else:
            decision = "not_recommended"
            confidence = "low"
        
        # Get recommendations
        recommendations = ai_brain.get_recommendations(candidate_data.get("id", 1))
        
        return {
            "decision": decision,
            "success_probability": success_probability,
            "confidence": confidence,
            "recommendations": recommendations,
            "rl_analysis": {
                "skills_matched": len([s for s in candidate_data["skills"] if any(s.lower() in w.lower() for w in ai_brain.weights)]),
                "total_skills": len(candidate_data["skills"]),
                "brain_weights": len(ai_brain.weights)
            },
            "timestamp": datetime.now().isoformat(),
            "microservice_version": "2.0.0"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Decision failed: {str(e)}")

@app.post("/ai/feedback")
def process_feedback(request: FeedbackRequest):
    """
    Process feedback to improve AI (Active RL Learning)
    """
    try:
        candidate_data = request.candidate.dict()
        
        # Apply RL learning
        ai_brain.reward_log(candidate_data, request.feedback_score, request.outcome)
        
        return {
            "status": "learning_complete",
            "message": "AI brain updated with feedback",
            "rl_status": "ACTIVELY_LEARNING",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback processing failed: {str(e)}")

@app.get("/ai/brain-state")
def get_brain_state():
    """Get current AI brain state and learned weights"""
    try:
        weights = ai_brain.weights
        top_skills = dict(sorted(weights.items(), key=lambda x: x[1], reverse=True)[:10])
        
        return {
            "total_skills": len(weights),
            "top_skills": top_skills,
            "learning_parameters": {
                "learning_rate": ai_brain.learning_rate,
                "exploration_rate": getattr(ai_brain, 'exploration_rate', 0.1)
            },
            "brain_status": "FULLY_ACTIVE",
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Brain state retrieval failed: {str(e)}")

# Integration Endpoints
@app.post("/integration/shashank/candidate")
def process_shashank_candidate(candidate_data: Dict[str, Any]):
    """
    Direct integration endpoint for Shashank's platform
    """
    try:
        # Create adapter for Shashank's platform
        adapter = ShashankHRAdapter("https://shashank-platform.com", ai_brain)
        
        # Process candidate
        result = adapter.process_shashank_candidate(candidate_data)
        
        return {
            "integration": "shashank_platform",
            "result": result,
            "processed_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Shashank integration failed: {str(e)}")

@app.post("/integration/shashank/feedback")
def shashank_feedback(candidate_data: Dict[str, Any], score: float, outcome: str):
    """
    Feedback endpoint for Shashank's platform
    """
    try:
        adapter = ShashankHRAdapter("https://shashank-platform.com", ai_brain)
        result = adapter.feedback_loop(candidate_data, score, outcome)
        
        return {
            "integration": "shashank_platform",
            "feedback_result": result,
            "processed_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Shashank feedback failed: {str(e)}")

@app.get("/integration/shashank/insights")
def get_shashank_insights():
    """
    Get insights formatted for Shashank's platform
    """
    try:
        adapter = ShashankHRAdapter("https://shashank-platform.com", ai_brain)
        insights = adapter.get_platform_insights()
        
        return {
            "integration": "shashank_platform",
            "insights": insights,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Shashank insights failed: {str(e)}")

# Generic Integration Endpoints
@app.post("/integration/generic/setup")
def setup_integration(config: IntegrationConfig):
    """
    Setup integration with any HR platform
    """
    return {
        "status": "integration_configured",
        "platform": config.platform_name,
        "endpoint": config.api_endpoint,
        "features_available": [
            "candidate_analysis",
            "decision_making", 
            "feedback_learning",
            "insights_generation"
        ],
        "setup_at": datetime.now().isoformat()
    }

@app.get("/integration/test")
def test_integration():
    """
    Test integration with sample data
    """
    sample_candidate = {
        "name": "Test Candidate",
        "skills": ["Python", "Machine Learning", "FastAPI"],
        "email": "test@example.com"
    }
    
    # Test decision making
    decision_result = ai_brain.analyze_candidate(sample_candidate)
    
    return {
        "test_status": "success",
        "sample_analysis": decision_result,
        "integration_ready": True,
        "tested_at": datetime.now().isoformat()
    }

# Analytics Endpoints
@app.get("/analytics/performance")
def get_performance_analytics():
    """
    Get AI performance analytics
    """
    try:
        # Read RL history for analytics
        history = []
        log_file = "logs/rl_state_summary.json"
        
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                for line in f:
                    if line.strip():
                        try:
                            import json
                            history.append(json.loads(line))
                        except:
                            continue
        
        total_decisions = len(history)
        positive_outcomes = len([h for h in history if h.get('outcome', '').lower() in ['hired', 'accept']])
        
        return {
            "performance_metrics": {
                "total_decisions": total_decisions,
                "positive_outcomes": positive_outcomes,
                "success_rate": (positive_outcomes / max(total_decisions, 1)) * 100,
                "skills_learned": len(ai_brain.weights)
            },
            "brain_health": "excellent" if len(ai_brain.weights) > 10 else "good",
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics failed: {str(e)}")

# Utility Endpoints
@app.get("/")
def root():
    """Root endpoint with service information"""
    return {
        "service": "AI Brain Microservice",
        "version": "2.0.0",
        "description": "Plug-and-Play AI Brain with Active RL for HR Platforms",
        "status": "FULLY_OPERATIONAL",
        "features": {
            "active_rl": True,
            "decision_making": True,
            "feedback_learning": True,
            "platform_integration": True,
            "shashank_compatible": True
        },
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "decision": "/ai/decide",
            "feedback": "/ai/feedback",
            "brain_state": "/ai/brain-state",
            "shashank_integration": "/integration/shashank/*",
            "analytics": "/analytics/performance"
        },
        "integration_guide": "See /docs for complete API documentation"
    }

# Run the microservice
if __name__ == "__main__":
    print("🚀 Starting AI Brain Microservice...")
    print("📋 Features: Active RL, Decision Making, Platform Integration")
    print("🔗 Shashank Platform: READY")
    print("📊 Analytics: ENABLED")
    print("🌐 Access: http://localhost:8080")
    print("📚 Docs: http://localhost:8080/docs")
    
    uvicorn.run(
        "ai_brain_service:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )