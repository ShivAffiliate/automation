#!/bin/bash

# Check if python3 bot.py is already running
if ! pgrep -f "python3 bot.py" > /dev/null; then
    # If not running, start the bot
    echo "Starting bot.py..."
    nohup python3 bot.py > bot.log 2>&1 &
    echo "bot.py started with PID $!"
else
    echo "bot.py is already running."
fi
