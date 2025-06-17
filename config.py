# YouTube API Configuration
YOUTUBE_API_KEY = "AIzaSyB_vnu1fnwMAZYRrCZz0sgjnPirmn6WjH0"  # Replace with your actual API key

# YouTube channels to monitor (channel IDs)
YOUTUBE_CHANNELS = [
    # Global Top
    "UCq-Fj5jknLsUf-MWSy4_brA",  # T-Series
    "UCbCmjCuTUZos6Inko4u57UQ",  # Cocomelon
    "UCpEhnqL0y41EpW2TvWAHD7Q",  # SET India
    "UCX1xppLvuj03ubLio8jslyA",  # Sony SAB
    "UCk8GzjMOrta8yxDcKfylJYw",  # Kids Diana Show
    "UCJplp5SjeGSdVdwsfb9Q7lQ",  # Like Nastya
    "UCvlE5gTbOvjiolFlEm-c_Ow",  # Vlad and Niki
    "UCxIJaCMEptJjxmmQgGFsnCg",  # Zee TV
    "UCJ5v_MCY6GNUBTO8-D3XoAg",  # WWE
    "UCc1x7e63ENb0r2z1dBpyR-g",  # Toys and Colors
    "UCgM5P6QGHmrvu5fDPx79mug",  # Love Island UK
    "UCVV9-BZ_8EybNWtbvnF8DHw",  # Love Island USA
    # Streamer Channels
    "UCbxQcz8IduMBON0vjeG3Jmg",  # KaiCenat
    "UCq1VRjE_pS7x0do4mjJO4CQ",  # HasanAbi (Hasan Piker)
    "UCUWXFGknddR9z1yBOA4qXAw",  # DDG
    # AMP Collective & Friends
    "UCJbYdyufHR-cxOuY96KIoqA",  # AMP official :contentReference[oaicite:4]{index=4}
    "UCvCfpQXRXdJdL07pzTIA6Cw",  # Kai Cenat (AMP)
    "UCUWTgOq1rRrwtJq4gkkXqQw",  # ImDavisss
    "UChH4tWqMNfdK7d3f6AZPapg",  # Fanum
    "UCn3sgGnUE3amtS3-V17gPAQ",  # Duke Dennis
    "UCiTD6Zs4u00vgbSbdFwdVsQ",  # Agent 00
    "UCSQFnr49AdwaEW4WmznBrzg",  # Chrisnxtdoor
    "UCY1dIB3xXwUGyv8UX6oyleA",  # Flight
    "UCGFea_nkVJnZ_Nkd2dCERLQ",  # JiDion
    "UC0Yri0mPJy3X5NnzNwh7vVg",  # BruceDropEmOff
    # Top Trending in Kenya (2025)
    "UCqBJ47FjJ...",             # Citizen TV Kenya :contentReference[oaicite:5]{index=5}
    "UCKTN…",                   # KTN News Kenya :contentReference[oaicite:6]{index=6}
    "UCUi4aspUA…",              # TechFreeze :contentReference[oaicite:7]{index=7}
    "UCqBJ…",                   # NTV Kenya :contentReference[oaicite:8]{index=8}
    "UC0YG5UA1s…",              # Churchill Television :contentReference[oaicite:9]{index=9}
    "UCcKlbixN7…",              # Alvins Audi :contentReference[oaicite:10]{index=10}
    "UC…UrbanStreet254…",       # Urban Street +254 :contentReference[oaicite:11]{index=11}
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