# 📊 Real-time Bitcoin Analytics with LangChain & Neo4j

This project ingests real-time Bitcoin market data, stores it in a property graph (Neo4j), and enables interactive analytics via a modular Streamlit dashboard. Natural language Q&A is supported using local LLMs via Ollama.

---

## 🔧 Tech Stack

- **Python** – ETL pipeline, data transformation, and orchestration
- **Neo4j (AuraDB / Local)** – Graph database for modeling BTC transactions
- **LangChain + Ollama (Mistral)** – Local LLM for query generation and summarization
- **Streamlit** – Dashboard for real-time visualization and interaction
- **Pyvis, Altair** – Graph and chart visualizations
- **CoinGecko API** – Source of live Bitcoin price and volume data

---

## 📂 Project Structure

```
langchain-bitcoin-analytics/
├── app.py                             # Main dashboard entrypoint
├── analysis/                          # Scripts for querying and summarization
│   ├── graph_pyvis.py                 # Visualize transaction graph with Pyvis
│   ├── langchain_qa.py                # Natural language → Cypher interface
│   ├── langchain_summary.py           # Summary generation with Mistral
│   └── price_chart.py                 # BTC price/volume visualization
├── db/
│   └── push_to_neo4j.py               # Push parsed data into Neo4j
├── ingest/
│   └── fetch_transactions.py          # Fetch real-time BTC market data
├── pipeline/
│   └── run_pipeline.py                # Optional: Run ingestion + simulation in one go
├── simulation/
│   └── simulate_wallets.py            # Generate synthetic wallets and link to txns
├── ui/
│   ├── tabs/                          # Code for individual Streamlit dashboard tabs
│   └── utils/                         # Shared functions: query, graph, refresh
├── utils/
│   └── cleanup.py                     # Dev utility for cleaning/reseting the database
├── notebooks/                         # Optional: Jupyter-based exploration
├── requirements.txt
├── .env                               # API keys and Neo4j credentials
├── README.md
└── todo.txt                           # Developer TODOs and feature planning
```

---

## ✅ Features

- 📥 Real-time BTC market data ingestion (price, volume, market cap)
- 🔄 Synthetic transaction simulation using deterministic wallet links
- 🧠 Natural language Q&A with LangChain + Mistral via Ollama
- 🔗 Interactive graph exploration with Pyvis
- 📊 Multi-tab Streamlit dashboard: price chart, wallet graph, summary, stats, Q&A
- 🧾 Editable Cypher queries with explanations and live results

---

## 🚀 Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Ollama + Mistral model**
   ```bash
   ollama run mistral
   ```

3. **Create a `.env` file with your Neo4j credentials**
   ```
   NEO4J_URI=bolt://localhost:7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_password
   ```

4. **Run the Streamlit dashboard**
   ```bash
   streamlit run app.py
   ```

---

## 📌 Example Workflow

```bash
# Step 1: Fetch BTC market data
python ingest/fetch_transactions.py

# Step 2: Push to Neo4j
python db/push_to_neo4j.py

# Step 3: Simulate wallets and generate relations
python simulation/simulate_wallets.py

# Step 4: Generate charts and summaries
python analysis/price_chart.py
python analysis/langchain_summary.py
python analysis/graph_pyvis.py
```

---

## 💡 Demo Use Cases

- Ask: “Which wallets received the most transactions last week?”
- See: Real-time rolling Bitcoin price + volume chart
- Explore: Transaction graph with colored wallets and directional edges
- Edit: Cypher queries with inline explanations and results

---

## 🧠 Author

**Saransh Kumar**  
📍 College Park, MD  
🔗 [linkedin.com/in/saransh-kr](https://linkedin.com/in/saransh-kr)  
🔗 [github.com/saranshkr](https://github.com/saranshkr)