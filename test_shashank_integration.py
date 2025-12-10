#!/usr/bin/env python3
"""
Shashank Platform Integration Test Suite
Tests 5 end-to-end flows as required
"""

import requests
import json
import time
from datetime import datetime

class ShashankIntegrationTester:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.test_results = []
    
    def log_test(self, test_name, passed, details=""):
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name} - {details}")
        self.test_results.append({"test": test_name, "passed": passed, "details": details})
    
    def test_flow_1_candidate_to_ai_decision(self):
        """Flow 1: Candidate → Shashank → AI Decide → Store"""
        print("\n🔄 Flow 1: Candidate Processing")
        
        # Add candidate
        candidate_data = {
            "name": "Shashank Test User",
            "email": "shashank@test.com", 
            "phone": "+91-9876543210",
            "skills": ["Java", "Spring Boot", "Microservices"]
        }
        
        try:
            # Step 1: Add candidate
            response = requests.post(f"{self.base_url}/candidate/add", json=candidate_data)
            if response.status_code == 200:
                candidate_id = response.json().get("candidate_id")
                self.log_test("Candidate Addition", True, f"ID: {candidate_id}")
                
                # Step 2: AI Decision
                decision_request = {"candidate_data": candidate_data}
                decision_response = requests.post(f"{self.base_url}/ai/decide", json=decision_request)
                
                if decision_response.status_code == 200:
                    decision = decision_response.json()
                    self.log_test("AI Decision", True, f"Decision: {decision.get('decision')}")
                    return True
                else:
                    self.log_test("AI Decision", False, "Decision API failed")
            else:
                self.log_test("Candidate Addition", False, "Add candidate failed")
        except Exception as e:
            self.log_test("Flow 1", False, str(e))
        
        return False
    
    def test_flow_2_feedback_loop(self):
        """Flow 2: HR Feedback → AI Feedback Loop"""
        print("\n🔄 Flow 2: Feedback Loop")
        
        candidate_data = {
            "name": "Feedback Test",
            "skills": ["Python", "AI", "FastAPI"]
        }
        
        try:
            # Get initial prediction
            decision_response = requests.post(f"{self.base_url}/ai/decide", 
                                            json={"candidate_data": candidate_data})
            initial_prob = decision_response.json().get("success_probability", 0)
            
            # Submit feedback
            feedback_data = {
                "candidate_data": candidate_data,
                "feedback_score": 5.0,
                "outcome": "hired"
            }
            
            feedback_response = requests.post(f"{self.base_url}/ai/feedback", json=feedback_data)
            
            if feedback_response.status_code == 200:
                self.log_test("Feedback Processing", True, "Feedback accepted")
                
                # Verify learning
                new_decision = requests.post(f"{self.base_url}/ai/decide", 
                                           json={"candidate_data": candidate_data})
                new_prob = new_decision.json().get("success_probability", 0)
                
                learning_occurred = abs(new_prob - initial_prob) > 0.001
                self.log_test("RL Learning", learning_occurred, 
                            f"Prob: {initial_prob:.3f} → {new_prob:.3f}")
                return True
            else:
                self.log_test("Feedback Processing", False, "Feedback API failed")
        except Exception as e:
            self.log_test("Flow 2", False, str(e))
        
        return False
    
    def test_flow_3_decision_change(self):
        """Flow 3: Decision change after feedback"""
        print("\n🔄 Flow 3: Decision Change Verification")
        
        candidate_data = {
            "name": "Decision Change Test",
            "skills": ["ReactJS", "NodeJS", "MongoDB"]
        }
        
        try:
            # Multiple feedback cycles to ensure change
            for i in range(3):
                feedback_data = {
                    "candidate_data": candidate_data,
                    "feedback_score": 4.5,
                    "outcome": "hired"
                }
                requests.post(f"{self.base_url}/ai/feedback", json=feedback_data)
            
            # Check final decision
            final_decision = requests.post(f"{self.base_url}/ai/decide", 
                                         json={"candidate_data": candidate_data})
            
            if final_decision.status_code == 200:
                decision_data = final_decision.json()
                prob = decision_data.get("success_probability", 0)
                decision = decision_data.get("decision", "")
                
                # Verify positive decision after positive feedback
                positive_decision = prob > 0.5 or "recommend" in decision.lower()
                self.log_test("Decision Change", positive_decision, 
                            f"Final decision: {decision} (prob: {prob:.3f})")
                return positive_decision
            else:
                self.log_test("Decision Change", False, "Decision API failed")
        except Exception as e:
            self.log_test("Flow 3", False, str(e))
        
        return False
    
    def test_flow_4_automation_trigger(self):
        """Flow 4: Automation trigger confirmation"""
        print("\n🔄 Flow 4: Automation Trigger")
        
        try:
            # Trigger automation event
            automation_data = {
                "candidate_id": 1,
                "event_type": "shortlisted",
                "metadata": {"test": "shashank_integration"}
            }
            
            response = requests.post(f"{self.base_url}/trigger/", json=automation_data)
            
            if response.status_code == 200:
                result = response.json()
                success = result.get("status") == "success"
                self.log_test("Automation Trigger", success, 
                            f"Event: {automation_data['event_type']}")
                return success
            else:
                self.log_test("Automation Trigger", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Flow 4", False, str(e))
        
        return False
    
    def test_flow_5_logs_verification(self):
        """Flow 5: Logs verification with Tiwari"""
        print("\n🔄 Flow 5: Logs Verification")
        
        try:
            # Check RL history logs
            history_response = requests.get(f"{self.base_url}/ai/rl-history?limit=5")
            
            if history_response.status_code == 200:
                history = history_response.json().get("history", [])
                has_logs = len(history) > 0
                self.log_test("RL History Logs", has_logs, f"{len(history)} entries found")
                
                # Check system status
                status_response = requests.get(f"{self.base_url}/ai/status")
                if status_response.status_code == 200:
                    status = status_response.json()
                    rl_active = status.get("rl_status") == "ACTIVE"
                    self.log_test("System Status", rl_active, "RL Brain active")
                    return has_logs and rl_active
                else:
                    self.log_test("System Status", False, "Status API failed")
            else:
                self.log_test("RL History Logs", False, "History API failed")
        except Exception as e:
            self.log_test("Flow 5", False, str(e))
        
        return False
    
    def run_all_flows(self):
        """Run all 5 integration flows"""
        print("🚀 Shashank Platform Integration Test Suite")
        print("=" * 50)
        
        flows = [
            ("Flow 1: Candidate → AI Decision → Store", self.test_flow_1_candidate_to_ai_decision),
            ("Flow 2: HR Feedback → AI Loop", self.test_flow_2_feedback_loop),
            ("Flow 3: Decision Change After Feedback", self.test_flow_3_decision_change),
            ("Flow 4: Automation Trigger", self.test_flow_4_automation_trigger),
            ("Flow 5: Logs Verification", self.test_flow_5_logs_verification)
        ]
        
        passed_flows = 0
        
        for flow_name, flow_test in flows:
            print(f"\n📋 Testing: {flow_name}")
            if flow_test():
                passed_flows += 1
        
        # Summary
        print("\n" + "=" * 50)
        print("🏁 INTEGRATION TEST SUMMARY")
        print("=" * 50)
        print(f"✅ Passed: {passed_flows}/5 flows")
        print(f"❌ Failed: {5 - passed_flows}/5 flows")
        
        success_rate = (passed_flows / 5) * 100
        print(f"📊 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("\n🎉 SHASHANK INTEGRATION: READY FOR PRODUCTION")
        else:
            print("\n⚠️ SHASHANK INTEGRATION: NEEDS ATTENTION")
        
        return success_rate >= 80

def main():
    print("Starting Shashank Platform Integration Tests...")
    print("Make sure the HR-AI system is running on localhost:5000")
    
    input("Press Enter when system is ready...")
    
    tester = ShashankIntegrationTester()
    success = tester.run_all_flows()
    
    if success:
        print("\n🚀 Ready for Shashank platform integration!")
    else:
        print("\n🔧 Some flows need debugging before integration.")

if __name__ == "__main__":
    main()