FINANCIAL RISK & ANOMALY ANALYSIS SYSTEM - README

OVERVIEW:
This is a backend system for quant-driven financial risk analysis. It uses vector similarity search to analyze financial events and provide numerical risk scores, confidence levels, and priorities with evidence-based justifications.

ARCHITECTURE:
- Vector Database: Qdrant for storing historical financial events.
- Similarity Search: Cosine similarity on sentence embeddings.
- Scoring: Weighted averages of historical risks with thresholds.

REQUIREMENTS:
- Python 3.8+
- Docker (for Qdrant)
- Dependencies: qdrant-client, sentence-transformers, flask, pyyaml, requests

SETUP STEPS:
1. Install Python dependencies:
   pip install qdrant-client sentence-transformers flask pyyaml requests

2. Start Qdrant database:
   docker run -p 6333:6333 qdrant/qdrant
   (Verify at http://localhost:6333/dashboard)

3. Load historical data:
   cd [project folder]
   python data_ingestion.py
   (Output: "Data ingestion complete." - loads 3 sample events)

4. Start the API server:
   python api.py
   (Output: "* Running on http://127.0.0.1:5000")

5. Test the system:
   python test_api.py
   (Or manually POST to http://127.0.0.1:5000/analyze with JSON {"description": "event text"})

EXPECTED OUTPUT:
- Status Code: 200
- JSON Response Example:
  {
    "risk_score": 0.73,
    "confidence_score": 0.51,
    "priority_level": "Medium",
    "justification": {
      "retrieved_events": [
        {
          "event_id": 1,
          "similarity": 0.83,
          "historical_risk": 0.8,
          "description": "volatility_spike in equities at 2020-03-15T00:00:00Z"
        },
        ...
      ],
      "calculation_notes": "Risk: weighted avg of similarities; Confidence: avg similarity capped at 0.9"
    }
  }

FILES:
- qdrant_config.yaml: Database configuration.
- data_ingestion.py: Script to load data into Qdrant.
- risk_scorer.py: Core scoring logic.
- api.py: Flask API endpoint.
- historical_events.json: Sample historical data.
- test_api.py: Test script.
- requirements.txt: Dependencies list.

TROUBLESHOOTING:
- If API fails: Ensure Qdrant is running and data is ingested.
- If model download hangs: Wait or check internet.
- For errors, check terminal output.

SUBMISSION:
Zip the project folder for hackathon submission. This system provides evidence-based financial risk insights for societal impact.