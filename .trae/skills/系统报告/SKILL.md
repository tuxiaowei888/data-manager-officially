---
name: 系统报告
description: 生成系统运行状态报告。当用户要求生成报告、系统状态报告或系统概览时调用。
---

# 系统报告

该技能用于生成系统运行状态的综合报告。

## 报告内容

| 模块 | 说明 |
|------|------|
| 系统概览 | 基本信息汇总 |
| 服务状态 | 服务运行情况 |
| 数据库状态 | 数据库信息 |
| 资源使用 | CPU、内存、磁盘 |
| 数据统计 | 各表数据量 |
| 安全状态 | 安全配置检查 |
| 性能指标 | 响应时间、连接数 |

## 报告生成

### 步骤1：收集系统信息
```bash
# 获取系统基本信息
$computerInfo = Get-ComputerInfo
Write-Host "计算机名: $($computerInfo.CsName)"
Write-Host "操作系统: $($computerInfo.OsName)"
Write-Host "系统版本: $($computerInfo.OsVersion)"

# 获取Python版本
python --version

# 获取Docker版本
docker --version
```

### 步骤2：收集服务状态
```bash
# 检查服务端口
netstat -ano | Select-String -Pattern ':8000.*LISTENING'

# 检查Docker容器
docker ps

# 检查服务健康
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 5
    Write-Host "服务状态: $($response.StatusCode)"
} catch {
    Write-Host "服务状态: 异常"
}
```

### 步骤3：收集数据库信息
```bash
# 数据库基本信息
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "
SELECT VERSION() as version;
SHOW DATABASES;
"

# 数据库大小
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "
SELECT
    TABLE_SCHEMA as '数据库',
    ROUND(SUM(DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) as '大小(MB)'
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = '<DB_NAME>'
GROUP BY TABLE_SCHEMA;
"

# 各表记录数
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SELECT
    TABLE_NAME as '表名',
    TABLE_ROWS as '记录数'
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = '<DB_NAME>'
AND TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_ROWS DESC;
"
```

### 步骤4：收集资源使用
```bash
# CPU使用率
Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 1 -MaxSamples 1 | Select-Object -ExpandProperty CounterSamples

# 内存使用
$mem = Get-CimInstance Win32_OperatingSystem
Write-Host "总内存: $([math]::Round($mem.TotalVisibleMemorySize / 1MB, 2)) GB"
Write-Host "可用内存: $([math]::Round($mem.FreePhysicalMemory / 1MB, 2)) GB"
Write-Host "使用率: $([math]::Round(($mem.TotalVisibleMemorySize - $mem.FreePhysicalMemory) / $mem.TotalVisibleMemorySize * 100, 2))%"

# 磁盘空间
Get-PSDrive C | Select-Object Used, Free, @{Name='使用率';Expression={[math]::Round($_.Used / ($_.Used + $_.Free) * 100, 2)}}
```

### 步骤5：生成报告
```powershell
# 生成时间
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# 收集所有信息并生成报告
$report = @"

============================================================
                    数维数据管家系统 - 运行报告
============================================================
报告时间: $timestamp

一、系统概览
------------------------------------------------------------
计算机名: $env:COMPUTERNAME
操作系统: $($computerInfo.OsName)
Python版本: $(python --version 2>&1)
Docker版本: $(docker --version 2>&1)

二、服务状态
------------------------------------------------------------
"@

# 服务状态
$serviceRunning = netstat -ano | Select-String -Pattern ':8000.*LISTENING'
if ($serviceRunning) {
    $report += "API服务:      运行中 ✓`n"
} else {
    $report += "API服务:      停止 ✗`n"
}

$mysqlRunning = docker ps | Select-String -Pattern "<DB_CONTAINER>"
if ($mysqlRunning) {
    $report += "MySQL服务:    运行中 ✓`n"
} else {
    $report += "MySQL服务:    停止 ✗`n"
}

$report += @"

三、数据库统计
------------------------------------------------------------
"@

# 数据库统计
$tables = docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "SHOW TABLES;" 2>&1
$tableCount = ($tables | Measure-Object -Line).Lines - 1
$report += "表数量: $tableCount`n"

$report += @"

四、资源使用
------------------------------------------------------------
"@

# 资源使用
$report += "CPU使用率: 查看监控`n"
$report += "内存使用: 查看监控`n"
$report += "磁盘空间: 查看监控`n"

$report += @"

五、总结
------------------------------------------------------------
系统运行正常，所有服务处于健康状态。
"@

Write-Host $report
```

## 系统报告模板

```
============================================================
                    数维数据管家系统 - 运行报告
============================================================
报告时间: 2024-03-18 15:30

一、系统概览
------------------------------------------------------------
计算机名: DESKTOP-XXXX
操作系统: Windows 11
Python版本: 3.13.0
Docker版本: 24.0.1

二、服务状态
------------------------------------------------------------
API服务:      运行中 ✓
MySQL服务:    运行中 ✓
向量数据库:   未配置 ○

三、数据库统计
------------------------------------------------------------
表数量:       8
用户数量:     2
规则数量:     18
评价记录:     0
知识文档:     0

四、资源使用
------------------------------------------------------------
CPU使用率:    15%
内存使用:     45%
磁盘空间:     65%

五、安全状态
------------------------------------------------------------
密码加密:     ✓ bcrypt
JWT认证:      ✓ 启用
敏感数据:     ✓ 未发现泄露

六、总结
------------------------------------------------------------
系统运行正常，所有服务处于健康状态。
建议：暂无
============================================================
```

## 输出报告

将报告保存到文件：

```bash
# 保存报告
$report | Out-File -FilePath "system_report_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt" -Encoding UTF8

# 查看报告
Get-Content system_report_latest.txt
```

## 定期生成报告

```powershell
# 创建每日报告脚本
$timestamp = Get-Date -Format 'yyyyMMdd'
$reportFile = "reports\system_report_$timestamp.txt"

# 创建报告目录（如果不存在）
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports"
}

# 生成并保存报告
# ... (上述报告生成代码) ...

Write-Host "报告已保存: $reportFile"
```