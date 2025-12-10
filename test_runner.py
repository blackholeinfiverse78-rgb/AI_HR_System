#!/usr/bin/env python3
import unittest
import sys
import os
from datetime import datetime

def run_tests():
    """Run all tests with minimal output"""
    
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    
    print("🧪 Running Test Suite:")
    print("   - test_rl_brain.py (RL functionality)")
    print("   - test_api.py (API endpoints)")
    print("   - test_rl_robustness.py (RL stress tests)")
    print()
    
    # Run with minimal verbosity
    runner = unittest.TextTestRunner(verbosity=1, stream=sys.stdout)
    result = runner.run(suite)
    
    # Print summary
    total = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total - failures - errors
    
    print(f"\n{'='*40}")
    print(f"TEST SUMMARY")
    print(f"{'='*40}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failures}")
    print(f"🔥 Errors: {errors}")
    print(f"📊 Success: {(passed/total)*100:.1f}%" if total > 0 else "No tests")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)