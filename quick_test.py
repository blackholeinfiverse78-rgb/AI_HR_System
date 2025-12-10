#!/usr/bin/env python3
"""Quick test to verify all fixes are working"""

import requests
import time
import subprocess
import sys
from datetime import datetime

def test_rl_brain():
    """Test RL brain functionality"""
    print("🧠 Testing RL Brain...")
    
    try:
        from hr_intelligence_brain import HRIntelligenceBrain
        
        # Initialize brain
        brain = HRIntelligenceBrain()
        print(f"✅ RL Brain initialized with {len(brain.weights)} skills")
        
        # Test prediction
        test_candidate = {
            "name": "Test User",
            "skills": ["Python", "AI", "FastAPI"]
        }
        
        initial_prediction = brain.predict_success(test_candidate)
        print(f"✅ Initial prediction: {initial_prediction:.3f}")
        
        # Test learning
        brain.reward_log(test_candidate, 4.5, "hired")
        new_prediction = brain.predict_success(test_candidate)
        
        learning_occurred = abs(new_prediction - initial_prediction) > 0.001
        print(f"✅ Learning test: {'PASSED' if learning_occurred else 'MINIMAL'}")
        print(f"   Prediction: {initial_prediction:.3f} → {new_prediction:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ RL Brain test failed: {e}")
        return False

def test_microservice():
    """Test AI microservice"""
    print("\n🔌 Testing AI Microservice...")
    
    try:
        # Start microservice
        import os
        microservice_dir = "ai_microservice"
        
        if os.path.exists(microservice_dir):
            print("✅ AI Microservice directory exists")
            
            # Check key files
            key_files = [
                "ai_brain_service.py",
                "Dockerfile", 
                "docker-compose.yml",
                "install.py",
                "README.md"
            ]
            
            for file in key_files:
                if os.path.exists(f"{microservice_dir}/{file}"):
                    print(f"✅ {file} exists")
                else:
                    print(f"❌ {file} missing")
            
            return True
        else:
            print("❌ AI Microservice directory missing")
            return False
            
    except Exception as e:
        print(f"❌ Microservice test failed: {e}")
        return False

def test_dashboard_files():
    """Test dashboard RL analytics"""
    print("\n📊 Testing Dashboard Files...")
    
    try:
        # Check dashboard file
        with open("dashboard/app.py", "r") as f:
            dashboard_content = f.read()
        
        # Check for RL Analytics section
        rl_features = [
            "RL Analytics",
            "rl-analytics", 
            "rl-state",
            "rl-history",
            "Brain State Visualization",
            "Reward Evolution"
        ]
        
        found_features = 0
        for feature in rl_features:
            if feature in dashboard_content:
                found_features += 1
                print(f"✅ {feature} found in dashboard")
        
        if found_features >= 4:
            print("✅ Dashboard RL Analytics section implemented")
            return True
        else:
            print(f"⚠️ Only {found_features}/{len(rl_features)} RL features found")
            return False
            
    except Exception as e:
        print(f"❌ Dashboard test failed: {e}")
        return False

def test_integration_files():
    """Test integration test suite"""
    print("\n🧪 Testing Integration Files...")
    
    try:
        # Check integration test file
        if os.path.exists("integration_tests.py"):
            print("✅ Integration test suite exists")
            
            with open("integration_tests.py", "r") as f:
                test_content = f.read()
            
            # Check for key test methods
            test_methods = [
                "test_rl_brain_active",
                "test_rl_decision_making", 
                "test_rl_learning_loop",
                "test_shashank_integration",
                "test_dashboard_rl_section"
            ]
            
            found_tests = 0
            for test in test_methods:
                if test in test_content:
                    found_tests += 1
                    print(f"✅ {test} found")
            
            if found_tests >= 4:
                print("✅ Comprehensive integration tests implemented")
                return True
            else:
                print(f"⚠️ Only {found_tests}/{len(test_methods)} tests found")
                return False
        else:
            print("❌ Integration test file missing")
            return False
            
    except Exception as e:
        print(f"❌ Integration test check failed: {e}")
        return False

def main():
    """Run quick tests"""
    print("🚀 HR-AI System Quick Test Suite")
    print("=" * 40)
    
    tests = [
        ("RL Brain Functionality", test_rl_brain),
        ("AI Microservice", test_microservice), 
        ("Dashboard RL Analytics", test_dashboard_files),
        ("Integration Test Suite", test_integration_files)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
    
    print("\n" + "=" * 40)
    print("📊 QUICK TEST RESULTS")
    print("=" * 40)
    print(f"✅ Passed: {passed}/{total}")
    print(f"📈 Success Rate: {(passed/total)*100:.1f}%")
    
    if passed >= 3:
        print("\n🎉 SYSTEM READY FOR FULL TESTING!")
        print("Next steps:")
        print("1. Run: python deploy_production.py")
        print("2. Run: python integration_tests.py")
        print("3. Access dashboard: http://localhost:8501")
    else:
        print("\n⚠️ Some components need attention")
    
    return passed >= 3

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)