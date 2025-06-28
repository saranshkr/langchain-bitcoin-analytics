# File: ui/utils/autorefresh.py

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import subprocess

def auto_refresh(interval=60, run_script=None, label=None, key="default"):
    """
    Auto-refreshes the Streamlit app and optionally runs a script before refresh.

    Parameters:
    - interval: Refresh interval in seconds (default 60)
    - run_script: Optional script path to run before refresh
    - key: Unique key for URL parameter and toggle state
    - label: Optional label to display above the toggle
    """

    # Read from URL
    query_state = st.query_params.get(f"refresh_{key}", "0")
    default_toggle = query_state == "1"

    if label:
        st.caption(label)

    toggle = st.toggle("Enable Auto-Refresh", value=default_toggle, key=f"toggle-{key}")

    # Update URL state
    st.query_params.update({f"refresh_{key}": "1" if toggle else "0"})

    if toggle:
        if run_script:
            try:
                subprocess.run(["python", run_script], check=True)
            except subprocess.CalledProcessError as e:
                st.error(f"❌ Failed to run: {run_script}\n\n{e}")
        st_autorefresh(interval=interval * 1000, key=f"autorefresh-{key}")
