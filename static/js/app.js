// VirtuTeams Control Panel JavaScript

let users = [];
let excludedDates = [];
let logs = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    updateCurrentTime();
    setInterval(updateCurrentTime, 1000);
    loadAllData();
    
    // Set default time to 9:00 AM
    document.getElementById('loginTime').value = '09:00';
    
    // Set default days (Monday to Saturday)
    for (let i = 1; i <= 6; i++) {
        document.getElementById(`day${i}`).checked = true;
    }
});

// Update current time display
function updateCurrentTime() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', {
        timeZone: 'Asia/Kolkata',
        hour12: false
    });
    document.getElementById('current-time').textContent = timeString + ' IST';
}

// Load all data from the API
async function loadAllData() {
    try {
        await Promise.all([
            loadUsers(),
            loadExcludedDates(),
            loadLogs()
        ]);
        updateDashboard();
    } catch (error) {
        console.error('Error loading data:', error);
        showAlert('Error loading data', 'danger');
    }
}

// Load users
async function loadUsers() {
    try {
        const response = await fetch('/api/users');
        users = await response.json();
        renderUsersTable();
        updateUserSelect();
    } catch (error) {
        console.error('Error loading users:', error);
    }
}

// Load excluded dates
async function loadExcludedDates() {
    try {
        const response = await fetch('/api/excluded-dates');
        excludedDates = await response.json();
        renderExcludedDates();
    } catch (error) {
        console.error('Error loading excluded dates:', error);
    }
}

// Load logs
async function loadLogs() {
    try {
        const response = await fetch('/api/logs');
        logs = await response.json();
        renderLogsTable();
    } catch (error) {
        console.error('Error loading logs:', error);
    }
}

// Render users table
function renderUsersTable() {
    const tbody = document.getElementById('users-table');
    tbody.innerHTML = '';
    
    users.forEach(user => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>
                <strong>${user.name}</strong>
            </td>
            <td>${user.email}</td>
            <td>
                <span class="badge bg-primary">${user.login_time}</span>
            </td>
            <td>
                ${getDayLabels(user.enabled_days)}
            </td>
            <td>
                <span class="status-badge status-active">Active</span>
            </td>
            <td>
                <button class="btn btn-sm btn-outline-primary me-1" onclick="editUser(${user.id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-outline-success me-1" onclick="testAutomation(${user.id})">
                    <i class="fas fa-play"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger" onclick="deleteUser(${user.id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Get day labels for display
function getDayLabels(enabledDays) {
    const dayNames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    return enabledDays.map(day => dayNames[day - 1]).join(', ');
}

// Render excluded dates
function renderExcludedDates() {
    const container = document.getElementById('excluded-dates-list');
    container.innerHTML = '';
    
    if (excludedDates.length === 0) {
        container.innerHTML = '<p class="text-muted">No excluded dates</p>';
        return;
    }
    
    excludedDates.forEach(item => {
        const div = document.createElement('div');
        div.className = 'excluded-date-item';
        div.innerHTML = `
            <div class="excluded-date-info">
                <div class="excluded-date-user">${item.user_name}</div>
                <div class="excluded-date-date">${formatDate(item.excluded_date)}</div>
                ${item.reason ? `<div class="excluded-date-reason">${item.reason}</div>` : ''}
            </div>
            <button class="btn btn-sm btn-outline-danger" onclick="removeExcludedDate(${item.id})">
                <i class="fas fa-times"></i>
            </button>
        `;
        container.appendChild(div);
    });
}

// Render logs table
function renderLogsTable() {
    const tbody = document.getElementById('logs-table');
    tbody.innerHTML = '';
    
    logs.forEach(log => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${log.user_name}</strong></td>
            <td>${formatDate(log.execution_date)}</td>
            <td>
                <span class="status-badge ${log.status === 'success' ? 'status-success' : 'status-error'}">
                    ${log.status}
                </span>
            </td>
            <td>
                <div class="log-message">${log.message || 'No message'}</div>
            </td>
            <td>${formatDateTime(log.created_at)}</td>
            <td>
                ${log.screenshot_path ? 
                    `<button class="btn btn-sm btn-outline-info" onclick="viewScreenshot('${log.screenshot_path}')">
                        <i class="fas fa-image"></i>
                    </button>` : ''
                }
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Update dashboard statistics
function updateDashboard() {
    document.getElementById('total-users').textContent = users.length;
    document.getElementById('excluded-dates').textContent = excludedDates.length;
    document.getElementById('recent-logs').textContent = logs.length;
    
    // Calculate active today
    const today = new Date().toISOString().split('T')[0];
    const activeToday = users.filter(user => {
        const todayDay = new Date().getDay();
        const dayNumber = todayDay === 0 ? 7 : todayDay; // Convert Sunday (0) to 7
        return user.enabled_days.includes(dayNumber.toString());
    }).length;
    document.getElementById('active-today').textContent = activeToday;
    
    renderScheduleOverview();
}

// Render schedule overview
function renderScheduleOverview() {
    const container = document.getElementById('schedule-overview');
    container.innerHTML = '';
    
    // Group users by login time
    const scheduleGroups = {};
    users.forEach(user => {
        if (!scheduleGroups[user.login_time]) {
            scheduleGroups[user.login_time] = [];
        }
        scheduleGroups[user.login_time].push(user);
    });
    
    // Sort by time
    const sortedTimes = Object.keys(scheduleGroups).sort();
    
    sortedTimes.forEach(time => {
        const group = scheduleGroups[time];
        group.forEach(user => {
            const div = document.createElement('div');
            div.className = 'schedule-item';
            div.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <div class="schedule-time">${time}</div>
                        <div class="schedule-user">${user.name}</div>
                        <div class="schedule-days">${getDayLabels(user.enabled_days)}</div>
                    </div>
                    <div>
                        <span class="status-badge status-active">Active</span>
                    </div>
                </div>
            `;
            container.appendChild(div);
        });
    });
}

// Show add user modal
function showAddUserModal() {
    document.getElementById('userModalTitle').textContent = 'Add New User';
    document.getElementById('userForm').reset();
    document.getElementById('userId').value = '';
    
    // Set default time and days
    document.getElementById('loginTime').value = '09:00';
    for (let i = 1; i <= 6; i++) {
        document.getElementById(`day${i}`).checked = true;
    }
    
    new bootstrap.Modal(document.getElementById('userModal')).show();
}

// Edit user
function editUser(userId) {
    const user = users.find(u => u.id === userId);
    if (!user) return;
    
    document.getElementById('userModalTitle').textContent = 'Edit User';
    document.getElementById('userId').value = user.id;
    document.getElementById('userName').value = user.name;
    document.getElementById('userEmail').value = user.email;
    document.getElementById('userPassword').value = user.password;
    document.getElementById('loginTime').value = user.login_time;
    
    // Set enabled days
    for (let i = 1; i <= 6; i++) {
        document.getElementById(`day${i}`).checked = user.enabled_days.includes(i.toString());
    }
    
    new bootstrap.Modal(document.getElementById('userModal')).show();
}

// Save user
async function saveUser() {
    const userId = document.getElementById('userId').value;
    const userData = {
        name: document.getElementById('userName').value,
        email: document.getElementById('userEmail').value,
        password: document.getElementById('userPassword').value,
        login_time: document.getElementById('loginTime').value,
        enabled_days: []
    };
    
    // Get enabled days
    for (let i = 1; i <= 6; i++) {
        if (document.getElementById(`day${i}`).checked) {
            userData.enabled_days.push(i.toString());
        }
    }
    
    try {
        const url = userId ? `/api/users/${userId}` : '/api/users';
        const method = userId ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(userData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            bootstrap.Modal.getInstance(document.getElementById('userModal')).hide();
            showAlert(userId ? 'User updated successfully' : 'User added successfully', 'success');
            loadAllData();
        } else {
            showAlert(result.error || 'Error saving user', 'danger');
        }
    } catch (error) {
        console.error('Error saving user:', error);
        showAlert('Error saving user', 'danger');
    }
}

// Delete user
async function deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user?')) return;
    
    try {
        const response = await fetch(`/api/users/${userId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('User deleted successfully', 'success');
            loadAllData();
        } else {
            showAlert(result.error || 'Error deleting user', 'danger');
        }
    } catch (error) {
        console.error('Error deleting user:', error);
        showAlert('Error deleting user', 'danger');
    }
}

// Test automation
async function testAutomation(userId) {
    const user = users.find(u => u.id === userId);
    if (!user) return;
    
    const button = event.target.closest('button');
    const originalContent = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    button.disabled = true;
    
    try {
        const response = await fetch(`/api/test-automation/${userId}`, {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert(`Automation test completed successfully for ${user.name}`, 'success');
        } else {
            showAlert(`Automation test failed: ${result.error}`, 'danger');
        }
        
        loadLogs();
    } catch (error) {
        console.error('Error testing automation:', error);
        showAlert('Error testing automation', 'danger');
    } finally {
        button.innerHTML = originalContent;
        button.disabled = false;
    }
}

// Show exclude date modal
function showExcludeDateModal() {
    document.getElementById('excludeDateForm').reset();
    new bootstrap.Modal(document.getElementById('excludeDateModal')).show();
}

// Update user select for exclude date modal
function updateUserSelect() {
    const select = document.getElementById('excludeUser');
    select.innerHTML = '<option value="">Select User</option>';
    
    users.forEach(user => {
        const option = document.createElement('option');
        option.value = user.id;
        option.textContent = user.name;
        select.appendChild(option);
    });
}

// Save excluded date
async function saveExcludedDate() {
    const data = {
        user_id: parseInt(document.getElementById('excludeUser').value),
        excluded_date: document.getElementById('excludeDate').value,
        reason: document.getElementById('excludeReason').value
    };
    
    try {
        const response = await fetch('/api/excluded-dates', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            bootstrap.Modal.getInstance(document.getElementById('excludeDateModal')).hide();
            showAlert('Date excluded successfully', 'success');
            loadExcludedDates();
            updateDashboard();
        } else {
            showAlert(result.error || 'Error excluding date', 'danger');
        }
    } catch (error) {
        console.error('Error excluding date:', error);
        showAlert('Error excluding date', 'danger');
    }
}

// Remove excluded date
async function removeExcludedDate(excludedId) {
    if (!confirm('Are you sure you want to remove this excluded date?')) return;
    
    try {
        const response = await fetch(`/api/excluded-dates/${excludedId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('Excluded date removed successfully', 'success');
            loadExcludedDates();
            updateDashboard();
        } else {
            showAlert(result.error || 'Error removing excluded date', 'danger');
        }
    } catch (error) {
        console.error('Error removing excluded date:', error);
        showAlert('Error removing excluded date', 'danger');
    }
}

// View screenshot
function viewScreenshot(screenshotPath) {
    // Open screenshot in new window
    window.open(screenshotPath, '_blank');
}

// Refresh data
function refreshData() {
    const button = event.target;
    const originalContent = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    button.disabled = true;
    
    loadAllData().finally(() => {
        button.innerHTML = originalContent;
        button.disabled = false;
    });
}

// Show alert
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Format date
function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Format date and time
function formatDateTime(dateString) {
    return new Date(dateString).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}
