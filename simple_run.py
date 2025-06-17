import os
import time
import json
import openai
import sys
import re
from datetime import datetime
import youtube_monitor
import video_processor
import social_poster
import config

# Set OpenAI API key
openai.api_key = config.OPENAI_API_KEY

def extract_video_id(url_or_id):
    """Extract video ID from a YouTube URL or return the ID if already provided."""
    # Check if it's a YouTube URL
    if "youtube.com" in url_or_id or "youtu.be" in url_or_id:
        # Handle youtube.com/watch?v= format
        watch_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', url_or_id)
        if watch_match:
            return watch_match.group(1)
        
        # Handle youtu.be/ format
        short_match = re.search(r'youtu\.be\/([0-9A-Za-z_-]{11})', url_or_id)
        if short_match:
            return short_match.group(1)
        
        # Handle youtube.com/shorts/ format
        shorts_match = re.search(r'shorts\/([0-9A-Za-z_-]{11})', url_or_id)
        if shorts_match:
            return shorts_match.group(1)
    
    # If it's already just the ID (11 characters of allowed chars)
    if re.match(r'^[0-9A-Za-z_-]{11}, url_or_id):
        return url_or_id
    
    return None

def main():
    """Simple test run to process a specific video."""
    # Create necessary directories
    os.makedirs(config.DOWNLOAD_PATH, exist_ok=True)
    os.makedirs(config.OUTPUT_PATH, exist_ok=True)
    
    # Get video ID from command line or prompt
    if len(sys.argv) > 1:
        url_or_id = sys.argv[1]
    else:
        url_or_id = input("Enter a YouTube video ID or URL to process: ")
    
    # Extract video ID
    video_id = extract_video_id(url_or_id)
    
    if not video_id:
        print(f"Error: Could not extract a valid YouTube video ID from '{url_or_id}'")
        print("Please provide either:")
        print("1. A YouTube video ID (11 characters, e.g., dQw4w9WgXcQ)")
        print("2. A YouTube video URL (e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
        print("3. A YouTube Shorts URL (e.g., https://www.youtube.com/shorts/6BEph-Pm0jg)")
        return
    
    print(f"Processing video ID: {video_id}")
    
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

if __name__ == "__main__":
    main()