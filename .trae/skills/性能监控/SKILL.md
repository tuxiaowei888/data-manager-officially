---
name: 性能监控
description: 监控系统性能，数据库查询性能分析。当用户要求性能分析、查看性能或优化系统时调用。
---

# 性能监控

该技能用于监控系统性能，包括API响应时间、数据库查询、内存使用等。

## 性能指标

| 指标 | 说明 | 目标值 |
|------|------|--------|
| API响应时间 | 接口响应速度 | < 500ms |
| 数据库查询时间 | SQL执行时间 | < 100ms |
| 内存使用 | 内存占用 | < 80% |
| CPU使用 | CPU占用 | < 70% |
| 并发连接数 | 同时连接数 | < 100 |

## 监控步骤

### 步骤1：API性能测试
```bash
# 测试根路径响应时间
Measure-Command { Invoke-WebRequest -Uri "http://localhost:8000/" } | Select-Object TotalMilliseconds

# 测试健康检查响应时间
Measure-Command { Invoke-WebRequest -Uri "http://localhost:8000/health" } | Select-Object TotalMilliseconds

# 测试登录接口响应时间
$body = @{username='admin'; password='admin123'}
Measure-Command {
    Invoke-RestMethod -Uri 'http://localhost:8000/api/v1/auth/login' `
                      -Method POST `
                      -Body $body `
                      -ContentType 'application/x-www-form-urlencoded'
}
```

### 步骤2：数据库性能检查
```bash
# 检查慢查询
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SHOW GLOBAL STATUS LIKE 'Slow_queries';
SHOW VARIABLES LIKE 'long_query_time';
"

# 检查连接数
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SHOW STATUS LIKE 'Threads_connected';
SHOW STATUS LIKE 'Max_used_connections';
"

# 检查表锁
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SHOW OPEN TABLES WHERE In_use > 0;
"
```

### 步骤3：系统资源监控
```bash
# CPU使用率
Get-Counter '\Processor(_Total)\% Processor Time'

# 内存使用
$mem = Get-CimInstance Win32_OperatingSystem
$memUsed = [math]::Round(($mem.TotalVisibleMemorySize - $mem.FreePhysicalMemory) / 1MB, 2)
$memTotal = [math]::Round($mem.TotalVisibleMemorySize / 1MB, 2)
Write-Host "内存使用: $memUsed GB / $memTotal GB"

# 磁盘IO
Get-Counter '\PhysicalDisk(_Total)\% Disk Time'
```

### 步骤4：Python进程监控
```bash
# 查看Python进程
Get-Process python | Select-Object Id, CPU, WorkingSet, StartTime

# 实时监控（每秒刷新）
Get-Process python | Format-Table Id, CPU, WorkingSet -AutoSize
```

## 性能分析

### API响应时间分析
```bash
# 测试多个接口的响应时间
$endpoints = @('/', '/health', '/api/v1/auth/login')

foreach ($endpoint in $endpoints) {
    $time = Measure-Command { Invoke-WebRequest -Uri "http://localhost:8000$endpoint" -TimeoutSec 5 }
    Write-Host "$endpoint : $($time.TotalMilliseconds) ms"
}
```

### 数据库查询分析
```bash
# 查看查询统计
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SHOW GLOBAL STATUS LIKE 'Questions';
SHOW GLOBAL STATUS LIKE 'Com_select';
SHOW GLOBAL STATUS LIKE 'Com_insert';
SHOW GLOBAL STATUS LIKE 'Com_update';
SHOW GLOBAL STATUS LIKE 'Com_delete';
"

# 查看innodb缓冲池
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "
SHOW ENGINE INNODB STATUS;
"
```

### 连接分析
```bash
# 查看当前连接
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SELECT * FROM information_schema.PROCESSLIST WHERE Command != 'Sleep';
"

# 查看最大连接数
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "
SHOW VARIABLES LIKE 'max_connections';
"
```

## 性能报告

```
## 性能监控报告
监控时间: 2024-03-18 15:30

### API性能
| 接口 | 响应时间 | 状态 |
|------|---------|------|
| / | 45ms | 正常 |
| /health | 12ms | 正常 |
| /api/v1/auth/login | 89ms | 正常 |

### 数据库性能
| 指标 | 值 | 状态 |
|------|-----|------|
| 查询数/秒 | 15 | 正常 |
| 慢查询数 | 0 | 正常 |
| 连接数 | 5/151 | 正常 |

### 系统资源
| 资源 | 使用率 | 状态 |
|------|--------|------|
| CPU | 15% | 正常 |
| 内存 | 45% | 正常 |
| 磁盘 | 20% | 正常 |

### 建议
1. 系统运行正常
2. 无性能瓶颈
3. 继续保持监控
```

## 性能优化建议

### 1. API响应慢
- 添加缓存
- 优化数据库查询
- 使用分页
- 减少不必要的数据加载

### 2. 数据库查询慢
- 添加索引
- 优化SQL语句
- 避免SELECT *
- 使用连接池

### 3. 内存使用高
- 清理不必要的缓存
- 优化数据加载
- 增加内存
- 检查内存泄漏

## 故障排查

### 响应时间突然变长
```bash
# 1. 检查数据库
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "SHOW PROCESSLIST;"

# 2. 检查系统资源
Get-Process | Sort-Object CPU -Descending | Select-Object -First 5

# 3. 查看慢查询日志
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "SHOW GLOBAL VARIABLES LIKE 'slow_query%';"
```

### 数据库连接数过多
```bash
# 1. 查看连接
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "SHOW PROCESSLIST;"

# 2. 查看最大连接
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "SHOW VARIABLES LIKE 'max_connections';"

# 3. 如果需要，可以临时增加连接数
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "SET GLOBAL max_connections = 200;"
```