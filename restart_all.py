import subprocess
import os
import time

services = [
    {"name": "Citizen Service", "dir": "services/citizen-vehicle-service", "port": 8001},
    {"name": "Station Service", "dir": "services/fuel-station-service", "port": 8002},
    {"name": "Queue Service", "dir": "services/queue-service", "port": 8003},
    {"name": "Transaction Service", "dir": "services/transaction-service", "port": 8005},
    {"name": "Quota Service", "dir": "services/quota-service", "port": 8006},
    {"name": "API Gateway", "dir": "gateway", "port": 8000}
]

base_path = "d:/MTIT assignment 2/Fuel Pass"

def kill_processes():
    print("Killing existing python processes...")
    try:
        # Kill all python processes except the current one
        # On Windows, we can use wmic or tasklist, but let's just use taskkill and ignore errors
        # To avoid killing itself, we can use a more specific title or just run it via cmd
        subprocess.run("taskkill /F /IM python.exe /FI \"PID ne %d\" /T" % os.getpid(), shell=True, capture_output=True)
    except:
        pass
    time.sleep(2)

def start_services():
    processes = []
    for svc in services:
        print(f"Starting {svc['name']} on port {svc['port']}...")
        full_path = os.path.join(base_path, svc['dir'])
        p = subprocess.Popen(
            ["python", "main.py"],
            cwd=full_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        processes.append(p)
        time.sleep(3) # Wait between starts
    return processes

if __name__ == "__main__":
    kill_processes()
    start_services()
    print("All services started in background.")
