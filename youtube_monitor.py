import os
import time
import googleapiclient.discovery
from datetime import datetime, timedelta
import config

def setup_youtube_api():
    """Initialize the YouTube API client."""
    api_service_name = "youtube"
    api_version = "v3"
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=config.YOUTUBE_API_KEY)
    
    return youtube

def get_latest_videos(youtube, channel_id, published_after):
    """Get videos published after the specified date for a channel."""
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=5,
        order="date",
        publishedAfter=published_after.strftime('%Y-%m-%dT%H:%M:%SZ'),
        type="video"
    )
    
    response = request.execute()
    return response.get('items', [])

def monitor_channels():
    """Monitor channels for new videos."""
    youtube = setup_youtube_api()
    
    # Check for videos published in the last hour
    check_time = datetime.utcnow() - timedelta(hours=1)
    
    new_videos = []
    
    for channel_id in config.YOUTUBE_CHANNELS:
        try:
            videos = get_latest_videos(youtube, channel_id, check_time)
            for video in videos:
                video_id = video['id']['videoId']
                title = video['snippet']['title']
                channel_title = video['snippet']['channelTitle']
                published_at = video['snippet']['publishedAt']
                
                print(f"New video found: '{title}' from {channel_title}")
                new_videos.append({
                    'video_id': video_id,
                    'title': title,
                    'channel': channel_title,
                    'published_at': published_at
                })
        except Exception as e:
            print(f"Error monitoring channel {channel_id}: {e}")
    
    return new_videos

if __name__ == "__main__":
    # Create download directory if it doesn't exist
    os.makedirs(config.DOWNLOAD_PATH, exist_ok=True)
    os.makedirs(config.OUTPUT_PATH, exist_ok=True)
    
    print("Starting YouTube channel monitor...")
    while True:
        new_videos = monitor_channels()
        
        # Here you would call your video processing pipeline
        for video in new_videos:
            print(f"Processing video: {video['title']}")
            # Call your video processing function here
            # process_video(video['video_id'])
        
        # Check every 10 minutes
        print("Waiting for 10 minutes before next check...")
        time.sleep(600)