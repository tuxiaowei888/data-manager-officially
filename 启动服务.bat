@echo off
title 数维数据管家 - API服务
color 0B
echo.
echo  ========================================
echo    数维数据管家 - 服务启动器
echo  ========================================
echo.
echo  正在启动服务...
echo.
cd /d "%~dp0"
python -m uvicorn main:app --host 0.0.0.0 --port 8000
pause
