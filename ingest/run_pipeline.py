# File: ingest/run_pipeline.py
# Description: Runs the ingestion and push scripts in parallel using threads and handles graceful shutdown

import threading
import subprocess
import time
import signal
import sys

FETCH_SCRIPT = "ingest/fetch_transactions.py"
PUSH_SCRIPT = "ingest/push_to_neo4j.py"
SIMULATE_SCRIPT = "ingest/simulate_wallets.py"
INTERVAL_SECONDS = 60

shutdown_flag = threading.Event()

def run_script(script, label, interval=INTERVAL_SECONDS):
    while not shutdown_flag.is_set():
        print(f"🚀 Running {label}...")
        process = subprocess.Popen(["python", script])

        try:
            process.wait()
        except KeyboardInterrupt:
            print(f"🛑 Interrupt received — terminating {label}")
            process.terminate()
            break

        if shutdown_flag.is_set():
            print(f"🔁 Shutdown requested — stopping {label}")
            process.terminate()
            break

        time.sleep(interval)

def signal_handler(sig, frame):
    print("\n🛑 Stopping pipeline threads...")
    shutdown_flag.set()
    time.sleep(1)
    sys.exit(0)

if __name__ == "__main__":
    print("🚦 Starting pipeline with threads...")

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    threads = [
        threading.Thread(target=run_script, args=(FETCH_SCRIPT, "Fetch Script")),
        threading.Thread(target=run_script, args=(PUSH_SCRIPT, "Push Script")),
        threading.Thread(target=run_script, args=(SIMULATE_SCRIPT, "Simulate Script", 300))
    ]

    for t in threads:
        t.start()

    for t in threads:
        t.join()
