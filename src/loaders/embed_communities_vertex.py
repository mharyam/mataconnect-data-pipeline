"""Embed community descriptions using Google Cloud Vertex AI."""

from google.cloud import aiplatform
from pymongo import MongoClient

from ..config import (
    GCP_PROJECT,
    GCP_REGION,
    MONGODB_URI,
    MONGODB_DATABASE,
    MONGODB_COLLECTION,
    validate_config,
)

# Validate environment variables are set
validate_config()

# Initialize Vertex AI
aiplatform.init(project=GCP_PROJECT, location=GCP_REGION)
model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko")

# Connect to MongoDB
mongo_client = MongoClient(MONGODB_URI)
collection = mongo_client[MONGODB_DATABASE][MONGODB_COLLECTION]

# Find documents without embeddings
query = {"$or": [{"embedding": {"$exists": False}}, {"embedding": []}]}
for doc in collection.find(query):
    try:
        description = doc.get("description", "")
        focus_areas = doc.get("focus_areas", [])
        focus_text = ", ".join(focus_areas)

        if not description.strip() and not focus_text.strip():
            print(f"Skipping empty content for {doc.get('name', '[Unnamed]')}")
            continue

        # Combine text fields for embedding
        combined_text = f"{description}. Focus areas: {focus_text}"

        # Get embedding from Vertex AI
        response = model.get_embeddings([combined_text])
        embedding = response[0].values

        # Save embedding to MongoDB
        collection.update_one({"_id": doc["_id"]}, {"$set": {"embedding": embedding}})

        print(f"✅ Embedded: {doc.get('name', '[Unnamed]')}")

    except Exception as e:
        print(f"❌ Error processing {doc.get('name', '[Unnamed]')}: {e}")

print("✨ Embedding process completed")
