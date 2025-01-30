from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random

def create_item_html(items):
    response = []
    print(f'{5 * "*"} Creating post {5 * "*"}')

    # Shuffle items to randomize order
    random.shuffle(items)

    # Iterate over items to build the message
    for item in items:
        if 'off' in item:
            # Ensure there's a URL, otherwise use a placeholder
            url = item.get("url", "#")
            
            # Create a buy button
            keyboard = [
                [InlineKeyboardButton("🛍️ Buy Now 🛒", callback_data='buy', url=url)],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            # Create message body
            html = ""

            # Add product image as a clickable link (if available)
            if 'image_url' in item:
                html += f'<a href="{item["image_url"]}"><img src="{item["image_url"]}" width="200" height="200"></a>\n\n'

            # Add the title
            html += f"🎉 <b>{item['title']}</b> 🎉\n\n"

            # Display the original price if available
            if 'original_price' in item:
                html += f"❌ <i>Was: ₹{item['original_price']}</i>\n"

            # Display the current price
            html += f"💰 <b>Now: ₹{item['price']}</b>\n\n"

            # Show savings if available
            if 'savings' in item:
                html += f"🔥 <b>You Save: ₹{item['savings']}!</b> 🔥\n\n"

            # Append the message and reply markup to the response
            response.append(html)
            response.append(reply_markup)

    return response
