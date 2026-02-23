import subprocess
import os
import sys

def run_project():
    backend_dir = os.path.join(os.getcwd(), 'backend')
    app_path = os.path.join(backend_dir, 'app.py')
    
    print("Starting HeartCare AI Backend Server...")
    try:
        # Run flask app
        subprocess.run([sys.executable, app_path])
    except KeyboardInterrupt:
        print("\nStopping Server...")

if __name__ == "__main__":
    run_project()
