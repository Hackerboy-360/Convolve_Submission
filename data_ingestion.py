# Data ingestion script for loading historical financial events into Qdrant
# Requires: qdrant-client, sentence-transformers (pre-trained model)
import json
import yaml  # Added import for YAML
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

print("Loading config...")
# Load config
with open('qdrant_config.yaml', 'r') as f:
    config = yaml.safe_load(f)
print("Config loaded.")

print("Connecting to Qdrant...")
client = QdrantClient(url="http://localhost:6333", verify=False)
print("Connected to Qdrant.")

print("Loading SentenceTransformer model (this may download files)...")
model = SentenceTransformer('paraphrase-MiniLM-L3-v2')  # Smaller model, 384-dim
print("Model loaded.")

print("Loading historical data...")
# Load historical data
with open('historical_events.json', 'r') as f:
    data = json.load(f)
print(f"Loaded {len(data)} events.")

print("Creating Qdrant collection...")
# Create collection if not exists
client.recreate_collection(
    collection_name=config['collection_name'],
    vectors_config={"size": config['vector_size'], "distance": config['distance']}
)
print("Collection created.")

print("Ingesting data...")
# Ingest data
for event in data:
    vector = model.encode(event['description']).tolist()  # Vectorize textual description
    payload = {
        "event_type": event["event_type"],
        "sector": event["sector"],
        "timestamp": event["timestamp"],
        "historical_risk": event["historical_risk"],
        "historical_confidence": event["historical_confidence"]
    }
    client.upsert(collection_name=config['collection_name'], points=[{"id": event["id"], "vector": vector, "payload": payload}])
    print(f"Ingested event ID {event['id']}.")

print("Data ingestion complete.")