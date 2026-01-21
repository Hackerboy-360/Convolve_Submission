# Similarity search and scoring module for financial risk analysis
# Requires: qdrant-client, sentence-transformers
import yaml
from qdrant_client import QdrantClient

# Load config
with open('qdrant_config.yaml', 'r') as f:
    config = yaml.safe_load(f)

client = None  # Initialize lazily

def compute_scores(input_event):
    global client
    if client is None:
        client = QdrantClient(url="http://localhost:6333", verify=False)
    from sentence_transformers import SentenceTransformer # pyright: ignore[reportMissingImports]
    model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
    
    # Vectorize input
    vector = model.encode(input_event['description']).tolist()
    
    # Retrieve top-5 similar events
    results = client.query_points(
        collection_name=config['collection_name'],
        query=vector,
        limit=5
    ).points
    
    # Aggregate scores
    total_weight = 0
    risk_sum = 0
    confidence_list = []
    retrieved = []
    
    for hit in results:
        similarity = hit.score
        payload = hit.payload
        risk_sum += similarity * payload['historical_risk']
        total_weight += similarity
        confidence_list.append(similarity)
        retrieved.append({
            "event_id": hit.id,
            "similarity": similarity,
            "historical_risk": payload['historical_risk'],
            "description": f"{payload['event_type']} in {payload['sector']} at {payload['timestamp']}"
        })
    
    risk_score = risk_sum / total_weight if total_weight > 0 else 0
    confidence_score = min(sum(confidence_list) / len(confidence_list), 0.9) if confidence_list else 0
    
    priority = "High" if risk_score > 0.7 and confidence_score > 0.7 else "Medium" if risk_score > 0.5 or confidence_score < 0.5 else "Low"
    
    return {
        "risk_score": round(risk_score, 2),
        "confidence_score": round(confidence_score, 2),
        "priority_level": priority,
        "justification": {
            "retrieved_events": retrieved,
            "calculation_notes": "Risk: weighted avg of similarities; Confidence: avg similarity capped at 0.9"
        }
    }