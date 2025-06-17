# YouTube Clip Automation System

This system automatically monitors YouTube channels, creates clips from new videos, and posts them to YouTube Shorts.

## Deployment Options

### Deploy to Render

1. Create a Render account at [render.com](https://render.com)

2. Connect your GitHub repository

3. Create a new Web Service:
   - Select your repository
   - Render will automatically detect the `render.yaml` configuration

4. Set up environment variables:
   - Add all the API keys and credentials from your config.py file

### Deploy to GitHub Actions

1. Create a GitHub repository for your project

2. Add GitHub Secrets for all your API keys and credentials

3. Create a GitHub Actions workflow file (see `.github/workflows/monitor.yml`)

## Local Setup

1. Install required packages:
   ```
   pip install -r requirements.txt
   ```

2. Configure API access:
   - Copy `config_example.py` to `config.py`
   - Add your API keys and credentials

3. Run the web server:
   ```
   python app.py
   ```

## API Endpoints

- `/` - Home page with status information
- `/start` - Start monitoring
- `/stop` - Stop monitoring
- `/status` - Get detailed status and processed videos

## Features

- Monitor specific YouTube channels for new uploads
- Download and process videos automatically
- Create vertical format clips optimized for Shorts
- Add title text overlays
- Automatically post to YouTube Shorts