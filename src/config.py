"""Configuration management for MataConnect data pipeline."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB Configuration
MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGODB_URI = os.getenv(
    "MONGODB_URI",
    f"mongodb+srv://maryammyusuf1802:{MONGODB_PASSWORD}@mataconnectcluster.us9anpd.mongodb.net/?retryWrites=true&w=majority&appName=MataConnectCluster",
)
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "mataconnect")
MONGODB_COLLECTION = os.getenv("MONGODB_COLLECTION", "communities")

# Google Cloud Configuration
GCP_PROJECT = os.getenv("GCP_PROJECT")
GCP_REGION = os.getenv("GCP_REGION", "us-central1")


# Validate required environment variables
def validate_config():
    """Validate that all required environment variables are set."""
    required_vars = [
        ("MONGODB_PASSWORD", MONGODB_PASSWORD),
        ("GCP_PROJECT", GCP_PROJECT),
    ]

    missing = [var[0] for var in required_vars if not var[1]]

    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}\n"
            "Please set them in your .env file or environment."
        )


# You can call this function when your application starts
validate_config()
