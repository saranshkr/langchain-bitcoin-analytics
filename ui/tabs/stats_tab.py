# File: ui/tabs/stats_tab.py

import streamlit as st
import pandas as pd
import altair as alt
from ui.utils.helpers import get_node_stats, get_graph_stats, get_24h_transaction_count, get_top_senders, get_top_receivers, get_daily_txn_counts
from ui.utils.autorefresh import auto_refresh


def render():
    st.markdown("### Node Statistics and Top Wallets")
    auto_refresh(
        interval=60,
        label="Stats refresh every minute.",
        key="stats"
    )
    try:
        wallets, txns = get_node_stats()
        tx24 = get_24h_transaction_count()
        total_edges, sent_count, received_count = get_graph_stats()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Wallet Nodes", wallets)
            st.metric("Transaction Nodes", txns)
        with col2:
            st.metric("Total Edges", total_edges)
            st.metric("Tx in Last 24h", tx24)
        with col3:
            st.metric("SENT Edges", sent_count)
            st.metric("RECEIVED_BY Edges", received_count)
    except Exception as e:
        st.error(f"Unable to load metrics: {e}")

    st.markdown("#### 🥇 Top 5 Wallets by Sent Transactions")
    try:
        df_sent = get_top_senders()
        st.dataframe(df_sent, use_container_width=True)
        chart = alt.Chart(df_sent.sort_values("sent_count", ascending=False)).mark_bar().encode(
            x=alt.X("wallet:N", sort="-y", title="Wallet"),
            y=alt.Y("sent_count:Q", title="Sent Txns"),
            tooltip=["wallet", "sent_count"]
        ).properties(height=300)

        st.altair_chart(chart, use_container_width=True)
    except Exception as e:
        st.error(f"Unable to load top senders: {e}")

    st.markdown("#### 🥈 Top 5 Wallets by Received Transactions")
    try:
        df_recv = get_top_receivers()
        st.dataframe(df_recv, use_container_width=True)
        chart = alt.Chart(df_recv.sort_values("received_count", ascending=False)).mark_bar().encode(
            x=alt.X("wallet:N", sort="-y", title="Wallet"),
            y=alt.Y("received_count:Q", title="Received Txns"),
            tooltip=["wallet", "received_count"]
        ).properties(height=300)

        st.altair_chart(chart, use_container_width=True)

    except Exception as e:
        st.error(f"Unable to load top receivers: {e}")

    st.markdown("#### 📅 Daily Transaction Counts (Last 7 Days)")
    try:
        df_days = get_daily_txn_counts()
        if not df_days.empty:
            df_days["day"] = df_days["day"].astype(str)
            st.line_chart(df_days.set_index("day"))
        else:
            st.info("Not enough data for daily transaction chart.")
    except Exception as e:
        st.error(f"Unable to load daily transaction count chart: {e}")
