# File: analysis/langchain_qa.py
# Description: Convert natural language questions into Cypher queries and run them on Neo4j

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

# Load env variables and connect
load_dotenv()
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

# Initialize local LLM
llm = ChatOllama(model="mistral")

# Few-shot prompt: user question → Cypher query
TEMPLATE = """
You are an expert Cypher developer. Convert the following natural language question into a Cypher query using the schema below.

Graph Schema:
(:Wallet)-[:SENT]->(:Transaction)-[:RECEIVED_BY]->(:Wallet)
Transaction has properties: timestamp, tx_id, price_usd, market_cap, volume_24h

Rules:
- Use clear variable names and Cypher best practices.
- If you need to compute a value using an alias (e.g., abs(sent - received)), first define the counts in one WITH clause, then use a second WITH clause for the computation.
- Never reuse an alias in the same WITH clause where it’s defined.
- Return meaningful data — not whole nodes unless explicitly requested.
- Output ONLY the Cypher query, nothing else.
- The query must be immediately executable in Neo4j.

Examples:

Q: Show 5 wallet addresses
A:
MATCH (w:Wallet)
RETURN w.address
LIMIT 5

Q: Transactions in the last 24 hours
A:
MATCH (t:Transaction)
WHERE datetime(t.timestamp) > datetime() - duration('P1D')
RETURN t.tx_id, t.timestamp

Q: Top 3 receivers yesterday
A:
MATCH (t:Transaction)-[:RECEIVED_BY]->(w:Wallet)
WHERE date(datetime(t.timestamp)) = date() - duration('P1D')
RETURN w.address AS wallet, count(*) AS received
ORDER BY received DESC
LIMIT 3

Q: {question}
A:
"""

prompt = PromptTemplate(input_variables=["question"], template=TEMPLATE)

def run_qa_question(question):
    formatted_prompt = prompt.format(question=question)
    cypher = llm.invoke(formatted_prompt).content.strip()

    print("\n📥 Prompt:\n", formatted_prompt)
    print("\n📤 Generated Cypher:\n", cypher)

    try:
        with driver.session() as session:
            result = session.run(cypher)
            records = [dict(r) for r in result]
        return cypher, records
    except Exception as e:
        return cypher, f"❌ Error running query: {e}"

if __name__ == "__main__":
    user_q = input("🔍 Ask a question: ")
    query, output = run_qa_question(user_q)

    print("\n✅ Cypher Query:\n", query)
    print("\n📊 Result:\n", output)
