#!/bin/bash

# VirtuTeams Auto Sign-In Script
# This script runs the Python automation every weekday at 9:50 AM IST

# Set the working directory
cd /Users/supreeth/Documents/Python

# Set the PATH to include Python
export PATH="/Library/Frameworks/Python.framework/Versions/3.13/bin:$PATH"

# Log file for tracking execution
LOG_FILE="/Users/supreeth/Documents/Python/virtueteams_auto_signin.log"

# Create log entry
echo "$(date): Starting VirtuTeams auto sign-in script" >> "$LOG_FILE"

# Run the Python script
python3 virtueteams_signin.py >> "$LOG_FILE" 2>&1

# Log completion
echo "$(date): VirtuTeams auto sign-in script completed" >> "$LOG_FILE"
echo "----------------------------------------" >> "$LOG_FILE"
