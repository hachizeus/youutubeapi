# Render Deployment Steps

## 1. Push Your Code to GitHub

```bash
git init
git add .
git commit -m "Initial setup for Render deployment"
git branch -M main
git remote add origin https://github.com/hachizeus/youutubeapi.git
git push -u origin main
```

## 2. Set Up on Render

1. Go to [render.com](https://render.com) and sign up/login
2. Click "New" and select "Web Service"
3. Connect to your GitHub repository: https://github.com/hachizeus/youutubeapi.git
4. Configure the service:
   - Name: youtube-clip-automation
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Select the appropriate plan (Free tier works for testing)

## 3. Set Environment Variables

Add these environment variables in the Render dashboard:
- `YOUTUBE_API_KEY`: AIzaSyB_vnu1fnwMAZYRrCZz0sgjnPirmn6WjH0
- `YOUTUBE_CLIENT_ID`: 1076110751369-3d5lbvknl7ni5pt8n7rne8j4oep2942o.apps.googleusercontent.com
- `YOUTUBE_CLIENT_SECRET`: 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
- `YOUTUBE_REFRESH_TOKEN`: 1//04912vaxGdrzFCgYIARAAGAQSNwF-L9Ir-Oz55n_tXc2Rl4K2iC9NicrNWCFCpHg8apEp1PlAfbqoMQ8Nd_VCvl931CQZ1bLsQBA
- `OPENAI_API_KEY`: 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

## 4. Deploy

Click "Create Web Service" and Render will deploy your application.

## 5. Start Monitoring

Once deployed, visit:
- `https://youtube-clip-automation.onrender.com/start` to start monitoring
- `https://youtube-clip-automation.onrender.com/status` to check status

## 6. Update YouTube API Settings

Go to Google Cloud Console and update your API key settings:
- Set "Application restrictions" to "None" or add Render's IP addresses
- This will allow your Render app to use the YouTube API