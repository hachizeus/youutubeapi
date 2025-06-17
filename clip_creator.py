import os
import time
import json
import openai
from datetime import datetime
import youtube_monitor
import video_processor
import config

# Set OpenAI API key
openai.api_key = config.OPENAI_API_KEY

def process_single_video(video_id):
    """Process a single video to create clips."""
    # Create necessary directories
    os.makedirs(config.DOWNLOAD_PATH, exist_ok=True)
    os.makedirs(config.OUTPUT_PATH, exist_ok=True)
    
    print(f"Processing video ID: {video_id}")
    
    # Process the video to create clips
    clips = video_processor.process_video(video_id)
    
    if clips:
        print(f"\nCreated {len(clips)} clips from video {video_id}:")
        for i, clip in enumerate(clips):
            print(f"  {i+1}. {clip['title']}")
            print(f"     Path: {clip['path']}")
        
        # Save clip info
        clip_info_file = f"clips_{video_id}.json"
        with open(clip_info_file, 'w') as f:
            json.dump(clips, f, indent=2)
            
        print(f"\nClip information saved to {clip_info_file}")
        print("\nYou can now manually upload these clips to YouTube Shorts or other platforms.")
    else:
        print(f"No clips were created for video {video_id}")

def monitor_and_create_clips():
    """Monitor YouTube channels and create clips from new videos."""
    # Create necessary directories
    os.makedirs(config.DOWNLOAD_PATH, exist_ok=True)
    os.makedirs(config.OUTPUT_PATH, exist_ok=True)
    
    print("Starting YouTube channel monitor...")
    
    # Keep track of processed videos
    processed_videos = set()
    if os.path.exists("processed_videos.json"):
        with open("processed_videos.json", 'r') as f:
            processed_data = json.load(f)
            processed_videos = set(item["video_id"] for item in processed_data)
    
    while True:
        try:
            # Monitor for new videos
            print("\nChecking for new videos...")
            new_videos = youtube_monitor.monitor_channels()
            
            for video in new_videos:
                video_id = video['video_id']
                
                # Skip if already processed
                if video_id in processed_videos:
                    print(f"Video {video_id} already processed, skipping")
                    continue
                
                print(f"\nProcessing video: {video['title']} ({video_id})")
                
                # Process the video to create clips
                clips = video_processor.process_video(video_id)
                
                if clips:
                    print(f"Created {len(clips)} clips from video {video_id}:")
                    for i, clip in enumerate(clips):
                        print(f"  {i+1}. {clip['title']}")
                        print(f"     Path: {clip['path']}")
                    
                    # Save clip info
                    clip_info_file = f"clips_{video_id}.json"
                    with open(clip_info_file, 'w') as f:
                        json.dump(clips, f, indent=2)
                        
                    print(f"\nClip information saved to {clip_info_file}")
                    print("You can now manually upload these clips to YouTube Shorts.")
                else:
                    print(f"No clips were created for video {video_id}")
                
                # Mark as processed
                processed_videos.add(video_id)
                with open("processed_videos.json", 'w') as f:
                    json.dump([{"video_id": vid, "processed_at": datetime.now().isoformat()} 
                              for vid in processed_videos], f)
            
            # Wait before next check
            print("\nWaiting for next check (10 minutes)...")
            time.sleep(600)  # 10 minutes
            
        except Exception as e:
            print(f"Error in monitoring loop: {e}")
            time.sleep(60)  # Wait a minute before retrying

if __name__ == "__main__":
    print("YouTube Clip Creator")
    print("===================")
    print("1. Process a specific video")
    print("2. Monitor channels for new videos")
    choice = input("\nEnter your choice (1 or 2): ")
    
    if choice == "1":
        video_id = input("Enter YouTube video ID: ")
        process_single_video(video_id)
    elif choice == "2":
        monitor_and_create_clips()
    else:
        print("Invalid choice. Exiting.")