import subprocess
import shlex

def login_to_fsa(username):
    """
    Opens the FSA login page and types the username. This version uses the most
    robust method to avoid AppleScript's "-1728" error by activating tabs directly
    instead of relying on their index number.
    """
    login_url = "https://fultonscienceacademy.myschoolapp.com/app/student?svcid=edu#login"
    
    # This AppleScript avoids asking for the tab's index, which was the source of the error.
    applescript_command = f"""
    tell application "Google Chrome"
	-- Set variables to hold our findings
	set targetURL to "myschoolapp.com"
	set foundTab to missing value
	set foundWindow to missing value
	
	-- Safely loop through windows and tabs to find our target
	repeat with w in windows
		try
			-- This 'try' block gracefully skips special windows that cause errors
			repeat with t in tabs of w
				if URL of t contains targetURL then
					set foundTab to t
					set foundWindow to w
					exit repeat
				end if
			end repeat
		end try
		if foundTab is not missing value then exit repeat
	end repeat
	
	-- After searching, decide what to do
	if foundTab is missing value then
		-- The tab was not found, so we need to create it.
		-- First, check if any windows exist at all.
		if not (exists window 1) then
			-- If no windows exist, activate Chrome to create one, then open the URL.
			activate
			delay 0.5 -- Give it a moment to open a window
			open location "{login_url}"
		else
			-- If a window exists, create the new tab in the frontmost window.
			make new tab at end of tabs of window 1 with properties {{URL:"{login_url}"}}
		end if
	else
		-- The tab was found. Now we activate it directly.
		set index of foundWindow to 1
		set active tab of foundWindow to foundTab
	end if
	
	-- Ensure Chrome is the front application
	activate
	
	-- Give the page a moment to load
	delay 2.5
	
	-- Execute JavaScript in the active tab of the front window
	tell active tab of window 1
		execute javascript "document.getElementById('Username').value = '{username}';"
		execute javascript "document.getElementById('Password').focus();"
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
            # This case should ideally not be reached with the new logic
            print(f"The script finished but did not report success. Result: {result}")
            return False
            
    except subprocess.CalledProcessError as e:
        print("An error occurred executing the AppleScript.")
        print(f"Error Details: {e.stderr}")
        return False

# --- MAIN PART OF THE SCRIPT ---
if __name__ == "__main__":
    my_username = "swang@student.fsaps.org"
    
    print(f"Attempting to log in as '{my_username}'...")
    
    if login_to_fsa(my_username):
        print("\nSuccess! FSA login page is ready.")
        print("Your username has been entered. Please type your password.")
    else:
        print("\nFailed to automate the login process.")