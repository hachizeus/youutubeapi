import os
import time
import json
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

def create_real_clip(video_id, title):
    """Download video and create a clip with text overlay."""
    import yt_dlp
    from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
    
    # Create necessary directories
    os.makedirs(config.DOWNLOAD_PATH, exist_ok=True)
    os.makedirs(config.OUTPUT_PATH, exist_ok=True)
    
    # Download the video
    output_path = os.path.join(config.DOWNLOAD_PATH, f"{video_id}.mp4")
    clip_path = os.path.join(config.OUTPUT_PATH, f"{video_id}_clip.mp4")
    
    try:
        # Download with yt-dlp
        ydl_opts = {
            'format': 'best[height<=720]',
            'outtmpl': output_path,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'https://www.youtube.com/watch?v={video_id}'])
        
        print(f"Downloaded video to {output_path}")
        
        # Process the video
        with VideoFileClip(output_path) as video:
            # Get video duration
            duration = video.duration
            
            # Create a clip of the most interesting part (first 30-60 seconds)
            clip_duration = min(config.MAX_CLIP_DURATION, duration)
            start_time = 0
            
            # If video is long, start a bit into it
            if duration > 120:
                start_time = 30
            
            clip = video.subclip(start_time, start_time + clip_duration)
            
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
            
            # Add title text
            txt_clip = TextClip(title, fontsize=70, color='white', bg_color='black',
                               size=(clip_resized.w, None), method='caption')
            txt_clip = txt_clip.set_duration(5).set_position(('center', 'bottom'))
            
            # Composite video with text
            final_clip = CompositeVideoClip([clip_resized, txt_clip])
            
            # Write the clip
            final_clip.write_videofile(clip_path, codec="libx264", audio_codec="aac")
            
            print(f"Created clip: {clip_path}")
            
            # Create clip info
            clip_info = {
                "path": clip_path,
                "title": f"{title} #shorts",
                "source_video": video_id
            }
            
            return clip_info
    except Exception as e:
        print(f"Error creating clip: {e}")
        
        # Create a placeholder if download fails
        with open(clip_path, 'w') as f:
            f.write(f"Placeholder for clip from video {video_id}: {title}")
        
        print(f"Created placeholder clip: {clip_path}")
        
        # Create clip info
        clip_info = {
            "path": clip_path,
            "title": f"{title} #shorts",
            "source_video": video_id
        }
        
        return clip_info

def monitor_channels():
    """Monitor channels for new videos."""
    # Enable the YouTube API first by visiting:
    # https://console.developers.google.com/apis/api/youtube.googleapis.com/overview?project=1076110751369
    
    print("Before running this script, make sure to enable the YouTube Data API v3 at:")
    print("https://console.developers.google.com/apis/api/youtube.googleapis.com/overview?project=1076110751369")
    print("\nPress Enter to continue or Ctrl+C to exit...")
    input()
    
    try:
        youtube = setup_youtube_api()
        print("YouTube API initialized successfully!")
    except Exception as e:
        print(f"Error initializing YouTube API: {e}")
        print("Please enable the YouTube Data API v3 and try again.")
        return
    
    # Check for videos published in the last day
    check_time = datetime.utcnow() - timedelta(days=1)
    
    print(f"Checking for videos published after {check_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    
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
                
                # Create a real clip
                clip_info = create_real_clip(video_id, title)
                
                # Post to YouTube Shorts
                if config.AUTO_POSTING:
                    print("Posting to YouTube Shorts...")
                    results = social_poster.post_clips([clip_info])
                    print(f"Posted clip to YouTube Shorts")
        except Exception as e:
            print(f"Error monitoring channel {channel_id}: {e}")

if __name__ == "__main__":
    print("YouTube Channel Monitor")
    print("======================")
    monitor_channels()