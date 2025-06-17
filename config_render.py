import os

# YouTube API Configuration
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

# YouTube channels to monitor (channel IDs)
YOUTUBE_CHANNELS = [
    "UC4tjY2tTltEKePusozUxtSA",
    "UCvCfpQXRXdJdL07pzTIA6Cw",
    "UCh2aTKSbIyxpnOsbHsmV-ig",
]

# YouTube (for Shorts)
YOUTUBE_CLIENT_ID = os.environ.get("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.environ.get("YOUTUBE_CLIENT_SECRET")
YOUTUBE_REFRESH_TOKEN = os.environ.get("YOUTUBE_REFRESH_TOKEN")

# OpenAI API Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Video Processing Settings
MAX_CLIP_DURATION = 60  # seconds
MIN_CLIP_DURATION = 15  # seconds
MAX_CLIPS_PER_VIDEO = 3

# Social Media Settings
PLATFORMS_TO_POST = ["youtube_shorts"]
AUTO_POSTING = True

# Paths
DOWNLOAD_PATH = "downloads/"
OUTPUT_PATH = "clips/"