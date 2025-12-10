import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hr_intelligence_brain import HRIntelligenceBrain
import time

class TestRLRobustness(unittest.TestCase):
    
    def setUp(self):
        self.brain = HRIntelligenceBrain()
    
    def test_stress_learning(self):
        """Test RL under high feedback load"""
        candidate = {"name": "Stress Test", "skills": ["Python", "AI"]}
        
        # Rapid feedback cycles
        for i in range(50):
            score = 5.0 if i % 2 == 0 else 1.0
            outcome = "hired" if i % 2 == 0 else "rejected"
            self.brain.reward_log(candidate, score, outcome)
        
        # Verify brain still functions
        prob = self.brain.predict_success(candidate)
        self.assertIsInstance(prob, float)
        self.assertGreater(len(self.brain.weights), 0)
    
    def test_skill_discovery_robustness(self):
        """Test new skill learning under various conditions"""
        initial_count = len(self.brain.weights)
        
        # Add diverse skills
        skills_sets = [
            ["NewTech1", "Framework1"],
            ["Language1", "Tool1", "Platform1"],
            ["Skill" + str(i) for i in range(10)]
        ]
        
        for skills in skills_sets:
            candidate = {"name": "Test", "skills": skills}
            self.brain.reward_log(candidate, 4.0, "hired")
        
        # Verify skill discovery
        self.assertGreater(len(self.brain.weights), initial_count)
    
    def test_weight_bounds(self):
        """Test weight boundaries under extreme feedback"""
        candidate = {"name": "Bounds Test", "skills": ["BoundTest"]}
        
        # Extreme positive feedback
        for _ in range(20):
            self.brain.reward_log(candidate, 5.0, "hired")
        
        # Check weights stay within bounds
        for weight in self.brain.weights.values():
            self.assertLessEqual(weight, 5.0)
            self.assertGreaterEqual(weight, 0.1)

if __name__ == '__main__':
    unittest.main()