@echo off
chcp 65001 >nul
title 数维数据管家系统 - 完整初始化

echo ============================================================
echo 数维数据管家系统 - 完整初始化与启动流程
echo ============================================================
echo.

echo [1/5] 检查 Docker...
docker ps >nul 2>&1
if errorlevel 1 (
    echo [错误] Docker 未运行，请先启动 Docker Desktop
    pause
    exit /b 1
)
echo Docker 运行正常
echo.

echo [2/5] 检查 MySQL 容器...
docker inspect my-mysql >nul 2>&1
if errorlevel 1 (
    echo [信息] MySQL 容器不存在，创建新容器...
    docker run --name my-mysql -e MYSQL_ROOT_PASSWORD=123456 -p 3306:3306 -d mysql:8.0
    if errorlevel 1 (
        echo [错误] 创建 MySQL 容器失败
        pause
        exit /b 1
    )
    echo MySQL 容器已创建
    echo 等待 10 秒让容器初始化...
    timeout /t 10 /nobreak >nul
echo.

echo [3/5] 启动 MySQL 容器...
docker start my-mysql
if errorlevel 1 (
    echo [警告] MySQL 容器启动失败或已运行
) else (
    echo MySQL 容器已启动
    echo 等待 5 秒让数据库准备就绪...
    timeout /t 5 /nobreak >nul
)
echo.

echo [4/5] 安装 Python 依赖...
echo 正在安装项目依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo [错误] 依赖安装失败，请以管理员身份运行此脚本
    pause
    exit /b 1
)
echo 依赖安装成功
echo.

echo [5/5] 初始化数据库...
echo 正在创建数据库表...
python scripts/full_init_db.py
if errorlevel 1 (
    echo [错误] 数据库初始化失败
    pause
    exit /b 1
)
echo 数据库初始化成功
echo.
echo ============================================================
echo ✅ 初始化完成！现在启动应用服务...
echo ============================================================
echo.
echo 服务地址：http://localhost:8000
echo 中文文档：http://localhost:8000/api-docs-cn
echo 健康检查：http://localhost:8000/health
echo.
echo 按 Ctrl+C 停止服务
echo ============================================================
echo.

REM 启动服务
python -m uvicorn main:app --host 0.0.0.0 --port 8000

echo.
echo 服务已停止
pause
