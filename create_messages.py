from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import random

# This function allows us to create an HTML message to send
# You can edit all fields of the message using HTML syntax

def create_item_html(items):
    response = []
    print(f'{5 * "*"} Creating post {5 * "*"}')

    # Shuffling items
    random.shuffle(items)

    # Iterate over items
    for item in items:
        # Skip if item is None
        if item is None:
            continue
        
        # Check if required keys are present in item
        if 'title' not in item or 'url' not in item or 'image' not in item or 'price' not in item:
            print(f"Skipping item with missing required fields: {item}")
            continue  # Skip items with missing required data
        
        # Creating buy button
        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now 🛒", callback_data='buy', url=item.get("url"))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Creating message body
        html = ""
        html += f"🎁 <b>{item['title']}</b> 🎁\n\n"

        # Check if description exists and add it
        if 'description' in item:
            html += f"{item['description']}\n"

        # Add image (invisible link to avoid break in layout)
        html += f"<a href='{item['image']}'>&#8205;</a>\n"

        # Check if 'savings' exists and add original price if available
        if 'savings' in item and 'original_price' in item:
            html += f"❌ Was: ₹{item['original_price']} ❌\n\n"

        # Add current price
        html += f"💰 <b>Now at: {item['price']}</b> 💰\n\n"

        # Add savings if present
        if 'savings' in item:
            html += f"✅ <b>You Save: ₹{item['savings']}</b> ✅\n\n"

        # Link for more details
        html += f"<b><a href='{item['url']}'>Click here for more details</a></b>"

        # Append HTML and reply markup to the response
        response.append(html)
        response.append(reply_markup)

    return response
