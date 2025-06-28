# File: ui/utils/helpers.py

import os
import pandas as pd
from datetime import datetime
from neo4j import GraphDatabase
from neo4j.time import Date, DateTime, Time, Duration
from dotenv import load_dotenv

# Load environment variables and initialize Neo4j driver
load_dotenv()
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))


def get_node_stats():
    with driver.session() as session:
        result = session.run("""
            RETURN
              count { MATCH (w:Wallet) RETURN w } AS wallet_count,
              count { MATCH (t:Transaction) RETURN t } AS txn_count
        """)
        record = result.single()
        return record["wallet_count"], record["txn_count"]


def get_graph_stats():
    with driver.session() as session:
        result = session.run("""
            MATCH ()-[r]->() RETURN
              count(r) AS total_edges,
              count { MATCH ()-[x:SENT]->() RETURN x } AS sent_count,
              count { MATCH ()-[y:RECEIVED_BY]->() RETURN y } AS received_count
        """)
        record = result.single()
        return record["total_edges"], record["sent_count"], record["received_count"]


def get_top_senders():
    query = """
        MATCH (w:Wallet)-[:SENT]->()
        RETURN w.address AS wallet, COUNT(*) AS sent_count
        ORDER BY sent_count DESC
        LIMIT 5
    """
    with driver.session() as session:
        result = session.run(query)
        return pd.DataFrame([dict(r) for r in result])


def get_top_receivers():
    query = """
        MATCH (w:Wallet)<-[:RECEIVED_BY]-()
        RETURN w.address AS wallet, COUNT(*) AS received_count
        ORDER BY received_count DESC
        LIMIT 5
    """
    with driver.session() as session:
        result = session.run(query)
        return pd.DataFrame([dict(r) for r in result])


def get_24h_transaction_count():
    query = """
        MATCH (t:Transaction)
        WHERE datetime(t.timestamp) > datetime() - duration('P1D')
        RETURN count(t) AS recent_txns
    """
    with driver.session() as session:
        record = session.run(query).single()
        return record["recent_txns"]


def get_daily_txn_counts():
    query = """
        MATCH (t:Transaction)
        WHERE datetime(t.timestamp) >= datetime() - duration('P7D')
        RETURN date(datetime(t.timestamp)) AS day, count(*) AS txn_count
        ORDER BY day
    """
    with driver.session() as session:
        result = session.run(query)
        return pd.DataFrame([dict(r) for r in result])


def run_custom_query(query):
    with driver.session() as session:
        result = session.run(query)
        return [dict(r) for r in result]


def flatten_value(val):
    if hasattr(val, "_properties"):
        return {k: flatten_value(v) for k, v in val._properties.items()}
    if isinstance(val, (Date, DateTime, Time, Duration)):
        return str(val)
    if isinstance(val, list):
        return [flatten_value(v) for v in val]
    if isinstance(val, dict):
        return {k: flatten_value(v) for k, v in val.items()}
    return val
