#!/usr/bin/env python3
"""
API Screenshots Generator
Creates sample API calls and responses for documentation
"""

import requests
import json
from datetime import datetime

class APIScreenshotGenerator:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.screenshots = []
    
    def capture_api_call(self, name, method, endpoint, data=None):
        """Capture API call for screenshot documentation"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                response = requests.post(url, json=data)
            
            screenshot = {
                "name": name,
                "method": method,
                "url": url,
                "request_data": data,
                "status_code": response.status_code,
                "response": response.json() if response.status_code == 200 else {"error": "Failed"},
                "timestamp": datetime.now().isoformat()
            }
            
            self.screenshots.append(screenshot)
            
            print(f"📸 {name}")
            print(f"   {method} {url}")
            if data:
                print(f"   Request: {json.dumps(data, indent=2)}")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {json.dumps(screenshot['response'], indent=2)}")
            print("-" * 50)
            
            return screenshot
            
        except Exception as e:
            print(f"❌ Failed to capture {name}: {e}")
            return None
    
    def generate_all_screenshots(self):
        """Generate all required API screenshots"""
        print("📸 Generating API Screenshots for Documentation")
        print("=" * 60)
        
        # 1. AI Decision API
        self.capture_api_call(
            "AI Decision API",
            "POST",
            "/ai/decide",
            {
                "candidate_data": {
                    "name": "John Doe",
                    "skills": ["Python", "FastAPI", "Machine Learning"],
                    "id": 1
                }
            }
        )
        
        # 2. AI Feedback API
        self.capture_api_call(
            "AI Feedback API",
            "POST", 
            "/ai/feedback",
            {
                "candidate_data": {
                    "name": "John Doe",
                    "skills": ["Python", "FastAPI", "Machine Learning"]
                },
                "feedback_score": 4.5,
                "outcome": "hired"
            }
        )
        
        # 3. Automation Event API
        self.capture_api_call(
            "Automation Event API",
            "POST",
            "/trigger/",
            {
                "candidate_id": 1,
                "event_type": "shortlisted",
                "metadata": {
                    "override_email": "custom@example.com"
                }
            }
        )
        
        # 4. RL Status API
        self.capture_api_call(
            "RL Status API",
            "GET",
            "/ai/status"
        )
        
        # 5. RL Analytics API
        self.capture_api_call(
            "RL Analytics API", 
            "GET",
            "/ai/rl-analytics"
        )
        
        # 6. System Health API
        self.capture_api_call(
            "System Health API",
            "GET", 
            "/health"
        )
        
        # 7. Candidate List API
        self.capture_api_call(
            "Candidate List API",
            "GET",
            "/candidate/list"
        )
        
        print(f"\n✅ Generated {len(self.screenshots)} API screenshots")
        return self.screenshots
    
    def save_screenshots(self):
        """Save screenshots to JSON file"""
        with open("api_screenshots.json", "w") as f:
            json.dump({
                "title": "HR-AI System API Screenshots",
                "generated_at": datetime.now().isoformat(),
                "total_screenshots": len(self.screenshots),
                "screenshots": self.screenshots
            }, f, indent=2)
        
        print(f"📄 Screenshots saved to: api_screenshots.json")
    
    def generate_postman_collection(self):
        """Generate Postman collection for easy testing"""
        collection = {
            "info": {
                "name": "HR-AI System API Collection",
                "description": "Complete API collection for HR-AI System with RL",
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
            },
            "item": []
        }
        
        for screenshot in self.screenshots:
            item = {
                "name": screenshot["name"],
                "request": {
                    "method": screenshot["method"],
                    "header": [
                        {
                            "key": "Content-Type",
                            "value": "application/json"
                        }
                    ],
                    "url": {
                        "raw": screenshot["url"],
                        "host": ["localhost"],
                        "port": "5000",
                        "path": screenshot["url"].replace("http://localhost:5000", "").split("/")[1:]
                    }
                }
            }
            
            if screenshot["request_data"]:
                item["request"]["body"] = {
                    "mode": "raw",
                    "raw": json.dumps(screenshot["request_data"], indent=2)
                }
            
            collection["item"].append(item)
        
        with open("HR_AI_System.postman_collection.json", "w") as f:
            json.dump(collection, f, indent=2)
        
        print(f"📮 Postman collection saved to: HR_AI_System.postman_collection.json")

def main():
    print("📸 API Screenshots Generator for HR-AI System")
    print("This will generate sample API calls for documentation")
    print("Make sure the system is running on localhost:5000")
    print()
    
    input("Press Enter to generate API screenshots...")
    
    generator = APIScreenshotGenerator()
    
    screenshots = generator.generate_all_screenshots()
    
    if screenshots:
        generator.save_screenshots()
        generator.generate_postman_collection()
        
        print("\n🎉 API Screenshots Generated Successfully!")
        print("📄 Files created:")
        print("   - api_screenshots.json (detailed responses)")
        print("   - HR_AI_System.postman_collection.json (Postman collection)")
        print("\n📋 Use these for:")
        print("   - Documentation screenshots")
        print("   - Postman testing")
        print("   - Integration examples")
    else:
        print("\n❌ Screenshot generation failed")
        print("💡 Make sure the system is running: python start_enhanced_system.py")

if __name__ == "__main__":
    main()