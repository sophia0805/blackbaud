import subprocess
import shlex
import platform
import time

def login_to_fsa_windows(username):
    """
    Windows-compatible version that uses PowerShell to automate Chrome login.
    """
    login_url = "https://fultonscienceacademy.myschoolapp.com/app/student?svcid=edu#login"
    
    powershell_script = f'''
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    
    # Function to find Chrome window with myschoolapp.com
    function Find-ChromeTab {{
        try {{
            $chrome = Get-Process chrome -ErrorAction SilentlyContinue
            if ($chrome) {{
                $shell = New-Object -ComObject Shell.Application
                $windows = $shell.Windows()
                
                foreach ($window in $windows) {{
                    try {{
                        if ($window.LocationURL -and $window.LocationURL.Contains("myschoolapp.com")) {{
                            return $window
                        }}
                    }} catch {{}}
                }}
            }}
            return $null
        }} catch {{
            return $null
        }}
    }}
    
    # Try to find existing tab first
    $existingWindow = Find-ChromeTab
    
    if ($existingWindow) {{
        # Activate existing window
        $existingWindow.Visible = $true
        $shell = New-Object -ComObject Shell.Application
        $shell.Windows() | Where-Object {{ $_.LocationURL -eq $existingWindow.LocationURL }} | ForEach-Object {{ $_.Activate() }}
    }} else {{
        # Open new Chrome window with the URL
        Start-Process "chrome" -ArgumentList "{login_url}"
        Start-Sleep -Seconds 3
    }}
    
    # Wait for page to load
    Start-Sleep -Seconds 3
    
    # Use SendKeys to type username (this is a basic approach)
    # Note: This requires the page to be focused and the username field to be active
    Write-Host "Chrome opened with FSA login page."
    Write-Host "Please manually click on the username field, then the script will type your username."
    Start-Sleep -Seconds 2
    
    # Type the username
    $username = "{username}"
    [System.Windows.Forms.SendKeys]::SendWait($username)
    
    Write-Host "Username entered. Please click on the password field."
    Start-Sleep -Seconds 1
    
    # Focus password field
    [System.Windows.Forms.SendKeys]::SendWait("{{TAB}}")
    
    Write-Host "Password field focused. Please enter your password manually."
    Write-Host "success"
    '''
    
    try:
        # Run PowerShell script
        process = subprocess.run(
            ['powershell', '-Command', powershell_script],
            capture_output=True, text=True, timeout=30
        )
        
        result = process.stdout.strip()
        if "success" in result:
            return True
        else:
            print(f"PowerShell script output: {result}")
            return False
            
    except subprocess.CalledProcessError as e:
        print("An error occurred executing the PowerShell script.")
        print(f"Error Details: {e.stderr}")
        return False
    except subprocess.TimeoutExpired:
        print("PowerShell script timed out.")
        return False

def login_to_fsa_mac(username):
    """
    macOS version using AppleScript (original code).
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

def login_to_fsa(username):
    """
    Cross-platform login function that automatically detects the OS and uses the appropriate method.
    """
    system = platform.system()
    
    if system == "Darwin":  # macOS
        print("Detected macOS, using AppleScript automation...")
        return login_to_fsa_mac(username)
    elif system == "Windows":
        print("Detected Windows, using PowerShell automation...")
        return login_to_fsa_windows(username)
    else:
        print(f"Unsupported operating system: {system}")
        print("This script currently supports macOS and Windows only.")
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