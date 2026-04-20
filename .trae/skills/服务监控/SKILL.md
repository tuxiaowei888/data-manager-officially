---
name: 服务监控
description: 监控服务状态，自动重启服务。当用户要求监控服务、检查状态或重启服务时调用。
---

# 服务监控

该技能用于监控系统服务状态，包括健康检查、自动重启等。

## 监控指标

| 指标 | 说明 | 阈值 |
|------|------|------|
| 服务状态 | 进程是否运行 | - |
| 响应时间 | API响应速度 | < 1秒 |
| 端口状态 | 端口是否监听 | - |
| 内存使用 | 内存占用情况 | < 80% |
| CPU使用 | CPU占用情况 | < 80% |
| 错误率 | 请求错误比例 | < 5% |

## 监控步骤

### 步骤1：检查服务状态
```bash
# 检查服务进程
Get-Process python -ErrorAction SilentlyContinue | Select-Object Id, ProcessName, CPU, WorkingSet

# 检查端口监听
netstat -ano | Select-String -Pattern ':8000.*LISTENING'

# 检查服务健康
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5
    Write-Host "服务健康: " $response.StatusCode
} catch {
    Write-Host "服务异常: " $_.Exception.Message
}
```

### 步骤2：检查Docker容器
```bash
# 检查MySQL容器
docker ps | Select-String -Pattern "<DB_CONTAINER>"

# 检查容器状态
docker inspect <DB_CONTAINER> | Select-String -Pattern '"Status"' -Context 0,2

# 检查容器资源
docker stats <DB_CONTAINER> --no-stream
```

### 步骤3：检查数据库连接
```bash
# 测试数据库连接
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "SELECT 1;"

# 检查数据库连接数
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "SHOW PROCESSLIST;"
```

### 步骤4：检查系统资源
```bash
# 检查CPU使用
Get-Process | Sort-Object CPU -Descending | Select-Object -First 5

# 检查内存使用
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 5

# 检查磁盘空间
Get-PSDrive C | Select-Object Used, Free
```

## 自动重启

### 重启服务
```bash
# 停止服务
Get-NetTCPConnection -LocalPort 8000 | Stop-Process -Force

# 等待
Start-Sleep -Seconds 2

# 启动服务
Start-Process python -ArgumentList "main.py" -NoNewWindow -PassThru
```

### 重启数据库容器
```bash
# 重启MySQL容器
docker restart <DB_CONTAINER>

# 等待启动
Start-Sleep -Seconds 10

# 验证
docker ps | Select-String -Pattern "<DB_CONTAINER>"
```

## 持续监控

### 设置监控循环
```powershell
# 持续监控服务（每30秒检查一次）
while ($true) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

    # 检查服务
    $serviceRunning = netstat -ano | Select-String -Pattern ':8000.*LISTENING'

    if ($serviceRunning) {
        Write-Host "[$timestamp] 服务正常" -ForegroundColor Green
    } else {
        Write-Host "[$timestamp] 服务异常，正在重启..." -ForegroundColor Red
        # 重启逻辑
    }

    # 检查MySQL
    $mysqlRunning = docker ps | Select-String -Pattern "<DB_CONTAINER>"
    if (-not $mysqlRunning) {
        Write-Host "[$timestamp] MySQL异常，正在重启..." -ForegroundColor Red
        docker restart <DB_CONTAINER>
    }

    Start-Sleep -Seconds 30
}
```

## 监控报告

```
## 服务监控报告
监控时间: 2024-03-18 15:30

### 服务状态
| 服务 | 状态 | 端口 | PID |
|------|------|------|-----|
| FastAPI | 运行中 | 8000 | 12345 |
| MySQL | 运行中 | 3306 | - |

### 系统资源
| 指标 | 值 | 状态 |
|------|-----|------|
| CPU使用 | 15% | 正常 |
| 内存使用 | 45% | 正常 |
| 磁盘空间 | 65% | 正常 |

### 数据库
- 连接数: 5
- 查询数/秒: 12
- 状态: 正常

### 建议
1. 服务运行正常
2. 资源使用良好
3. 无需干预
```

## 故障处理

### 服务无响应
```bash
# 1. 检查端口
netstat -ano | Select-String -Pattern ':8000'

# 2. 查看进程
Get-Process python | Select-Object Id, CPU, WorkingSet

# 3. 查看错误日志
Select-String -Path logs/*.log -Pattern "ERROR" -Tail 20

# 4. 重启服务
Get-NetTCPConnection -LocalPort 8000 | Stop-Process -Force
Start-Process python -ArgumentList "main.py" -NoNewWindow
```

### 数据库连接失败
```bash
# 1. 检查容器
docker ps | Select-String -Pattern "mysql"

# 2. 查看日志
docker logs <DB_CONTAINER> --tail 50

# 3. 重启容器
docker restart <DB_CONTAINER>

# 4. 等待就绪
Start-Sleep -Seconds 10
```

### 内存不足
```bash
# 1. 查看内存使用
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10

# 2. 清理Python进程
Get-Process python | Stop-Process -Force

# 3. 重启服务
Start-Process python -ArgumentList "main.py" -NoNewWindow
```