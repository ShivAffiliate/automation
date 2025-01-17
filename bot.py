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



# Define search keywords (could be dynamic or static)
keywords = ["Electronics", "Fashion", "Books", "Home Appliances", "Toys", "Beauty"]
IST = pytz.timezone('Asia/Kolkata')

def is_active() -> bool:
    now_utc = datetime.now(pytz.utc)
    now_ist = now_utc.astimezone(IST)

    cuurent_hour = now_ist.hour
    now = datetime.now().time()
    return MIN_HOUR <= cuurent_hour < MAX_HOUR

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
                        logging.info(f"Sending post to channel...")
                        prepared_messages = send_message(prepared_messages)
                        time.sleep(60)  # Wait 1 minute before sending the next deal
                    except Exception as e:
                        logging.error(f"Error sending message: {e}")
                        prepared_messages = prepared_messages[2:]  # Skip the problematic message
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
