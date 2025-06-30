# File: app.py
# Description: Streamlit dashboard with modularized tabs and Neo4j queries

import streamlit as st
import streamlit.components.v1 as components
import os
from datetime import datetime
from dotenv import load_dotenv
from neo4j import GraphDatabase

# Import tab renderers
from ui.tabs import price_chart, wallet_graph, summary_tab, stats_tab, query_explorer

# Load environment variables and connect to Neo4j
load_dotenv()
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

# UI setup
st.set_page_config(page_title="Bitcoin Analytics Dashboard", layout="wide")
st.title("Real-time Bitcoin Analytics Dashboard")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Price Chart",
    "🔗 Wallet Graph",
    "🧠 Summary",
    "📊 Stats",
    "💬 Query Explorer"
])

# Render each tab
with tab1:
    price_chart.render()

with tab2:
    wallet_graph.render()

with tab3:
    summary_tab.render()

with tab4:
    stats_tab.render()

with tab5:
    query_explorer.render()

# Footer
st.markdown("---")
st.caption(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
