import os
import random
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip
import config
import social_poster

# Create necessary directories
os.makedirs(config.OUTPUT_PATH, exist_ok=True)

def create_sample_clip(video_id, title):
    """Create a sample clip with text overlay."""
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

# Create sample clips for the videos we found
videos = [
    {"id": "rPv52YvNTAE", "title": "So Close to America, Then THIS Happened"},
    {"id": "qabZYEi_QCA", "title": "Agent Visits the NEW OTK Mansion"},
    {"id": "lTP6AJ8ww6g", "title": "Getting Ready for Streamer Prom"}
]

# Process each video
for video in videos:
    print(f"Creating sample clip for: {video['title']}")
    clip_info = create_sample_clip(video["id"], video["title"])
    
    # Post to YouTube Shorts
    print("Posting to YouTube Shorts...")
    results = social_poster.post_clips([clip_info])
    print(f"Posted clip to YouTube Shorts")