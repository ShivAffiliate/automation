import time
import requests
from telegram import Bot

# Function to fetch Amazon deals using amazon-paapi library
from amazon_paapi import AmazonAPI

def get_amazon_deals():
    # Your Amazon API credentials
    ACCESS_KEY = 'AKIAJXUERUL33LJNDZJA'  # Replace with your Access Key
    SECRET_KEY = 'IWJ/bhA6FKAgq2h0ldQlWQUDdFSCKgSLIPKG5nkM'  # Replace with your Secret Key
    ASSOCIATE_TAG = 'shivaffilia00-21'  # Replace with your Associate Tag

    # Set up Amazon API client using amazon-paapi
    amazon = AmazonAPI(ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG)

    # Example ASIN (Amazon Standard Identification Number) to search for
    item_ids = ['B07PGL2ZSL']  # Replace with the ASINs you are interested in

    try:
        # Fetch the product details from Amazon
        products = amazon.get_items(item_ids)

        deals = []
        for product in products:
            deals.append({
                'platform': 'Amazon',
                'title': product.title,
                'price': product.price_and_currency,
                'link': product.url
            })
        return deals
    except Exception as e:
        print(f"Error fetching Amazon deals: {e}")
        return []

# Function to fetch Flipkart deals
def get_flipkart_deals():
    flipkart_url = 'https://affiliate-api.flipkart.net/affiliate/offers/json/'
    headers = {
        'Fk-Affiliate-Id': 'shivkumar32',  # Replace with your Flipkart Affiliate ID
        'Fk-Affiliate-Token': '075da0b624da4d2b8bc5f79f3f19115b',   # Replace with your Flipkart API Key
    }
    params = {
        'tracking_id': 'shivkumar32'  # Replace with your Flipkart affiliate tracking ID
    }

    response = requests.get(flipkart_url, headers=headers, params=params)

    if response.status_code == 200:
        deals = response.json()['offers']  # Assuming the API returns 'offers' as the deals
        flipkart_deals = []
        for deal in deals:
            flipkart_deals.append({
                'platform': 'Flipkart',
                'title': deal.get('title', 'No title'),
                'price': deal.get('price', 'Price not available'),
                'link': deal.get('url', '#')
            })
        return flipkart_deals
    else:
        print("Error fetching Flipkart deals")
        return []

# Function to merge Amazon and Flipkart deals
def merge_deals(amazon_deals, flipkart_deals):
    all_deals = amazon_deals + flipkart_deals
    return all_deals

# Function to send messages to Telegram
def send_to_telegram(message):
    bot = Bot(token='7928675863:AAHF-5tTGWdJ-yw8MdWzgs_sJnyWSDwAApw')  # Replace with your Telegram Bot token
    bot.send_message(chat_id='@testchannel09012025', text=message)  # Replace with your channel's username

# Function to send deals to Telegram
def send_deals_to_telegram(deals):
    for deal in deals:
        message = f"{deal['platform']} Deal:\n{deal['title']}\nPrice: {deal['price']}\nLink: {deal['link']}"
        send_to_telegram(message)

# Main function to automate fetching and sending deals
def main():
    while True:
        # Fetch deals from Amazon and Flipkart
        amazon_deals = get_amazon_deals()
        flipkart_deals = get_flipkart_deals()
        
        # Merge the deals
        merged_deals = merge_deals(amazon_deals, flipkart_deals)
        
        # Send the merged deals to Telegram
        send_deals_to_telegram(merged_deals)
        
        # Sleep for 1 hour before fetching new deals
        time.sleep(3600)  # 3600 seconds = 1 hour

if __name__ == "__main__":
    main()
