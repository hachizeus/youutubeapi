import os
import json
import webbrowser
import time
import requests
from urllib.parse import urlparse, parse_qs

# Configuration
CLIENT_ID = input("Enter your YouTube OAuth Client ID: ")
CLIENT_SECRET = input("Enter your YouTube OAuth Client Secret: ")
REDIRECT_URI = "https://developers.google.com/oauthplayground"
SCOPES = "https://www.googleapis.com/auth/youtube.upload"

def get_youtube_tokens():
    """Get YouTube OAuth tokens using manual flow."""
    # Generate the authorization URL
    auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPES}"
        "&response_type=code"
        "&access_type=offline"
        "&prompt=consent"
    )
    
    print(f"\nOpening browser to authorize the application...")
    webbrowser.open(auth_url)
    
    print("\n1. Sign in with your Google account")
    print("2. Click 'Allow' to grant permissions")
    print("3. You'll be redirected to the OAuth Playground")
    print("4. Copy the authorization code from the page")
    
    auth_code = input("\nEnter the authorization code: ")
    
    if not auth_code:
        print("No authorization code provided")
        return None
    
    print("\nExchanging authorization code for tokens...")
    
    # Exchange the authorization code for tokens
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": auth_code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    
    response = requests.post(token_url, data=token_data)
    if response.status_code != 200:
        print(f"Failed to get tokens: {response.text}")
        return None
    
    tokens = response.json()
    return {
        "access_token": tokens.get("access_token"),
        "refresh_token": tokens.get("refresh_token"),
        "expires_in": tokens.get("expires_in")
    }

def update_config_file(tokens):
    """Update the config.py file with the tokens."""
    config_path = "config.py"
    
    with open(config_path, 'r') as f:
        config_content = f.read()
    
    # Update the YouTube client secret and refresh token
    config_content = config_content.replace(
        'YOUTUBE_CLIENT_SECRET = ""',
        f'YOUTUBE_CLIENT_SECRET = "{CLIENT_SECRET}"'
    )
    
    config_content = config_content.replace(
        'YOUTUBE_REFRESH_TOKEN = ""',
        f'YOUTUBE_REFRESH_TOKEN = "{tokens["refresh_token"]}"'
    )
    
    with open(config_path, 'w') as f:
        f.write(config_content)
    
    print("Config file updated with YouTube tokens")

if __name__ == "__main__":
    print("YouTube OAuth Setup")
    print("===================")
    
    tokens = get_youtube_tokens()
    if tokens and tokens.get("refresh_token"):
        update_config_file(tokens)
        print("\nSetup complete! You can now post to YouTube Shorts automatically.")
    else:
        print("\nSetup failed. Please try again.")