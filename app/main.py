from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import CandidateCreate, FeedbackCreate, AutomationTrigger
from app.agents.email_agent import send_email
from app.agents.whatsapp_agent import send_whatsapp
from app.agents.voice_agent import trigger_voice_call
from app.utils.helpers import load_json, save_json
from app.utils.data_validator import ensure_data_integrity
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize data validation on startup
try:
    validation_result = ensure_data_integrity()
    logger.info(f"Data validation completed: {validation_result}")
except Exception as e:
    logger.error(f"Data validation failed: {e}")
    raise

app = FastAPI(
    title="HR-AI System", 
    version="1.0.0", 
    description="AI-powered HR automation with multi-channel communication"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "HR-AI System Running", 
        "status": "active",
        "communication_channels": ["email", "whatsapp", "voice"]
    }

@app.get("/health")
def health():
    try:
        from app.utils.data_validator import DataValidator
        system_status = DataValidator.get_system_status()
        
        return {
            "status": "healthy", 
            "timestamp": datetime.now().isoformat(),
            "data_files": system_status["data_files"],
            "directories": system_status["directories"],
            "permissions": system_status["permissions"],
            "pipelines": {
                "email": "active",
                "whatsapp": "active", 
                "voice": "active"
            }
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"System health check failed: {str(e)}")

@app.get("/system/status")
def system_status():
    """Get detailed system status and diagnostics"""
    try:
        from app.utils.data_validator import DataValidator
        status = DataValidator.get_system_status()
        
        # Add file counts
        candidates = load_json("data/candidates.json")
        feedback_logs = load_json("feedback/feedback_log.csv")
        
        status["statistics"] = {
            "total_candidates": len(candidates) if isinstance(candidates, list) else 0,
            "total_feedback_logs": len(feedback_logs) if isinstance(feedback_logs, list) else 0,
            "system_uptime": datetime.now().isoformat()
        }
        
        return status
    except Exception as e:
        logger.error(f"System status check failed: {e}")
        raise HTTPException(status_code=500, detail=f"System status unavailable: {str(e)}")

# Candidate endpoints
@app.post("/candidate/add")
def add_candidate(candidate: CandidateCreate):
    try:
        candidates = load_json("data/candidates.json")
        if not isinstance(candidates, list):
            candidates = []
        
        candidate_id = max([c.get("id", 0) for c in candidates], default=0) + 1
        candidate_dict = candidate.dict()
        candidate_dict["id"] = candidate_id
        candidate_dict["match_score"] = 0.0
        
        candidates.append(candidate_dict)
        save_json("data/candidates.json", candidates)
        
        return {"status": "success", "candidate_id": candidate_id, "message": "Candidate added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/candidate/list")
def list_candidates():
    candidates = load_json("data/candidates.json")
    return candidates if isinstance(candidates, list) else []

@app.get("/candidate/{candidate_id}")
def get_candidate(candidate_id: int):
    candidates = load_json("data/candidates.json")
    if not isinstance(candidates, list):
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    candidate = next((c for c in candidates if c.get("id") == candidate_id), None)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate

# Feedback endpoints
@app.post("/feedback/hr_feedback")
def submit_feedback(feedback: FeedbackCreate):
    try:
        import csv
        import os
        
        # Validate candidate exists
        candidates = load_json("data/candidates.json")
        if not isinstance(candidates, list):
            raise HTTPException(status_code=400, detail="Invalid candidates data")
        
        candidate = next((c for c in candidates if c.get("id") == feedback.candidate_id), None)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        timestamp = datetime.now().isoformat()
        
        # Log to CSV file
        csv_file = "feedback/feedback_log.csv"
        file_exists = os.path.exists(csv_file)
        
        try:
            with open(csv_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["timestamp", "candidate_id", "score", "comment", "outcome", "event"])
                writer.writerow([timestamp, feedback.candidate_id, feedback.feedback_score, 
                               feedback.comment, feedback.actual_outcome, "feedback_processed"])
        except Exception as csv_error:
            logger.error(f"CSV logging failed: {csv_error}")
            # Continue with JSON logging as fallback
        
        # Also log to JSON for backward compatibility
        log_entry = {
            "timestamp": timestamp,
            "candidate_id": feedback.candidate_id,
            "score": feedback.feedback_score,
            "comment": feedback.comment,
            "outcome": feedback.actual_outcome,
            "event": "feedback_processed"
        }
        
        # Log to system log
        system_logs = load_json("feedback/system_log.json")
        if not isinstance(system_logs, list):
            system_logs = []
        
        system_logs.append({
            "timestamp": timestamp,
            "event": "feedback_processed",
            "details": log_entry
        })
        save_json("feedback/system_log.json", system_logs)
        
        return {
            "status": "success", 
            "message": "Feedback submitted successfully",
            "feedback_id": len(system_logs),
            "timestamp": timestamp
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Feedback submission failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to submit feedback: {str(e)}")

@app.get("/feedback/logs")
def get_feedback_logs():
    try:
        import csv
        logs = []
        
        # Try to read from CSV file first
        csv_file = "feedback/feedback_log.csv"
        if os.path.exists(csv_file):
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                logs = list(reader)
        
        # Fallback to JSON file
        if not logs:
            json_logs = load_json("feedback/system_log.json")
            if isinstance(json_logs, list):
                logs = [log.get("details", {}) for log in json_logs if log.get("event") == "feedback_processed"]
        
        return logs
    except Exception as e:
        logger.error(f"Failed to load feedback logs: {e}")
        return []

# Multi-channel automation endpoints
@app.post("/trigger/")
def trigger_automation(trigger: AutomationTrigger):
    candidates = load_json("data/candidates.json")
    if not isinstance(candidates, list):
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    candidate = next((c for c in candidates if c.get("id") == trigger.candidate_id), None)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    results = []
    
    try:
        if trigger.event_type == "shortlisted":
            email_result = send_email(trigger.candidate_id, "shortlisted", 
                                    trigger.metadata.get("override_email"))
            whatsapp_result = send_whatsapp(trigger.candidate_id, "shortlisted", 
                                          trigger.metadata.get("override_phone"))
            results.extend([email_result, whatsapp_result])
            
        elif trigger.event_type == "rejected":
            email_result = send_email(trigger.candidate_id, "rejected", 
                                    trigger.metadata.get("override_email"))
            whatsapp_result = send_whatsapp(trigger.candidate_id, "rejected", 
                                          trigger.metadata.get("override_phone"))
            results.extend([email_result, whatsapp_result])
            
        elif trigger.event_type == "interview_scheduled":
            email_result = send_email(trigger.candidate_id, "interview", 
                                    trigger.metadata.get("override_email"))
            whatsapp_result = send_whatsapp(trigger.candidate_id, "interview", 
                                          trigger.metadata.get("override_phone"))
            voice_result = trigger_voice_call(trigger.candidate_id, "interview_reminder")
            results.extend([email_result, whatsapp_result, voice_result])
            
        elif trigger.event_type == "onboarding_completed":
            whatsapp_result = send_whatsapp(trigger.candidate_id, "onboarding", 
                                          trigger.metadata.get("override_phone"))
            voice_result = trigger_voice_call(trigger.candidate_id, "onboarding")
            results.extend([whatsapp_result, voice_result])
        
        return {
            "status": "success", 
            "event_type": trigger.event_type, 
            "results": results,
            "total_communications": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Automation failed: {str(e)}")

@app.get("/trigger/history/{candidate_id}")
def get_automation_history(candidate_id: int):
    return {"candidate_id": candidate_id, "automation_history": [], "message": "History feature simplified"}

# Individual channel endpoints for testing
@app.post("/communication/email")
def send_email_only(candidate_id: int, template: str = "shortlisted", override_email: str = None):
    result = send_email(candidate_id, template, override_email)
    return {"channel": "email", "result": result}

@app.post("/communication/whatsapp")
def send_whatsapp_only(candidate_id: int, message_type: str = "shortlisted", override_phone: str = None):
    result = send_whatsapp(candidate_id, message_type, override_phone)
    return {"channel": "whatsapp", "result": result}

@app.post("/communication/voice")
def trigger_voice_only(candidate_id: int, call_type: str = "onboarding"):
    result = trigger_voice_call(candidate_id, call_type)
    return {"channel": "voice", "result": result}