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
        crontab -l 2>/dev/null | grep run_virtueteams_signin.sh || echo "No cron job found"
        echo ""
        echo "Recent logs:"
        if [ -f "virtueteams_auto_signin.log" ]; then
            tail -10 virtueteams_auto_signin.log
        else
            echo "No log file found yet"
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
        echo "Disabling auto sign-in (removing cron job)..."
        crontab -l 2>/dev/null | grep -v run_virtueteams_signin.sh | crontab -
        echo "Auto sign-in disabled"
        ;;
    "enable")
        echo "Enabling auto sign-in (adding cron job)..."
        echo "50 9 * * 1-5 /Users/supreeth/Documents/Python/run_virtueteams_signin.sh" | crontab -
        echo "Auto sign-in enabled for weekdays at 9:50 AM IST"
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
        echo "Schedule: Weekdays (Mon-Fri) at 9:50 AM IST"
        ;;
esac
