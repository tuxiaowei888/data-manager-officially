@echo off
chcp 65001 >nul
title 数维数据管家系统 - 快速启动

echo ============================================================
echo 数维数据管家系统 - 快速启动脚本
echo ============================================================
echo.

echo [1/3] 检查 Docker...
docker ps >nul 2>&1
if errorlevel 1 (
    echo [错误] Docker 未运行，请先启动 Docker Desktop
    pause
    exit /b 1
)
echo Docker 运行正常
echo.

echo [2/3] 启动 MySQL 容器...
docker start my-mysql
if errorlevel 1 (
    echo [警告] MySQL 容器启动失败或已运行
    echo 将继续尝试启动服务...
) else (
    echo MySQL 容器已启动
    echo 等待 5 秒让数据库准备就绪...
    timeout /t 5 /nobreak >nul
)
echo.

echo [3/3] 安装核心依赖并启动服务...
echo 正在安装核心依赖...
pip install fastapi uvicorn sqlalchemy pymysql pydantic --user
if errorlevel 1 (
    echo [警告] 依赖安装失败，将尝试直接启动服务...
)
echo.

echo 启动服务...
echo 服务地址：http://localhost:8000
echo 健康检查：http://localhost:8000/health
echo.
echo 按 Ctrl+C 停止服务
echo ============================================================
echo.

REM 启动服务
python main.py

echo.
echo 服务已停止
pause