# ingest/fetch_transactions.py

import requests
import time
import datetime
import json
from pathlib import Path

def fetch_bitcoin_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        market_data = data.get("market_data", {})
        timestamp = datetime.datetime.now().isoformat()

        extracted = {
            "timestamp": timestamp,
            "price_usd": market_data.get("current_price", {}).get("usd"),
            "market_cap": market_data.get("market_cap", {}).get("usd"),
            "volume_24h": market_data.get("total_volume", {}).get("usd"),
        }

        print(json.dumps(extracted, indent=2))
        return extracted
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)

    i = 0

    while i < 10:
        data = fetch_bitcoin_data()
        if data:
            # print(data)
            ts = data["timestamp"].replace(":", "-")
            out_file = out_dir / f"btc_data_{ts}.json"
            with open(out_file, "w") as f:
                json.dump(data, f, indent=2)
        time.sleep(30)

        i += 1
