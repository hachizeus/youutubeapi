import os
import time
import json
import openai
from datetime import datetime
import youtube_monitor
import video_processor
import social_poster
import config

# Set OpenAI API key
openai.api_key = config.OPENAI_API_KEY

def save_processed_videos(video_id):
    """Save processed video ID to avoid reprocessing."""
    processed_file = "processed_videos.json"
    
    processed = []
    if os.path.exists(processed_file):
        with open(processed_file, 'r') as f:
            processed = json.load(f)
    
    processed.append({
        "video_id": video_id,
        "processed_at": datetime.now().isoformat()
    })
    
    with open(processed_file, 'w') as f:
        json.dump(processed, f)

def is_already_processed(video_id):
    """Check if a video has already been processed."""
    processed_file = "processed_videos.json"
    
    if not os.path.exists(processed_file):
        return False
    
    with open(processed_file, 'r') as f:
        processed = json.load(f)
    
    return any(item["video_id"] == video_id for item in processed)

def main():
    """Main function to run the entire pipeline."""
    # Create necessary directories
    os.makedirs(config.DOWNLOAD_PATH, exist_ok=True)
    os.makedirs(config.OUTPUT_PATH, exist_ok=True)
    
    print("Starting YouTube clip automation system...")
    
    while True:
        try:
            # Monitor for new videos
            print("Checking for new videos...")
            new_videos = youtube_monitor.monitor_channels()
            
            for video in new_videos:
                video_id = video['video_id']
                
                # Skip if already processed
                if is_already_processed(video_id):
                    print(f"Video {video_id} already processed, skipping")
                    continue
                
                print(f"Processing video: {video['title']} ({video_id})")
                
                # Process the video to create clips
                clips = video_processor.process_video(video_id)
                
                if clips:
                    print(f"Created {len(clips)} clips from video {video_id}")
                    
                    # Post clips to social media
                    results = social_poster.post_clips(clips)
                    
                    print(f"Posted {len(clips)} clips to social media platforms")
                    
                    # Save results
                    with open(f"results_{video_id}.json", 'w') as f:
                        json.dump(results, f)
                else:
                    print(f"No clips were created for video {video_id}")
                
                # Mark as processed
                save_processed_videos(video_id)
            
            # Wait before next check
            print("Waiting for next check...")
            time.sleep(600)  # 10 minutes
            
        except Exception as e:
            print(f"Error in main loop: {e}")
            time.sleep(60)  # Wait a minute before retrying

if __name__ == "__main__":
    main()