import subprocess
import time
import os
from dotenv import load_dotenv

load_dotenv()
username = os.getenv('email')

def login_and_click_next(username):
    print("Executing Step 1: Entering username and clicking 'Next'...")
    login_url = "https://fultonscienceacademy.myschoolapp.com/app/student?svcid=edu#login"
    step1 = f"""
        document.getElementById('Username').value = '{username}';
        var inputEvent = new Event('input', {{ bubbles: true }});
        document.getElementById('Username').dispatchEvent(inputEvent);
        setTimeout(() => {{
            const nextButton = document.getElementById('nextBtn');
            if (nextButton) {{ nextButton.click(); }}
        }}, 100);
    """
    applescript_command = f"""
    tell application "Google Chrome"
        activate
        if not (exists window 1) then
            open location "{login_url}"
        else
            tell window 1
                if (get URL of tab 1) contains "myschoolapp.com" then
                    set active tab index to 1
                else
                    make new tab at end of tabs with properties {{URL:"{login_url}"}}
                end if
            end tell
        end if
        delay 1
        tell active tab of window 1
            execute javascript "{step1.replace('"', '\\"')}"
        end tell
        return "success"
    end tell
    """
    try:
        process = subprocess.run(
            ['osascript', '-e', applescript_command],
            capture_output=True, text=True, check=True, timeout=20
        )
        return process.stdout.strip() == "success"
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print("An error occurred during Step 1 (Username/Next Button).")
        if isinstance(e, subprocess.CalledProcessError): print(f"Error Details: {e.stderr}")
        return False

def click_google_button():
    print("Step 2: Clicking 'Continue with Google'...")
    step2 = """
        const buttonText = 'Continue with Google';
        const googleButton = Array.from(document.querySelectorAll('button'))
                                 .find(el => el.textContent.trim() === buttonText);
        if (googleButton) { googleButton.click(); }
    """
    applescript_command = f"""
    tell application "Google Chrome"
        tell active tab of window 1
            execute javascript "{step2.replace('"', '\\"')}"
        end tell
        return "success"
    end tell
    """
    try:
        process = subprocess.run(
            ['osascript', '-e', applescript_command],
            capture_output=True, text=True, check=True, timeout=20
        )
        return process.stdout.strip() == "success"
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print("An error occurred during Step 2 (Clicking Google Button).")
        if isinstance(e, subprocess.CalledProcessError): print(f"Error Details: {e.stderr}")
        return False

def select_google_account(email):
    print(f"Step 3: Selecting Google account '{email}'...")
    step3 = f"""
        const accountSelector = 'div[data-identifier="{email}"]';
        const accountDiv = document.querySelector(accountSelector);
        if (accountDiv) {{
            accountDiv.click();
        }} else {{
            console.error(`Google Account div for {email} was not found.`);
        }}
    """
    applescript_command = f"""
    tell application "Google Chrome"
        -- We target the active tab of the frontmost window, which will be the popup.
        tell active tab of front window
            execute javascript "{step3.replace('"', '\\"')}"
        end tell
        return "success"
    end tell
    """

    try:
        process = subprocess.run(
            ['osascript', '-e', applescript_command],
            capture_output=True, text=True, check=True, timeout=20
        )
        return process.stdout.strip() == "success"
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print("An error occurred during Step 3 (Selecting Google Account).")
        if isinstance(e, subprocess.CalledProcessError): print(f"Error Details: {e.stderr}")
        return False
    
if __name__ == "__main__":    
    print("--- Starting Full Automation Process ---")
    
    if login_and_click_next(username):
        print("'Next' button clicked.")
        print("\nWaiting for the next page...")
        time.sleep(1)
        
        if click_google_button():
            print("'Continue with Google' button clicked.")
            print("\nWaiting for Google Account chooser...")
            time.sleep(1)
            
            if select_google_account(username):
                print("Google Account selected.")
            else:
                print("\nFailed to complete Step 3.")
        else:
            print("\nFailed to complete Step 2.")
    else:
        print("\nFailed to complete Step 1.")