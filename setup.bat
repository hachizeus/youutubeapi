@echo off
echo Installing required packages...
pip install -r requirements.txt

echo Creating directories...
mkdir downloads
mkdir clips

echo.
echo Setup complete! Before running the system:
echo 1. Edit config.py to add your YouTube API key
echo 2. Add your OpenAI API key to config.py
echo 3. Add YouTube channel IDs to monitor
echo 4. Run the system with: python main.py
echo.
pause