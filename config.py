# YouTube API Configuration
YOUTUBE_API_KEY = "AIzaSyB_vnu1fnwMAZYRrCZz0sgjnPirmn6WjH0"  # Replace with your actual API key

# YouTube channels to monitor (channel IDs)
YOUTUBE_CHANNELS = [
    "UC4tjY2tTltEKePusozUxtSA",  # Replace with actual channel IDs
    "UCvCfpQXRXdJdL07pzTIA6Cw",
    "UCh2aTKSbIyxpnOsbHsmV-ig",
]




# YouTube (for Shorts)
YOUTUBE_CLIENT_ID = "1076110751369-3d5lbvknl7ni5pt8n7rne8j4oep2942o.apps.googleusercontent.com"  # From your OAuth credentials
YOUTUBE_CLIENT_SECRET = "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"  # Add your YouTube client secret
YOUTUBE_REFRESH_TOKEN = "1//04912vaxGdrzFCgYIARAAGAQSNwF-L9Ir-Oz55n_tXc2Rl4K2iC9NicrNWCFCpHg8apEp1PlAfbqoMQ8Nd_VCvl931CQZ1bLsQBA"  # Add your YouTube refresh token

# OpenAI API Configuration
OPENAI_API_KEY = "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"

# Video Processing Settings
MAX_CLIP_DURATION = 60  # seconds
MIN_CLIP_DURATION = 15  # seconds
MAX_CLIPS_PER_VIDEO = 3

# Social Media Settings
PLATFORMS_TO_POST = ["youtube_shorts"]  # Enable YouTube Shorts posting
AUTO_POSTING = True  # Enable auto-posting

# Paths
DOWNLOAD_PATH = "downloads/"
OUTPUT_PATH = "clips/"