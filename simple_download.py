import os
from pytube import YouTube
from moviepy.editor import VideoFileClip
import config
import social_poster

# Create necessary directories
os.makedirs(config.DOWNLOAD_PATH, exist_ok=True)
os.makedirs(config.OUTPUT_PATH, exist_ok=True)

# YouTube Shorts URL
url = "https://www.youtube.com/shorts/6BEph-Pm0jg"
video_id = "6BEph-Pm0jg"

print(f"Downloading YouTube Shorts: {url}")

try:
    # Download the video using pytube
    yt = YouTube(url)
    print(f"Video title: {yt.title}")
    
    # Get the highest resolution stream
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    
    if not stream:
        print("No suitable stream found, trying with file extension only")
        stream = yt.streams.filter(file_extension='mp4').first()
    
    if stream:
        # Download the video
        video_path = os.path.join(config.DOWNLOAD_PATH, f"{video_id}.mp4")
        stream.download(output_path=config.DOWNLOAD_PATH, filename=f"{video_id}.mp4")
        print(f"Downloaded video to {video_path}")
        
        # Create a clip
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
                "title": f"{yt.title} #shorts",
                "source_video": video_id
            }
            
            # Post to YouTube Shorts
            if config.AUTO_POSTING:
                results = social_poster.post_clips([clip_info])
                print(f"Posted clip to YouTube Shorts")
    else:
        print("No suitable stream found for download")
        
except Exception as e:
    print(f"Error: {e}")