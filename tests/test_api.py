import unittest
import requests
import json

class TestAPI(unittest.TestCase):
    BASE_URL = "http://localhost:5000"
    
    def test_health(self):
        response = requests.get(f"{self.BASE_URL}/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("status", response.json())
    
    def test_ai_decision(self):
        data = {"candidate_data": {"name": "Test", "skills": ["Python"]}}
        response = requests.post(f"{self.BASE_URL}/ai/decide", json=data)
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertIn("decision", result)
        self.assertIn("success_probability", result)
    
    def test_ai_feedback(self):
        data = {
            "candidate_data": {"name": "Test", "skills": ["Python"]},
            "feedback_score": 4.0,
            "outcome": "hired"
        }
        response = requests.post(f"{self.BASE_URL}/ai/feedback", json=data)
        self.assertEqual(response.status_code, 200)
    
    def test_candidate_add(self):
        data = {
            "name": "Test User",
            "email": "test@test.com",
            "phone": "+91-9999999999",
            "skills": ["Testing"]
        }
        response = requests.post(f"{self.BASE_URL}/candidate/add", json=data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()