#!/bin/bash

LOG_FILE="~/cron.log"

echo "=== $(date) ===" >> "$LOG_FILE"

source "$HOME/.virtualenvs/pimoroni/bin/activate" && \
python "$HOME/deep-work-scoreboard/main.py" --display >> "$LOG_FILE" 2>&1

echo "Exit code: $?" >> "$LOG_FILE"