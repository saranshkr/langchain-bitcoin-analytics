#!/bin/bash

# run.sh
# Usage: ./run.sh [--regen]

REGEN=false

# Parse arguments
for arg in "$@"; do
  if [ "$arg" == "--regen" ]; then
    REGEN=true
  fi
done

# Optional: Regenerate assets
if [ "$REGEN" = true ]; then
  echo "🔁 Regenerating price chart, summary, and graph..."

  echo "📉 Generating Bitcoin price chart..."
  python analysis/price_chart.py

  echo "🧠 Generating NLP summary..."
  python analysis/langchain_summary.py

  echo "🔗 Generating wallet graph..."
  python analysis/graph_pyvis.py

  echo "✅ Preprocessing complete."
fi

# Optional: short delay to ensure data is committed
echo "⏳ Waiting for data stabilization..."
sleep 5

# Start the Streamlit app
echo "🚀 Launching dashboard..."
streamlit run app.py
