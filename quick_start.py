import subprocess
import sys
import time

print("Starting HR AI System...")
print("=" * 60)

# Start FastAPI
fastapi_process = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"],
    cwd=r"c:\Users\A\Downloads\AI_HR_System-main (1)\AI_HR_System-main"
)

time.sleep(2)

# Start Streamlit
streamlit_process = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "dashboard/app.py"],
    cwd=r"c:\Users\A\Downloads\AI_HR_System-main (1)\AI_HR_System-main"
)

print("\nFastAPI Backend: http://localhost:5000/docs")
print("Streamlit Dashboard: http://localhost:8501")
print("\nPress Ctrl+C to stop both services")

try:
    fastapi_process.wait()
    streamlit_process.wait()
except KeyboardInterrupt:
    fastapi_process.terminate()
    streamlit_process.terminate()
    print("\nServices stopped")
