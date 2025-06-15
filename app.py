# File: app.py
# Streamlit dashboard with expanded Stats tab and Neo4j queries

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
        return val._properties
    return str(val)

# UI setup
st.set_page_config(page_title="Bitcoin Analytics Dashboard", layout="wide")
st.title("📊 Real-time Bitcoin Analytics Dashboard")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Price Chart", "🔗 Wallet Graph", "🧠 Summary", "📊 Stats", "💬 Query Explorer"])

# Tab 1: Price chart
with tab1:
    chart_path = "btc_price_volume.png"
    st.markdown("### 📈 Bitcoin Price (5-pt Moving Average) & 24h Volume")
    if os.path.exists(chart_path):
        st.image(chart_path, caption="Bitcoin Price and 24h Volume (Last 2 Days)", use_container_width=True)
        try:
            df = pd.read_csv("btc_price_volume.csv")
            if len(df) < 12:
                st.warning("Volume bars may be inaccurate — need more data for stable 24h rolling volume.")
        except:
            st.info("Volume accuracy improves with more data collected over time.")
    else:
        st.warning("Price chart not found. Run `price_chart.py` to generate it.")

# Tab 2: Wallet Graph
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
    st.markdown("### 📊 Node Statistics and Top Wallets")
    try:
        wallets, txns = get_node_stats()
        st.metric("Wallet Nodes", wallets)
        st.metric("Transaction Nodes", txns)
    except Exception as e:
        st.error(f"Unable to fetch stats from Neo4j: {e}")

    try:
        tx24 = get_24h_transaction_count()
        st.metric("Tx in Last 24h", tx24)
    except Exception as e:
        st.error(f"Unable to load 24h stats: {e}")

    st.markdown("#### 🥇 Top 5 Wallets by Sent Transactions")
    try:
        df_sent = get_top_senders()
        st.dataframe(df_sent, use_container_width=True)
        st.bar_chart(df_sent.set_index("wallet"))
    except Exception as e:
        st.error(f"Unable to load top senders: {e}")

    st.markdown("#### 🥈 Top 5 Wallets by Received Transactions")
    try:
        df_recv = get_top_receivers()
        st.dataframe(df_recv, use_container_width=True)
        st.bar_chart(df_recv.set_index("wallet"))
    except Exception as e:
        st.error(f"Unable to load top receivers: {e}")

    st.markdown("#### 📅 Daily Transaction Counts (Last 7 Days)")
    try:
        df_days = get_daily_txn_counts()
        if not df_days.empty:
            st.line_chart(df_days.set_index("day"))
        else:
            st.info("Not enough data for daily volume chart.")
    except Exception as e:
        st.error(f"Unable to load daily volume chart: {e}")

# Tab 5: Query Explorer
with tab5:
    st.markdown("### 💬 Run Custom Cypher Queries")

    sample_queries = {
        "Show 5 Wallets": "MATCH (w:Wallet) RETURN w LIMIT 5",
        "Show 5 Transactions": "MATCH (t:Transaction) RETURN t LIMIT 5",
        "Transactions by wallet_017": "MATCH (w:Wallet {address: 'wallet_017'})-[:SENT]->(t:Transaction)-[:RECEIVED_BY]->(r:Wallet) RETURN r.address AS receiver, t.tx_id AS tx_id",
        "Top 5 Receivers": "MATCH (w:Wallet)<-[:RECEIVED_BY]-() RETURN w.address AS wallet, count(*) AS received ORDER BY received DESC LIMIT 5",
        "Last 24h Transactions": "MATCH (t:Transaction) WHERE datetime(t.timestamp) > datetime() - duration('P1D') RETURN t.tx_id, t.timestamp, t.price_usd",
        "Transaction Volume Per Day (7 days)": "MATCH (t:Transaction) WHERE datetime(t.timestamp) >= datetime() - duration('P7D') RETURN date(datetime(t.timestamp)) AS day, count(*) AS txn_count ORDER BY day",
        "Received by wallet_017 in last 24h": "MATCH (t:Transaction)-[:RECEIVED_BY]->(w:Wallet {address: 'wallet_017'}) WHERE datetime(t.timestamp) > datetime() - duration('P1D') RETURN t.tx_id, t.timestamp"
    }

    query_choice = st.selectbox("▶ Select a sample query:", options=["(choose one)"] + list(sample_queries.keys()))
    if query_choice != "(choose one)":
        default_query = sample_queries[query_choice]
    else:
        default_query = "MATCH (n) RETURN n LIMIT 5"

    query_input = st.text_area("Enter Cypher Query:", default_query, height=150)

    if st.button("Run Query"):
        try:
            records = run_custom_query(query_input)
            flat_records = [{k: flatten_value(v) for k, v in row.items()} for row in records]
            st.dataframe(pd.DataFrame(flat_records))
        except Exception as e:
            st.error(f"⚠️ Error running query: {e}")


# Footer
st.markdown("---")
st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
