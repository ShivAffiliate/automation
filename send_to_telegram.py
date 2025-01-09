from telegram import Bot

# Set up the bot with the token
bot = Bot(token='7928675863:AAHF-5tTGWdJ-yw8MdWzgs_sJnyWSDwAApw')

# Function to send messages to Telegram
def send_to_telegram(message):
    bot.send_message(chat_id='@TrendifyStoreBot', text=message)  # Replace @TrendifyStoreBot with your channel's chat ID
