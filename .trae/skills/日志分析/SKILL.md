---
name: 日志分析
description: 分析日志文件，查找错误和异常。当用户要求分析日志、查看错误或调试问题时调用。
---

# 日志分析

该技能用于分析日志文件，查找错误和异常信息。

## 日志位置

| 日志类型 | 位置 | 说明 |
|---------|------|------|
| 应用日志 | `logs/app.log` | 应用运行日志 |
| 错误日志 | `logs/error.log` | 错误日志 |
| 访问日志 | `logs/access.log` | API访问日志 |
| 系统日志 | `logs/system.log` | 系统日志 |

## 分析步骤

### 步骤1：查找日志文件
```bash
# 列出日志目录
Get-ChildItem -Path logs -ErrorAction SilentlyContinue

# 查找所有日志文件
Get-ChildItem -Recurse -Filter "*.log"
```

### 步骤2：查找错误
```bash
# 查找错误关键词
Select-String -Path logs/*.log -Pattern "ERROR|错误|Exception|失败"

# 查找最近1小时的错误
$oneHourAgo = (Get-Date).AddHours(-1)
Select-String -Path logs/*.log -Pattern "ERROR" | Where-Object { $_.Line -match $oneHourAgo.ToString("yyyy-MM-dd HH") }
```

### 步骤3：统计错误
```bash
# 统计错误数量
$errorCount = (Select-String -Path logs/*.log -Pattern "ERROR" | Measure-Object).Count
Write-Host "错误总数: $errorCount"

# 按类型统计
$errors = Select-String -Path logs/*.log -Pattern "ERROR" | ForEach-Object { $_ }
$errors | Group-Object | Sort-Object Count -Descending | Select-Object Name, Count
```

### 步骤4：分析异常堆栈
```bash
# 查找异常堆栈
Select-String -Path logs/*.log -Pattern "Traceback|堆栈" -Context 0,10

# 查找特定异常类型
Select-String -Path logs/*.log -Pattern "ValueError|TypeError|AttributeError"
```

## 常用查询

### 1. 查找关键错误
```bash
# 查找数据库连接错误
Select-String -Path logs/*.log -Pattern "Connection refused|连接失败"

# 查找认证错误
Select-String -Path logs/*.log -Pattern "Authentication|认证失败|401"

# 查找API错误
Select-String -Path logs/*.log -Pattern "500|Internal Server Error"
```

### 2. 查找特定时间范围
```bash
# 查找今天下午的错误
Select-String -Path logs/*.log -Pattern "ERROR" | Where-Object { $_.Line -match "2024-03-18 14" }

# 查找最近N条日志
Get-Content logs/app.log -Tail 50
```

### 3. 查找用户相关错误
```bash
# 查找特定用户的错误
Select-String -Path logs/*.log -Pattern "user_id=123.*ERROR"

# 查找特定IP的错误
Select-String -Path logs/access.log -Pattern "192.168.1.100.*404"
```

## 分析输出格式

```
## 日志分析报告

### 概览
- 分析时间: 2024-03-18 15:30
- 日志范围: logs/
- 错误总数: X

### 错误统计
| 错误类型 | 数量 | 占比 |
|---------|------|------|
| 数据库错误 | X | X% |
| 认证错误 | X | X% |
| API错误 | X | X% |

### 最新错误（最近5条）
1. [时间] 错误描述
2. [时间] 错误描述
...

### 建议
1. 优先修复高频率错误
2. 检查数据库连接配置
3. 加强错误处理
```

## 日志级别

| 级别 | 关键词 | 严重性 |
|------|--------|--------|
| ERROR | 错误 | 高 |
| WARNING | 警告 | 中 |
| INFO | 信息 | 低 |
| DEBUG | 调试 | 低 |

## 故障排除

### 问题：找不到日志文件
```bash
# 检查日志目录是否存在
Test-Path logs

# 创建日志目录
New-Item -ItemType Directory -Path logs
```

### 问题：日志文件过大
```bash
# 查看日志大小
Get-ChildItem logs/*.log | Sort-Object Length -Descending

# 压缩旧日志
Compress-Archive -Path logs/app.log -DestinationPath logs/archive_$(Get-Date -Format 'yyyyMMdd').zip

# 清空日志（谨慎）
# Clear-Content logs/app.log
```

### 问题：无法读取日志编码
```bash
# 尝试不同编码
Get-Content logs/app.log -Encoding UTF8 -Tail 100

# 或
Get-Content logs/app.log -Encoding GBK -Tail 100
```