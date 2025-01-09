import requests
from amazon_paapi import AmazonAPI

def get_amazon_deals():
    # Define your Amazon API credentials
    ACCESS_KEY = 'AKIAJXUERUL33LJNDZJA'  # Your Amazon Access Key
    SECRET_KEY = 'IWJ/bhA6FKAgq2h0ldQlWQUDdFSCKgSLIPKG5nkM'  # Your Amazon Secret Key
    ASSOCIATE_TAG = 'shivaffilia00-21'  # Your Amazon Associate Tag

    # Set up Amazon API client using amazon-paapi
    amazon = AmazonAPI(ACCESS_KEY, SECRET_KEY, ASSOCIATE_TAG)

    # Example ASIN (Amazon Standard Identification Number) to search for
    item_ids = ['B07PGL2ZSL']  # Example: You can use your desired product's ASIN here

    # Fetch the product details from Amazon
    try:
        products = amazon.get_items(item_ids)

        # Extract relevant details and return them
        deals = []
        for product in products:
            deals.append({
                'title': product.title,
                'price': product.price_and_currency,
                'link': product.url
            })

        return deals
    
    except Exception as e:
        print(f"Error fetching Amazon deals: {e}")
        return []

# Example usage
amazon_deals = get_amazon_deals()
print(amazon_deals)

