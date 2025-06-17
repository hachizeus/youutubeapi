# Deployment Instructions

## Option 1: Deploy to Render

1. **Create a GitHub repository**
   - Create a new repository on GitHub
   - Push your code to the repository:
     ```
     git init
     git add .
     git commit -m "Initial commit"
     git branch -M main
     git remote add origin https://github.com/yourusername/your-repo-name.git
     git push -u origin main
     ```

2. **Sign up for Render**
   - Go to [render.com](https://render.com) and create an account
   - Connect your GitHub account

3. **Create a new Web Service**
   - Click "New" and select "Web Service"
   - Select your repository
   - Render will automatically detect the `render.yaml` configuration
   - Set the following environment variables:
     - `YOUTUBE_API_KEY`
     - `YOUTUBE_CLIENT_ID`
     - `YOUTUBE_CLIENT_SECRET`
     - `YOUTUBE_REFRESH_TOKEN`
     - `OPENAI_API_KEY`

4. **Deploy the service**
   - Click "Create Web Service"
   - Render will build and deploy your application
   - Your service will be available at `https://your-service-name.onrender.com`

5. **Start monitoring**
   - Visit `https://your-service-name.onrender.com/start` to start monitoring
   - Check status at `https://your-service-name.onrender.com/status`

## Option 2: Deploy with GitHub Actions

1. **Create a GitHub repository**
   - Create a new repository on GitHub
   - Push your code to the repository

2. **Set up GitHub Secrets**
   - Go to your repository settings
   - Click on "Secrets and variables" > "Actions"
   - Add the following secrets:
     - `YOUTUBE_API_KEY`
     - `YOUTUBE_CHANNEL_1`
     - `YOUTUBE_CHANNEL_2`
     - `YOUTUBE_CLIENT_ID`
     - `YOUTUBE_CLIENT_SECRET`
     - `YOUTUBE_REFRESH_TOKEN`
     - `OPENAI_API_KEY`

3. **Enable GitHub Actions**
   - GitHub will automatically detect the workflow file in `.github/workflows/`
   - You can manually trigger the workflow from the "Actions" tab
   - The workflow will also run automatically every 2 hours

## Important Notes

1. **API Restrictions**
   - Make sure your YouTube API key allows requests from your deployment platform
   - For Render, you may need to set "Application restrictions" to "None" or add Render's IP addresses

2. **Storage Considerations**
   - Both Render and GitHub Actions have limited storage
   - Consider using cloud storage (like AWS S3) for storing videos and clips

3. **Monitoring**
   - Set up monitoring to ensure your service stays running
   - Render provides built-in monitoring and logs