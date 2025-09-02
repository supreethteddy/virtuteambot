#!/bin/bash

# VirtuTeams Automation Monitor
# This script helps you monitor the automation status

echo "🔍 VirtuTeams Automation Monitor"
echo "================================"
echo ""

# Check current time
echo "🕐 Current Time:"
echo "   UTC: $(date -u)"
echo "   IST: $(TZ='Asia/Kolkata' date)"
echo ""

# Check if it's a weekday
WEEKDAY=$(date +%u)
if [ "$WEEKDAY" -ge 1 ] && [ "$WEEKDAY" -le 5 ]; then
    echo "✅ Today is a weekday (Day $WEEKDAY)"
    echo "   Automation should run today!"
else
    echo "❌ Today is weekend (Day $WEEKDAY)"
    echo "   No automation scheduled for weekends"
fi
echo ""

# Show schedule
echo "📅 Automation Schedule:"
echo "   9:25 AM IST - Schedule Verification"
echo "   9:30 AM IST - Supreeth Sign-In (Primary)"
echo "   9:32 AM IST - Supreeth Sign-In (Backup)"
echo "   9:35 AM IST - Kavya Sign-In (Primary)"
echo "   9:37 AM IST - Kavya Sign-In (Backup)"
echo ""

# Check if it's time for automation
CURRENT_HOUR=$(TZ='Asia/Kolkata' date +%H)
CURRENT_MINUTE=$(TZ='Asia/Kolkata' date +%M)

if [ "$CURRENT_HOUR" = "09" ]; then
    if [ "$CURRENT_MINUTE" -ge 25 ] && [ "$CURRENT_MINUTE" -le 40 ]; then
        echo "🎯 AUTOMATION TIME!"
        echo "   The workflows should be running now or soon"
        echo "   Check GitHub Actions for status"
    else
        echo "⏰ Not automation time yet"
    fi
else
    echo "⏰ Not automation time (9:25-9:40 AM IST)"
fi
echo ""

echo "🔗 GitHub Actions Links:"
echo "   Repository: https://github.com/supreethteddy/virtuteambot"
echo "   Actions: https://github.com/supreethteddy/virtuteambot/actions"
echo ""

echo "📊 Monitoring Tips:"
echo "   1. Check GitHub Actions tab for workflow runs"
echo "   2. Look for green checkmarks (✅) for success"
echo "   3. Download screenshots from artifacts"
echo "   4. Check logs for any errors"
echo ""

echo "🛠️ Manual Testing:"
echo "   You can manually trigger workflows from GitHub Actions tab"
echo "   Click 'Run workflow' button to test anytime"
