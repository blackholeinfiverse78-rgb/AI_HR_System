import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hr_intelligence_brain import HRIntelligenceBrain

class TestRLBrain(unittest.TestCase):
    
    def setUp(self):
        self.brain = HRIntelligenceBrain()
    
    def test_prediction(self):
        candidate = {"name": "Test", "skills": ["Python", "AI"]}
        prob = self.brain.predict_success(candidate)
        self.assertIsInstance(prob, float)
        self.assertGreaterEqual(prob, 0.0)
        self.assertLessEqual(prob, 1.0)
    
    def test_learning(self):
        candidate = {"name": "Test", "skills": ["React"]}
        initial = self.brain.predict_success(candidate)
        self.brain.reward_log(candidate, 5.0, "hired")
        updated = self.brain.predict_success(candidate)
        self.assertNotEqual(initial, updated)
    
    def test_skill_discovery(self):
        initial_skills = len(self.brain.weights)
        candidate = {"name": "Test", "skills": ["NewSkill123"]}
        self.brain.predict_success(candidate)
        self.assertGreater(len(self.brain.weights), initial_skills)

if __name__ == '__main__':
    unittest.main()