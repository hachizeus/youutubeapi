import os
import json
import openai
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import config

# Set OpenAI API key
openai.api_key = config.OPENAI_API_KEY

def create_clip_from_local_video():
    """Create a clip from a local video file."""
    # Create necessary directories
    os.makedirs(config.OUTPUT_PATH, exist_ok=True)
    
    # Ask for local video path
    video_path = input("Enter the path to your local video file: ")
    
    if not os.path.exists(video_path):
        print(f"Error: File not found at {video_path}")
        return
    
    try:
        # Get video info
        video_id = os.path.basename(video_path).split('.')[0]
        title = input("Enter a title for the clip: ")
        
        # Create clip path
        clip_path = os.path.join(config.OUTPUT_PATH, f"{video_id}_clip.mp4")
        
        # Process the video
        with VideoFileClip(video_path) as video:
            # Get video duration
            duration = video.duration
            
            # Ask for clip start and end times
            print(f"Video duration: {duration:.2f} seconds")
            start_time = float(input(f"Enter clip start time (0-{duration:.2f}): "))
            end_time = float(input(f"Enter clip end time ({start_time:.2f}-{duration:.2f}): "))
            
            # Validate times
            start_time = max(0, min(start_time, duration - 5))
            end_time = min(duration, max(start_time + 5, end_time))
            
            # Create clip
            clip = video.subclip(start_time, end_time)
            
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
            
            print(f"\nCreated clip: {clip_path}")
            
            # Create clip info
            clip_info = {
                "path": clip_path,
                "title": f"{title} #shorts",
                "source_video": video_id
            }
            
            # Save clip info
            with open(f"clip_info_{video_id}.json", 'w') as f:
                json.dump(clip_info, f, indent=2)
            
            print(f"Clip info saved to clip_info_{video_id}.json")
            
            # Instructions for manual upload
            print("\nTo upload this clip to YouTube Shorts:")
            print("1. Go to YouTube Studio: https://studio.youtube.com/")
            print("2. Click 'CREATE' > 'Upload videos'")
            print("3. Select the clip file from the 'clips' folder")
            print("4. Add '#shorts' to the title or description")
            print("5. Click 'NEXT' and complete the upload process")
            
    except Exception as e:
        print(f"Error creating clip: {e}")

if __name__ == "__main__":
    print("Manual Clip Creator")
    print("==================")
    create_clip_from_local_video()