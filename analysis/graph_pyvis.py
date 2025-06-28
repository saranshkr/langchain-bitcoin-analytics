# File: analysis/graph_pyvis.py
# Description: Visualizes wallet-transaction graph as an interactive HTML using Pyvis

import os
from pyvis.network import Network
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

# Connect to Neo4j
driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def fetch_graph_data(limit=30):
    query = f'''
    MATCH (w:Wallet)-[:SENT]->(t:Transaction)
    RETURN w.address AS from, t.tx_id AS to
    UNION
    MATCH (t:Transaction)-[:RECEIVED_BY]->(w:Wallet)
    RETURN t.tx_id AS from, w.address AS to
    LIMIT {limit}
    '''
    with driver.session() as session:
        result = session.run(query)
        return [(record["from"], record["to"]) for record in result]

def create_pyvis_graph(edges, output_file="wallet_graph.html"):
    net = Network(height="800px", width="100%", directed=True)
    net.barnes_hut()

    for from_node, to_node in edges:
        net.add_node(from_node, label=from_node, color="skyblue" if "wallet_" in from_node else "orange")
        net.add_node(to_node, label=to_node, color="skyblue" if "wallet_" in to_node else "orange")
        net.add_edge(from_node, to_node)

    net.set_options('''
    var options = {
      "nodes": {
        "font": {
          "size": 16
        }
      },
      "edges": {
        "arrows": {
          "to": {
            "enabled": true
          }
        }
      },
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      }
    }
    ''')
    net.show(output_file)
    print(f"✅ Graph exported to: {output_file}")

if __name__ == "__main__":
    print("📡 Fetching wallet graph from Neo4j...")
    edges = fetch_graph_data()
    print(f"🔗 {len(edges)} edges loaded.")
    create_pyvis_graph(edges)
    driver.close()
