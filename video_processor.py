import os
import yt_dlp
import openai
import json
from moviepy.editor import VideoFileClip
import config

def download_video(video_id):
    """Download a YouTube video using yt-dlp."""
    output_path = os.path.join(config.DOWNLOAD_PATH, f"{video_id}.mp4")
    
    if os.path.exists(output_path):
        print(f"Video {video_id} already downloaded")
        return output_path
    
    ydl_opts = {
        'format': 'best[height<=720]',
        'outtmpl': output_path,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f'https://www.youtube.com/watch?v={video_id}'])
        print(f"Downloaded video {video_id}")
        return output_path
    except Exception as e:
        print(f"Error downloading video {video_id}: {e}")
        return None

def transcribe_video(video_path):
    """Transcribe video using OpenAI's Whisper API."""
    try:
        # Extract audio from video
        audio_path = video_path.replace('.mp4', '.mp3')
        os.system(f'ffmpeg -i "{video_path}" -q:a 0 -map a "{audio_path}" -y')
        
        # Use OpenAI API for transcription
        with open(audio_path, "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
        
        # Clean up audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)
            
        return transcript["text"], []  # No segments with OpenAI API
    except Exception as e:
        print(f"Error transcribing video: {e}")
        return "", []

def find_highlights(transcript, segments):
    """Use OpenAI to find interesting clips in the video."""
    try:
        prompt = f"""
        Based on this video transcript, identify the {config.MAX_CLIPS_PER_VIDEO} most engaging 
        segments that would make good short-form content (15-60 seconds each).
        
        For each segment, provide:
        1. Start time (in seconds)
        2. End time (in seconds)
        3. A catchy title for the clip
        
        Transcript:
        {transcript[:4000]}  # Limit transcript length for API
        
        Format your response as JSON:
        [
            {{"start": 120, "end": 150, "title": "Example Highlight Title"}},
            ...
        ]
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )
        
        # Parse the JSON response
        content = response.choices[0].message.content
        # Extract JSON part from the response
        json_str = content.strip()
        if "```json" in json_str:
            json_str = json_str.split("```json")[1].split("```")[0].strip()
        elif "```" in json_str:
            json_str = json_str.split("```")[1].strip()
            
        highlights = json.loads(json_str)
        return highlights
    except Exception as e:
        print(f"Error finding highlights: {e}")
        # Fallback: create clips at regular intervals
        total_duration = sum(segment.get("end", 0) - segment.get("start", 0) for segment in segments)
        if total_duration > 0:
            clip_duration = min(60, max(15, total_duration / 3))
            return [
                {"start": i * clip_duration, "end": (i + 1) * clip_duration, 
                 "title": f"Clip {i+1}"} 
                for i in range(min(3, int(total_duration / clip_duration)))
            ]
        return []

def create_clip(video_path, start_time, end_time, title, clip_number):
    """Create a short clip from the video."""
    try:
        # Extract video ID from path
        video_id = os.path.basename(video_path).split('.')[0]
        output_path = os.path.join(config.OUTPUT_PATH, f"{video_id}_clip_{clip_number}.mp4")
        
        with VideoFileClip(video_path) as video:
            # Ensure start and end times are within video duration
            max_duration = video.duration
            start = max(0, min(start_time, max_duration - 5))
            end = min(max_duration, max(start + 5, end_time))
            
            # Create clip
            clip = video.subclip(start, end)
            
            # Resize for vertical platforms (9:16 aspect ratio)
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
            # clip_with_text = clip_resized.set_title(title)  # You'll need to implement this
            
            # Write the final clip
            clip_resized.write_videofile(output_path, codec="libx264", audio_codec="aac")
            
            return output_path
    except Exception as e:
        print(f"Error creating clip: {e}")
        return None

def process_video(video_id):
    """Process a video: download, transcribe, find highlights, create clips."""
    # Download the video
    video_path = download_video(video_id)
    if not video_path:
        return []
    
    # Transcribe the video
    transcript, segments = transcribe_video(video_path)
    if not transcript:
        return []
    
    # Find highlights
    highlights = find_highlights(transcript, segments)
    
    # Create clips
    clips = []
    for i, highlight in enumerate(highlights):
        if i >= config.MAX_CLIPS_PER_VIDEO:
            break
            
        clip_path = create_clip(
            video_path, 
            highlight["start"], 
            highlight["end"], 
            highlight["title"],
            i
        )
        
        if clip_path:
            clips.append({
                "path": clip_path,
                "title": highlight["title"],
                "source_video": video_id
            })
    
    return clips