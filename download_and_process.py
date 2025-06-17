import os
import json
import openai
import requests
import googleapiclient.discovery
from googleapiclient.http import MediaIoBaseDownload
import io
import config
import video_processor
import social_poster

# Set OpenAI API key
openai.api_key = config.OPENAI_API_KEY

# Create necessary directories
os.makedirs(config.DOWNLOAD_PATH, exist_ok=True)
os.makedirs(config.OUTPUT_PATH, exist_ok=True)

def get_video_info(video_id):
    """Get video information using YouTube API."""
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=config.YOUTUBE_API_KEY)
    
    request = youtube.videos().list(
        part="snippet,contentDetails",
        id=video_id
    )
    response = request.execute()
    
    if response["items"]:
        return response["items"][0]
    return None

def download_video_with_api(video_id):
    """Download video using YouTube API and OAuth."""
    # First, get a new access token using refresh token
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "client_id": config.YOUTUBE_CLIENT_ID,
        "client_secret": config.YOUTUBE_CLIENT_SECRET,
        "refresh_token": config.YOUTUBE_REFRESH_TOKEN,
        "grant_type": "refresh_token"
    }
    
    token_response = requests.post(token_url, data=token_data)
    if token_response.status_code != 200:
        print(f"Failed to refresh token: {token_response.text}")
        return None
    
    access_token = token_response.json().get("access_token")
    
    # Now download the video
    output_path = os.path.join(config.DOWNLOAD_PATH, f"{video_id}.mp4")
    
    # Use YouTube Data API to get direct download URL
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", 
        developerKey=config.YOUTUBE_API_KEY)
    
    # Get video info
    video_info = get_video_info(video_id)
    if not video_info:
        print(f"Could not find video with ID {video_id}")
        return None
    
    title = video_info["snippet"]["title"]
    print(f"Video title: {title}")
    
    # Try alternative download method using pytube
    try:
        from pytube import YouTube
        
        print("Downloading with pytube...")
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        if stream:
            stream.download(output_path=config.DOWNLOAD_PATH, filename=f"{video_id}.mp4")
            print(f"Downloaded video to {output_path}")
            return output_path
    except Exception as e:
        print(f"pytube download failed: {e}")
    
    # If pytube fails, try with requests directly
    try:
        print("Trying direct download...")
        # This is a simplified approach and may not work for all videos
        video_url = f"https://www.youtube.com/get_video_info?video_id={video_id}"
        response = requests.get(video_url)
        
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded video to {output_path}")
            return output_path
    except Exception as e:
        print(f"Direct download failed: {e}")
    
    print("All download methods failed")
    return None

# The YouTube Shorts video ID
video_id = "6BEph-Pm0jg"
print(f"Processing YouTube Shorts video ID: {video_id}")

# Get video info
video_info = get_video_info(video_id)
if video_info:
    title = video_info["snippet"]["title"]
    print(f"Video title: {title}")
    
    # Try to download the video
    video_path = download_video_with_api(video_id)
    
    if video_path:
        print(f"Successfully downloaded video to {video_path}")
        
        # Create a clip manually since we already have the video
        from moviepy.editor import VideoFileClip
        
        try:
            # Create output directory if it doesn't exist
            os.makedirs(config.OUTPUT_PATH, exist_ok=True)
            
            # Create a clip from the downloaded video
            clip_path = os.path.join(config.OUTPUT_PATH, f"{video_id}_clip.mp4")
            
            with VideoFileClip(video_path) as video:
                # Get video duration
                duration = video.duration
                
                # Create a clip of the first 30 seconds or the whole video if shorter
                clip_duration = min(30, duration)
                clip = video.subclip(0, clip_duration)
                
                # Resize for vertical format (9:16 aspect ratio)
                clip_resized = clip.resize(height=1920)
                w, h = clip_resized.size
                if w > 1080:
                    # Crop to 9:16 aspect ratio
                    crop_width = 1080
                    x_center = w / 2
                    clip_resized = clip_resized.crop(
                        x1=max(0, x_center - crop_width/2),
                        y1=0,
                        x2=min(w, x_center + crop_width/2),
                        y2=h
                    )
                
                # Write the clip
                clip_resized.write_videofile(clip_path, codec="libx264", audio_codec="aac")
                
                print(f"Created clip: {clip_path}")
                
                # Create clip info
                clip_info = {
                    "path": clip_path,
                    "title": f"{title} #shorts",
                    "source_video": video_id
                }
                
                # Post to YouTube Shorts
                if config.AUTO_POSTING:
                    results = social_poster.post_clips([clip_info])
                    print(f"Posted clip to social media platforms")
                    
                    # Save results
                    with open(f"results_{video_id}.json", 'w') as f:
                        json.dump(results, f, indent=2)
                        
                    print(f"Results saved to results_{video_id}.json")
        except Exception as e:
            print(f"Error creating clip: {e}")
    else:
        print("Failed to download video")
else:
    print(f"Could not find video with ID {video_id}")