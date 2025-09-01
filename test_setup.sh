#!/bin/bash

# Test script to verify the automation setup
echo "Testing VirtuTeams Auto Sign-In Setup"
echo "====================================="

# Check if Python is available
echo "1. Checking Python installation..."
if command -v python3 &> /dev/null; then
    echo "✅ Python3 is installed: $(python3 --version)"
else
    echo "❌ Python3 is not found in PATH"
    exit 1
fi

# Check if Playwright is installed
echo "2. Checking Playwright installation..."
if python3 -c "import playwright; print('✅ Playwright is installed')" 2>/dev/null; then
    echo "✅ Playwright is available"
else
    echo "❌ Playwright is not installed"
    exit 1
fi

# Check if the main script exists
echo "3. Checking main script..."
if [ -f "virtueteams_signin.py" ]; then
    echo "✅ Main script exists: virtueteams_signin.py"
else
    echo "❌ Main script not found"
    exit 1
fi

# Check if wrapper script exists and is executable
echo "4. Checking wrapper script..."
if [ -x "run_virtueteams_signin.sh" ]; then
    echo "✅ Wrapper script exists and is executable"
else
    echo "❌ Wrapper script not found or not executable"
    exit 1
fi

# Check cron job
echo "5. Checking cron job..."
if crontab -l | grep -q "run_virtueteams_signin.sh"; then
    echo "✅ Cron job is set up"
    echo "   Schedule: $(crontab -l | grep run_virtueteams_signin.sh)"
else
    echo "❌ Cron job not found"
    exit 1
fi

echo ""
echo "🎉 All checks passed! Your automation is ready to run."
echo "The script will run every weekday (Monday-Friday) at 9:50 AM IST"
echo "Logs will be saved to: /Users/supreeth/Documents/Python/virtueteams_auto_signin.log"
