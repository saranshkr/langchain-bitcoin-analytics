import os
import json
from pathlib import Path
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load environment variables
load_dotenv()
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# Paths
raw_dir = Path("data/raw")
log_file = Path("data/pushed_files.txt")
log_file.parent.mkdir(parents=True, exist_ok=True)
log_file.touch(exist_ok=True)

# Connect to Neo4j
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def create_transaction_node(tx, data):
    query = """
    MERGE (t:Transaction {timestamp: $timestamp})
    SET t.price_usd = $price_usd,
        t.market_cap = $market_cap,
        t.volume_24h = $volume_24h
    """
    tx.run(query, **data)

def ingest_new_files():
    with open(log_file, "r") as f:
        pushed = set(line.strip() for line in f.readlines())

    json_files = sorted(raw_dir.glob("*.json"))

    with driver.session() as session:
        for file in json_files:
            if file.name in pushed:
                continue

            try:
                with open(file) as f:
                    data = json.load(f)
                print(f"🚀 Ingesting {file.name}")
                session.execute_write(create_transaction_node, data)

                with open(log_file, "a") as log:
                    log.write(f"{file.name}\n")

            except Exception as e:
                print(f"❌ Failed to push {file.name}: {e}")

if __name__ == "__main__":
    ingest_new_files()
