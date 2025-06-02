bitcoin-langchain-neo4j/
├── ingest/
│   └── fetch_transactions.py        # Pulls data from CoinGecko or similar
├── db/
│   └── push_to_neo4j.py             # Handles Neo4j graph population
├── analysis/
│   ├── network_analysis.py          # Graph algorithms (clustering, etc.)
│   └── langchain_summary.py         # Langchain-based summaries
├── config/
│   └── settings.yaml                # API keys, Neo4j creds, etc.
├── notebooks/
│   └── exploratory.ipynb            # Optional EDA or testing
├── requirements.txt
├── README.md
└── .env                             # For secrets (to be gitignored)
