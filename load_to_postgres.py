import os
import json
import psycopg2
import logging
from datetime import datetime
from dotenv import load_dotenv

# --- Configuration & Setup ---
load_dotenv()

# Database connection details
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")

# Data lake path
TODAY = datetime.now().strftime('%Y-%m-%d')
RAW_MESSAGES_DIR = os.path.join('data', 'raw', 'telegram_messages', TODAY)

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


def load_enrichment_data(cursor):
    """Loads enriched image detection data into PostgreSQL."""
    ENRICHED_OUTPUT_DIR = os.path.join('data', 'enriched', TODAY)
    detections_file = os.path.join(
        ENRICHED_OUTPUT_DIR, 'image_detections.json')

    if not os.path.exists(detections_file):
        logging.warning("No image detection data file found to load.")
        return

    # Create table for enriched data
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw.image_detections (
            id SERIAL PRIMARY KEY,
            data JSONB,
            loaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
    """)

    with open(detections_file, 'r', encoding='utf-8') as f:
        detections = json.load(f)
        for detection_data in detections:
            cursor.execute(
                "INSERT INTO raw.image_detections (data) VALUES (%s);",
                (json.dumps(detection_data),)
            )
    logging.info(f"Loaded {len(detections)
                           } image detections into raw.image_detections.")


def load_data():
    # Connects to PostgreSQL, creates schema and table, and loads JSON data.
    conn = None
    try:
        # Establish database connection
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()
        logging.info("Successfully connected to PostgreSQL.")

        # Create raw schema and table if they don't exist
        cursor.execute("CREATE SCHEMA IF NOT EXISTS raw;")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw.telegram_messages (
                id SERIAL PRIMARY KEY,
                data JSONB,
                file_name VARCHAR(255),
                loaded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
        """)
        conn.commit()
        logging.info(
            "Schema 'raw' and table 'raw.telegram_messages' are ready.")

        # Check if the directory exists
        if not os.path.exists(RAW_MESSAGES_DIR):
            logging.warning(f"Directory not found: {
                            RAW_MESSAGES_DIR}. No new data to load.")
            return

        # Iterate over JSON files in the data lake directory
        for filename in os.listdir(RAW_MESSAGES_DIR):
            if filename.endswith('.json'):
                file_path = os.path.join(RAW_MESSAGES_DIR, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    messages = json.load(f)
                    for message_data in messages:
                        # Insert each message as a new row with its JSONB data
                        cursor.execute(
                            "INSERT INTO raw.telegram_messages (data, file_name) VALUES (%s, %s);",
                            (json.dumps(message_data), filename)
                        )
                logging.info(f"Loaded data from {filename}.")

        conn.commit()
        logging.info("All new data has been loaded successfully.")
        load_enrichment_data(cursor)

    except (Exception, psycopg2.Error) as error:
        logging.error(
            f"Error while connecting to or working with PostgreSQL: {error}")
    finally:
        # Close the database connection
        if conn:
            cursor.close()
            conn.close()
            logging.info("PostgreSQL connection closed.")


if __name__ == "__main__":
    load_data()
