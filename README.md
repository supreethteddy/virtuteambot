# VirtuTeams Auto Sign-In Bot

Automated browser bot that signs into VirtuTeams and clicks the "Sign In" button for time tracking every weekday at 9:50 AM IST.

## 🚀 Cloud Deployment Options

### Option 1: GitHub Actions (Recommended - FREE)

**Steps:**
1. Create a new GitHub repository
2. Upload the `.github/workflows/virtueteams.yml` file
3. The automation will run automatically every weekday at 9:50 AM IST

**Benefits:**
- ✅ Completely FREE
- ✅ No server management required
- ✅ Automatic scheduling
- ✅ Screenshots saved as artifacts
- ✅ Manual trigger option for testing

**Schedule:** Monday-Friday at 9:50 AM IST (4:20 AM UTC)

### Option 2: AWS EC2 (Low Cost)

**Steps:**
1. Launch an EC2 instance (t3.micro is sufficient)
2. Install dependencies:
```bash
sudo apt update
sudo apt install python3 python3-pip chromium-browser
pip3 install playwright
playwright install chromium
```
3. Upload your script and set up cron:
```bash
crontab -e
# Add: 50 9 * * 1-5 /path/to/run_virtueteams_signin.sh
```

**Cost:** ~$8-10/month

### Option 3: DigitalOcean Droplet

**Steps:**
1. Create a $5/month droplet
2. Follow same setup as AWS EC2
3. Set up cron job

**Cost:** $5/month

### Option 4: Railway/Render (Free Tier)

**Steps:**
1. Create account on Railway or Render
2. Connect your GitHub repository
3. Set up cron job or use their scheduling

**Cost:** FREE (with limitations)

## 📁 Files Structure

```
├── .github/workflows/virtueteams.yml  # GitHub Actions workflow
├── virtueteams_signin.py              # Main Python script
├── run_virtueteams_signin.sh          # Local wrapper script
├── manage_virtueteams.sh              # Management script
└── test_setup.sh                      # Test script
```

## 🔧 Configuration

### Update Credentials
Edit the `users` list in `virtueteams_signin.py`:

```python
users = [
    {"name": "Your Name", "email": "your.email@example.com", "password": "your_password"},
    # Add more users if needed
]
```

### Update Schedule
For GitHub Actions, edit the cron expression in `.github/workflows/virtueteams.yml`:

```yaml
- cron: '20 4 * * 1-5'  # 9:50 AM IST on weekdays
```

## 📊 Monitoring

### GitHub Actions
- Check the "Actions" tab in your repository
- View logs and download screenshots
- Manual trigger available for testing

### Local/Server Deployment
- Logs saved to: `virtueteams_auto_signin.log`
- Screenshots saved as: `*_dashboard_before.png`, `*_after_signin.png`

## 🛠️ Troubleshooting

### Common Issues:
1. **Login fails** - Check credentials and network connectivity
2. **Button not found** - Website structure may have changed
3. **Timeout errors** - Network issues or slow loading

### Debug Steps:
1. Run manually: `python3 virtueteams_signin.py`
2. Check screenshots for visual debugging
3. Review logs for error messages

## 🔒 Security Notes

- Store credentials securely (use environment variables in production)
- Consider using 2FA if available
- Monitor logs for any suspicious activity

## 📅 Schedule Details

- **Days:** Monday, Tuesday, Wednesday, Thursday, Friday
- **Time:** 9:50 AM IST (India Standard Time)
- **Excludes:** Weekends (Saturday, Sunday)
- **Timezone:** UTC+5:30 (IST)

## 🎯 Features

- ✅ Automatic login to VirtuTeams
- ✅ Location spoofing (Bangalore, India)
- ✅ Smart button detection (4 different methods)
- ✅ Screenshot capture for verification
- ✅ Error handling and logging
- ✅ Cloud deployment ready
- ✅ Manual trigger capability
