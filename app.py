# File: app.py
# Description: Streamlit dashboard with tabbed layout, node/edge stats in Wallet Graph tab, Neo4j integration

import streamlit as st
import streamlit.components.v1 as components
import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Load environment variables and connect to Neo4j
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

# UI setup
st.set_page_config(page_title="Bitcoin Analytics Dashboard", layout="wide")
st.title("📊 Real-time Bitcoin Analytics Dashboard")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Price Chart", "🔗 Wallet Graph", "🧠 Summary", "📊 Stats"])

# Tab 1: Price chart
with tab1:
    chart_path = "btc_price_volume.png"
    st.markdown("### 📈 Bitcoin Price (5-pt Moving Average) & 24h Volume")
    if os.path.exists(chart_path):
        st.image(chart_path, caption="Bitcoin Price and 24h Volume (Last 2 Days)", use_column_width=True)
        try:
            df = pd.read_csv("btc_price_volume.csv")
            if len(df) < 12:
                st.warning("Volume bars may be inaccurate — need more data for stable 24h rolling volume.")
        except:
            st.info("Volume accuracy improves with more data collected over time.")
    else:
        st.warning("Price chart not found. Run `price_chart.py` to generate it.")

# Tab 2: Wallet Graph + node/edge stats
with tab2:
    st.markdown("### 🔗 Wallet–Transaction Graph")
    try:
        total_edges, sent_count, received_count = get_graph_stats()
        wallets, txns = get_node_stats()
        st.metric("Wallet Nodes", wallets)
        st.metric("Transaction Nodes", txns)
        st.metric("Total Edges", total_edges)
        st.caption(f"🟠 SENT: {sent_count} | 🔵 RECEIVED_BY: {received_count}")
    except Exception as e:
        st.error(f"Could not load graph stats: {e}")

    graph_path = "wallet_graph.html"
    if os.path.exists(graph_path):
        with open(graph_path, "r") as f:
            html = f.read()
        components.html(html, height=800, scrolling=True)
    else:
        st.warning("Wallet graph not found. Run `graph_pyvis.py` to generate it.")

# Tab 3: Langchain Summary
with tab3:
    summary_path = "latest_summary.txt"
    st.markdown("### 🧠 Langchain NLP Summary")
    if os.path.exists(summary_path):
        with open(summary_path, "r") as f:
            summary = f.read()
        st.text_area("Generated Summary", summary, height=200)
    else:
        st.info("No summary found. Run your `langchain_summary.py` script to generate one.")

# Tab 4: Stats
with tab4:
    st.markdown("### 📊 Node Statistics (from Neo4j)")
    try:
        wallets, txns = get_node_stats()
        st.metric(label="Wallet Nodes", value=wallets)
        st.metric(label="Transaction Nodes", value=txns)
    except Exception as e:
        st.error(f"Unable to fetch stats from Neo4j: {e}")

# Footer
st.markdown("---")
st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
