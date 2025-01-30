import os
import csv
import random
import time
from datetime import datetime, timedelta
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from amazon_api import search_items  # Assuming this is a valid import for fetching Amazon deals.

# Constants
IST = pytz.timezone("Asia/Kolkata")
MAX_DEALS = 24
DAYS_TO_KEEP_FILES = 5
DEALS_FOLDER = "deals_csv"
TELEGRAM_CHANNEL_LINK = "https://t.me/megalootsjunction"

# X.com login details (replace with your credentials)
X_USERNAME = "shivkumaraffiliate@gmail.com"
X_PASSWORD = "Secure#2510"

# Selenium WebDriver setup
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Predefined list of hashtags for SEO
HASHTAGS = [
    "#AmazonDeals", "#MegaLoot", "#BestDeals", "#Shopping", "#Sale", "#Discounts", 
    "#Electronics", "#HotDeals", "#SaveBig", "#DealAlert", "#ShopSmart", "#MegaSale", 
    "#DealOfTheDay", "#AmazonFinds", "#OnlineShopping", "#BigSavings", "#ShopNow", 
    "#SaleAlert", "#LimitedOffer", "#ExclusiveDeals", "#MegaDiscounts", "#DealsOfTheDay"
]

# Function to remove emojis or unsupported characters
def remove_emojis(text):
    return text.encode('ascii', 'ignore').decode('ascii')

def create_csv_file(deals):
    """Create a CSV file with the fetched deals."""
    os.makedirs(DEALS_FOLDER, exist_ok=True)
    now_ist = datetime.now(IST)
    filename = f"{DEALS_FOLDER}/Deals_{now_ist.strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Price", "Original Price", "Savings", "Image URL", "Affiliate URL"])
        for deal in deals:
            writer.writerow([deal.get("title", "N/A"),
                             deal.get("price", "N/A"),
                             deal.get("original_price", "N/A"),
                             deal.get("savings", "N/A"),
                             deal.get("image", "N/A"),
                             deal.get("url", "N/A")])
    return filename

def fetch_deals():
    """Fetch deals from Amazon using PAAPI."""
    keywords = ["Electronics"]
    all_items = []

    for keyword in keywords:
        for page in range(1, 10):
            try:
                items = search_items(keyword, keyword, item_page=page)
                if items:
                    all_items.extend(items)
                time.sleep(1)  # API rate limit
            except Exception as e:
                print(f"Error fetching deals for {keyword} on page {page}: {e}")
    
    # Shuffle and limit deals to MAX_DEALS
    random.shuffle(all_items)
    return all_items[:MAX_DEALS]

def randomize_hashtags():
    """Randomly select between 1 and 4 hashtags for SEO from the predefined list."""
    num_hashtags = random.randint(1, 4)  # Randomly select between 1 to 4 hashtags
    return random.sample(HASHTAGS, num_hashtags)  # Select random hashtags

def send_to_x_com(driver, deals_csv):
    """Send deals to X (Twitter) using Selenium."""
    # Log in to X.com (formerly Twitter)
    driver.get("https://x.com/login")
    time.sleep(5)
    
    # Enter credentials
    driver.find_element(By.NAME, "text").send_keys(X_USERNAME)  # Email/Username field
    driver.find_element(By.XPATH, "//span[text()='Next']").click()  # Click Next
    time.sleep(2)

    # Wait and enter username if prompted
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@name='text']"))
    )
    username_field.send_keys("megadealsjunc")  # Replace with actual username/email
    username_field.send_keys(Keys.ENTER)

    # Enter password
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    password_field.send_keys(X_PASSWORD + Keys.RETURN)
    time.sleep(5)
    
    # Read deals from CSV
    with open(deals_csv, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for deal in reader:
            # Limit title to 50 characters
            title = deal['Title']
            brief_title = title[:50] + "..." if len(title) > 50 else title

            message = (
                f"🎉 {brief_title} 🎉\n\n"  # Use brief title here
                f"💰 Price: {deal['Price']}\n"
                f"❌ Was: {deal['Original Price']}\n"
                f"🔥 Savings: {deal['Savings']} 🔥\n\n"
                f"🛍️ Buy now: {deal['Affiliate URL']}\n\n"
                f"For more such deals, join our Telegram channel: {TELEGRAM_CHANNEL_LINK}\n\n"
            )
            
            # Add random hashtags (1 to 4 random hashtags)
            hashtags = " ".join(randomize_hashtags())
            message += hashtags

            # Remove emojis or unsupported characters from the message
            message = remove_emojis(message)

            # Post the message on X.com (Twitter)
            time.sleep(5)
            
            post_tweet = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Post text']"))
            )
            post_tweet.send_keys(message)
            post_tweet.send_keys(Keys.CONTROL, Keys.ENTER)  # Ctrl+Enter to post
            print("Tweet Posted successfully")
            time.sleep(60)

            time.sleep(3600)  # Wait for 1 hour before posting the next deal

def delete_old_csv_files():
    """Delete CSV files older than 5 days."""
    now = datetime.now(IST)
    cutoff_time = now - timedelta(days=DAYS_TO_KEEP_FILES)
    
    if os.path.exists(DEALS_FOLDER):
        for file in os.listdir(DEALS_FOLDER):
            file_path = os.path.join(DEALS_FOLDER, file)
            file_time = datetime.fromtimestamp(os.path.getmtime(file_path), tz=IST)
            
            if file_time < cutoff_time:
                os.remove(file_path)
                print(f"Deleted old file: {file}")

if __name__ == "__main__":
    try:
        # Step 1: Fetch deals and save them to a CSV file
        deals = fetch_deals()
        csv_file = create_csv_file(deals)
        print(f"Deals saved to {csv_file}")

        # Step 2: Send deals to X.com (Twitter)
        send_to_x_com(driver, csv_file)

        # Step 3: Delete old CSV files
        delete_old_csv_files()

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
