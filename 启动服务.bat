@echo off
chcp 65001 >nul
title 数维数据管家系统 - 完整启动

echo ============================================================
echo 数维数据管家系统 - 完整启动流程
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
docker start shuwei-mysql
if errorlevel 1 (
    echo [警告] MySQL 容器启动失败或已运行
    echo 将继续尝试启动服务...
) else (
    echo MySQL 容器已启动
    echo 等待 5 秒让数据库准备就绪...
    timeout /t 5 /nobreak >nul
)
echo.

echo [3/3] 启动应用服务...
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
