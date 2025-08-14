import subprocess

def login_to_fsa(username):
    """
    Windows-only version that uses PowerShell to automate Chrome login.
    Opens the FSA login page and automatically fills the username field.
    """
    login_url = "https://fultonscienceacademy.myschoolapp.com/app?svcid=edu#login"
    
    # PowerShell script to automate Chrome with JavaScript injection
    powershell_script = f'''
    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing
    
    # Function to find and focus Chrome window with myschoolapp.com
    function Find-AndFocus-ChromeTab {{
        try {{
            $chrome = Get-Process chrome -ErrorAction SilentlyContinue
            if ($chrome) {{
                $shell = New-Object -ComObject Shell.Application
                $windows = $shell.Windows()
                
                foreach ($window in $windows) {{
                    try {{
                        if ($window.LocationURL -and $window.LocationURL.Contains("myschoolapp.com")) {{
                            # Activate the window and bring it to front
                            $window.Visible = $true
                            $window.Activate()
                            return $true
                        }}
                    }} catch {{}}
                }}
            }}
            return $false
        }} catch {{
            return $false
        }}
    }}
    
    # Try to find and focus existing tab first
    $found = Find-AndFocus-ChromeTab
    
    if (-not $found) {{
        # Open new Chrome window with the URL
        Start-Process "chrome" -ArgumentList "{login_url}"
        Start-Sleep -Seconds 4
    }}
    
    # Wait for page to load and ensure Chrome is focused
    Start-Sleep -Seconds 3
    
    # Activate Chrome using Shell
    $shell = New-Object -ComObject Shell.Application
    $shell.Windows() | Where-Object {{ $_.LocationURL -and $_.LocationURL.Contains("myschoolapp.com") }} | ForEach-Object {{ $_.Activate() }}
    
    Start-Sleep -Seconds 2
    
    Write-Host "Chrome is now focused. Attempting to automatically fill the username field..."
    
    # Use JavaScript injection to fill the username field
    $javascript = "document.getElementById('Username').value = '{username}'; document.getElementById('Username').focus();"
    
    # Try to execute JavaScript through the Shell object
    try {{
        $shell.Windows() | Where-Object {{ $_.LocationURL -and $_.LocationURL.Contains("myschoolapp.com") }} | ForEach-Object {{
            try {{
                $_.ExecScript($javascript, "JavaScript")
                Write-Host "Username field filled successfully using JavaScript!"
            }} catch {{
                Write-Host "JavaScript injection failed, trying alternative method..."
                # Alternative: Use SendKeys as fallback
                Start-Sleep -Seconds 1
                [System.Windows.Forms.SendKeys]::SendWait("^a")  # Select all
                Start-Sleep -Milliseconds 200
                [System.Windows.Forms.SendKeys]::SendWait("{username}")
                Write-Host "Username entered using SendKeys fallback method."
            }}
        }}
    }} catch {{
        Write-Host "Shell JavaScript execution failed, using SendKeys method..."
        Start-Sleep -Seconds 1
        [System.Windows.Forms.SendKeys]::SendWait("^a")  # Select all
        Start-Sleep -Milliseconds 200
        [System.Windows.Forms.SendKeys]::SendWait("{username}")
        Write-Host "Username entered using SendKeys method."
    }}
    
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

# --- MAIN PART OF THE SCRIPT ---
if __name__ == "__main__":
    my_username = "swang@student.fsaps.org"
    
    print(f"Attempting to log in as '{my_username}'...")
    
    if login_to_fsa(my_username):
        print("\nSuccess! FSA login page is ready.")
        print("Your username has been entered. Please type your password.")
    else:
        print("\nFailed to automate the login process.")