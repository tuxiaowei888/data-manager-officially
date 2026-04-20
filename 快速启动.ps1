# 数维数据管家系统 - 快速启动脚本

Write-Host "============================================================" -ForegroundColor Green
Write-Host "数维数据管家系统 - 快速启动脚本" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

# [1/3] 检查 Docker
Write-Host "[1/3] 检查 Docker..." -ForegroundColor Cyan
try {
    docker ps > $null 2>&1
    Write-Host "Docker 运行正常" -ForegroundColor Green
} catch {
    Write-Host "[错误] Docker 未运行，请先启动 Docker Desktop" -ForegroundColor Red
    Read-Host "按 Enter 键退出..."
    exit 1
}
Write-Host ""

# [2/3] 启动 MySQL 容器
Write-Host "[2/3] 启动 MySQL 容器..." -ForegroundColor Cyan
try {
    docker start my-mysql > $null 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "MySQL 容器已启动" -ForegroundColor Green
        Write-Host "等待 5 秒让数据库准备就绪..." -ForegroundColor Yellow
        Start-Sleep -Seconds 5
    } else {
        Write-Host "[警告] MySQL 容器启动失败或已运行" -ForegroundColor Yellow
        Write-Host "将继续尝试启动服务..." -ForegroundColor Yellow
    }
} catch {
    Write-Host "[警告] MySQL 容器操作失败" -ForegroundColor Yellow
}
Write-Host ""

# [3/3] 安装核心依赖并启动服务
Write-Host "[3/3] 安装核心依赖并启动服务..." -ForegroundColor Cyan
Write-Host "正在安装核心依赖..." -ForegroundColor Yellow
try {
    pip install fastapi uvicorn sqlalchemy pymysql pydantic --user
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[警告] 依赖安装失败，将尝试直接启动服务..." -ForegroundColor Yellow
    }
} catch {
    Write-Host "[警告] 依赖安装失败，将尝试直接启动服务..." -ForegroundColor Yellow
}
Write-Host ""

Write-Host "启动服务..." -ForegroundColor Green
Write-Host "服务地址：http://localhost:8000" -ForegroundColor Cyan
Write-Host "健康检查：http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

# 启动服务
python main.py

Write-Host ""
Write-Host "服务已停止" -ForegroundColor Green
Read-Host "按 Enter 键退出..."
