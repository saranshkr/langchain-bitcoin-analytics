# File: ui/tabs/summary_tab.py
# Description: Streamlit tab for displaying NLP-generated summaries of recent Bitcoin trends and wallet activity

import streamlit as st
import os
from ui.utils.autorefresh import auto_refresh


def render():
    st.markdown("### Langchain NLP Summary")
    auto_refresh(
        interval=3600,
        run_script="analysis/langchain_summary.py",
        label="Summary auto-refreshes every hour.",
        key="summary"
    )
    summary_path = "latest_summary.txt"
    if os.path.exists(summary_path):
        with open(summary_path, "r") as f:
            summary = f.read()
        st.text_area("Generated Summary", summary, height=200)
    else:
        st.info("No summary found. Run your `langchain_summary.py` script to generate one.")
