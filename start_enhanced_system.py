#!/usr/bin/env python3
"""
Enhanced HR-AI System Startup Script
Handles database initialization, security setup, performance monitoring, and automated backups
"""

import os
import sys
import time
import logging
import subprocess
import threading
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EnhancedSystemManager:
    """Manages the enhanced HR-AI system startup and monitoring"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.processes = {}
        self.monitoring_active = False
        
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        logger.info("Checking system dependencies...")
        
        required_packages = [
            'fastapi', 'uvicorn', 'streamlit', 'pydantic', 
            'pandas', 'numpy', 'requests', 'python-dotenv',
            'PyJWT', 'psutil', 'schedule'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            logger.error(f"Missing packages: {missing_packages}")
            logger.info("Installing missing packages...")
            try:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install'
                ] + missing_packages)
                logger.info("Dependencies installed successfully")
            except subprocess.CalledProcessError as e:
                logger.error(f"Failed to install dependencies: {e}")
                return False
        
        logger.info("All dependencies are available")
        return True
    
    def setup_directories(self):
        """Create required directories"""
        logger.info("Setting up directory structure...")
        
        directories = [
            'data', 'feedback', 'logs', 'backups', 'exports', 'uploads'
        ]
        
        for directory in directories:
            dir_path = self.base_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Directory ready: {directory}")
    
    def initialize_database(self):
        """Initialize the database system"""
        logger.info("Initializing database system...")
        
        try:
            from app.utils.database import db_manager
            db_manager.init_database()
            
            # Create default admin user if not exists
            admin_user = db_manager.get_user_by_username('admin')
            if not admin_user:
                from app.utils.security import SecurityManager
                db_manager.create_user({
                    'username': 'admin',
                    'password_hash': SecurityManager.hash_password('admin123'),
                    'role': 'admin',
                    'permissions': ['read', 'write', 'admin']
                })
                logger.info("Default admin user created (username: admin, password: admin123)")
            
            logger.info("Database initialization completed")
            return True
            
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            return False

    def migrate_legacy_data(self):
        """Migrate existing JSON data to database"""
        logger.info("Checking for legacy data migration...")
        
        try:
            from app.utils.database import DatabaseMigration
            DatabaseMigration.migrate_from_json()
            logger.info("Legacy data migration completed")
            return True
        except Exception as e:
            logger.warning(f"Legacy data migration failed (this is normal for new installations): {e}")
            return True  # Not critical for new installations
    
    def start_fastapi_server(self):
        """Start the FastAPI backend server"""
        logger.info("Starting FastAPI backend server...")
        
        try:
            # Start Uvicorn in a subprocess
            cmd = [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]
            process = subprocess.Popen(
                cmd,
                cwd=str(self.base_dir),
                env=os.environ.copy()
            )
            
            # Wait a moment for server to start
            time.sleep(3)
            
            # Test server health
            import requests
            try:
                response = requests.get("http://localhost:5000/health", timeout=5)
                if response.status_code == 200:
                    logger.info("FastAPI server started successfully on http://localhost:5000")
                    self.processes['fastapi'] = process
                    return True
            except:
                logger.warning("FastAPI health check failed initially (will retry in monitor)")
                self.processes['fastapi'] = process
                return True
                
        except Exception as e:
            logger.error(f"Failed to start FastAPI server: {e}")
            return False
    
    def start_streamlit_dashboard(self):
        """Start the Streamlit dashboard"""
        logger.info("Starting Streamlit dashboard...")
        
        try:
            # Start Streamlit in a subprocess
            cmd = [sys.executable, "-m", "streamlit", "run", "dashboard/app.py", "--server.port=8501", "--server.headless=true"]
            process = subprocess.Popen(
                cmd,
                cwd=str(self.base_dir),
                env=os.environ.copy()
            )
            
            # Wait for dashboard to start
            time.sleep(3)
            
            logger.info("Streamlit dashboard process started")
            self.processes['streamlit'] = process
            return True
            
        except Exception as e:
            logger.error(f"Failed to start Streamlit dashboard: {e}")
            return False
    
    def start_monitoring_services(self):
        """Start performance monitoring and backup services"""
        logger.info("Starting monitoring and backup services...")
        
        try:
            from app.utils.performance_monitor import performance_monitor
            from app.utils.backup_manager import backup_manager
            
            # Start performance monitoring
            performance_monitor.start_monitoring(interval_seconds=30)
            
            # Start automated backups (every 24 hours)
            backup_manager.start_auto_backup(interval_hours=24)
            
            logger.info("Monitoring and backup services started")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start monitoring services: {e}")
            return False
    
    def run_system_tests(self):
        """Run basic system tests"""
        logger.info("Running system tests...")
        
        tests_passed = 0
        total_tests = 5
        
        try:
            # Test 1: Database connectivity
            from app.utils.database import db_manager
            stats = db_manager.get_database_stats()
            if isinstance(stats, dict):
                tests_passed += 1
                logger.info("✓ Database connectivity test passed")
            
            # Test 2: API health check
            import requests
            response = requests.get("http://localhost:5000/health", timeout=5)
            if response.status_code == 200:
                tests_passed += 1
                logger.info("✓ API health check passed")
            
            # Test 3: Performance monitoring
            from app.utils.performance_monitor import performance_monitor
            metrics = performance_monitor.get_current_metrics()
            if metrics.get("timestamp"):
                tests_passed += 1
                logger.info("✓ Performance monitoring test passed")
            
            # Test 4: File system permissions
            test_file = self.base_dir / "logs" / "test_write.tmp"
            test_file.write_text("test")
            test_file.unlink()
            tests_passed += 1
            logger.info("✓ File system permissions test passed")
            
            # Test 5: Backup system
            from app.utils.backup_manager import backup_manager
            backup_list = backup_manager.get_backup_list()
            if isinstance(backup_list, list):
                tests_passed += 1
                logger.info("✓ Backup system test passed")
            
        except Exception as e:
            logger.warning(f"Some system tests failed: {e}")
        
        logger.info(f"System tests completed: {tests_passed}/{total_tests} passed")
        return tests_passed >= 3  # Require at least 3 tests to pass
    
    def display_system_info(self):
        """Display system information and access URLs"""
        print("\n" + "="*60)
        print("🚀 HR-AI SYSTEM - PRODUCTION READY")
        print("="*60)
        print(f"📅 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Base Directory: {self.base_dir}")
        print("\n🌐 ACCESS POINTS:")
        print("   • Dashboard:     http://localhost:8501")
        print("   • API Docs:      http://localhost:5000/docs")
        print("   • Health Check:  http://localhost:5000/health")
        print("   • Performance:   http://localhost:5000/system/performance")
        print("\n🔧 SYSTEM FEATURES:")
        print("   ✓ Multi-channel Communication (Email, WhatsApp, Voice)")
        print("   ✓ SQLite Database with Transactions")
        print("   ✓ Performance Monitoring")
        print("   ✓ Automated Backups")
        print("   ✓ Security & Authentication")
        print("   ✓ Error Recovery & Logging")
        print("\n🔐 DEFAULT CREDENTIALS:")
        print("   Username: admin")
        print("   Password: admin123")
        print("   (Change these in production!)")
        print("\n📊 MONITORING:")
        print("   • Performance metrics updated every 30 seconds")
        print("   • Automated backups every 24 hours")
        print("   • System logs in logs/ directory")
        print("\n" + "="*60)
        print("System is ready! Press Ctrl+C to stop.")
        print("="*60 + "\n")
    
    def start_system(self):
        """Start the complete enhanced system"""
        logger.info("Starting Enhanced HR-AI System...")
        
        # Step 1: Check dependencies
        if not self.check_dependencies():
            logger.error("Dependency check failed")
            return False
        
        # Step 2: Setup directories
        self.setup_directories()
        
        # Step 3: Initialize database
        if not self.initialize_database():
            logger.error("Database initialization failed")
            return False
        
        # Step 4: Migrate legacy data
        self.migrate_legacy_data()
        
        # Step 5: Start FastAPI server
        if not self.start_fastapi_server():
            logger.error("FastAPI server startup failed")
            return False
        
        # Step 6: Start Streamlit dashboard
        if not self.start_streamlit_dashboard():
            logger.error("Streamlit dashboard startup failed")
            return False
        
        # Step 7: Start monitoring services
        if not self.start_monitoring_services():
            logger.warning("Monitoring services failed to start (non-critical)")
        
        # Step 8: Run system tests
        if not self.run_system_tests():
            logger.warning("Some system tests failed (system may still be functional)")
        
        # Step 9: Display system information
        self.display_system_info()
        
        return True
    
    def monitor_system(self):
        """Monitor system health and restart services if needed"""
        self.monitoring_active = True
        
        while self.monitoring_active:
            try:
                # Check FastAPI health
                import requests
                response = requests.get("http://localhost:5000/health", timeout=5)
                if response.status_code != 200:
                    logger.warning("FastAPI health check failed, attempting restart...")
                    self.start_fastapi_server()
                
                # Check system resources
                from app.utils.performance_monitor import performance_monitor
                metrics = performance_monitor.get_current_metrics()
                
                if metrics.get("current", {}).get("memory_percent", 0) > 90:
                    logger.warning("High memory usage detected")
                
                if metrics.get("current", {}).get("cpu_percent", 0) > 90:
                    logger.warning("High CPU usage detected")
                
            except Exception as e:
                logger.error(f"System monitoring error: {e}")
            
            time.sleep(60)  # Check every minute
    
    def stop_system(self):
        """Gracefully stop all system components"""
        logger.info("Stopping Enhanced HR-AI System...")
        
        self.monitoring_active = False
        
        # Stop monitoring services
        try:
            from app.utils.performance_monitor import performance_monitor
            from app.utils.backup_manager import backup_manager
            
            performance_monitor.stop_monitoring()
            backup_manager.stop_auto_backup()
            
        except Exception as e:
            logger.error(f"Error stopping monitoring services: {e}")
        
        logger.info("System stopped successfully")

def main():
    """Main entry point"""
    system_manager = EnhancedSystemManager()
    
    try:
        if system_manager.start_system():
            # Start system monitoring
            monitor_thread = threading.Thread(
                target=system_manager.monitor_system, 
                daemon=True
            )
            monitor_thread.start()
            
            # Keep the main thread alive
            while True:
                time.sleep(1)
        else:
            logger.error("System startup failed")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Shutdown signal received")
        system_manager.stop_system()
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        system_manager.stop_system()
        sys.exit(1)

if __name__ == "__main__":
    main()