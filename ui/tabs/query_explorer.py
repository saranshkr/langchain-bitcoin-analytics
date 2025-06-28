# File: ui/tabs/query_explorer.py

import streamlit as st
import pandas as pd
from analysis.langchain_qa import run_qa_question, llm
from ui.utils.helpers import run_custom_query, flatten_value


def render():
    st.markdown("### Query Explorer & Q&A")

    mode = st.radio("Choose input mode:", ["Cypher Query", "Natural Language Question"], horizontal=True)

    if mode == "Cypher Query":
        sample_queries = {
            "Show 5 Wallets": "MATCH (w:Wallet) RETURN w LIMIT 5",
            "Show 5 Transactions": "MATCH (t:Transaction) RETURN t.tx_id, t.timestamp, t.price_usd LIMIT 5",
            "Transactions by wallet_017": "MATCH (w:Wallet {address: 'wallet_017'})-[:SENT]->(t:Transaction)-[:RECEIVED_BY]->(r:Wallet) RETURN r.address AS receiver, t.tx_id AS tx_id",
            "Top 5 Receivers": "MATCH (w:Wallet)<-[:RECEIVED_BY]-() RETURN w.address AS wallet, count(*) AS received ORDER BY received DESC LIMIT 5",
            "Last 24h Transactions": "MATCH (t:Transaction) WHERE datetime(t.timestamp) > datetime() - duration('P1D') RETURN t.tx_id, t.timestamp, t.price_usd",
            "Transaction Volume Per Day (7 days)": "MATCH (t:Transaction) WHERE datetime(t.timestamp) >= datetime() - duration('P7D') RETURN date(datetime(t.timestamp)) AS day, count(*) AS txn_count ORDER BY day",
            "Received by wallet_017 in last 24h": "MATCH (t:Transaction)-[:RECEIVED_BY]->(w:Wallet {address: 'wallet_017'}) WHERE datetime(t.timestamp) > datetime() - duration('P1D') RETURN t.tx_id, t.timestamp"
        }

        query_choice = st.selectbox("Select a sample query:", options=["(choose one)"] + list(sample_queries.keys()))
        default_query = sample_queries.get(query_choice, "MATCH (n) RETURN n LIMIT 5")

        query_input = st.text_area("Enter Cypher Query:", default_query, height=150)

        if st.button("Run Query"):
            try:
                records = run_custom_query(query_input)
                flat_records = [{k: flatten_value(v) for k, v in row.items()} for row in records]
                st.dataframe(pd.DataFrame(flat_records))
            except Exception as e:
                st.error(f"⚠️ Error running query: {e}")

    else:
        st.markdown("#### Ask a Question")

        user_q = st.text_input("Enter your question:", placeholder="e.g., Which wallets sent transactions yesterday?")

        if "generated_query" not in st.session_state:
            st.session_state["generated_query"] = ""
        if "explanation" not in st.session_state:
            st.session_state["explanation"] = ""

        if st.button("Generate Cypher Query"):
            with st.spinner("Generating Cypher query and explanation..."):
                query, _ = run_qa_question(user_q)
                st.session_state["generated_query"] = query
                explain_prompt = f"Explain the following Cypher query in 2-3 sentences:\n\n{query}"
                st.session_state["explanation"] = llm.invoke(explain_prompt).content.strip()

        if "generated_query" in st.session_state:
            st.markdown("#### Generated Cypher Query (editable)")
            edited_query = st.text_area(
                "Modify the query before running it:",
                value=st.session_state["generated_query"],
                height=150,
                key="editable_query"
            )

            with st.expander("🗞 Explanation of this query"):
                st.markdown(st.session_state["explanation"])

            if st.button("Run Edited Query"):
                try:
                    records = run_custom_query(edited_query)
                    flat_records = [{k: flatten_value(v) for k, v in row.items()} for row in records]
                    st.dataframe(pd.DataFrame(flat_records))
                except Exception as e:
                    st.error(f"⚠️ Error running query: {e}")
