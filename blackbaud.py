import subprocess
import shlex

def login_to_fsa(username):
    """
    Opens the FSA login page and types the username. This version assumes that
    if the fsa tab is open, it is always the first tab of the frontmost window.
    """
    login_url = "https://fultonscienceacademy.myschoolapp.com/app/student?svcid=edu#login"
    applescript_command = f"""
    tell application "Google Chrome"
        -- Bring Chrome to the front
        activate

        -- Check if any window exists. If not, open the URL which creates a window.
        if not (exists window 1) then
            open location "{login_url}"
        else
            -- A window exists, so check the first tab of the frontmost window.
            tell window 1
                if (get URL of tab 1) contains "myschoolapp.com" then
                    -- The correct tab is already the first tab. Make sure it's active.
                    set active tab index to 1
                else
                    -- The first tab isn't the correct one, so create a new tab.
                    make new tab at end of tabs with properties {{URL:"{login_url}"}}
                end if
            end tell
        end if

        -- Give the page a moment to load
        delay 1.5

        -- Execute JavaScript in the active tab of the front window
        -- to populate the username field.
        tell active tab of window 1
            execute javascript "document.getElementById('Username').value = '{username}';"
            delay 5
            execute javascript "Array.from(document.querySelectorAll('button')).find(el => el.textContent.trim() === 'Next').click();"
        end tell

        return "success"
    end tell
    """
    
    try:
        process = subprocess.run(
            ['osascript', '-e', applescript_command],
            capture_output=True, text=True, check=True, timeout=15
        )
        
        result = process.stdout.strip()
        if result == "success":
            return True
        else:
            print(f"The script finished but did not report success. Result: {result}")
            return False
            
    except subprocess.CalledProcessError as e:
        print("An error occurred executing the AppleScript.")
        print(f"Error Details: {e.stderr}")
        return False
    except subprocess.TimeoutExpired:
        print("The AppleScript command timed out after 15 seconds.")
        return False

if __name__ == "__main__":
    my_username = "swang@student.fsaps.org"
    
    print(f"Attempting to log in as '{my_username}'...")
    
    if login_to_fsa(my_username):
        print("\nSuccess! FSA login page is ready.")
        print("Your username has been entered. Please type your password.")
    else:
        print("\nFailed to automate the login process.")