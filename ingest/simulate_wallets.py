# File: ingest/simulate_wallets.py
# Description: Simulates wallet activity for unlinked transactions in Neo4j

import os
import random
import hashlib
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load environment variables
load_dotenv()
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# Create a pool of fake wallet addresses
WALLET_COUNT = 50
WALLET_POOL = [f"wallet_{i:03d}" for i in range(WALLET_COUNT)]

# Connect to Neo4j
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def generate_tx_id(timestamp):
    return hashlib.sha256(timestamp.encode()).hexdigest()[:16]

def simulate_wallet_links():
    with driver.session() as session:
        txns = session.run("""
            MATCH (t:Transaction)
            WHERE t.simulated IS NULL
            RETURN t.timestamp AS ts
            ORDER BY ts
        """)
        count = 0
        for record in txns:
            timestamp = record["ts"]
            tx_id = generate_tx_id(str(timestamp))
            sender = random.choice(WALLET_POOL)
            receivers = random.sample([w for w in WALLET_POOL if w != sender], random.choice([1, 2]))
            session.execute_write(link_wallets, timestamp, tx_id, sender, receivers)
            count += 1

        print(f"✅ Simulated wallets for {count} new transaction(s)")

def link_wallets(tx, timestamp, tx_id, sender, receivers):
    # Link sender to transaction
    tx.run("""
        MERGE (s:Wallet {address: $sender})
        MERGE (t:Transaction {tx_id: $tx_id})
        SET t.timestamp = $timestamp, t.simulated = true
        MERGE (s)-[:SENT]->(t)
    """, timestamp=timestamp, tx_id=tx_id, sender=sender)

    # Link receivers to transaction
    for r in receivers:
        tx.run("""
            MERGE (r:Wallet {address: $receiver})
            MERGE (t:Transaction {tx_id: $tx_id})
            MERGE (t)-[:RECEIVED_BY]->(r)
        """, tx_id=tx_id, receiver=r)

if __name__ == "__main__":
    simulate_wallet_links()
