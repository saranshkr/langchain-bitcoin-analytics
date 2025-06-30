# 📊 Real-time Bitcoin Analytics Dashboard with LangChain & Neo4j

A real-time dashboard for exploring Bitcoin transaction data using Neo4j, LangChain (LLM-powered Q&A), and Streamlit. Supports natural language query generation, graph visualization, wallet activity stats, and price/volume trends.

<br>

## 🧩 Features

- **Real-time ingestion** of Bitcoin transactions
- **Cypher query generation** from natural language using LangChain + Mistral
- **Interactive wallet graph** (Pyvis)
- **Statistical summaries** (daily tx counts, top wallets, 24h stats)
- **Price chart** with 5-point moving average & 24h volume bars
- **Q&A mode** for explainable query interaction
- **Auto-refresh support** per tab
- **Custom ingestion pipeline** (fetch, push, simulate)

<br>

## 📁 Project Structure

```
.
├── README.md
├── analysis
│   ├── graph_pyvis.py             # Generates wallet graph from Neo4j
│   ├── langchain_qa.py            # Natural language to Cypher query
│   ├── langchain_summary.py       # Summary generator using LangChain
│   └── price_chart.py             # BTC price/volume chart
├── app.py                         # Streamlit dashboard entry point
├── ingest
│   ├── fetch_transactions.py      # Get BTC data from external API
│   ├── push_to_neo4j.py           # Push new transactions to Neo4j
│   ├── run_pipeline.py            # Runs fetch + push + simulation as threads
│   └── simulate_wallets.py        # Adds Wallet nodes & edges to txns
├── requirements.txt
├── run.sh                         # Shell script to regenerate data + launch dashboard
├── todo.txt
├── ui
│   ├── tabs
│   │   ├── price_chart.py
│   │   ├── query_explorer.py
│   │   ├── stats_tab.py
│   │   ├── summary_tab.py
│   │   └── wallet_graph.py
│   └── utils
│       ├── autorefresh.py         # Utility for per-tab auto-refresh
│       └── helpers.py             # Shared Neo4j query helpers
└── utils
    └── cleanup.py                 # Optional cleanup script
```

<br>

## 🚀 Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

Ensure you have [Ollama](https://ollama.com/) running with the `mistral` model for local LLM inference.

### 2. Create your `.env` file:

```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

<br>

## 📌 Example Workflow

### Start the ingestion pipeline

```bash
python ingest/run_pipeline.py
```

Use Ctrl+C to stop the pipeline

### Run the regeneration scripts (optional) and launch dashboard

```bash
bash run.sh [--regen]
```

<br>

## 💬 Example Questions

- Who received the highest transaction volume this week?
- Show wallets that sent transactions yesterday
- What are total transactions in the last 24 hours?
- Top 5 receivers this month?

<br>

## 🧠 Powered by

- [Neo4j](https://neo4j.com/) for graph storage
- [LangChain](https://github.com/langchain-ai/langchain) + [Ollama](https://ollama.com/) for local LLM reasoning
- [Streamlit](https://streamlit.io/) for interactive UI

<br>

## 🧠 Author

**Saransh Kumar**  
🔗 [linkedin.com/in/saransh-kr](https://linkedin.com/in/saransh-kr)  
🔗 [github.com/saranshkr](https://github.com/saranshkr)
