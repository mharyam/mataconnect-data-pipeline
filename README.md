# MataConnect Data Pipeline

MataConnect's data pipeline is designed to process, clean, and prepare community data for use in the AI-powered search engine. This pipeline ensures that the data is accurate, consistent, and ready for embedding generation and vector search.

## Features

- **Data Scraping**: Collects raw community data from various sources.
- **Data Cleaning**: Cleans and transforms raw data into structured formats.
- **Embedding Generation**: Uses Google Vertex AI to generate embeddings for community descriptions.
- **Continuous Validation**: Ensures data integrity and consistency through automated checks.

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd mataconnect-data-pipeline
   ```

2. Create a virtual environment and activate it:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Pipeline

Run the appropriate script based on the task you need to perform
