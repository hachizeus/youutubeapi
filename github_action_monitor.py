import os
import json
import time
from datetime import datetime, timedelta
import googleapiclient.discovery
import config
import social_poster

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

def create_sample_clip(video_id, title):
    """Create a sample clip with text overlay."""
    from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
    
    # Create necessary directories
    os.makedirs(config.OUTPUT_PATH, exist_ok=True)
    
    # Create clip path
    clip_path = os.path.join(config.OUTPUT_PATH, f"{video_id}_clip.mp4")
    
    # Create a simple color background clip
    color_clip = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=15)
    
    # Create text clips
    title_clip = TextClip(title, fontsize=60, color='white', size=(1000, None), 
                         method='caption', align='center')
    title_clip = title_clip.set_position(('center', 200)).set_duration(15)
    
    hashtag_clip = TextClip("#shorts", fontsize=70, color='white', 
                           size=(1000, None), method='caption')
    hashtag_clip = hashtag_clip.set_position(('center', 1700)).set_duration(15)
    
    # Create composite clip
    final_clip = CompositeVideoClip([color_clip, title_clip, hashtag_clip])
    
    # Write the clip
    final_clip.write_videofile(clip_path, codec="libx264", fps=24)
    
    print(f"Created sample clip: {clip_path}")
    
    # Create clip info
    clip_info = {
        "path": clip_path,
        "title": f"{title} #shorts",
        "source_video": video_id
    }
    
    return clip_info

def monitor_channels():
    """Monitor channels for new videos."""
    # Check for videos published in the last day
    check_time = datetime.utcnow() - timedelta(days=1)
    print(f"Checking for videos published after {check_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    
    try:
        youtube = setup_youtube_api()
        
        # Store processed videos
        processed_videos = []
        
        for channel_id in config.YOUTUBE_CHANNELS:
            try:
                print(f"Checking channel: {channel_id}")
                videos = get_latest_videos(youtube, channel_id, check_time)
                
                if not videos:
                    print(f"No new videos found for channel {channel_id}")
                    continue
                    
                print(f"Found {len(videos)} new videos for channel {channel_id}")
                
                for video in videos:
                    video_id = video['id']['videoId']
                    title = video['snippet']['title']
                    channel_title = video['snippet']['channelTitle']
                    published_at = video['snippet']['publishedAt']
                    
                    print(f"\nNew video found: '{title}' from {channel_title}")
                    print(f"Video ID: {video_id}")
                    print(f"Published at: {published_at}")
                    
                    # Create a sample clip
                    clip_info = create_sample_clip(video_id, title)
                    
                    # Post to YouTube Shorts
                    if config.AUTO_POSTING:
                        print("Posting to YouTube Shorts...")
                        results = social_poster.post_clips([clip_info])
                        print(f"Posted clip to YouTube Shorts")
                    
                    # Add to processed videos
                    processed_videos.append({
                        "video_id": video_id,
                        "title": title,
                        "channel": channel_title,
                        "published_at": published_at,
                        "clip_path": clip_info["path"]
                    })
                    
            except Exception as e:
                print(f"Error monitoring channel {channel_id}: {e}")
        
        # Save processed videos
        with open("processed_videos.json", "w") as f:
            json.dump(processed_videos, f, indent=2)
        
    except Exception as e:
        print(f"Error in monitoring: {e}")

if __name__ == "__main__":
    print("Running YouTube channel monitor...")
    monitor_channels()
    print("Monitoring complete.")