import os
import json
import logging
import asyncio
from datetime import datetime, timezone
from dotenv import load_dotenv
from datetime import timedelta

from telethon.sync import TelegramClient
from telethon.errors import FloodWaitError

# --- Configuration & Setup ---

# Load environment variables from .env file
load_dotenv()
API_ID = os.getenv("TELEGRAM_API_ID")
API_HASH = os.getenv("TELEGRAM_API_HASH")
PHONE_NUMBER = os.getenv("TELEGRAM_PHONE_NUMBER")

# Define target Telegram channels
TARGET_CHANNELS = [
    'tikvahpharma',
    'lobelia4cosmetics',
    'CheMed123',
]

# Define data storage paths
TODAY = datetime.now().strftime('%Y-%m-%d')
RAW_MESSAGES_DIR = os.path.join('data', 'raw', 'telegram_messages', TODAY)
RAW_IMAGES_DIR = os.path.join('data', 'raw', 'telegram_images', TODAY)

# Create directories if they don't exist
os.makedirs(RAW_MESSAGES_DIR, exist_ok=True)
os.makedirs(RAW_IMAGES_DIR, exist_ok=True)

# --- Logging Setup ---

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Configure logging to write to both a file and the console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('logs', 'scraper.log')),
        logging.StreamHandler()
    ]
)

# --- Main Scraping Logic ---


async def scrape_channel(client, channel_username):
    """Scrapes messages and images from a single Telegram channel."""
    logging.info(f"Starting scrape for channel: {channel_username}")
    messages_data = []

    try:
        # Get the channel entity
        channel = await client.get_entity(channel_username)

        # Iterate through messages
        # Limit for demonstration
        async for message in client.iter_messages(channel, limit=200):

            # Skip messages older than 24 hours
            print("custom check", message.date, " now ",
                  datetime.now(tz=timezone.utc))
            print("custom check", message.date - datetime.now(tz=timezone.utc))
            if message.date < datetime.now(tz=timezone.utc) - timedelta(days=1):
                continue

            image_path = None
            if message.photo:
                # Download image if the message contains one
                try:
                    # Define a unique path for the image
                    image_path = os.path.join(
                        RAW_IMAGES_DIR, f"{message.id}.jpg")
                    await message.download_media(file=image_path)
                    logging.info(f"Downloaded image {
                                 message.id}.jpg from {channel_username}")
                except Exception as e:
                    logging.error(f"Failed to download image {
                                  message.id} from {channel_username}: {e}")
                    image_path = None  # Reset path if download fails

            # Convert message to dictionary and add image path
            message_dict = message.to_dict()
            message_dict['image_path'] = image_path
            messages_data.append(message_dict)

        # Save messages to a JSON file
        if messages_data:
            output_path = os.path.join(
                RAW_MESSAGES_DIR, f"{channel_username}.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(messages_data, f, ensure_ascii=False,
                          indent=4, default=str)
            logging.info(
                f"Successfully saved {len(messages_data)} messages from {
                    channel_username} to {output_path}"
            )

    except FloodWaitError as e:
        logging.error(f"Flood wait error for {
                      channel_username}. Waiting for {e.seconds} seconds.")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        logging.error(f"An error occurred while scraping {
                      channel_username}: {e}")


async def main():
    # Main function to initialize the client and scrape all target channels.
    logging.info("--- Starting Telegram Scraping Session ---")

    # Use a session file to avoid logging in every time
    async with TelegramClient('telegram_session', API_ID, API_HASH) as client:
        for channel in TARGET_CHANNELS:
            await scrape_channel(client, channel)

    logging.info("--- Telegram Scraping Session Finished ---")


if __name__ == "__main__":
    # Run the main asynchronous function
    asyncio.run(main())
