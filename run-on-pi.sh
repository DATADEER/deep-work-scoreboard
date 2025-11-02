#!/bin/bash

LOG_FILE="$HOME/deep-work-scoreboard/cron.log"

echo "=== $(date) ===" >> "$LOG_FILE"

source "$HOME/.virtualenvs/pimoroni/bin/activate" && \
python -u "$HOME/deep-work-scoreboard/main.py" --display | tee -a "$LOG_FILE"

echo "Exit code: $?" >> "$LOG_FILE"