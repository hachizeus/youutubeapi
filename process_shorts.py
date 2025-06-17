import os
import json
import openai
import re
import youtube_monitor
import video_processor
import social_poster
import config

# Set OpenAI API key
openai.api_key = config.OPENAI_API_KEY

# Create necessary directories
os.makedirs(config.DOWNLOAD_PATH, exist_ok=True)
os.makedirs(config.OUTPUT_PATH, exist_ok=True)

# The YouTube Shorts URL
url = "https://www.youtube.com/shorts/6BEph-Pm0jg?feature=share"

# Extract video ID from URL
match = re.search(r'shorts\/([0-9A-Za-z_-]{11})', url)
if match:
    video_id = match.group(1)
    print(f"Processing YouTube Shorts video ID: {video_id}")
    
    # Process the video to create clips
    clips = video_processor.process_video(video_id)
    
    if clips:
        print(f"Created {len(clips)} clips from video {video_id}")
        
        # Post clips to social media
        results = social_poster.post_clips(clips)
        
        print(f"Posted {len(clips)} clips to social media platforms")
        
        # Save results
        with open(f"results_{video_id}.json", 'w') as f:
            json.dump(results, f, indent=2)
            
        print(f"Results saved to results_{video_id}.json")
    else:
        print(f"No clips were created for video {video_id}")
else:
    print("Could not extract video ID from the URL")