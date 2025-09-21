from playwright.sync_api import sync_playwright
import time

# Reshab's credentials only
users = [
    {"name": "Reshab", "email": "ceo@boostmysites.com", "password": "Reshab@8!"},
]

def sign_in(user):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Headless for cloud deployment
        context = browser.new_context(
            permissions=["geolocation"],
            geolocation={"latitude": 12.9716, "longitude": 77.5946},
            locale="en-US"
        )
        page = context.new_page()

        print(f"\n🔐 Logging in for: {user['name']}...")

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

            print(f"\n✅ Successfully logged in and reached dashboard for {user['name']}")

            # Step 4: Find and click the green "Sign In" button in Time Tracking section
            print(f"\n🔍 Looking for the green 'Sign In' button...")
            
            # Take a screenshot before looking for buttons
            page.screenshot(path=f"{user['name']}_dashboard_before.png")
            print(f"📸 Dashboard screenshot saved as {user['name']}_dashboard_before.png")
            
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
                print(f"⚠️ Method 1 failed: {e}")
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
                                print(f"✅ Found green 'Sign In' button with color: {bg_color}")
                                break
                except Exception as e:
                    print(f"⚠️ Method 2 failed: {e}")
            
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
                                print(f"✅ Found 'Sign In' button with color: {bg_color}")
                                break
                except Exception as e:
                    print(f"⚠️ Method 3 failed: {e}")
            
            # Method 4: Use CSS selector for any Sign In button
            if not sign_in_button:
                try:
                    print("🔍 Method 4: Using CSS selector for 'Sign In' button...")
                    sign_in_button = page.query_selector('button:has-text("Sign In")')
                    if sign_in_button and sign_in_button.is_visible():
                        bg_color = sign_in_button.evaluate('el => window.getComputedStyle(el).backgroundColor')
                        print(f"✅ Found 'Sign In' button using CSS selector with color: {bg_color}")
                except Exception as e:
                    print(f"⚠️ Method 4 failed: {e}")

            # Click the Sign In button if found
            if sign_in_button and sign_in_button.is_visible():
                print(f"\n🎯 Clicking the 'Sign In' button...")
                sign_in_button.click()
                time.sleep(3)
                print(f"✅ Successfully clicked 'Sign In' button for {user['name']}")
                
                # Take a screenshot after clicking
                page.screenshot(path=f"{user['name']}_after_signin.png")
                print(f"📸 Screenshot saved as {user['name']}_after_signin.png")
            else:
                print(f"❌ Could not find the 'Sign In' button for {user['name']}")
                
                # Debug: List all buttons for troubleshooting
                print(f"\n🔍 Debug: Listing all visible buttons:")
                try:
                    buttons = page.evaluate("""
                        Array.from(document.querySelectorAll('button')).map((btn, index) => ({
                            index,
                            text: btn.textContent.trim(),
                            visible: !!(btn.offsetParent),
                            bgColor: window.getComputedStyle(btn).backgroundColor,
                            className: btn.className,
                            id: btn.id
                        }))
                    """)
                    
                    visible_buttons = [b for b in buttons if b['visible']]
                    print(f"Found {len(visible_buttons)} visible buttons:")
                    
                    for b in visible_buttons:
                        print(f"[{b['index']}] '{b['text']}' - Color: {b['bgColor']} - Class: {b['className']} - ID: {b['id']}")
                        
                        # Check if any button contains "sign" or "in" (case insensitive)
                        if "sign" in b['text'].lower() or "in" in b['text'].lower():
                            print(f"    ⭐ This button might be the one we're looking for!")
                            
                except Exception as e:
                    print(f"⚠️ Error listing buttons: {e}")

        except Exception as e:
            print(f"❌ Error for {user['name']}: {e}")
            try:
                page.screenshot(path=f"{user['name']}_error.png")
                print(f"📸 Error screenshot saved as {user['name']}_error.png")
            except:
                print("⚠️ Could not save error screenshot")
        finally:
            time.sleep(8)  # Keep browser open longer to see the result
            browser.close()

# Run for Reshab
for user in users:
    sign_in(user)
