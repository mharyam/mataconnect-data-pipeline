from google.cloud import aiplatform
from pymongo import MongoClient


GCP_PROJECT = "your-gcp-project-id"
GCP_REGION = "us-central1"  # or "europe-west4" etc.

MONGO_URI = "your-mongodb-connection-string"
DATABASE_NAME = "mataconnect"
COLLECTION_NAME = "communities"


aiplatform.init(project=GCP_PROJECT, location=GCP_REGION)
model = aiplatform.TextEmbeddingModel.from_pretrained("textembedding-gecko")


mongo_client = MongoClient(MONGO_URI)
collection = mongo_client[DATABASE_NAME][COLLECTION_NAME]


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
