import subprocess
import threading

def run_backend():
    subprocess.run(["python", "backend/main.py"])  # Hoặc run_backend.py nếu bạn tạo file chạy uvicorn

def run_frontend():
    subprocess.run(["streamlit", "run", "frontend/app.py"])

# Chạy backend và frontend cùng lúc
threading.Thread(target=run_backend).start()
threading.Thread(target=run_frontend).start()
