@echo off
rem Mo terminal tai thu muc chua file nay va chay Claude Code (tiep phien cu, bat Chrome)
cd /d "%~dp0"
where wt >nul 2>nul
if %errorlevel%==0 (
    start "" wt -d "%~dp0." cmd /k claude --continue --chrome
) else (
    start "" cmd /k claude --continue --chrome
)
