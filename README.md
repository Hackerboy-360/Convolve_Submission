# Financial Risk & Anomaly Analysis System

## Overview
A backend system for quant-driven financial risk analysis using vector similarity search. Accepts financial event descriptions and outputs numerical risk scores, confidence levels, and priority with evidence-based justifications.

## Architecture
- **Vector Database**: Qdrant for storing and retrieving similar historical events.
- **Similarity Search**: Cosine similarity on sentence embeddings.
- **Scoring Logic**: Weighted averages of historical risks, thresholds for priority.

## Setup
1. Install dependencies: `pip install qdrant-client sentence-transformers flask pyyaml requests`.
2. Start Qdrant: `docker run -p 6333:6333 qdrant/qdrant`.
3. Load data: `python data_ingestion.py`.
4. Run API: `python api.py`.
5. Test: `python test_api.py`.

## API Usage
- **Endpoint**: POST `/analyze`
- **Input**: `{"description": "event description"}`
- **Output**: JSON with `risk_score` (0-1), `confidence_score` (0-1), `priority_level` (Low/Medium/High), `justification` (retrieved events).

## Files
- `qdrant_config.yaml`: Database config.
- `data_ingestion.py`: Loads historical data.
- `risk_scorer.py`: Scoring logic.
- `api.py`: Flask API.
- `historical_events.json`: Sample data.
- `test_api.py`: Test script.
