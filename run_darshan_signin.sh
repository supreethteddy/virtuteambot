#!/bin/bash

# Darshan's VirtuTeams Auto Sign-In Script
# This script runs Darshan's Python automation at 9:05 AM IST, Monday-Saturday

# Set the working directory
cd /Users/supreeth/virtuteambot

# Set the PATH to include Python
export PATH="/Library/Frameworks/Python.framework/Versions/3.13/bin:$PATH"

# Log file for tracking execution
LOG_FILE="/Users/supreeth/virtuteambot/darshan_virtueteams.log"

# Create log entry
echo "$(date): Starting Darshan's VirtuTeams auto sign-in script" >> "$LOG_FILE"

# Run Darshan's Python script
python3 darshan_virtueteams.py >> "$LOG_FILE" 2>&1

# Log completion
echo "$(date): Darshan's VirtuTeams auto sign-in script completed" >> "$LOG_FILE"
echo "----------------------------------------" >> "$LOG_FILE"
