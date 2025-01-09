from telegram import Bot

# Set up the bot with the token
bot = Bot(token='YOUR_TELEGRAM_BOT_API_KEY')

# Function to send messages to Telegram
def send_to_telegram(message):
    bot.send_message(chat_id='@YOUR_CHANNEL', text=message)
