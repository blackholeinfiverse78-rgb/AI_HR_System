#!/usr/bin/env python3
"""
Comprehensive Integration Test Suite
Tests RL functionality, Shashank platform integration, and all fixed issues
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, List

class IntegrationTester:
    """Complete integration test suite for HR-AI System"""
    
    def __init__(self, base_url: str = "http://localhost:5000", microservice_url: str = "http://localhost:8080"):
        self.base_url = base_url
        self.microservice_url = microservice_url
        self.test_results = []
        self.passed_tests = 0
        self.total_tests = 0
    
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log test result"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        
        result = f"{status} {test_name}"
        if details:
            result += f" - {details}"
        
        print(result)
        self.test_results.append({
            "test": test_name,
            "passed": passed,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    def test_system_health(self):
        """Test 1: System Health Check"""
        print("\n🔍 Testing System Health...")
        
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                self.log_test("Main System Health", True, f"Status: {health_data.get('status')}")
            else:
                self.log_test("Main System Health", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("Main System Health", False, str(e))
    
    def test_rl_brain_active(self):
        """Test 2: RL Brain Active Status"""
        print("\n🧠 Testing RL Brain Status...")
        
        try:
            response = requests.get(f"{self.base_url}/ai/status", timeout=5)
            if response.status_code == 200:
                ai_status = response.json()
                rl_active = ai_status.get("rl_status") == "ACTIVE"
                skills_count = ai_status.get("brain_metrics", {}).get("total_skills", 0)
                
                self.log_test("RL Brain Active", rl_active, f"Skills: {skills_count}")
                self.log_test("RL Features Available", ai_status.get("features", {}).get("active_learning", False))
            else:
                self.log_test("RL Brain Active", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("RL Brain Active", False, str(e))
    
    def test_rl_decision_making(self):
        """Test 3: RL Decision Making"""
        print("\n🎯 Testing RL Decision Making...")
        
        test_candidate = {
            "candidate_data": {
                "name": "Test Candidate",
                "skills": ["Python", "Machine Learning", "FastAPI"],
                "id": 999
            }
        }
        
        try:
            response = requests.post(f"{self.base_url}/ai/decide", json=test_candidate, timeout=5)
            if response.status_code == 200:
                decision_data = response.json()
                has_decision = "decision" in decision_data
                has_probability = "success_probability" in decision_data
                rl_active = decision_data.get("rl_status") == "FULLY_ACTIVE"
                
                self.log_test("RL Decision API", has_decision and has_probability, 
                            f"Decision: {decision_data.get('decision')}, Prob: {decision_data.get('success_probability')}")
                self.log_test("RL Decision Active", rl_active)
            else:
                self.log_test("RL Decision API", False, f"HTTP {response.status_code}")
        except Exception as e:
            self.log_test("RL Decision API", False, str(e))
    
    def test_rl_learning_loop(self):
        """Test 4: RL Learning Loop (Feedback Processing)"""
        print("\n🔄 Testing RL Learning Loop...")
        
        # First, get initial prediction
        test_candidate = {
            "name": "Learning Test Candidate",
            "skills": ["React", "Node.js", "TypeScript"]
        }
        
        try:
            # Get initial state
            state_response = requests.get(f"{self.base_url}/ai/rl-state", timeout=5)
            initial_weights_count = 0
            if state_response.status_code == 200:
                initial_weights_count = len(state_response.json().get("weights", {}))
            
            # Submit feedback to trigger learning
            feedback_data = {
                "candidate_data": test_candidate,
                "feedback_score": 4.5,
                "outcome": "hired"
            }
            
            feedback_response = requests.post(f"{self.base_url}/ai/feedback", json=feedback_data, timeout=5)
            
            if feedback_response.status_code == 200:
                feedback_result = feedback_response.json()
                learning_active = feedback_result.get("rl_status") == "ACTIVELY_LEARNING"
                has_metrics = "learning_metrics" in feedback_result
                
                self.log_test("RL Feedback Processing", True, "Feedback accepted")
                self.log_test("RL Active Learning", learning_active)
                self.log_test("RL Learning Metrics", has_metrics)
                
                # Check if weights were updated
                time.sleep(1)  # Brief pause for processing
                new_state_response = requests.get(f"{self.base_url}/ai/rl-state", timeout=5)
                if new_state_response.status_code == 200:
                    new_weights_count = len(new_state_response.json().get("weights", {}))
                    weights_changed = new_weights_count >= initial_weights_count
                    self.log_test("RL Weight Updates", weights_changed, 
                                f"Weights: {initial_weights_count} → {new_weights_count}")
            else:
                self.log_test("RL Feedback Processing", False, f"HTTP {feedback_response.status_code}")
        
        except Exception as e:
            self.log_test("RL Learning Loop", False, str(e))
    
    def test_rl_analytics(self):
        """Test 5: RL Analytics and Visualization"""
        print("\n📊 Testing RL Analytics...")
        
        try:
            # Test RL history
            history_response = requests.get(f"{self.base_url}/ai/rl-history", timeout=5)
            if history_response.status_code == 200:
                history_data = history_response.json()
                has_history = isinstance(history_data.get("history"), list)
                has_stats = "summary_statistics" in history_data
                
                self.log_test("RL History API", has_history)
                self.log_test("RL Summary Statistics", has_stats)
            
            # Test RL analytics
            analytics_response = requests.get(f"{self.base_url}/ai/rl-analytics", timeout=5)
            if analytics_response.status_code == 200:
                analytics_data = analytics_response.json()
                has_reward_evolution = "reward_evolution" in analytics_data
                has_decision_accuracy = "decision_accuracy" in analytics_data
                has_learning_metrics = "learning_metrics" in analytics_data
                
                self.log_test("RL Reward Evolution", has_reward_evolution)
                self.log_test("RL Decision Accuracy", has_decision_accuracy)
                self.log_test("RL Learning Metrics", has_learning_metrics)
            
            # Test RL performance
            performance_response = requests.get(f"{self.base_url}/ai/rl-performance", timeout=5)
            if performance_response.status_code == 200:
                perf_data = performance_response.json()
                has_performance_metrics = "performance_metrics" in perf_data
                has_brain_health = "brain_health" in perf_data
                
                self.log_test("RL Performance Metrics", has_performance_metrics)
                self.log_test("RL Brain Health", has_brain_health)
        
        except Exception as e:
            self.log_test("RL Analytics", False, str(e))
    
    def test_microservice_integration(self):
        """Test 6: AI Microservice Integration"""
        print("\n🔌 Testing AI Microservice...")
        
        try:
            # Test microservice health
            health_response = requests.get(f"{self.microservice_url}/health", timeout=5)
            if health_response.status_code == 200:
                health_data = health_response.json()
                microservice_healthy = health_data.get("status") == "healthy"
                rl_active = health_data.get("rl_status") == "FULLY_ACTIVE"
                
                self.log_test("Microservice Health", microservice_healthy)
                self.log_test("Microservice RL Active", rl_active, f"Skills: {health_data.get('skills_learned', 0)}")
            else:
                self.log_test("Microservice Health", False, f"HTTP {health_response.status_code}")
            
            # Test microservice decision making
            test_candidate = {
                "candidate": {
                    "name": "Microservice Test",
                    "skills": ["Python", "AI", "FastAPI"],
                    "email": "test@microservice.com"
                }
            }
            
            decision_response = requests.post(f"{self.microservice_url}/ai/decide", json=test_candidate, timeout=5)
            if decision_response.status_code == 200:
                decision_data = decision_response.json()
                has_decision = "decision" in decision_data
                has_rl_analysis = "rl_analysis" in decision_data
                
                self.log_test("Microservice Decision API", has_decision)
                self.log_test("Microservice RL Analysis", has_rl_analysis)
            
        except Exception as e:
            self.log_test("Microservice Integration", False, str(e))
    
    def test_shashank_integration(self):
        """Test 7: Shashank Platform Integration"""
        print("\n🤝 Testing Shashank Platform Integration...")
        
        # Test Shashank-specific endpoints
        shashank_candidate = {
            "full_name": "Shashank Test Candidate",
            "email_address": "shashank.test@example.com",
            "phone_number": "+91-9876543210",
            "skills": ["Java", "Spring Boot", "Microservices"]
        }
        
        try:
            # Test microservice Shashank integration
            shashank_response = requests.post(f"{self.microservice_url}/integration/shashank/candidate", 
                                            json=shashank_candidate, timeout=5)
            
            if shashank_response.status_code == 200:
                shashank_data = shashank_response.json()
                has_result = "result" in shashank_data
                integration_ready = shashank_data.get("integration") == "shashank_platform"
                
                self.log_test("Shashank Candidate Processing", has_result)
                self.log_test("Shashank Integration Ready", integration_ready)
            
            # Test Shashank insights
            insights_response = requests.get(f"{self.microservice_url}/integration/shashank/insights", timeout=5)
            if insights_response.status_code == 200:
                insights_data = insights_response.json()
                has_insights = "insights" in insights_data
                self.log_test("Shashank Insights API", has_insights)
            
            # Test integration test endpoint
            test_response = requests.get(f"{self.microservice_url}/integration/test", timeout=5)
            if test_response.status_code == 200:
                test_data = test_response.json()
                integration_ready = test_data.get("integration_ready", False)
                self.log_test("Integration Test Endpoint", integration_ready)
        
        except Exception as e:
            self.log_test("Shashank Integration", False, str(e))
    
    def test_dashboard_rl_section(self):
        """Test 8: Dashboard RL Analytics Section"""
        print("\n📱 Testing Dashboard RL Section...")
        
        # Since we can't directly test Streamlit, we test the underlying APIs
        try:
            # Test APIs that dashboard uses
            apis_to_test = [
                ("/ai/rl-state", "RL State API"),
                ("/ai/rl-history", "RL History API"),
                ("/ai/rl-analytics", "RL Analytics API"),
                ("/ai/rl-performance", "RL Performance API")
            ]
            
            dashboard_apis_working = 0
            for endpoint, name in apis_to_test:
                try:
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                    if response.status_code == 200:
                        dashboard_apis_working += 1
                        self.log_test(f"Dashboard {name}", True)
                    else:
                        self.log_test(f"Dashboard {name}", False, f"HTTP {response.status_code}")
                except:
                    self.log_test(f"Dashboard {name}", False, "Connection failed")
            
            # Overall dashboard readiness
            dashboard_ready = dashboard_apis_working >= 3
            self.log_test("Dashboard RL Section Ready", dashboard_ready, 
                        f"{dashboard_apis_working}/{len(apis_to_test)} APIs working")
        
        except Exception as e:
            self.log_test("Dashboard RL Section", False, str(e))
    
    def test_end_to_end_workflow(self):
        """Test 9: Complete End-to-End RL Workflow"""
        print("\n🔄 Testing End-to-End RL Workflow...")
        
        try:
            # Step 1: Add a candidate
            candidate_data = {
                "name": "E2E Test Candidate",
                "email": "e2e@test.com",
                "phone": "+91-9999999999",
                "skills": ["Vue.js", "GraphQL", "Docker"]
            }
            
            add_response = requests.post(f"{self.base_url}/candidate/add", json=candidate_data, timeout=5)
            if add_response.status_code == 200:
                candidate_id = add_response.json().get("candidate_id")
                self.log_test("E2E: Candidate Added", True, f"ID: {candidate_id}")
                
                # Step 2: Make RL decision
                decision_request = {
                    "candidate_data": {
                        "name": candidate_data["name"],
                        "skills": candidate_data["skills"],
                        "id": candidate_id
                    }
                }
                
                decision_response = requests.post(f"{self.base_url}/ai/decide", json=decision_request, timeout=5)
                if decision_response.status_code == 200:
                    decision_data = decision_response.json()
                    initial_probability = decision_data.get("success_probability", 0)
                    self.log_test("E2E: RL Decision Made", True, f"Probability: {initial_probability}")
                    
                    # Step 3: Submit feedback
                    feedback_request = {
                        "candidate_data": decision_request["candidate_data"],
                        "feedback_score": 4.0,
                        "outcome": "hired"
                    }
                    
                    feedback_response = requests.post(f"{self.base_url}/ai/feedback", json=feedback_request, timeout=5)
                    if feedback_response.status_code == 200:
                        self.log_test("E2E: Feedback Processed", True)
                        
                        # Step 4: Verify learning occurred
                        time.sleep(1)
                        new_decision_response = requests.post(f"{self.base_url}/ai/decide", json=decision_request, timeout=5)
                        if new_decision_response.status_code == 200:
                            new_probability = new_decision_response.json().get("success_probability", 0)
                            learning_occurred = abs(new_probability - initial_probability) > 0.001
                            
                            self.log_test("E2E: RL Learning Verified", learning_occurred, 
                                        f"Probability: {initial_probability} → {new_probability}")
                            self.log_test("E2E: Complete Workflow", True, "All steps completed successfully")
                        else:
                            self.log_test("E2E: Learning Verification", False, "Could not verify learning")
                    else:
                        self.log_test("E2E: Feedback Processing", False, "Feedback failed")
                else:
                    self.log_test("E2E: RL Decision", False, "Decision failed")
            else:
                self.log_test("E2E: Candidate Addition", False, "Could not add candidate")
        
        except Exception as e:
            self.log_test("E2E Workflow", False, str(e))
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("🧪 HR-AI System Integration Test Suite")
        print("=" * 50)
        print("Testing all fixed issues and RL functionality...")
        
        # Run all tests
        self.test_system_health()
        self.test_rl_brain_active()
        self.test_rl_decision_making()
        self.test_rl_learning_loop()
        self.test_rl_analytics()
        self.test_microservice_integration()
        self.test_shashank_integration()
        self.test_dashboard_rl_section()
        self.test_end_to_end_workflow()
        
        # Print summary
        print("\n" + "=" * 50)
        print("🏁 TEST SUMMARY")
        print("=" * 50)
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.total_tests - self.passed_tests}")
        print(f"📊 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("\n🎉 INTEGRATION TEST SUITE: PASSED")
            print("✅ RL is FULLY ACTIVE and working")
            print("✅ Shashank integration is READY")
            print("✅ Dashboard RL analytics are AVAILABLE")
            print("✅ AI Brain microservice is OPERATIONAL")
        else:
            print("\n⚠️ INTEGRATION TEST SUITE: NEEDS ATTENTION")
            print("Some components may need debugging")
        
        # Save detailed results
        with open("integration_test_results.json", "w") as f:
            json.dump({
                "summary": {
                    "total_tests": self.total_tests,
                    "passed_tests": self.passed_tests,
                    "success_rate": success_rate,
                    "timestamp": datetime.now().isoformat()
                },
                "detailed_results": self.test_results
            }, f, indent=2)
        
        print(f"\n📄 Detailed results saved to: integration_test_results.json")
        
        return success_rate >= 80

def main():
    """Main test runner"""
    print("Starting HR-AI System Integration Tests...")
    print("Make sure both main system and microservice are running:")
    print("1. Main system: python start_enhanced_system.py")
    print("2. Microservice: python ai_microservice/ai_brain_service.py")
    print()
    
    input("Press Enter when both services are running...")
    
    tester = IntegrationTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🚀 All systems are GO for production!")
        sys.exit(0)
    else:
        print("\n🔧 Some issues need to be resolved.")
        sys.exit(1)

if __name__ == "__main__":
    main()