import requests

def get_flipkart_deals():
    # Flipkart API URL for deals
    flipkart_url = 'https://affiliate-api.flipkart.net/affiliate/offers/json/'
    headers = {
        'Fk-Affiliate-Id': 'shivkumar32',  # Your Flipkart Affiliate ID
        'Fk-Affiliate-Token': '075da0b624da4d2b8bc5f79f3f19115b',   # Your Flipkart API Key
    }
    params = {
        'tracking_id': 'shivkumar32'  # Your Flipkart affiliate tracking ID
    }

    response = requests.get(flipkart_url, headers=headers, params=params)

    if response.status_code == 200:
        deals = response.json()  # Assuming the API returns JSON data
        return deals
    else:
        print("Error fetching Flipkart deals")
        return []

