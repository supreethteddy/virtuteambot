#!/bin/bash

# VirtuTeams Auto Sign-In Management Script
# This script helps you manage the automated sign-in process

case "$1" in
    "start")
        echo "Starting VirtuTeams auto sign-in..."
        ./run_virtueteams_signin.sh
        ;;
    "test")
        echo "Testing the automation setup..."
        ./test_setup.sh
        ;;
    "status")
        echo "Checking automation status..."
        echo "Cron job status:"
        echo "Supreeth & Kavya:"
        crontab -l 2>/dev/null | grep run_virtueteams_signin.sh || echo "  No cron job found"
        echo "Darshan:"
        crontab -l 2>/dev/null | grep run_darshan_signin.sh || echo "  No cron job found"
        echo ""
        echo "Recent logs:"
        if [ -f "virtueteams_auto_signin.log" ]; then
            echo "Supreeth & Kavya logs:"
            tail -10 virtueteams_auto_signin.log
        else
            echo "No Supreeth & Kavya log file found yet"
        fi
        if [ -f "darshan_virtueteams.log" ]; then
            echo ""
            echo "Darshan logs:"
            tail -10 darshan_virtueteams.log
        else
            echo "No Darshan log file found yet"
        fi
        ;;
    "logs")
        echo "Showing full log file..."
        if [ -f "virtueteams_auto_signin.log" ]; then
            cat virtueteams_auto_signin.log
        else
            echo "No log file found"
        fi
        ;;
    "disable")
        echo "Disabling auto sign-in (removing cron jobs)..."
        crontab -l 2>/dev/null | grep -v run_virtueteams_signin.sh | grep -v run_darshan_signin.sh | crontab -
        echo "Auto sign-in disabled for all accounts"
        ;;
    "enable")
        echo "Enabling auto sign-in (adding cron jobs)..."
        # Add existing cron job for Supreeth and Kavya
        echo "50 9 * * 1-5 /Users/supreeth/Documents/Python/run_virtueteams_signin.sh" | crontab -
        # Add new cron job for Darshan at 9:05 AM IST, Monday-Saturday
        (crontab -l 2>/dev/null; echo "5 9 * * 1-6 /Users/supreeth/virtuteambot/run_darshan_signin.sh") | crontab -
        echo "Auto sign-in enabled:"
        echo "  - Supreeth & Kavya: Weekdays at 9:50 AM IST"
        echo "  - Darshan: Monday-Saturday at 9:05 AM IST"
        ;;
    "screenshots")
        echo "Recent screenshots:"
        ls -la *.png 2>/dev/null | head -10 || echo "No screenshots found"
        ;;
    *)
        echo "VirtuTeams Auto Sign-In Management"
        echo "=================================="
        echo ""
        echo "Usage: $0 {start|test|status|logs|disable|enable|screenshots}"
        echo ""
        echo "Commands:"
        echo "  start       - Run the sign-in script manually"
        echo "  test        - Test the automation setup"
        echo "  status      - Check cron job and recent logs"
        echo "  logs        - Show full log file"
        echo "  disable     - Disable automatic execution"
        echo "  enable      - Enable automatic execution"
        echo "  screenshots - Show recent screenshots"
        echo ""
        echo "Schedule:"
        echo "  - Supreeth & Kavya: Weekdays (Mon-Fri) at 9:50 AM IST"
        echo "  - Darshan: Monday-Saturday at 9:05 AM IST"
        ;;
esac
