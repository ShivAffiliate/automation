import time
from amazon_deals import get_amazon_deals
from flipkart_deals import get_flipkart_deals
from send_to_telegram import send_to_telegram

def merge_deals(amazon_deals, flipkart_deals):
    # Merge both lists (you can customize this logic based on your need)
    all_deals = []
    
    for deal in amazon_deals:
        all_deals.append({
            "platform": "Amazon",
            "title": deal.get('title', ''),
            "price": deal.get('price', ''),
            "link": deal.get('link', '')
        })
    
    for deal in flipkart_deals:
        all_deals.append({
            "platform": "Flipkart",
            "title": deal.get('title', ''),
            "price": deal.get('price', ''),
            "link": deal.get('link', '')
        })
    
    return all_deals

def send_deals_to_telegram(deals):
    for deal in deals:
        message = f"{deal['platform']} Deal: {deal['title']}\nPrice: {deal['price']}\nLink: {deal['link']}"
        send_to_telegram(message)

def main():
    while True:
        # Fetch deals from Amazon and Flipkart
        amazon_deals = get_amazon_deals()
        flipkart_deals = get_flipkart_deals()
        
        # Merge the deals
        merged_deals = merge_deals(amazon_deals, flipkart_deals)
        
        # Send the merged deals to Telegram
        send_deals_to_telegram(merged_deals)
        
        # Sleep for an hour before checking again
        time.sleep(3600)

if __name__ == "__main__":
    main()
