@echo off
echo YouTube Clip Creator - Test Run
echo ==============================
echo.
echo This script will process a sample YouTube video to test the system.
echo.

set /p VIDEO_ID=Enter a YouTube video ID (e.g., dQw4w9WgXcQ): 

echo.
echo Processing video ID: %VIDEO_ID%
echo.

python simple_run.py %VIDEO_ID%

echo.
echo Test complete! Check the "clips" folder for generated clips.
pause