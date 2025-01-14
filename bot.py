from typing import List
import telegram
from amazon_api import search_items
from create_messages import create_item_html
import time
from datetime import datetime
import pytz
import random
from consts import *
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ********** Author: Samir Salman **********

# Define search keywords (could be dynamic or static)
keywords = ["Electronics", "Fashion", "Books", "Home Appliances", "Toys", "Beauty"]

# Mapping keywords to respective channel IDs
category_channel_mapping = {
    "Electronics": "@electronics_channel",
    "Fashion": "@fashion_channel",
    "Books": "@books_channel",
    "Home Appliances": "@home_appliances_channel",
    "Toys": "@toys_channel",
    "Beauty": "@beauty_channel"
}

IST = pytz.timezone('Asia/Kolkata')

def is_active() -> bool:
    """Check if the bot should be active based on current time."""
    now_utc = datetime.now(pytz.utc)
    now_ist = now_utc.astimezone(IST)

    current_hour = now_ist.hour
    return MIN_HOUR <= current_hour < MAX_HOUR

def send_message(bot: telegram.Bot, category: str, item_data: List[str]) -> List[str]:
    """Send a single message to the appropriate Telegram channel based on category."""
    try:
        # Get the channel for the category
        channel = category_channel_mapping.get(category)
        if channel:
            bot.send_message(
                chat_id=channel,
                text=item_data[0],
                reply_markup=item_data[1],
                parse_mode=telegram.ParseMode.HTML,
            )
            logging.info(f"Message sent successfully to {channel}.")
        else:
            logging.warning(f"No channel mapped for category: {category}")
    except Exception as e:
        logging.error(f"Error sending message to {category} channel: {e}")
    
    return item_data[2:]  # Return the remaining items in the list

def run_bot(bot: telegram.Bot, keywords: List[str]) -> None:
    """Run the bot to fetch and send deals."""
    while True:
        try:
            all_items = []
            
            # Iterate over all keywords to fetch items
            for keyword in keywords:
                for page in range(1, 10):
                    try:
                        # Fetch items for the keyword
                        items = search_items(keyword, keyword, item_page=page)
                        if items:
                            all_items.extend(items)
                            logging.info(f"Fetched {len(items)} items for keyword: {keyword}, page: {page}")
                        else:
                            logging.warning(f"No items returned for keyword: {keyword}, page: {page}")
                    except Exception as e:
                        logging.error(f"Error fetching items for keyword: {keyword}, page: {page}: {e}")
                    time.sleep(1)  # API rate limit
            
            if not all_items:
                logging.warning("No items fetched from the API. Retrying after a short pause.")
                time.sleep(300)  # Wait before retrying
                continue

            logging.info(f"Total items fetched: {len(all_items)}")

            # Shuffle results
            random.shuffle(all_items)

            # Generate HTML messages
            try:
                prepared_messages = create_item_html(all_items)
                logging.info(f"Prepared {len(prepared_messages)//2} messages for posting.")
            except Exception as e:
                logging.error(f"Error generating messages: {e}")
                continue

            # While there are items to send
            while prepared_messages:
                if is_active():
                    try:
                        logging.info(f"Sending post to channels...")
                        current_item_data = prepared_messages.pop(0)  # Get the first item for sending
                        category = current_item_data[2]  # Assuming the 3rd element contains the category
                        prepared_messages = send_message(bot, category, current_item_data)
                        time.sleep(60)  # Wait 1 minute before sending the next deal
                    except Exception as e:
                        logging.error(f"Error sending message: {e}")
                        continue
                else:
                    logging.info(f"Bot inactive during off hours.")
                    time.sleep(300)  # Wait 5 minutes before checking again

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    try:
        bot = telegram.Bot(token=TOKEN)
        logging.info("Bot instance created successfully.")
        run_bot(bot=bot, keywords=keywords)
    except Exception as e:
        logging.critical(f"Failed to initialize bot: {e}")
