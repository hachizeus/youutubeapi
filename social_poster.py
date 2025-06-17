import os
import requests
import json
import time
from datetime import datetime
import config

class SocialMediaPoster:
    def __init__(self):
        """Initialize the social media poster."""
        self.platforms = {
            "tiktok": self.post_to_tiktok,
            "instagram": self.post_to_instagram,
            "twitter": self.post_to_twitter,
            "youtube_shorts": self.post_to_youtube_shorts
        }
    
    def post_clip(self, clip_info, platforms=None):
        """Post a clip to specified platforms."""
        if not config.AUTO_POSTING:
            print(f"Auto-posting disabled. Clip ready at: {clip_info['path']}")
            return {"success": False, "message": "Auto-posting disabled"}
            
        if platforms is None:
            platforms = config.PLATFORMS_TO_POST
        
        results = {}
        
        for platform in platforms:
            if platform in self.platforms:
                print(f"Posting to {platform}...")
                try:
                    result = self.platforms[platform](clip_info)
                    results[platform] = result
                    print(f"Successfully posted to {platform}")
                except Exception as e:
                    print(f"Error posting to {platform}: {e}")
                    results[platform] = {"success": False, "error": str(e)}
                
                # Add delay between posts to avoid rate limits
                time.sleep(5)
            else:
                print(f"Platform {platform} not supported")
        
        return results
    
    def post_to_tiktok(self, clip_info):
        """Post a clip to TikTok."""
        # TikTok API implementation using TikTok Business API
        try:
            if not config.TIKTOK_ACCESS_TOKEN:
                print("TikTok access token not configured")
                return {
                    "success": False,
                    "message": "TikTok access token not configured",
                    "clip_path": clip_info['path']
                }
                
            # Upload video to TikTok
            # Note: This is a simplified implementation - actual TikTok API is more complex
            url = "https://business-api.tiktok.com/open_api/v1.3/video/upload/"
            headers = {
                "Access-Token": config.TIKTOK_ACCESS_TOKEN,
                "Content-Type": "multipart/form-data"
            }
            
            with open(clip_info['path'], 'rb') as video_file:
                files = {'video_file': video_file}
                data = {
                    'post_info': json.dumps({
                        'title': clip_info['title'],
                        'description': f"{clip_info['title']} #shorts #viral"
                    })
                }
                
                response = requests.post(url, headers=headers, files=files, data=data)
                
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "post_id": result.get('data', {}).get('video_id'),
                    "platform": "tiktok"
                }
            else:
                print(f"TikTok API error: {response.text}")
                return {
                    "success": False,
                    "message": f"TikTok API error: {response.status_code}",
                    "clip_path": clip_info['path']
                }
        except Exception as e:
            print(f"TikTok posting error: {e}")
            return {
                "success": False,
                "message": f"Manual upload required: {str(e)}",
                "clip_path": clip_info['path']
            }
    
    def post_to_instagram(self, clip_info):
        """Post a clip to Instagram Reels."""
        try:
            # Using Meta Graph API (requires Instagram Business account)
            url = f"https://graph.facebook.com/v17.0/{config.INSTAGRAM_BUSINESS_ID}/media"
            
            # First, upload the video
            params = {
                "access_token": config.INSTAGRAM_ACCESS_TOKEN,
                "media_type": "REELS",
                "video_url": clip_info['path'],  # This should be a publicly accessible URL
                "caption": clip_info['title']
            }
            
            response = requests.post(url, params=params)
            result = response.json()
            
            if 'id' in result:
                # Publish the container
                publish_url = f"https://graph.facebook.com/v17.0/{config.INSTAGRAM_BUSINESS_ID}/media_publish"
                publish_params = {
                    "access_token": config.INSTAGRAM_ACCESS_TOKEN,
                    "creation_id": result['id']
                }
                
                publish_response = requests.post(publish_url, params=publish_params)
                publish_result = publish_response.json()
                
                return {
                    "success": True,
                    "post_id": publish_result.get('id'),
                    "platform": "instagram"
                }
            else:
                raise Exception(f"Instagram upload failed: {result.get('error', {}).get('message')}")
        except Exception as e:
            raise Exception(f"Instagram posting error: {e}")
    
    def post_to_twitter(self, clip_info):
        """Post a clip to Twitter/X."""
        try:
            # Twitter API v2 implementation
            # Note: Twitter API v2 requires paid access for media uploads
            
            # This is a simplified example - actual implementation would use tweepy or similar
            print("Twitter posting requires paid API access")
            print(f"Please upload {clip_info['path']} manually to Twitter")
            
            return {
                "success": False,
                "message": "Manual upload required",
                "clip_path": clip_info['path']
            }
        except Exception as e:
            raise Exception(f"Twitter posting error: {e}")
    
    def post_to_youtube_shorts(self, clip_info):
        """Post a clip to YouTube Shorts."""
        try:
            if not config.YOUTUBE_CLIENT_ID or not config.YOUTUBE_CLIENT_SECRET or not config.YOUTUBE_REFRESH_TOKEN:
                print("YouTube OAuth credentials not fully configured")
                return {
                    "success": False,
                    "message": "YouTube OAuth credentials not configured",
                    "clip_path": clip_info['path']
                }
                
            # Get a new access token using refresh token
            token_url = "https://oauth2.googleapis.com/token"
            token_data = {
                "client_id": config.YOUTUBE_CLIENT_ID,
                "client_secret": config.YOUTUBE_CLIENT_SECRET,
                "refresh_token": config.YOUTUBE_REFRESH_TOKEN,
                "grant_type": "refresh_token"
            }
            
            token_response = requests.post(token_url, data=token_data)
            if token_response.status_code != 200:
                print(f"Failed to refresh YouTube token: {token_response.text}")
                return {
                    "success": False,
                    "message": "Failed to refresh YouTube token",
                    "clip_path": clip_info['path']
                }
                
            access_token = token_response.json().get("access_token")
            
            # Check if file exists and is a valid video file
            if not os.path.exists(clip_info['path']):
                print(f"Error: File not found at {clip_info['path']}")
                return {
                    "success": False,
                    "message": "File not found",
                    "clip_path": clip_info['path']
                }
                
            # Prepare metadata
            metadata = {
                "snippet": {
                    "title": clip_info['title'],
                    "description": f"{clip_info['title']} #shorts",
                    "tags": ["shorts", "viral", "trending"],
                    "categoryId": "22"  # People & Blogs
                },
                "status": {
                    "privacyStatus": "public",
                    "selfDeclaredMadeForKids": False
                }
            }
            
            # Use the resumable upload protocol
            # Step 1: Start the resumable session
            session_url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
            session_headers = {
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json; charset=UTF-8",
                "X-Upload-Content-Type": "video/mp4"
            }
            
            session_response = requests.post(
                session_url,
                headers=session_headers,
                data=json.dumps(metadata)
            )
            
            if session_response.status_code != 200:
                print(f"Failed to start upload session: {session_response.text}")
                return {
                    "success": False,
                    "message": f"Failed to start upload session: {session_response.status_code}",
                    "clip_path": clip_info['path']
                }
                
            # Get the upload URL from the Location header
            upload_url = session_response.headers.get('Location')
            
            # Step 2: Upload the file
            with open(clip_info['path'], 'rb') as video_file:
                video_data = video_file.read()
                
                upload_headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "video/mp4"
                }
                
                upload_response = requests.put(
                    upload_url,
                    headers=upload_headers,
                    data=video_data
                )
            
            if upload_response.status_code in [200, 201]:
                try:
                    result = upload_response.json()
                    video_id = result.get('id')
                except:
                    # If response is not JSON, try to extract video ID from response
                    video_id = "unknown"
                    
                return {
                    "success": True,
                    "video_id": video_id,
                    "platform": "youtube_shorts"
                }
            else:
                print(f"YouTube API upload error: {upload_response.text}")
                return {
                    "success": False,
                    "message": f"YouTube API upload error: {upload_response.status_code}",
                    "clip_path": clip_info['path']
                }
        except Exception as e:
            print(f"YouTube Shorts posting error: {e}")
            return {
                "success": False,
                "message": f"Manual upload required: {str(e)}",
                "clip_path": clip_info['path']
            }


def post_clips(clips, platforms=None):
    """Post multiple clips to social media platforms."""
    poster = SocialMediaPoster()
    results = []
    
    for clip in clips:
        result = poster.post_clip(clip, platforms)
        results.append({
            "clip": clip,
            "posting_results": result,
            "timestamp": datetime.now().isoformat()
        })
    
    return results