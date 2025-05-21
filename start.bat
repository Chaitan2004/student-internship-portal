@echo off
REM Start Docker containers in detached mode
docker-compose up -d

REM Wait a few seconds to let the app start
timeout /t 5

REM Open the default browser to your app URL (assuming localhost:5000)
start http://localhost:5000

REM Optional: keep the command window open or exit
pause
