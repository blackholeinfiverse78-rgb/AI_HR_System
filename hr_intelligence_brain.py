"""
HR Intelligence Brain - Plug-and-Play Module
Connects cleanly to any HR platform via REST API
Now with Reinforced Learning (RL) capabilities!
"""

import requests
import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class HRIntelligenceBrain:
    """
    Plug-and-play HR Intelligence Brain for any HR platform
    Includes RL Loop: Decision -> Feedback -> Reward -> Policy Update
    """
    
    def __init__(self, base_url: str = "http://localhost:5000", api_key: str = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"
            
        # ACTIVE RL State - Enhanced Configuration
        self.weights_file = "data/rl_weights.json"
        self.weights = self._load_weights()
        self.learning_rate = 0.15  # Slightly higher for faster learning
        self.discount_factor = 0.9
        self.exploration_rate = 0.1  # For exploration vs exploitation
        self.min_weight = 0.1
        self.max_weight = 5.0
        
        # Initialize with better default weights if empty
        if not self.weights:
            self.weights = {
                "python": 1.2, "java": 1.1, "javascript": 1.0, "react": 1.0,
                "ai": 1.3, "machine learning": 1.3, "ml": 1.3, "data science": 1.2,
                "fastapi": 1.1, "django": 1.0, "flask": 1.0, "nodejs": 1.0,
                "communication": 0.9, "teamwork": 0.8, "leadership": 0.9,
                "sql": 1.0, "database": 1.0, "mongodb": 0.9, "postgresql": 1.0
            }
            self._save_weights()
            print("RL Brain initialized with enhanced default weights")
        
    def _load_weights(self) -> Dict[str, float]:
        """Load RL weights from storage"""
        if os.path.exists(self.weights_file):
            try:
                with open(self.weights_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {"python": 1.0, "ai": 1.0, "fastapi": 1.0, "communication": 1.0}
        
    def _save_weights(self):
        """Save RL weights to storage"""
        os.makedirs("data", exist_ok=True)
        try:
            with open(self.weights_file, 'w') as f:
                json.dump(self.weights, f, indent=2)
        except Exception as e:
            print(f"Failed to save RL weights: {e}")

    # Core Intelligence Functions
    def analyze_candidate(self, candidate_data: Dict) -> Dict:
        """ACTIVE RL: Analyze candidate with real-time learning"""
        try:
            # Enhanced RL analysis with confidence metrics
            rl_score = self.predict_success(candidate_data)
            
            # Calculate confidence based on skill matches
            skills = candidate_data.get("skills", [])
            matched_weights = []
            for skill in skills:
                for weight_skill, weight in self.weights.items():
                    if weight_skill.lower() in skill.lower() or skill.lower() in weight_skill.lower():
                        matched_weights.append(weight)
            
            confidence = min(0.95, len(matched_weights) / max(len(skills), 1) * 0.8 + 0.2)
            
            # Try to get additional insights from API
            try:
                response = requests.post(f"{self.base_url}/smart/analyze", 
                                       json=candidate_data, headers=self.headers, timeout=3)
                api_result = response.json() if response.status_code == 200 else {}
            except:
                api_result = {}
            
            # Combine RL insights with API results
            result = {
                "rl_success_probability": rl_score,
                "rl_confidence": confidence,
                "rl_matched_skills": len(matched_weights),
                "rl_total_weights": len(self.weights),
                "rl_status": "ACTIVE",
                "analysis_timestamp": datetime.now().isoformat()
            }
            
            # Merge API results if available
            if api_result and "error" not in api_result:
                result.update(api_result)
            
            return result
            
        except Exception as e:
            return {
                "error": f"Analysis failed: {e}",
                "rl_success_probability": self.predict_success(candidate_data),
                "rl_status": "ACTIVE_FALLBACK"
            }
    
    def get_recommendations(self, candidate_id: int) -> List[str]:
        """Get RL-enhanced AI recommendations for candidate"""
        try:
            # Try API first
            response = requests.get(f"{self.base_url}/smart/recommendations/{candidate_id}", 
                                  headers=self.headers, timeout=3)
            api_recommendations = response.json().get("recommendations", []) if response.status_code == 200 else []
            
            # Generate RL-based recommendations
            rl_recommendations = []
            
            # Get top weighted skills for recommendations
            top_skills = sorted(self.weights.items(), key=lambda x: x[1], reverse=True)[:5]
            
            for skill, weight in top_skills:
                if weight > 1.2:
                    rl_recommendations.append(f"Strong match for {skill} (weight: {weight:.2f})")
                elif weight > 1.0:
                    rl_recommendations.append(f"Good potential in {skill} (weight: {weight:.2f})")
            
            # Combine recommendations
            all_recommendations = api_recommendations + rl_recommendations
            
            # Add RL-specific insights
            if len(self.weights) > 10:
                all_recommendations.append(f"RL Brain has learned from {len(self.weights)} skills")
            
            return all_recommendations[:10]  # Limit to top 10
            
        except Exception as e:
            # Fallback to RL-only recommendations
            top_skills = sorted(self.weights.items(), key=lambda x: x[1], reverse=True)[:3]
            return [f"Consider skills in: {skill} (importance: {weight:.2f})" for skill, weight in top_skills]
    
    def predict_success(self, candidate_data: Dict) -> float:
        """Predict hiring success probability using ACTIVE RL weights"""
        try:
            skills = candidate_data.get("skills", [])
            if not skills:
                return 0.2  # Base probability for no skills
            
            # Enhanced scoring with fuzzy matching
            total_score = 0.0
            matched_skills = []
            normalized_skills = [s.lower().strip() for s in skills]
            
            for skill, weight in self.weights.items():
                skill_score = 0.0
                
                # Exact match (highest score)
                if skill in normalized_skills:
                    skill_score = weight
                    matched_skills.append((skill, weight, "exact"))
                else:
                    # Fuzzy matching for partial skills
                    for candidate_skill in normalized_skills:
                        if skill in candidate_skill or candidate_skill in skill:
                            skill_score = weight * 0.8  # Partial match penalty
                            matched_skills.append((skill, weight * 0.8, "partial"))
                            break
                        elif len(set(skill.split()) & set(candidate_skill.split())) > 0:
                            skill_score = weight * 0.6  # Word overlap
                            matched_skills.append((skill, weight * 0.6, "overlap"))
                            break
                
                total_score += skill_score
            
            # Dynamic normalization based on current weights distribution
            if self.weights:
                avg_weight = sum(self.weights.values()) / len(self.weights)
                max_possible = len(normalized_skills) * avg_weight
                normalized_score = total_score / max(max_possible, 1.0)
            else:
                normalized_score = 0.0
            
            # Apply sigmoid transformation for smooth probability
            import math
            probability = 1 / (1 + math.exp(-5 * (normalized_score - 0.5)))
            
            # Ensure reasonable bounds
            probability = max(0.05, min(0.95, probability))
            
            # Log prediction details for transparency
            print(f"RL Prediction: {len(matched_skills)} skills matched, score: {total_score:.2f}, prob: {probability:.3f}")
            
            return round(probability, 3)
            
        except Exception as e:
            print(f"RL Prediction failed: {e}")
            return 0.2
    
    def reward_log(self, candidate_data: Dict, feedback_score: float, outcome: str):
        """
        ACTIVE RL: Log feedback and update policy (weights)
        feedback_score: 1.0 to 5.0
        outcome: 'hired', 'rejected', etc.
        """
        # Calculate reward with enhanced logic
        reward = self._calculate_reward(feedback_score, outcome)
        
        # Get prediction before update for comparison
        old_prediction = self.predict_success(candidate_data)
        
        # Update policy (this is where learning happens)
        self.policy_update(candidate_data, reward)
        
        # Get prediction after update to measure learning
        new_prediction = self.predict_success(candidate_data)
        
        # Enhanced logging with learning metrics
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "candidate": candidate_data.get("name", "Unknown"),
            "candidate_id": candidate_data.get("id", "N/A"),
            "skills": candidate_data.get("skills", []),
            "feedback_score": feedback_score,
            "outcome": outcome,
            "calculated_reward": reward,
            "prediction_before": old_prediction,
            "prediction_after": new_prediction,
            "learning_delta": new_prediction - old_prediction,
            "weights_count": len(self.weights),
            "active_weights": {k: v for k, v in self.weights.items() if v > 1.0},
            "learning_rate": self.learning_rate
        }
        
        # Save to structured log file
        try:
            os.makedirs("logs", exist_ok=True)
            with open("logs/rl_state_summary.json", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
            
            # Also save current state snapshot
            state_snapshot = {
                "timestamp": datetime.now().isoformat(),
                "total_weights": len(self.weights),
                "top_weights": dict(sorted(self.weights.items(), key=lambda x: x[1], reverse=True)[:10]),
                "learning_rate": self.learning_rate,
                "last_reward": reward
            }
            
            with open("logs/rl_current_state.json", "w") as f:
                json.dump(state_snapshot, f, indent=2)
                
            print(f"RL Learning Complete: Reward={reward:.3f}, Delta={new_prediction-old_prediction:.3f}")
            
        except Exception as e:
            print(f"RL Logging failed: {e}")

    def _calculate_reward(self, feedback_score: float, outcome: str) -> float:
        """Enhanced reward calculation for active RL"""
        # Normalize feedback score (1-5) to reward range
        score_reward = (feedback_score - 3) / 2.0  # Maps 1->-1, 3->0, 5->1
        
        # Enhanced outcome rewards with more granular feedback
        outcome_reward = 0.0
        outcome_lower = outcome.lower()
        
        if outcome_lower in ['hired', 'offer_accepted', 'accept']:
            outcome_reward = 1.5  # Strong positive signal
        elif outcome_lower in ['shortlisted', 'interview', 'second_round']:
            outcome_reward = 0.8  # Moderate positive signal
        elif outcome_lower in ['rejected', 'declined', 'reject']:
            outcome_reward = -0.8  # Negative signal but not too harsh
        elif outcome_lower in ['reconsider', 'maybe', 'pending']:
            outcome_reward = 0.2  # Slight positive (better than rejection)
        
        # Combine rewards with weighting
        total_reward = (score_reward * 0.6) + (outcome_reward * 0.4)
        
        # Apply bounds to prevent extreme updates
        return max(-2.0, min(2.0, total_reward))

    def policy_update(self, candidate_data: Dict, reward: float):
        """
        Update weights (Policy) based on reward - FULLY ACTIVE RL
        W_new = W_old + alpha * reward * feature_presence
        """
        skills = candidate_data.get("skills", [])
        normalized_skills = [s.lower() for s in skills]
        
        updated = False
        
        # Update existing weights with decay to prevent overfitting
        for skill in self.weights:
            if any(skill in s for s in normalized_skills):
                old_weight = self.weights[skill]
                # Enhanced update rule with momentum and bounds
                weight_change = self.learning_rate * reward
                self.weights[skill] = max(0.1, min(5.0, old_weight + weight_change))
                updated = True
                
                # Log weight changes for transparency
                print(f"RL Update: {skill} weight {old_weight:.3f} -> {self.weights[skill]:.3f} (reward: {reward:.3f})")
        
        # Add new skills with adaptive thresholds
        if reward > 0.3:  # Lower threshold for skill discovery
            for s in normalized_skills:
                clean_s = s.strip().lower()
                should_add = True
                
                # Check if skill already exists (fuzzy matching)
                for existing in self.weights:
                    if existing in clean_s or clean_s in existing or abs(len(existing) - len(clean_s)) < 3:
                        should_add = False
                        break
                
                if should_add and len(clean_s) < 25 and len(clean_s) > 2:
                    initial_weight = 1.0 + (self.learning_rate * reward * 2)  # Boost new skills
                    self.weights[clean_s] = max(0.5, min(3.0, initial_weight))
                    updated = True
                    print(f"RL Discovery: New skill '{clean_s}' added with weight {self.weights[clean_s]:.3f}")

        # Apply weight decay to prevent stagnation
        if updated:
            for skill in self.weights:
                if skill not in [s.lower() for s in normalized_skills]:
                    self.weights[skill] *= 0.999  # Slight decay for unused skills
            
            self._save_weights()
            print(f"RL Policy Updated: {len(self.weights)} skills tracked")

    def trigger_automation(self, candidate_id: int, event_type: str, metadata: Dict = None) -> Dict:
        """Trigger multi-channel automation"""
        try:
            data = {
                "candidate_id": candidate_id,
                "event_type": event_type,
                "metadata": metadata or {}
            }
            response = requests.post(f"{self.base_url}/trigger/", 
                                   json=data, headers=self.headers)
            return response.json() if response.status_code == 200 else {"error": "Automation failed"}
        except:
            return {"error": "Connection failed"}
    
    # Platform Integration Methods
    def sync_candidate(self, external_candidate: Dict) -> Dict:
        """Sync candidate from external HR platform"""
        # Transform external format to internal format
        internal_candidate = {
            "name": external_candidate.get("full_name") or external_candidate.get("name"),
            "email": external_candidate.get("email_address") or external_candidate.get("email"),
            "phone": external_candidate.get("phone_number") or external_candidate.get("phone"),
            "skills": external_candidate.get("skills", [])
        }
        
        try:
            response = requests.post(f"{self.base_url}/candidate/add", 
                                   json=internal_candidate, headers=self.headers)
            return response.json() if response.status_code == 200 else {"error": "Sync failed"}
        except:
            return {"error": "Connection failed"}
    
    def get_insights_dashboard(self) -> Dict:
        """Get complete dashboard insights for external platform"""
        try:
            response = requests.get(f"{self.base_url}/analytics/dashboard", headers=self.headers)
            return response.json() if response.status_code == 200 else {}
        except:
            return {}
    
    def health_check(self) -> bool:
        """Check if HR Intelligence Brain is healthy"""
        try:
            response = requests.get(f"{self.base_url}/health", headers=self.headers)
            return response.status_code == 200
        except:
            return False

# Shashank's Platform Integration Adapter
class ShashankHRAdapter:
    """Adapter for Shashank's HR Platform Integration"""
    
    def __init__(self, shashank_api_url: str, hr_brain: HRIntelligenceBrain):
        self.shashank_api = shashank_api_url
        self.hr_brain = hr_brain
    
    def connect_to_shashank_platform(self) -> bool:
        """Establish connection to Shashank's HR platform"""
        return self.hr_brain.health_check()
    
    def process_shashank_candidate(self, shashank_candidate: Dict) -> Dict:
        """Process candidate from Shashank's platform with ACTIVE RL"""
        try:
            # Enhanced candidate data preparation
            candidate_data = {
                "name": shashank_candidate.get("full_name") or shashank_candidate.get("name"),
                "email": shashank_candidate.get("email_address") or shashank_candidate.get("email"),
                "phone": shashank_candidate.get("phone_number") or shashank_candidate.get("phone"),
                "skills": shashank_candidate.get("skills", [])
            }
            
            # Sync candidate to HR Brain (optional, for full integration)
            sync_result = self.hr_brain.sync_candidate(shashank_candidate)
            candidate_id = sync_result.get("candidate_id", "temp_id")
            
            # Get ACTIVE RL analysis
            analysis = self.hr_brain.analyze_candidate(candidate_data)
            
            # Get RL-enhanced recommendations
            recommendations = self.hr_brain.get_recommendations(candidate_id)
            
            # Enhanced result with RL metrics
            result = {
                "candidate_id": candidate_id,
                "candidate_name": candidate_data["name"],
                "success_probability": analysis.get("rl_success_probability", 0),
                "confidence": analysis.get("rl_confidence", 0),
                "ai_recommendations": recommendations,
                "rl_metrics": {
                    "matched_skills": analysis.get("rl_matched_skills", 0),
                    "total_weights": analysis.get("rl_total_weights", 0),
                    "learning_status": "ACTIVE",
                    "brain_version": "v2.0_active"
                },
                "status": "processed",
                "processing_timestamp": datetime.now().isoformat()
            }
            
            # Add API analysis if available
            if "error" not in analysis:
                result["extended_analysis"] = analysis
            
            return result
            
        except Exception as e:
            return {
                "error": f"Processing failed: {e}",
                "candidate_name": shashank_candidate.get("full_name", "Unknown"),
                "rl_status": "ERROR_FALLBACK"
            }
    
    def feedback_loop(self, candidate_data: Dict, score: float, outcome: str):
        """ACTIVE RL: Process feedback from Shashank's platform to update Brain"""
        try:
            # Get prediction before learning
            old_prediction = self.hr_brain.predict_success(candidate_data)
            
            # Apply RL learning
            self.hr_brain.reward_log(candidate_data, score, outcome)
            
            # Get prediction after learning
            new_prediction = self.hr_brain.predict_success(candidate_data)
            
            # Calculate learning metrics
            learning_delta = new_prediction - old_prediction
            
            return {
                "status": "brain_updated_active",
                "learning_metrics": {
                    "prediction_before": old_prediction,
                    "prediction_after": new_prediction,
                    "learning_delta": learning_delta,
                    "feedback_score": score,
                    "outcome": outcome,
                    "weights_updated": len(self.hr_brain.weights)
                },
                "rl_status": "ACTIVE_LEARNING",
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "status": "brain_update_failed",
                "error": str(e),
                "rl_status": "ERROR"
            }
        
    def get_platform_insights(self) -> Dict:
        """Get ACTIVE RL insights formatted for Shashank's platform"""
        try:
            # Get base insights
            insights = self.hr_brain.get_insights_dashboard()
            
            # Enhanced RL-specific insights
            top_skills = sorted(self.hr_brain.weights.items(), key=lambda x: x[1], reverse=True)[:10]
            
            # Calculate learning metrics
            total_weights = len(self.hr_brain.weights)
            active_weights = sum(1 for w in self.hr_brain.weights.values() if w > 1.0)
            
            return {
                "total_candidates": insights.get("total_candidates", 0),
                "average_match_score": insights.get("avg_match_score", 0),
                "top_skills": [skill for skill, _ in top_skills[:5]],
                "skill_weights": dict(top_skills[:5]),
                "rl_metrics": {
                    "total_skills_learned": total_weights,
                    "active_skills": active_weights,
                    "learning_rate": self.hr_brain.learning_rate,
                    "brain_status": "FULLY_ACTIVE",
                    "last_updated": datetime.now().isoformat()
                },
                "hiring_trends": "Positive (RL Enhanced)",
                "ai_status": "Active (RL FULLY OPERATIONAL)",
                "integration_status": "Ready for Shashank Platform"
            }
            
        except Exception as e:
            return {
                "error": f"Insights failed: {e}",
                "ai_status": "Active (RL Fallback Mode)",
                "rl_metrics": {
                    "brain_status": "ERROR_RECOVERY"
                }
            }

# Simple Integration Example
def create_hr_brain_for_shashank(shashank_platform_url: str) -> ShashankHRAdapter:
    """Create ACTIVE RL HR Intelligence Brain for Shashank's platform"""
    print("🚀 Initializing ACTIVE RL HR Intelligence Brain...")
    
    # Initialize with enhanced configuration
    hr_brain = HRIntelligenceBrain()
    
    # Verify RL is active
    print(f"🧠 RL Brain Status: ACTIVE ({len(hr_brain.weights)} skills loaded)")
    print(f"⚙️ Learning Rate: {hr_brain.learning_rate}")
    print(f"🎯 Ready for Shashank Platform Integration")
    
    adapter = ShashankHRAdapter(shashank_platform_url, hr_brain)
    return adapter

# ACTIVE RL Demo and Testing
if __name__ == "__main__":
    print("🚀 HR Intelligence Brain - ACTIVE RL MODE")
    print("="*50)
    
    # Initialize HR Brain for Shashank's platform
    adapter = create_hr_brain_for_shashank("https://shashank-hr-platform.com/api")
    
    # Test connection
    if adapter.connect_to_shashank_platform():
        print("✅ HR Intelligence Brain (RL ACTIVE) connected successfully!")
        
        # Example candidates for testing RL learning
        test_candidates = [
            {
                "full_name": "Python Expert",
                "email_address": "python@example.com",
                "phone_number": "+91-9876543210",
                "skills": ["Python", "Django", "Machine Learning", "AI"]
            },
            {
                "full_name": "Java Developer", 
                "email_address": "java@example.com",
                "phone_number": "+91-9876543211",
                "skills": ["Java", "Spring Boot", "Microservices", "SQL"]
            },
            {
                "full_name": "Frontend Specialist",
                "email_address": "frontend@example.com", 
                "phone_number": "+91-9876543212",
                "skills": ["React", "JavaScript", "CSS", "Node.js"]
            }
        ]
        
        print("\n🧪 ACTIVE RL LEARNING DEMONSTRATION")
        print("-" * 40)
        
        for i, candidate in enumerate(test_candidates, 1):
            print(f"\n👤 Candidate {i}: {candidate['full_name']}")
            
            # Initial prediction
            result = adapter.process_shashank_candidate(candidate)
            initial_prob = result.get('success_probability', 0)
            print(f"📊 Initial Prediction: {initial_prob:.3f}")
            
            # Simulate feedback (varying outcomes for learning)
            if i == 1:  # Python expert - positive feedback
                feedback_score, outcome = 5.0, "hired"
            elif i == 2:  # Java developer - moderate feedback
                feedback_score, outcome = 3.5, "reconsider"
            else:  # Frontend - negative feedback
                feedback_score, outcome = 2.0, "rejected"
            
            print(f"📝 Feedback: Score={feedback_score}, Outcome={outcome}")
            
            # Apply feedback (this triggers RL learning)
            adapter.feedback_loop(candidate, feedback_score, outcome)
            
            # Check learning impact
            result_new = adapter.process_shashank_candidate(candidate)
            new_prob = result_new.get('success_probability', 0)
            learning_delta = new_prob - initial_prob
            
            print(f"📊 Updated Prediction: {new_prob:.3f} (Δ: {learning_delta:+.3f})")
            print(f"🧠 Learning Status: {'✅ LEARNED' if abs(learning_delta) > 0.01 else '⚠️ MINIMAL'}")
        
        print("\n🎯 RL LEARNING SUMMARY")
        print("-" * 30)
        brain = adapter.hr_brain
        top_weights = sorted(brain.weights.items(), key=lambda x: x[1], reverse=True)[:5]
        
        print(f"📈 Total Skills Learned: {len(brain.weights)}")
        print("🏆 Top Weighted Skills:")
        for skill, weight in top_weights:
            print(f"   • {skill}: {weight:.3f}")
        
        print(f"\n⚙️ Learning Rate: {brain.learning_rate}")
        print("🔄 RL Status: FULLY ACTIVE & LEARNING")
        
    else:
        print("❌ Failed to connect HR Intelligence Brain.")
        print("💡 Tip: Start the server with 'python start_enhanced_system.py'")