#!/bin/bash

# Check if python3 bot.py is already running
if ! pgrep -f "python3 bot.py" > /dev/null
then
    # If not running, start the bot
    echo "Starting bot.py..."
    nohup python3 bot.py &
else
    echo "bot.py is already running."
fi
