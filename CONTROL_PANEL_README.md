# VirtuTeams Automation Control Panel

A modern web-based control panel for managing VirtuTeams automation with user management, scheduling, and date exclusions.

## 🚀 Features

### 👥 User Management
- **Add New Users**: Create new automation accounts with credentials
- **Edit Users**: Modify user details, login times, and active days
- **Delete Users**: Remove users and their associated scripts
- **Test Automation**: Run automation scripts manually for testing

### 📅 Schedule Management
- **Custom Login Times**: Set individual login times for each user
- **Day Toggles**: Enable/disable automation for specific days (Monday-Saturday)
- **Visual Schedule**: See all users' schedules at a glance

### 📆 Date Exclusions
- **Calendar Integration**: Select specific dates to exclude from automation
- **User-Specific**: Exclude dates for individual users
- **Reason Tracking**: Add reasons for exclusions (holidays, sick leave, etc.)

### 📊 Monitoring & Logs
- **Real-time Dashboard**: View automation statistics
- **Execution Logs**: Track automation runs and results
- **Screenshot Management**: View and download automation screenshots
- **Status Monitoring**: See which users are active today

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip3
- Modern web browser

### Quick Start
1. **Run the startup script**:
   ```bash
   ./start_control_panel.sh
   ```

2. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

### Manual Setup
1. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   python3 -m playwright install chromium
   ```

2. **Start the application**:
   ```bash
   python3 app.py
   ```

## 📱 How to Use

### Adding a New User
1. Click **"Add New User"** button
2. Fill in the user details:
   - **Name**: User's display name
   - **Email**: VirtuTeams login email
   - **Password**: VirtuTeams password
   - **Login Time**: When automation should run (HH:MM format)
   - **Active Days**: Select which days automation should run
3. Click **"Save User"**

### Managing Schedules
- **View Schedule**: Go to "Schedule & Exclusions" tab to see all users' schedules
- **Edit Schedule**: Click the edit button on any user to modify their schedule
- **Day Toggles**: Use checkboxes to enable/disable specific days

### Excluding Dates
1. Go to **"Schedule & Exclusions"** tab
2. Click **"Exclude Date"** button
3. Select the user and date to exclude
4. Add an optional reason
5. Click **"Exclude Date"**

### Testing Automation
- Click the **play button** (▶️) next to any user to test their automation
- Check the **"Automation Logs"** tab to see results
- View screenshots in the logs section

## 🗄️ Database

The control panel uses SQLite database (`virtueteams.db`) with three main tables:

- **users**: Stores user credentials and schedule settings
- **excluded_dates**: Tracks dates when automation should not run
- **automation_logs**: Records automation execution history

## 🔧 API Endpoints

### Users
- `GET /api/users` - Get all users
- `POST /api/users` - Add new user
- `PUT /api/users/<id>` - Update user
- `DELETE /api/users/<id>` - Delete user

### Excluded Dates
- `GET /api/excluded-dates` - Get excluded dates
- `POST /api/excluded-dates` - Add excluded date
- `DELETE /api/excluded-dates/<id>` - Remove excluded date

### Logs
- `GET /api/logs` - Get automation logs

### Testing
- `POST /api/test-automation/<user_id>` - Test user automation

## 🎨 Interface Features

### Dashboard
- **Total Users**: Count of all configured users
- **Active Today**: Users scheduled to run today
- **Excluded Dates**: Number of excluded dates
- **Recent Logs**: Latest automation logs

### Responsive Design
- Works on desktop, tablet, and mobile devices
- Modern Bootstrap 5 interface
- Dark/light theme support
- Real-time updates

### User Experience
- **Intuitive Navigation**: Tab-based interface
- **Visual Feedback**: Status badges and icons
- **Error Handling**: Clear error messages
- **Loading States**: Spinner indicators during operations

## 🔒 Security Features

- **Password Protection**: User passwords are stored securely
- **Input Validation**: All inputs are validated
- **Error Handling**: Graceful error handling and user feedback
- **Database Security**: SQLite with proper parameterized queries

## 📁 File Structure

```
virtuteambot/
├── app.py                          # Flask backend application
├── requirements.txt                # Python dependencies
├── start_control_panel.sh         # Startup script
├── templates/
│   └── index.html                 # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css              # Custom styles
│   └── js/
│       └── app.js                 # Frontend JavaScript
├── virtueteams.db                 # SQLite database (created automatically)
└── *_virtueteams.py               # Generated user scripts
```

## 🚨 Troubleshooting

### Common Issues

1. **Port 5000 already in use**:
   - Change the port in `app.py`: `app.run(port=5001)`

2. **Playwright browser not found**:
   - Run: `python3 -m playwright install chromium`

3. **Database errors**:
   - Delete `virtueteams.db` to reset the database

4. **Permission errors**:
   - Make sure scripts are executable: `chmod +x *.sh`

### Getting Help

- Check the browser console for JavaScript errors
- Check the terminal for Python errors
- Verify all dependencies are installed
- Ensure Playwright browsers are installed

## 🔄 Integration with Existing System

The control panel integrates seamlessly with your existing automation:

- **Existing Scripts**: Your current Kavya, Supreeth, and Darshan scripts continue to work
- **GitHub Actions**: Existing workflows remain unchanged
- **Cron Jobs**: Local cron jobs continue to run
- **New Users**: Automatically creates individual scripts for new users

## 🎯 Next Steps

1. **Start the control panel**: `./start_control_panel.sh`
2. **Add your existing users**: Import Kavya, Supreeth, and Darshan
3. **Configure schedules**: Set up individual login times
4. **Test automation**: Use the test buttons to verify everything works
5. **Set up exclusions**: Add any holidays or special dates

Enjoy your new VirtuTeams Automation Control Panel! 🎉
