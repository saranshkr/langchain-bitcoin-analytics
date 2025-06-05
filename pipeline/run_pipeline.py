# pipeline/run_pipeline.py

import time
import subprocess
import threading

FETCH_SCRIPT = ["python", "ingest/fetch_transactions.py"]
PUSH_SCRIPT = ["python", "db/push_to_neo4j.py"]

def fetch_loop():
    while True:
        print("\n📥 [Fetch] Getting new Bitcoin data...")
        subprocess.run(FETCH_SCRIPT)
        time.sleep(60)

def push_loop():
    # Delay slightly to allow first fetch
    print("⏳ [Push] Waiting 10 seconds for initial fetch...")
    time.sleep(10)
    while True:
        print("\n🚀 [Push] Sending data to Neo4j...")
        subprocess.run(PUSH_SCRIPT)
        time.sleep(60)

def run_pipeline():
    print("🚀 Starting real-time Bitcoin pipeline (parallel fetch + push)...")

    fetch_thread = threading.Thread(target=fetch_loop, daemon=True)
    push_thread = threading.Thread(target=push_loop, daemon=True)

    fetch_thread.start()
    push_thread.start()

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Pipeline stopped by user.")

if __name__ == "__main__":
    run_pipeline()
