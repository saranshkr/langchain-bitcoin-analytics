# File: ui/tabs/price_chart.py

import streamlit as st
import os
import pandas as pd
from ui.utils.autorefresh import auto_refresh


def render():
    st.markdown("### Bitcoin Price (5-pt Moving Average) & 24h Volume")
    auto_refresh(
        interval=60, 
        run_script="analysis/price_chart.py", 
        label="This chart updates every minute using live data.",
        key="price_chart"
    )
    chart_path = "btc_price_volume.png"
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
