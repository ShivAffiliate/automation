#!/bin/bash
if ! pgrep -f "python3 x.py" > /dev/null; then
    # If not running, start x.py
    echo "Starting x.py..."
    nohup python3 x.py > x.log 2>&1 &
    echo "x.py started with PID $!"
else
    echo "x.py is already running."
fi
