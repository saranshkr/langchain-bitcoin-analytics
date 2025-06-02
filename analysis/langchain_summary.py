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

def summarize_data(data):
    """Generate NLP summary using Mistral."""
    price_series = [f"{record['time']}: ${record['price']}" for record in data]
    volume_series = [f"${record['volume']}" for record in data]

    prompt = ChatPromptTemplate.from_template("""
    You are a data analyst. Here is a time series of Bitcoin prices:

    {data}

    Summarize the trends you observe. Mention any increase, decrease, or stability in price and volume. Keep it short and precise.
    """)

    formatted = prompt.format_messages(data="\n".join(price_series))
    response = llm.invoke(formatted)
    return response.content

if __name__ == "__main__":
    print("📡 Fetching Bitcoin data from Neo4j...")
    data = fetch_prices()
    print("🧠 Generating summary using Mistral...\n")
    summary = summarize_data(data)
    print("🔍 NLP Summary:\n")
    print(summary)
