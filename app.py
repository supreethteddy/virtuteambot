from flask import Flask, render_template, request, jsonify
import json
import os
import subprocess
from datetime import datetime, date
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('virtueteams.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            login_time TEXT NOT NULL,
            enabled_days TEXT NOT NULL DEFAULT '1,2,3,4,5,6',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Excluded dates table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS excluded_dates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            excluded_date DATE NOT NULL,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Automation logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS automation_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            execution_date DATE NOT NULL,
            status TEXT NOT NULL,
            message TEXT,
            screenshot_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect('virtueteams.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users ORDER BY name')
    users = []
    for row in cursor.fetchall():
        users.append({
            'id': row[0],
            'name': row[1],
            'email': row[2],
            'password': row[3],
            'login_time': row[4],
            'enabled_days': row[5].split(',') if row[5] else []
        })
    conn.close()
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.json
    conn = sqlite3.connect('virtueteams.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO users (name, email, password, login_time, enabled_days)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['email'],
            data['password'],
            data['login_time'],
            ','.join(data['enabled_days'])
        ))
        conn.commit()
        user_id = cursor.lastrowid
        
        # Create individual Python script for the user
        create_user_script(data['name'], data['email'], data['password'])
        
        conn.close()
        return jsonify({'success': True, 'id': user_id})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    conn = sqlite3.connect('virtueteams.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE users 
            SET name = ?, email = ?, password = ?, login_time = ?, enabled_days = ?
            WHERE id = ?
        ''', (
            data['name'],
            data['email'],
            data['password'],
            data['login_time'],
            ','.join(data['enabled_days']),
            user_id
        ))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = sqlite3.connect('virtueteams.db')
    cursor = conn.cursor()
    
    try:
        # Get user name for script deletion
        cursor.execute('SELECT name FROM users WHERE id = ?', (user_id,))
        user_name = cursor.fetchone()[0]
        
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        cursor.execute('DELETE FROM excluded_dates WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM automation_logs WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        # Delete user script file
        script_file = f"{user_name.lower()}_virtueteams.py"
        if os.path.exists(script_file):
            os.remove(script_file)
        
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/excluded-dates', methods=['GET'])
def get_excluded_dates():
    user_id = request.args.get('user_id')
    conn = sqlite3.connect('virtueteams.db')
    cursor = conn.cursor()
    
    if user_id:
        cursor.execute('''
            SELECT ed.*, u.name 
            FROM excluded_dates ed 
            JOIN users u ON ed.user_id = u.id 
            WHERE ed.user_id = ?
            ORDER BY ed.excluded_date
        ''', (user_id,))
    else:
        cursor.execute('''
            SELECT ed.*, u.name 
            FROM excluded_dates ed 
            JOIN users u ON ed.user_id = u.id 
            ORDER BY ed.excluded_date
        ''')
    
    excluded_dates = []
    for row in cursor.fetchall():
        excluded_dates.append({
            'id': row[0],
            'user_id': row[1],
            'user_name': row[3],
            'excluded_date': row[2],
            'reason': row[4],
            'created_at': row[5]
        })
    
    conn.close()
    return jsonify(excluded_dates)

@app.route('/api/excluded-dates', methods=['POST'])
def add_excluded_date():
    data = request.json
    conn = sqlite3.connect('virtueteams.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO excluded_dates (user_id, excluded_date, reason)
            VALUES (?, ?, ?)
        ''', (data['user_id'], data['excluded_date'], data['reason']))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/excluded-dates/<int:excluded_id>', methods=['DELETE'])
def delete_excluded_date(excluded_id):
    conn = sqlite3.connect('virtueteams.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM excluded_dates WHERE id = ?', (excluded_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/logs', methods=['GET'])
def get_logs():
    user_id = request.args.get('user_id')
    conn = sqlite3.connect('virtueteams.db')
    cursor = conn.cursor()
    
    if user_id:
        cursor.execute('''
            SELECT al.*, u.name 
            FROM automation_logs al 
            JOIN users u ON al.user_id = u.id 
            WHERE al.user_id = ?
            ORDER BY al.execution_date DESC, al.created_at DESC
            LIMIT 50
        ''', (user_id,))
    else:
        cursor.execute('''
            SELECT al.*, u.name 
            FROM automation_logs al 
            JOIN users u ON al.user_id = u.id 
            ORDER BY al.execution_date DESC, al.created_at DESC
            LIMIT 50
        ''')
    
    logs = []
    for row in cursor.fetchall():
        logs.append({
            'id': row[0],
            'user_id': row[1],
            'user_name': row[4],
            'execution_date': row[2],
            'status': row[3],
            'message': row[5],
            'screenshot_path': row[6],
            'created_at': row[7]
        })
    
    conn.close()
    return jsonify(logs)

@app.route('/api/test-automation/<int:user_id>', methods=['POST'])
def test_automation(user_id):
    conn = sqlite3.connect('virtueteams.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, email, password FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return jsonify({'success': False, 'error': 'User not found'})
    
    try:
        # Run the user's automation script
        script_file = f"{user[0].lower()}_virtueteams.py"
        result = subprocess.run(['python3', script_file], 
                              capture_output=True, text=True, timeout=300)
        
        # Log the result
        conn = sqlite3.connect('virtueteams.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO automation_logs (user_id, execution_date, status, message)
            VALUES (?, ?, ?, ?)
        ''', (user_id, date.today().isoformat(), 
              'success' if result.returncode == 0 else 'error',
              result.stdout + result.stderr))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        })
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': 'Automation timed out'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def create_user_script(name, email, password):
    script_content = f'''from playwright.sync_api import sync_playwright
import time

# {name}'s credentials only
users = [
    {{"name": "{name}", "email": "{email}", "password": "{password}"}},
]

def sign_in(user):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Headless for cloud deployment
        context = browser.new_context(
            permissions=["geolocation"],
            geolocation={{"latitude": 12.9716, "longitude": 77.5946}},
            locale="en-US"
        )
        page = context.new_page()

        print(f"\\n🔐 Logging in for: {{user['name']}}...")

        try:
            # Step 1: Login page with longer timeout
            print("📱 Navigating to login page...")
            page.goto("https://www.virtuteams.com/auth?tab=signin", timeout=60000)
            time.sleep(3)  # Wait for page to load

            # Step 2: Fill login credentials
            print("🔑 Filling login credentials...")
            page.wait_for_selector('#signin-email', timeout=15000)
            page.fill('#signin-email', user["email"])
            page.fill('#signin-password', user["password"])
            
            print("🖱️ Clicking Sign In button...")
            page.get_by_role("button", name="Sign In").click()
            
            # Wait for navigation to complete - but don't fail if it times out
            print("⏳ Waiting for login to complete...")
            try:
                page.wait_for_load_state('networkidle', timeout=30000)
            except:
                print("⚠️ Network idle timeout, but continuing...")
            
            time.sleep(5)  # Extra wait for any redirects

            # Step 3: Go to dashboard
            print("🏠 Navigating to dashboard...")
            page.goto("https://www.virtuteams.com/dashboard", timeout=60000)
            
            # Wait for dashboard to load - but don't fail if it times out
            try:
                page.wait_for_load_state('networkidle', timeout=30000)
            except:
                print("⚠️ Dashboard network idle timeout, but continuing...")
            
            time.sleep(8)  # Increased wait time for dashboard to fully load

            print(f"\\n✅ Successfully logged in and reached dashboard for {{user['name']}}")

            # Step 4: Find and click the green "Sign In" button in Time Tracking section
            print(f"\\n🔍 Looking for the green 'Sign In' button...")
            
            # Take a screenshot before looking for buttons
            page.screenshot(path=f"{{user['name']}}_dashboard_before.png")
            print(f"📸 Dashboard screenshot saved as {{user['name']}}_dashboard_before.png")
            
            # Try multiple selectors to find the green Sign In button
            sign_in_button = None
            
            # Method 1: Look for button with "Sign In" text (most reliable)
            try:
                print("🔍 Method 1: Looking for 'Sign In' button by text...")
                sign_in_button = page.get_by_role("button", name="Sign In")
                if sign_in_button.is_visible():
                    print("✅ Found 'Sign In' button using role selector")
                else:
                    sign_in_button = None
            except Exception as e:
                print(f"⚠️ Method 1 failed: {{e}}")
                sign_in_button = None
            
            # Method 2: Look for button with green background color
            if not sign_in_button:
                try:
                    print("🔍 Method 2: Looking for green 'Sign In' button by color...")
                    buttons = page.query_selector_all('button')
                    for button in buttons:
                        if button.is_visible():
                            text = button.text_content().strip()
                            bg_color = button.evaluate('el => window.getComputedStyle(el).backgroundColor')
                            if text == "Sign In" and ("green" in bg_color.lower() or "rgb(34, 197, 94)" in bg_color or "rgb(22, 163, 74)" in bg_color):
                                sign_in_button = button
                                print(f"✅ Found green 'Sign In' button with color: {{bg_color}}")
                                break
                except Exception as e:
                    print(f"⚠️ Method 2 failed: {{e}}")
            
            # Method 3: Look for any button with "Sign In" text regardless of color
            if not sign_in_button:
                try:
                    print("🔍 Method 3: Looking for any 'Sign In' button...")
                    buttons = page.query_selector_all('button')
                    for button in buttons:
                        if button.is_visible():
                            text = button.text_content().strip()
                            if text == "Sign In":
                                sign_in_button = button
                                bg_color = button.evaluate('el => window.getComputedStyle(el).backgroundColor')
                                print(f"✅ Found 'Sign In' button with color: {{bg_color}}")
                                break
                except Exception as e:
                    print(f"⚠️ Method 3 failed: {{e}}")
            
            # Method 4: Use CSS selector for any Sign In button
            if not sign_in_button:
                try:
                    print("🔍 Method 4: Using CSS selector for 'Sign In' button...")
                    sign_in_button = page.query_selector('button:has-text("Sign In")')
                    if sign_in_button and sign_in_button.is_visible():
                        bg_color = sign_in_button.evaluate('el => window.getComputedStyle(el).backgroundColor')
                        print(f"✅ Found 'Sign In' button using CSS selector with color: {{bg_color}}")
                except Exception as e:
                    print(f"⚠️ Method 4 failed: {{e}}")

            # Click the Sign In button if found
            if sign_in_button and sign_in_button.is_visible():
                print(f"\\n🎯 Clicking the 'Sign In' button...")
                sign_in_button.click()
                time.sleep(3)
                print(f"✅ Successfully clicked 'Sign In' button for {{user['name']}}")
                
                # Take a screenshot after clicking
                page.screenshot(path=f"{{user['name']}}_after_signin.png")
                print(f"📸 Screenshot saved as {{user['name']}}_after_signin.png")
            else:
                print(f"❌ Could not find the 'Sign In' button for {{user['name']}}")
                
                # Debug: List all buttons for troubleshooting
                print(f"\\n🔍 Debug: Listing all visible buttons:")
                try:
                    buttons = page.evaluate("""
                        Array.from(document.querySelectorAll('button')).map((btn, index) => ({{
                            index,
                            text: btn.textContent.trim(),
                            visible: !!(btn.offsetParent),
                            bgColor: window.getComputedStyle(btn).backgroundColor,
                            className: btn.className,
                            id: btn.id
                        }}))
                    """)
                    
                    visible_buttons = [b for b in buttons if b['visible']]
                    print(f"Found {{len(visible_buttons)}} visible buttons:")
                    
                    for b in visible_buttons:
                        print(f"[{{b['index']}}] '{{b['text']}}' - Color: {{b['bgColor']}} - Class: {{b['className']}} - ID: {{b['id']}}")
                        
                        # Check if any button contains "sign" or "in" (case insensitive)
                        if "sign" in b['text'].lower() or "in" in b['text'].lower():
                            print(f"    ⭐ This button might be the one we're looking for!")
                            
                except Exception as e:
                    print(f"⚠️ Error listing buttons: {{e}}")

        except Exception as e:
            print(f"❌ Error for {{user['name']}}: {{e}}")
            try:
                page.screenshot(path=f"{{user['name']}}_error.png")
                print(f"📸 Error screenshot saved as {{user['name']}}_error.png")
            except:
                print("⚠️ Could not save error screenshot")
        finally:
            time.sleep(8)  # Keep browser open longer to see the result
            browser.close()

# Run for {name}
for user in users:
    sign_in(user)
'''
    
    with open(f"{name.lower()}_virtueteams.py", "w") as f:
        f.write(script_content)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
