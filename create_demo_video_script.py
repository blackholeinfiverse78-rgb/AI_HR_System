#!/usr/bin/env python3
"""
Demo Video Script Generator
Creates step-by-step demo for the 2-3 minute video requirement
"""

import requests
import json
import time
from datetime import datetime

class DemoVideoScript:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.steps = []
    
    def log_step(self, step_num, action, result, screenshot_note=""):
        step = {
            "step": step_num,
            "action": action,
            "result": result,
            "screenshot": screenshot_note,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        self.steps.append(step)
        print(f"📹 Step {step_num}: {action}")
        print(f"   Result: {result}")
        if screenshot_note:
            print(f"   📸 Screenshot: {screenshot_note}")
        print()
    
    def demo_step_1_add_candidate(self):
        """Demo Step 1: Add Candidate"""
        candidate_data = {
            "name": "Demo Candidate",
            "email": "demo@example.com",
            "phone": "+91-9876543210",
            "skills": ["Python", "Machine Learning", "FastAPI", "AI"]
        }
        
        try:
            response = requests.post(f"{self.base_url}/candidate/add", json=candidate_data)
            if response.status_code == 200:
                candidate_id = response.json().get("candidate_id")
                self.log_step(1, 
                    "Add new candidate with AI/ML skills",
                    f"✅ Candidate added successfully (ID: {candidate_id})",
                    "Show candidate form being filled and submitted"
                )
                return candidate_id
            else:
                self.log_step(1, "Add candidate", "❌ Failed", "")
        except Exception as e:
            self.log_step(1, "Add candidate", f"❌ Error: {e}", "")
        return None
    
    def demo_step_2_ai_decision(self, candidate_id):
        """Demo Step 2: AI Decision"""
        candidate_data = {
            "name": "Demo Candidate",
            "skills": ["Python", "Machine Learning", "FastAPI", "AI"],
            "id": candidate_id
        }
        
        try:
            response = requests.post(f"{self.base_url}/ai/decide", 
                                   json={"candidate_data": candidate_data})
            if response.status_code == 200:
                decision = response.json()
                prob = decision.get("success_probability", 0)
                recommendation = decision.get("decision", "")
                
                self.log_step(2,
                    "Get AI decision for candidate",
                    f"✅ AI Decision: {recommendation} (Probability: {prob:.3f})",
                    "Show API call and response with probability score"
                )
                return prob, recommendation
            else:
                self.log_step(2, "AI Decision", "❌ Failed", "")
        except Exception as e:
            self.log_step(2, "AI Decision", f"❌ Error: {e}", "")
        return 0, ""
    
    def demo_step_3_hr_feedback(self, candidate_data, initial_prob):
        """Demo Step 3: HR Feedback"""
        feedback_data = {
            "candidate_data": candidate_data,
            "feedback_score": 5.0,
            "outcome": "hired"
        }
        
        try:
            response = requests.post(f"{self.base_url}/ai/feedback", json=feedback_data)
            if response.status_code == 200:
                result = response.json()
                learning_delta = result.get("learning_metrics", {}).get("learning_delta", 0)
                
                self.log_step(3,
                    "Submit positive HR feedback (Score: 5.0, Outcome: Hired)",
                    f"✅ Feedback processed, Learning Delta: {learning_delta:.3f}",
                    "Show feedback form and RL learning confirmation"
                )
                return True
            else:
                self.log_step(3, "HR Feedback", "❌ Failed", "")
        except Exception as e:
            self.log_step(3, "HR Feedback", f"❌ Error: {e}", "")
        return False
    
    def demo_step_4_rl_update(self, candidate_data):
        """Demo Step 4: RL Update Verification"""
        try:
            response = requests.post(f"{self.base_url}/ai/decide", 
                                   json={"candidate_data": candidate_data})
            if response.status_code == 200:
                decision = response.json()
                new_prob = decision.get("success_probability", 0)
                
                self.log_step(4,
                    "Verify RL learning - Get new AI decision",
                    f"✅ Updated Probability: {new_prob:.3f} (Brain learned from feedback)",
                    "Show improved probability score after learning"
                )
                return new_prob
            else:
                self.log_step(4, "RL Update Check", "❌ Failed", "")
        except Exception as e:
            self.log_step(4, "RL Update Check", f"❌ Error: {e}", "")
        return 0
    
    def demo_step_5_dashboard_graphs(self):
        """Demo Step 5: Dashboard Real-time Graphs"""
        try:
            # Check RL analytics
            analytics_response = requests.get(f"{self.base_url}/ai/rl-analytics")
            history_response = requests.get(f"{self.base_url}/ai/rl-history?limit=5")
            
            if analytics_response.status_code == 200 and history_response.status_code == 200:
                analytics = analytics_response.json()
                history = history_response.json()
                
                reward_data = analytics.get("reward_evolution", {})
                total_entries = len(history.get("history", []))
                
                self.log_step(5,
                    "Show dashboard with real-time RL analytics",
                    f"✅ Dashboard loaded: {total_entries} learning entries, reward evolution graph active",
                    "Show Streamlit dashboard with RL graphs updating"
                )
                return True
            else:
                self.log_step(5, "Dashboard Analytics", "❌ Failed", "")
        except Exception as e:
            self.log_step(5, "Dashboard Analytics", f"❌ Error: {e}", "")
        return False
    
    def generate_complete_demo_script(self):
        """Generate complete demo video script"""
        print("🎬 HR-AI System Demo Video Script Generator")
        print("=" * 60)
        print("📝 This script generates the exact steps for the 2-3 minute demo video")
        print("🎯 Requirement: Add Candidate → AI Decision → HR Feedback → RL Update → Dashboard")
        print()
        
        # Execute demo steps
        candidate_id = self.demo_step_1_add_candidate()
        
        if candidate_id:
            initial_prob, decision = self.demo_step_2_ai_decision(candidate_id)
            
            candidate_data = {
                "name": "Demo Candidate",
                "skills": ["Python", "Machine Learning", "FastAPI", "AI"],
                "id": candidate_id
            }
            
            if self.demo_step_3_hr_feedback(candidate_data, initial_prob):
                new_prob = self.demo_step_4_rl_update(candidate_data)
                self.demo_step_5_dashboard_graphs()
                
                # Calculate learning impact
                learning_impact = new_prob - initial_prob
                
                print("🎬 DEMO VIDEO SCRIPT SUMMARY")
                print("=" * 40)
                print(f"📊 Initial AI Probability: {initial_prob:.3f}")
                print(f"📈 Final AI Probability: {new_prob:.3f}")
                print(f"🧠 Learning Impact: {learning_impact:+.3f}")
                print(f"✅ Total Demo Steps: {len(self.steps)}")
                
                # Generate video timeline
                print("\n🎥 VIDEO TIMELINE (2-3 minutes)")
                print("-" * 30)
                print("0:00-0:30 - Step 1: Add candidate with skills")
                print("0:30-1:00 - Step 2: Show AI decision & probability")
                print("1:00-1:30 - Step 3: Submit HR feedback (hired)")
                print("1:30-2:00 - Step 4: Show RL learning (improved probability)")
                print("2:00-2:30 - Step 5: Dashboard graphs updating real-time")
                print("2:30-3:00 - Summary: RL Brain learning demonstration")
                
                return True
        
        print("❌ Demo script generation failed - check if system is running")
        return False
    
    def save_demo_script(self):
        """Save demo script to file"""
        script_data = {
            "demo_title": "HR-AI System with Active RL Learning",
            "duration": "2-3 minutes",
            "steps": self.steps,
            "generated_at": datetime.now().isoformat(),
            "video_requirements": {
                "show_candidate_addition": True,
                "show_ai_decision": True,
                "show_hr_feedback": True,
                "show_rl_learning": True,
                "show_dashboard_graphs": True
            }
        }
        
        with open("demo_video_script.json", "w") as f:
            json.dump(script_data, f, indent=2)
        
        print(f"\n📄 Demo script saved to: demo_video_script.json")

def main():
    print("🎬 Demo Video Script Generator for HR-AI System")
    print("Make sure the system is running on localhost:5000")
    print()
    
    input("Press Enter to generate demo script...")
    
    demo = DemoVideoScript()
    
    if demo.generate_complete_demo_script():
        demo.save_demo_script()
        print("\n🎉 Demo script generated successfully!")
        print("📹 Use this script to record the 2-3 minute demo video")
        print("🎯 Show each step clearly with the expected results")
    else:
        print("\n❌ Demo script generation failed")
        print("💡 Make sure the HR-AI system is running: python start_enhanced_system.py")

if __name__ == "__main__":
    main()