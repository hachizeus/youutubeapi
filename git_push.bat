@echo off
echo Pushing code to GitHub repository...

git init
git add .
git commit -m "Initial setup for Render deployment"
git branch -M main
git remote add origin https://github.com/hachizeus/youutubeapi.git
git push -u origin main

echo.
echo Code pushed to GitHub. Now set up the project on Render.com
pause