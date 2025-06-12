"""MongoDB data loader for MataConnect."""

import os
import json
from pymongo import MongoClient


def connect_to_mongodb():
    """Connect to MongoDB Atlas cluster."""
    # Get password from environment variable for security
    password = os.getenv("MONGODB_PASSWORD")
    if not password:
        raise ValueError("Please set the MONGODB_PASSWORD environment variable")

    # MongoDB connection string
    connection_string = (
        f"mongodb+srv://maryammyusuf1802:{password}@mataconnectcluster.us9anpd."
        "mongodb.net/?retryWrites=true&w=majority&appName=MataConnectCluster"
    )

    try:
        # Create a MongoDB client
        client = MongoClient(connection_string)

        # Test the connection
        client.admin.command("ping")
        print("Successfully connected to MongoDB!")

        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise


def load_json_to_mongodb(json_file_path, database_name, collection_name):
    """Load JSON data into MongoDB Atlas."""
    try:
        # Read JSON file
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Connect to MongoDB
        client = connect_to_mongodb()
        db = client[database_name]
        collection = db[collection_name]

        # If data is a list, use insert_many, otherwise use insert_one
        if isinstance(data, list):
            result = collection.insert_many(data)
            print(f"Successfully inserted {len(result.inserted_ids)} documents")
        else:
            result = collection.insert_one(data)
            print(f"Successfully inserted document with id: {result.inserted_id}")

    except Exception as e:
        print(f"Error loading data to MongoDB: {e}")
        raise
    finally:
        if "client" in locals():
            client.close()


def get_collection_count(database_name, collection_name):
    """Get the count of documents in a collection."""
    try:
        client = connect_to_mongodb()
        db = client[database_name]
        collection = db[collection_name]
        count = collection.count_documents({})
        print(f"Number of documents in {collection_name}: {count}")
        return count
    except Exception as e:
        print(f"Error getting collection count: {e}")
        raise
    finally:
        if "client" in locals():
            client.close()


if __name__ == "__main__":
    # Example usage
    # json_file_path = "../../data/NYC_Women_Resource_Network_Database.json"
    json_file_path = "../../data/rladies_chapters.json"
    database_name = "mataconnect"
    collection_name = "communities"

    # First set your MongoDB password as an environment variable:
    # export MONGODB_PASSWORD='your_password_here'

    # Load data into MongoDB
    load_json_to_mongodb(json_file_path, database_name, collection_name)

    # Get document count
    get_collection_count(database_name, collection_name)
