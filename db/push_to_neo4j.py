# db/push_to_neo4j.py

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load Neo4j credentials
load_dotenv()
print("URI =", os.getenv("NEO4J_URI"))

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

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

def ingest_all():
    raw_dir = Path("data/raw")
    json_files = sorted(raw_dir.glob("*.json"))

    with driver.session() as session:
        for file in json_files:
            with open(file) as f:
                data = json.load(f)
            print(f"Ingesting {file.name}")
            session.execute_write(create_transaction_node, data)

if __name__ == "__main__":
    ingest_all()
