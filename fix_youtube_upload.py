import os
import json
import requests
import config

def upload_to_youtube(video_path, title, description):
    """Upload a video to YouTube using the resumable upload protocol."""
    print(f"Uploading {video_path} to YouTube...")
    
    # Get a new access token using refresh token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "client_id": config.YOUTUBE_CLIENT_ID,
        "client_secret": config.YOUTUBE_CLIENT_SECRET,
        "refresh_token": config.YOUTUBE_REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
    
    token_response = requests.post(token_url, data=token_data)
    if token_response.status_code != 200:
        print(f"Failed to refresh YouTube token: {token_response.text}")
        return False
        
    access_token = token_response.json().get("access_token")
    
    # Check if file exists
    if not os.path.exists(video_path):
        print(f"Error: File not found at {video_path}")
        return False
    
    # Prepare metadata
    metadata = {
        "snippet": {
            "title": title,
            "description": f"{description} #shorts",
            "tags": ["shorts", "viral", "trending"],
            "categoryId": "22"  # People & Blogs
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False
        }
    }
    
    # Step 1: Start the resumable session
    session_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
    session_headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Type": "video/mp4"
    }
    
    session_response = requests.post(
        session_url,
        headers=session_headers,
        data=json.dumps(metadata)
    )
    
    if session_response.status_code != 200:
        print(f"Failed to start upload session: {session_response.text}")
        return False
        
    # Get the upload URL from the Location header
    upload_url = session_response.headers.get('Location')
    
    # Step 2: Upload the file
    with open(video_path, 'rb') as video_file:
        video_data = video_file.read()
        
        upload_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "video/mp4"
        }
        
        upload_response = requests.put(
            upload_url,
            headers=upload_headers,
            data=video_data
        )
    
    if upload_response.status_code in [200, 201, 204]:
        print(f"Successfully uploaded video to YouTube!")
        return True
    else:
        print(f"YouTube API upload error: {upload_response.status_code}")
        print(f"Response: {upload_response.text}")
        return False

if __name__ == "__main__":
    # Test with a sample video
    video_path = input("Enter path to video file: ")
    title = input("Enter video title: ")
    description = input("Enter video description: ")
    
    success = upload_to_youtube(video_path, title, description)
    
    if success:
        print("Upload successful!")
    else:
        print("Upload failed.")