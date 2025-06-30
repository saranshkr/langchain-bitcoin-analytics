# File: ui/tabs/wallet_graph.py
# Description: Streamlit tab for rendering the wallet–transaction graph and related statistics

import streamlit as st
import streamlit.components.v1 as components
import os
from ui.utils.helpers import get_graph_stats, get_node_stats
from ui.utils.autorefresh import auto_refresh


def render():
    st.markdown("### Wallet-Transaction Graph")
    auto_refresh(
        interval=300,
        run_script="analysis/graph_pyvis.py",
        label="Graph auto-refreshes every 5 minutes with simulated wallet transactions.",
        key="wallet_graph"
    )
    try:
        total_edges, sent_count, received_count = get_graph_stats()
        wallets, txns = get_node_stats()
        st.metric("Wallet Nodes", wallets)
        st.metric("Transaction Nodes", txns)
        st.metric("Total Edges", total_edges)
        st.caption(f"🕘 SENT: {sent_count} | 🕘 RECEIVED_BY: {received_count}")
    except Exception as e:
        st.error(f"Could not load graph stats: {e}")

    graph_path = "wallet_graph.html"
    if os.path.exists(graph_path):
        with open(graph_path, "r") as f:
            html = f.read()
        components.html(html, height=800, scrolling=True)
    else:
        st.warning("Wallet graph not found. Run `graph_pyvis.py` to generate it.")
