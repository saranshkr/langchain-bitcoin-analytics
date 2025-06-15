# analysis/langchain_summary.py

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Neo4j connection setup
driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

# Use Mistral model running locally via Ollama
llm = ChatOllama(model="mistral")

def fetch_prices(n=10):
    """Fetch Bitcoin price data from Neo4j."""
    with driver.session() as session:
        result = session.run(
            """
            MATCH (t:Transaction)
            RETURN t.timestamp AS time, t.price_usd AS price, t.volume_24h AS volume
            ORDER BY t.timestamp ASC
            LIMIT $n
            """, {"n": n}
        )
        return list(result)


def get_top_wallets(n=3):
    """Query Neo4j for top n most active receiving wallets."""
    with driver.session() as session:
        result = session.run(
            """
            MATCH (w:Wallet)<-[:RECEIVED_BY]-(:Transaction)
            RETURN w.address AS address, count(*) AS received_count
            ORDER BY received_count DESC
            LIMIT $n
            """, {"n": n}
        )
        return list(result)


def summarize_data(price_data, wallet_data):
    price_series = [f"{record['time']}: ${record['price']}" for record in price_data]

    wallet_lines = [f"{w['address']}: {w['received_count']} txns received" for w in wallet_data]
    wallet_info = "\n".join(wallet_lines)

    prompt = ChatPromptTemplate.from_template("""
    You are a data analyst. Here is Bitcoin time series price data:

    {price_data}

    And here is wallet activity:

    {wallet_data}

    Provide a short, clear summary covering price trends and wallet activity.
    """)

    formatted = prompt.format_messages(
        price_data="\n".join(price_series),
        wallet_data=wallet_info
    )
    response = llm.invoke(formatted)
    return response.content


if __name__ == "__main__":
    print("📡 Fetching Bitcoin data from Neo4j...")
    price_data = fetch_prices()
    wallet_data = get_top_wallets()

    print("🧠 Generating combined summary...\n")
    summary = summarize_data(price_data, wallet_data)

    print("🔍 NLP Summary:\n")
    print(summary)

    with open("latest_summary.txt", "w") as f:
        f.write(summary)
