# 📊 Real-time Bitcoin Analysis with Langchain and Neo4j

This project ingests real-time Bitcoin transaction data, stores it in a graph database (Neo4j), and uses local open-source language models via Ollama to generate natural language summaries of trends in the data.

---

## 🔧 Tech Stack

- **Python**: Data ingestion, transformation, and orchestration
- **Neo4j (AuraDB Cloud)**: Graph database for storing transaction data
- **Langchain + Ollama (Mistral)**: Local LLM for summarization, no API keys needed
- **CoinGecko API**: Public Bitcoin market data source

---

## 📦 Project Structure

```
bitcoin-langchain-neo4j/
├── ingest/
│   └── fetch_transactions.py        # Fetches BTC data and saves JSON
├── db/
│   └── push_to_neo4j.py             # Pushes data to Neo4j AuraDB
├── analysis/
│   └── langchain_summary.py         # Generates summaries using Mistral
├── config/
│   └── settings.yaml                # Config file (not yet used)
├── data/
│   └── raw/                         # Stored BTC data snapshots
├── .env                             # Environment variables (Neo4j credentials)
├── requirements.txt
└── README.md
```

---

## ✅ Features Implemented

- ✅ Real-time BTC data ingestion from CoinGecko
- ✅ Graph modeling and storage in Neo4j
- ✅ Summarization using Mistral via Ollama (no API keys)
- ✅ CLI-based output of trends and summaries

---

## 📥 Setup Instructions

1. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Ollama and run Mistral**  
   ```bash
   ollama run mistral
   ```

3. **Create a `.env` file with your Neo4j Aura credentials**  
   ```
   NEO4J_URI=neo4j+s://xxxxx.databases.neo4j.io
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_password
   ```

4. **Run scripts**  
   - Ingest new data:
     ```bash
     python ingest/fetch_transactions.py
     ```
   - Push data to Neo4j:
     ```bash
     python db/push_to_neo4j.py
     ```
   - Generate summary:
     ```bash
     python analysis/langchain_summary.py
     ```

---

## 🚀 Next Steps

- Add wallet-to-transaction relationships
- Integrate Langchain Q&A interface
- Build a Streamlit dashboard for live interaction

---

## 🧠 Author

Saransh Kumar  
📍 College Park, MD  
🔗 [linkedin.com/in/saransh-kr](https://linkedin.com/in/saransh-kr) | [github.com/saranshkr](https://github.com/saranshkr)
