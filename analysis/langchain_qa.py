# File: analysis/langchain_qa.py
# Description: Convert natural language questions into Cypher queries and run them on Neo4j

import os
from dotenv import load_dotenv
from neo4j import GraphDatabase
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

# Load environment variables
load_dotenv()
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

# Choose model source here
llm = ChatOllama(model="mistral", temperature=0.0)

# Cypher generation prompt
TEMPLATE = """
You are an expert Cypher developer assisting a user in querying a property graph database using natural language. 
Use the following schema to generate accurate and executable Cypher queries.

Graph Schema:
(:Wallet)-[:SENT]->(:Transaction)-[:RECEIVED_BY]->(:Wallet)

Transaction node properties:
- timestamp (datetime)
- tx_id (string)
- price_usd (float)
- market_cap (float)
- volume_24h (float)

Guidelines:
- Use clear, consistent variable names like `wallet`, `txn`, `volume`, `received_count`, etc.
- Use multiple WITH clauses for complex logic or intermediate aggregations.
- Never reuse an alias in the same WITH clause where it’s being defined.
- Return only specific scalar properties (e.g., `wallet.address`, `txn.tx_id`) unless asked for whole nodes.
- Prefer aggregations like `count()`, `sum()`, `avg()`, `max()` over `collect()`, unless lists are required.
- Do not include comments, explanations, or extra spacing — only the final Cypher query.
- Your output must be syntactically correct and ready to execute in Neo4j without modification.
- If the question is ambiguous, make a useful, reasonable assumption and generate the best-fit query.
- If the user refers to an earlier question (e.g., “same as before”), handle context appropriately for follow-ups.

Examples:

Q: Show the addresses of the first 5 wallets  
A:  
MATCH (w:Wallet)  
RETURN w.address  
LIMIT 5

Q: What are the total number of transactions in the last 24 hours?  
A:  
MATCH (t:Transaction)  
WHERE datetime(t.timestamp) > datetime() - duration('P1D')  
RETURN count(*) AS txn_count

Q: Who received the highest transaction volume this week?  
A:  
MATCH (t:Transaction)-[:RECEIVED_BY]->(w:Wallet)  
WHERE datetime(t.timestamp) > datetime() - duration('P7D')  
WITH w, sum(t.volume_24h) AS total_volume  
RETURN w.address AS wallet, total_volume  
ORDER BY total_volume DESC  
LIMIT 1

Q: {question}

A:
"""

prompt = PromptTemplate(input_variables=["question"], template=TEMPLATE)

def run_qa_question(question: str):
    formatted_prompt = prompt.format(question=question)
    cypher = llm.invoke(formatted_prompt).content.strip()

    print("\nQuestion:", question)
    print("\nGenerated Cypher:\n", cypher)

    try:
        with driver.session() as session:
            result = session.run(cypher)
            records = [dict(r) for r in result]
        return cypher, records
    except Exception as e:
        return cypher, f"❌ Error running query: {e}"

# CLI testing
if __name__ == "__main__":
    user_q = input("🔍 Ask a question: ")
    query, output = run_qa_question(user_q)

    print("\n✅ Cypher Query:\n", query)
    print("\n📊 Result:\n", output)
