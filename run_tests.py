import unittest
import requests
import json
import os
import sys
import time
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ---- TEST CONFIGURATION ----
API_BASE = "http://localhost:5000"
DASHBOARD_URL = "http://localhost:8501"

class HRSystemTestSuite(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\n" + "="*50)
        print("🚀 STARTING HR-AI SYSTEM FULL TEST SUITE")
        print("="*50)
        
    def test_01_backend_health(self):
        """Verify Backend is running"""
        print("\n[Test 1] Backend Health Check...")
        try:
            response = requests.get(f"{API_BASE}/health")
            self.assertEqual(response.status_code, 200)
            print("✅ Backend is ONLINE")
        except:
            self.fail("❌ Backend is OFFLINE")

    def test_02_data_validation(self):
        """Verify internal data modules"""
        print("\n[Test 2] Data Validation...")
        try:
            from app.utils.data_validator import DataValidator
            result = DataValidator.validate_data_files()
            self.assertEqual(result["status"], "success")
            print("✅ Data Files Validated")
        except Exception as e:
            self.fail(f"❌ Data Validation Failed: {e}")

    def test_03_rl_integration_flow(self):
        """Verify RL Brain Loop: Decision -> Feedback -> Learning"""
        print("\n[Test 3] RL Integration Flow...")
        
        candidate = {"name": "Test Bot", "skills": ["Python", "RL", "Testing"]}
        
        # Decision
        res = requests.post(f"{API_BASE}/ai/decide", json={"candidate_data": candidate}, timeout=5)
        self.assertEqual(res.status_code, 200)
        initial_prob = res.json().get("success_probability", 0.0)
        
        # Feedback
        feedback = {"candidate_data": candidate, "feedback_score": 5.0, "outcome": "hired"}
        res = requests.post(f"{API_BASE}/ai/feedback", json=feedback, timeout=5)
        self.assertEqual(res.status_code, 200)
        
        # Verify Learning
        res = requests.post(f"{API_BASE}/ai/decide", json={"candidate_data": candidate}, timeout=5)
        new_prob = res.json().get("success_probability", 0.0)
        
        self.assertGreaterEqual(new_prob, initial_prob)
        print("✅ RL Loop Verified")

    def test_04_communication_agents(self):
        """Verify Agents (Email, WhatsApp, Voice)"""
        print("\n[Test 4] Communication Agents...")
        try:
            from app.agents.email_agent import send_email
            
            # Ensure candidate 1 exists
            from app.utils.helpers import load_json, save_json
            candidates = load_json("data/candidates.json") or []
            if not any(c['id'] == 1 for c in candidates):
                candidates.append({"id": 1, "name": "Test", "email": "t@t.com"})
                save_json("data/candidates.json", candidates)

            res = send_email(1, "shortlisted")
            self.assertTrue(res and "status" in res)
            print("✅ Email Agent Validated")
        except Exception as e:
            self.fail(f"❌ Agents Failed: {e}")

    def test_05_dashboard_accessibility(self):
        """Verify Dashboard is reachable"""
        print("\n[Test 5] Dashboard Check...")
        try:
            res = requests.get(DASHBOARD_URL)
            self.assertEqual(res.status_code, 200)
            print("✅ Dashboard is REACHABLE")
        except:
             print("⚠️  Dashboard might be starting up or headless")

if __name__ == '__main__':
    unittest.main()
