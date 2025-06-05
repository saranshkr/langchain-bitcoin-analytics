# File: utils/cleanup.py
# Description: Deletes raw data files older than a specified number of hours and updates pushed_files.txt

import os
import datetime
from pathlib import Path

RAW_DIR = Path("data/raw")
LOG_FILE = Path("data/pushed_files.txt")
AGE_LIMIT_HOURS = 24  # Change this to adjust retention duration

def purge_old_files():
    now = datetime.datetime.now()
    cutoff = now - datetime.timedelta(hours=AGE_LIMIT_HOURS)
    deleted_files = []

    for file in RAW_DIR.glob("*.json"):
        file_time = datetime.datetime.fromtimestamp(file.stat().st_mtime)
        if file_time < cutoff:
            print(f"🗑️ Deleting old file: {file.name}")
            file.unlink()
            deleted_files.append(file.name)

    # Remove deleted files from the log
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            entries = [line.strip() for line in f if line.strip() not in deleted_files]
        with open(LOG_FILE, "w") as f:
            f.write("\n".join(entries) + ("\n" if entries else ""))

if __name__ == "__main__":
    purge_old_files()
