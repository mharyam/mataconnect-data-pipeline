"""Embed community descriptions using Google Cloud Vertex AI."""

import logging
import time
from vertexai.preview.language_models import TextEmbeddingModel
from pymongo import MongoClient, UpdateOne

from ..config import (
    MONGODB_URI,
    MONGODB_DATABASE,
    MONGODB_COLLECTION,
    validate_config,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

validate_config()

DOC_LINK = "https://console.cloud.google.com/vertex-ai/publishers/google/model-garden/gemini-embedding-001"

# Connect to MongoDB
mongo_client = MongoClient(MONGODB_URI)
collection = mongo_client[MONGODB_DATABASE][MONGODB_COLLECTION]
logger.info(
    f"Connected to MongoDB database: {MONGODB_DATABASE}, collection: {MONGODB_COLLECTION}"
)

# Find documents without embeddings that have descriptions
query = {
    "$and": [
        {"$or": [{"embedding": {"$exists": False}}, {"embedding": []}]},
        {"description": {"$exists": True}},
        {"description": {"$ne": None}},
        {"description": {"$ne": ""}},
    ]
}
# Get total count before creating cursor
total_docs = collection.count_documents(query)
# Create cursor with batch size and limit
collection_query = collection.find(query).limit(50)
model = TextEmbeddingModel.from_pretrained("gemini-embedding-001")
logger.info(f"Fetched {total_docs} documents to process")


doc_to_update = []
for doc in collection_query:
    try:
        description = doc.get("description", "") or ""
        focus_areas = doc.get("focus_areas", []) or []
        focus_text = ", ".join(focus_areas)

        # if not description.strip() and not focus_text.strip():
        #     logger.warning(f"Skipping empty content for {doc.get('name', '[Unnamed]')}")
        #     continue

        # Combine text fields for embedding
        combined_text = f"{description}. Focus areas: {focus_text}".strip()

        # Get embedding from Vertex AI
        response = model.get_embeddings([combined_text])
        embedding = response[0].values

        # Save embedding to MongoDB
        # collection.update_one({"_id": doc["_id"]}, {"$set": {"embedding": embedding}})
        doc_to_update.append(
            {
                "_id": doc["_id"],
                "embedding": embedding,
            }
        )
        logger.info(f"Successfully embedded: {doc.get('name', '[Unnamed]')}")
        time.sleep(10)  # Rate limit to avoid quota issues

    except Exception as e:
        logger.error(
            f"Error processing {doc.get('name', '[Unnamed]')}: {e}", exc_info=True
        )

# Bulk update embeddings in MongoDB
if doc_to_update:
    try:
        bulk_ops = [
            UpdateOne({"_id": doc["_id"]}, {"$set": {"embedding": doc["embedding"]}})
            for doc in doc_to_update
        ]
        result = collection.bulk_write(bulk_ops, ordered=False)
        logger.info(
            f"Bulk update completed: matched={result.matched_count}, modified={result.modified_count}"
        )
    except Exception as e:
        logger.error(f"Error during bulk update: {e}", exc_info=True)

logger.info("✨ Embedding process completed")
