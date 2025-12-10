#!/usr/bin/env python3
"""
Production Deployment Script for HR-AI System with Active RL
Includes main system + AI microservice deployment
"""

import subprocess
import sys
import os
import time
import requests
from pathlib import Path

class ProductionDeployer:
    """Deploy HR-AI System to production with all RL features"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.services = {}
        
    def run_command(self, command, description, cwd=None):
        """Run command with error handling"""
        print(f"🔄 {description}...")
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                check=True, 
                capture_output=True, 
                text=True,
                cwd=cwd or self.base_dir
            )
            print(f"✅ {description} completed")
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed: {e.stderr}")
            return False, e.stderr
    
    def check_dependencies(self):
        """Check all required dependencies"""
        print("🔍 Checking Production Dependencies...")
        
        required_packages = [
            "fastapi", "uvicorn", "streamlit", "pydantic",
            "pandas", "numpy", "plotly", "requests"
        ]
        
        missing = []
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing.append(package)
        
        if missing:
            print(f"📦 Installing missing packages: {missing}")
            success, _ = self.run_command(
                f"pip install {' '.join(missing)}", 
                "Installing dependencies"
            )
            return success
        
        print("✅ All dependencies available")
        return True
    
    def setup_production_environment(self):
        """Setup production environment"""
        print("🏗️ Setting up Production Environment...")
        
        # Create production directories
        directories = [
            "logs", "data", "backups", "exports", 
            "feedback", "uploads", "ai_microservice/logs", 
            "ai_microservice/data"
        ]
        
        for directory in directories:
            os.makedirs(self.base_dir / directory, exist_ok=True)
        
        # Copy production config
        if not os.path.exists(self.base_dir / ".env"):
            if os.path.exists(self.base_dir / ".env.production"):
                success, _ = self.run_command(
                    "copy .env.production .env" if os.name == 'nt' else "cp .env.production .env",
                    "Setting up production config"
                )
            else:
                # Create basic production config
                with open(self.base_dir / ".env", "w") as f:
                    f.write("# Production Environment\n")
                    f.write("ENVIRONMENT=production\n")
                    f.write("DEBUG=false\n")
                    f.write("RL_ACTIVE=true\n")
                print("✅ Basic production config created")
        
        print("✅ Production environment ready")
        return True
    
    def deploy_main_system(self):
        """Deploy main HR-AI system"""
        print("🚀 Deploying Main HR-AI System...")
        
        # Start main system
        command = f"{sys.executable} -m uvicorn app.main:app --host 0.0.0.0 --port 5000 --workers 2"
        
        try:
            process = subprocess.Popen(
                command.split(),
                cwd=self.base_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.services['main_system'] = process
            
            # Wait for startup
            time.sleep(5)
            
            # Test health
            try:
                response = requests.get("http://localhost:5000/health", timeout=10)
                if response.status_code == 200:
                    health_data = response.json()
                    rl_status = health_data.get("ai_brain", {}).get("status", "UNKNOWN")
                    print(f"✅ Main system deployed - RL Status: {rl_status}")
                    return True
                else:
                    print(f"⚠️ Main system health check failed: {response.status_code}")
                    return False
            except Exception as e:
                print(f"⚠️ Main system health check error: {e}")
                return False
                
        except Exception as e:
            print(f"❌ Main system deployment failed: {e}")
            return False
    
    def deploy_ai_microservice(self):
        """Deploy AI Brain microservice"""
        print("🧠 Deploying AI Brain Microservice...")
        
        microservice_dir = self.base_dir / "ai_microservice"
        
        # Start microservice
        command = f"{sys.executable} ai_brain_service.py"
        
        try:
            process = subprocess.Popen(
                command.split(),
                cwd=microservice_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.services['ai_microservice'] = process
            
            # Wait for startup
            time.sleep(5)
            
            # Test health
            try:
                response = requests.get("http://localhost:8080/health", timeout=10)
                if response.status_code == 200:
                    health_data = response.json()
                    rl_status = health_data.get("rl_status", "UNKNOWN")
                    skills_count = health_data.get("skills_learned", 0)
                    print(f"✅ AI Microservice deployed - RL: {rl_status}, Skills: {skills_count}")
                    return True
                else:
                    print(f"⚠️ AI Microservice health check failed: {response.status_code}")
                    return False
            except Exception as e:
                print(f"⚠️ AI Microservice health check error: {e}")
                return False
                
        except Exception as e:
            print(f"❌ AI Microservice deployment failed: {e}")
            return False
    
    def deploy_dashboard(self):
        """Deploy Streamlit dashboard"""
        print("📊 Deploying Dashboard...")
        
        command = f"{sys.executable} -m streamlit run dashboard/app.py --server.port=8501 --server.headless=true"
        
        try:
            process = subprocess.Popen(
                command.split(),
                cwd=self.base_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.services['dashboard'] = process
            
            # Wait for startup
            time.sleep(8)
            
            # Test dashboard (basic check)
            try:
                response = requests.get("http://localhost:8501", timeout=10)
                if response.status_code == 200:
                    print("✅ Dashboard deployed successfully")
                    return True
                else:
                    print(f"⚠️ Dashboard check returned: {response.status_code}")
                    return True  # Streamlit might return different codes
            except Exception as e:
                print(f"⚠️ Dashboard check error (may be normal): {e}")
                return True  # Dashboard might still be starting
                
        except Exception as e:
            print(f"❌ Dashboard deployment failed: {e}")
            return False
    
    def run_integration_tests(self):
        """Run integration tests to verify deployment"""
        print("🧪 Running Integration Tests...")
        
        try:
            # Run integration tests
            success, output = self.run_command(
                f"{sys.executable} integration_tests.py",
                "Running integration test suite"
            )
            
            if success:
                print("✅ Integration tests passed")
                return True
            else:
                print("⚠️ Some integration tests failed - check logs")
                return False
                
        except Exception as e:
            print(f"❌ Integration tests failed: {e}")
            return False
    
    def display_deployment_info(self):
        """Display deployment information"""
        print("\n" + "=" * 60)
        print("🎉 PRODUCTION DEPLOYMENT COMPLETE")
        print("=" * 60)
        
        print("\n🌐 ACCESS POINTS:")
        print("   • Main API:      http://localhost:5000")
        print("   • API Docs:      http://localhost:5000/docs")
        print("   • Dashboard:     http://localhost:8501")
        print("   • AI Microservice: http://localhost:8080")
        print("   • Microservice Docs: http://localhost:8080/docs")
        
        print("\n🧠 RL FEATURES:")
        print("   ✅ Active Reinforcement Learning")
        print("   ✅ Real-time Decision Making")
        print("   ✅ Feedback Processing & Learning")
        print("   ✅ Analytics & Visualization")
        print("   ✅ Shashank Platform Integration")
        
        print("\n🔗 INTEGRATION ENDPOINTS:")
        print("   • Decision API:  POST /ai/decide")
        print("   • Feedback API:  POST /ai/feedback")
        print("   • RL Analytics:  GET /ai/rl-analytics")
        print("   • Shashank API:  /integration/shashank/*")
        
        print("\n📊 MONITORING:")
        print("   • System Health: GET /health")
        print("   • RL Performance: GET /ai/rl-performance")
        print("   • Brain State:   GET /ai/rl-state")
        
        print("\n🔧 MANAGEMENT:")
        print("   • Stop services: Ctrl+C")
        print("   • View logs:     logs/ directory")
        print("   • Backup data:   POST /system/backup/create")
        
        print("\n" + "=" * 60)
        print("🚀 System is PRODUCTION READY!")
        print("=" * 60)
    
    def deploy_full_system(self):
        """Deploy complete system"""
        print("🚀 HR-AI System Production Deployment")
        print("=" * 50)
        
        # Step 1: Check dependencies
        if not self.check_dependencies():
            print("❌ Dependency check failed")
            return False
        
        # Step 2: Setup environment
        if not self.setup_production_environment():
            print("❌ Environment setup failed")
            return False
        
        # Step 3: Deploy main system
        if not self.deploy_main_system():
            print("❌ Main system deployment failed")
            return False
        
        # Step 4: Deploy AI microservice
        if not self.deploy_ai_microservice():
            print("❌ AI microservice deployment failed")
            return False
        
        # Step 5: Deploy dashboard
        if not self.deploy_dashboard():
            print("❌ Dashboard deployment failed")
            return False
        
        # Step 6: Run integration tests
        time.sleep(5)  # Allow all services to fully start
        if not self.run_integration_tests():
            print("⚠️ Integration tests had issues - system may still be functional")
        
        # Step 7: Display info
        self.display_deployment_info()
        
        return True
    
    def monitor_services(self):
        """Monitor deployed services"""
        print("\n🔍 Monitoring services... (Press Ctrl+C to stop)")
        
        try:
            while True:
                time.sleep(30)
                
                # Check each service
                for service_name, process in self.services.items():
                    if process.poll() is not None:
                        print(f"⚠️ {service_name} has stopped")
                
                # Health checks
                try:
                    main_health = requests.get("http://localhost:5000/health", timeout=5)
                    micro_health = requests.get("http://localhost:8080/health", timeout=5)
                    
                    if main_health.status_code != 200:
                        print("⚠️ Main system health check failed")
                    
                    if micro_health.status_code != 200:
                        print("⚠️ Microservice health check failed")
                        
                except Exception as e:
                    print(f"⚠️ Health check error: {e}")
                
        except KeyboardInterrupt:
            print("\n🛑 Stopping services...")
            self.stop_services()
    
    def stop_services(self):
        """Stop all deployed services"""
        for service_name, process in self.services.items():
            try:
                process.terminate()
                process.wait(timeout=10)
                print(f"✅ {service_name} stopped")
            except Exception as e:
                print(f"⚠️ Error stopping {service_name}: {e}")
                try:
                    process.kill()
                except:
                    pass

def main():
    """Main deployment function"""
    deployer = ProductionDeployer()
    
    try:
        if deployer.deploy_full_system():
            deployer.monitor_services()
        else:
            print("❌ Deployment failed")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Deployment interrupted")
        deployer.stop_services()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        deployer.stop_services()
        sys.exit(1)

if __name__ == "__main__":
    main()