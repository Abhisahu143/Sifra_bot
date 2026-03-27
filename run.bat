@echo off
echo Installing requirements...
pip install -r requirements.txt
echo.
echo Starting Telegram AI Assistant Bot...
python bot.py
pause
