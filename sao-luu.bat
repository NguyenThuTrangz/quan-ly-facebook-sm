@echo off
rem Sao luu lich su tro chuyen + bo nho cua Claude vao thu muc backup
chcp 65001 >nul
set "SRC=%USERPROFILE%\.claude\projects\D--claude-remote"
set "DST=%~dp0backup\D--claude-remote"
robocopy "%SRC%" "%DST%" /E /XO /NFL /NDL /NJH /NJS >nul
echo Da sao luu vao: %DST%
