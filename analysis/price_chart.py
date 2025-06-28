# File: analysis/price_chart.py
# Description: Plots Bitcoin price (as moving average) and volume from Neo4j with 2-day filter and volume note

import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# Neo4j driver
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def fetch_price_volume_data():
    query = '''
    MATCH (t:Transaction)
    RETURN t.timestamp AS timestamp, t.price_usd AS price, t.volume_24h AS volume
    ORDER BY t.timestamp
    '''
    with driver.session() as session:
        result = session.run(query)
        data = [{"timestamp": r["timestamp"], "price": r["price"], "volume": r["volume"]} for r in result]
    return pd.DataFrame(data)

def plot_price_volume(df, output_file="btc_price_volume.png"):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)

    # Filter to last 2 days
    cutoff = datetime.datetime.now() - datetime.timedelta(days=7)
    df = df[df.index >= cutoff].copy()

    # Compute 5-point moving average for price
    df["MA_5"] = df["price"].rolling(window=5).mean()

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax1.set_xlabel("Timestamp")
    ax1.set_ylabel("Price (USD)", color="tab:red")
    ax1.plot(df.index, df["MA_5"], color="tab:red", label="5-pt MA")
    ax1.tick_params(axis='y', labelcolor="tab:red")

    # Plot volume bars if enough data
    ax2 = ax1.twinx()
    if len(df) >= 12:
        ax2.set_ylabel("Volume (24h, USD)", color="tab:blue")
        ax2.bar(df.index, df["volume"], width=0.001, alpha=0.3, color="tab:blue", label="Volume")
        ax2.tick_params(axis='y', labelcolor="tab:blue")
    else:
        ax2.set_yticks([])
        ax2.set_ylabel("Volume (insufficient data)", color="gray")

    plt.title("Bitcoin Price (Moving Avg) and Volume - Last 2 Days")
    fig.tight_layout()
    plt.savefig(output_file)
    print(f"✅ Chart saved as {output_file}")

if __name__ == "__main__":
    print("📡 Fetching BTC price/volume data...")
    df = fetch_price_volume_data()
    if not df.empty:
        plot_price_volume(df)
    else:
        print("⚠️ No data found in Neo4j.")
    driver.close()
