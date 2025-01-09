import os
import time
import requests
from telegram import Bot
from amazon_paapi import AmazonApi


def get_amazon_deals():
    # Load credentials from environment variables
    ACCESS_KEY = os.getenv('AMAZON_ACCESS_KEY')
    SECRET_KEY = os.getenv('AMAZON_SECRET_KEY')
    ASSOCIATE_TAG = os.getenv('AMAZON_ASSOCIATE_TAG')
    
    # Set your country code to 'IN' for India
    COUNTRY = os.getenv('AMAZON_COUNTRY', 'IN')  # Default to 'IN' (India) if not set

    if not (ACCESS_KEY and SECRET_KEY and ASSOCIATE_TAG):
        print("Amazon API credentials are not set. Please configure environment variables.")
        return []

    # Initialize Amazon API client with 'IN' country code for India
    amazon = AmazonApi(ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG, COUNTRY)
    item_ids = ['B07PGL2ZSL']  # Replace with actual ASINs

    try:
        # Fetch product details
        products = amazon.get_items(item_ids)
        deals = []
        for product in products:
            deal = {
                'platform': 'Amazon',
                'title': product.get('ItemInfo', {}).get('Title', {}).get('DisplayValue', 'No Title'),
                'price': product.get('Offers', {}).get('Listings', [{}])[0].get('Price', {}).get('DisplayAmount', 'Price Not Available'),
                'link': product.get('DetailPageURL', '#')
            }
            deals.append(deal)
        return deals
    except Exception as e:
        print(f"Error fetching Amazon deals: {e}")
        return []


def get_flipkart_deals():
    flipkart_url = 'https://affiliate-api.flipkart.net/affiliate/offers/json/'
    headers = {
        'Fk-Affiliate-Id': os.getenv('FLIPKART_AFFILIATE_ID'),
        'Fk-Affiliate-Token': os.getenv('FLIPKART_AFFILIATE_TOKEN')
    }

    if not (headers['Fk-Affiliate-Id'] and headers['Fk-Affiliate-Token']):
        print("Flipkart API credentials are not set. Please configure environment variables.")
        return []

    try:
        response = requests.get(flipkart_url, headers=headers)
        if response.status_code == 200:
            offers = response.json().get('offers', [])
            deals = []
            for offer in offers:
                deal = {
                    'platform': 'Flipkart',
                    'title': offer.get('title', 'No Title'),
                    'price': offer.get('price', 'Price Not Available'),
                    'link': offer.get('url', '#')
                }
                deals.append(deal)
            return deals
        else:
            print(f"Error fetching Flipkart deals: {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching Flipkart deals: {e}")
        return []


def send_to_telegram(bot, chat_id, message):
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")


def send_deals_to_telegram(bot, chat_id, deals):
    for deal in deals:
        message = (
            f"{deal['platform']} Deal:\n"
            f"Title: {deal['title']}\n"
            f"Price: {deal['price']}\n"
            f"Link: {deal['link']}"
        )
        send_to_telegram(bot, chat_id, message)


def main():
    # Configure environment variables for sensitive information
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

    if not (telegram_token and telegram_chat_id):
        print("Telegram bot token or chat ID is not set. Please configure environment variables.")
        return

    bot = Bot(token=telegram_token)

    while True:
        # Fetch deals from Amazon and Flipkart
        amazon_deals = get_amazon_deals()
        flipkart_deals = get_flipkart_deals()

        # Merge the deals from both platforms
        all_deals = amazon_deals + flipkart_deals

        # Send the merged deals to Telegram
        send_deals_to_telegram(bot, telegram_chat_id, all_deals)

        # Wait for 1 hour before fetching deals again
        time.sleep(3600)  # 3600 seconds = 1 hour


if __name__ == "__main__":
    main()
