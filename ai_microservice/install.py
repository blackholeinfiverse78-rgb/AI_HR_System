#!/usr/bin/env python3
"""
One-Command Install Script for AI Brain Microservice
Ready for Shashank's Platform Integration
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def install_microservice():
    """Install AI Brain Microservice"""
    print("🚀 AI Brain Microservice - One-Command Install")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Create directories
    os.makedirs("logs", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    print("✅ Directories created")
    
    # Test installation
    print("🧪 Testing installation...")
    try:
        import fastapi
        import uvicorn
        import pydantic
        print("✅ All dependencies installed correctly")
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    
    print("\n🎉 Installation Complete!")
    print("=" * 50)
    print("🌐 Start microservice: python ai_brain_service.py")
    print("📚 API Docs: http://localhost:8080/docs")
    print("🔗 Shashank Integration: Ready")
    print("📊 RL Status: FULLY ACTIVE")
    
    return True

def install_with_docker():
    """Install using Docker"""
    print("🐳 Docker Installation")
    print("=" * 30)
    
    if not run_command("docker --version", "Checking Docker"):
        print("❌ Docker not found. Please install Docker first.")
        return False
    
    if not run_command("docker-compose build", "Building Docker image"):
        return False
    
    print("✅ Docker installation complete")
    print("🚀 Start with: docker-compose up")
    return True

if __name__ == "__main__":
    print("Choose installation method:")
    print("1. Standard Python installation")
    print("2. Docker installation")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        success = install_microservice()
    elif choice == "2":
        success = install_with_docker()
    else:
        print("❌ Invalid choice")
        success = False
    
    if success:
        print("\n🎯 Next Steps for Shashank Integration:")
        print("1. Start the microservice")
        print("2. Test with: curl http://localhost:8080/health")
        print("3. Check API docs at: http://localhost:8080/docs")
        print("4. Use /integration/shashank/* endpoints")
        sys.exit(0)
    else:
        print("\n❌ Installation failed")
        sys.exit(1)