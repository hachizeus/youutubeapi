import os
import json
import requests
import webbrowser
import config

def verify_youtube_credentials():
    """Test YouTube OAuth credentials and fix if needed."""
    print("Testing YouTube OAuth credentials...")
    
    # Try to get a new access token using the refresh token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "client_id": config.YOUTUBE_CLIENT_ID,
        "client_secret": config.YOUTUBE_CLIENT_SECRET,
        "refresh_token": config.YOUTUBE_REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
    
    response = requests.post(token_url, data=token_data)
    
    if response.status_code == 200:
        print("✓ YouTube OAuth credentials are working correctly!")
        return True
    else:
        print("✗ YouTube OAuth credentials are not working.")
        print(f"Error: {response.text}")
        return False

def create_oauth_app():
    """Guide user through creating a properly configured OAuth app."""
    print("\n=== YouTube OAuth App Setup Guide ===\n")
    print("To fix the OAuth verification issue, you need to create a new OAuth app with the correct settings:")
    
    print("\n1. Go to Google Cloud Console: https://console.cloud.google.com/")
    print("2. Create a new project or select an existing one")
    print("3. Enable the YouTube Data API v3")
    print("4. Go to 'OAuth consent screen'")
    print("   - Set User Type to 'External'")
    print("   - Fill in the required app information")
    print("   - Add yourself as a test user")
    print("5. Go to 'Credentials'")
    print("   - Create OAuth client ID")
    print("   - Application type: 'Web application'")
    print("   - Add authorized redirect URI: 'https://developers.google.com/oauthplayground'")
    
    proceed = input("\nHave you completed these steps? (y/n): ")
    if proceed.lower() != 'y':
        print("Please complete the steps and run this script again.")
        return False
    
    # Update credentials
    client_id = input("\nEnter your new OAuth Client ID: ")
    client_secret = input("Enter your new OAuth Client Secret: ")
    
    # Update config file
    with open("config.py", 'r') as f:
        config_content = f.read()
    
    config_content = config_content.replace(
        f'YOUTUBE_CLIENT_ID = "{config.YOUTUBE_CLIENT_ID}"',
        f'YOUTUBE_CLIENT_ID = "{client_id}"'
    )
    
    config_content = config_content.replace(
        f'YOUTUBE_CLIENT_SECRET = "{config.YOUTUBE_CLIENT_SECRET}"',
        f'YOUTUBE_CLIENT_SECRET = "{client_secret}"'
    )
    
    with open("config.py", 'w') as f:
        f.write(config_content)
    
    print("\nCredentials updated in config.py")
    return True

def get_new_refresh_token():
    """Get a new refresh token using OAuth Playground."""
    print("\n=== Getting New Refresh Token ===\n")
    
    # Open OAuth Playground
    playground_url = (
        "https://developers.google.com/oauthplayground/#step1"
        "&scopes=https%3A//www.googleapis.com/auth/youtube.upload"
        f"&client_id={config.YOUTUBE_CLIENT_ID}"
        f"&client_secret={config.YOUTUBE_CLIENT_SECRET}"
        "&redirect_uri=https://developers.google.com/oauthplayground"
    )
    
    print("Opening OAuth Playground in your browser...")
    webbrowser.open(playground_url)
    
    print("\nFollow these steps:")
    print("1. In the left panel, find 'YouTube Data API v3' and select 'https://www.googleapis.com/auth/youtube.upload'")
    print("2. Click 'Authorize APIs' and sign in with your Google account")
    print("3. Click 'Exchange authorization code for tokens'")
    print("4. Copy the 'Refresh token' value")
    
    refresh_token = input("\nEnter the new refresh token: ")
    
    if not refresh_token:
        print("No refresh token provided.")
        return False
    
    # Update config file
    with open("config.py", 'r') as f:
        config_content = f.read()
    
    config_content = config_content.replace(
        f'YOUTUBE_REFRESH_TOKEN = "{config.YOUTUBE_REFRESH_TOKEN}"',
        f'YOUTUBE_REFRESH_TOKEN = "{refresh_token}"'
    )
    
    with open("config.py", 'w') as f:
        f.write(config_content)
    
    print("\nRefresh token updated in config.py")
    return True

if __name__ == "__main__":
    print("YouTube OAuth Verification Fix")
    print("=============================\n")
    
    if verify_youtube_credentials():
        print("\nYour YouTube OAuth setup is working correctly!")
        print("You can now run the main.py script to start auto-posting.")
    else:
        print("\nLet's fix your YouTube OAuth setup...")
        
        if create_oauth_app():
            if get_new_refresh_token():
                print("\nSetup complete! Try running this script again to verify your credentials.")
            else:
                print("\nFailed to update refresh token. Please try again.")
        else:
            print("\nFailed to update OAuth app. Please try again.")