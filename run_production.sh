#!/bin/bash
echo "🚀 Starting HR-AI System (Production Mode)"
echo "=========================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p data logs backups exports uploads

# Start the system
echo "🚀 Starting HR-AI System..."
echo "   - API Server: http://localhost:5000"
echo "   - Dashboard: http://localhost:8501"
echo ""

python start_enhanced_system.py