---
name: 数据库备份
description: 定时备份数据库。当用户要求备份数据库、创建备份或恢复数据时调用。
---

# 数据库备份

该技能用于备份和恢复MySQL数据库。

## 备份操作

### 1. 创建完整备份
```bash
# 备份整个数据库
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
docker exec -it <DB_CONTAINER> mysqldump -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> > "backup_$timestamp.sql"

# 验证备份文件
Get-ChildItem -Filter "backup_*.sql" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

### 2. 备份特定表
```bash
# 备份特定表
docker exec -it <DB_CONTAINER> mysqldump -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> users channels rule_configs > "partial_backup_$timestamp.sql"
```

### 3. 压缩备份
```bash
# 压缩备份文件
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupFile = "backup_$timestamp.sql"
$zipFile = "backup_$timestamp.zip"

# 先创建备份
docker exec -it <DB_CONTAINER> mysqldump -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> > $backupFile

# 压缩
Compress-Archive -Path $backupFile -DestinationPath $zipFile

# 删除原始文件
Remove-Item $backupFile

# 验证
Get-ChildItem -Filter "backup_*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

## 恢复操作

### 1. 从完整备份恢复
```bash
# 查找最新备份
$latestBackup = Get-ChildItem -Filter "backup_*.sql" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

# 恢复前先删除并重建数据库
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "DROP DATABASE IF EXISTS <DB_NAME>; CREATE DATABASE <DB_NAME>;"

# 恢复数据
docker exec -i <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> < $latestBackup.FullName

# 验证
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "SHOW TABLES;"
```

### 2. 从压缩备份恢复
```bash
# 解压备份
$latestZip = Get-ChildItem -Filter "backup_*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Expand-Archive -Path $latestZip.FullName -DestinationPath "."

# 获取解压后的sql文件
$sqlFile = Get-ChildItem -Filter "*.sql" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

# 恢复数据库
docker exec -i <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> < $sqlFile.FullName
```

## 定时备份

### 创建定时备份脚本
```powershell
# backup_task.ps1
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupDir = "backups"
$backupFile = "$backupDir\backup_$timestamp.sql"

# 创建备份目录（如果不存在）
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir
}

# 执行备份
docker exec -it <DB_CONTAINER> mysqldump -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> > $backupFile

# 压缩备份
$zipFile = "$backupDir\backup_$timestamp.zip"
Compress-Archive -Path $backupFile -DestinationPath $zipFile

# 删除原始sql文件
Remove-Item $backupFile

# 删除7天前的备份
$sevenDaysAgo = (Get-Date).AddDays(-7)
Get-ChildItem -Path $backupDir -Filter "backup_*.zip" | Where-Object { $_.LastWriteTime -lt $sevenDaysAgo } | Remove-Item

Write-Host "备份完成: $zipFile"
```

### 设置Windows计划任务
```bash
# 创建每日备份计划任务
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File backup_task.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At "03:00"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries

Register-ScheduledTask -TaskName "DatabaseBackup" -Action $action -Trigger $trigger -Settings $settings -Description "每日数据库备份"
```

## 备份管理

### 列出所有备份
```bash
# 列出备份文件
Get-ChildItem -Path "backups" -Filter "backup_*.zip" | Sort-Object LastWriteTime -Descending | Select-Object Name, Length, LastWriteTime
```

### 备份统计
```bash
# 统计备份数量
$count = (Get-ChildItem -Path "backups" -Filter "backup_*.zip" | Measure-Object).Count
Write-Host "备份文件数量: $count"

# 统计备份总大小
$size = (Get-ChildItem -Path "backups" -Filter "backup_*.zip" | Measure-Object -Property Length -Sum).Sum / 1MB
Write-Host "备份总大小: $([math]::Round($size, 2)) MB"
```

### 验证备份
```bash
# 验证备份文件完整性
$latestBackup = Get-ChildItem -Filter "backup_*.sql" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($latestBackup) {
    # 检查文件大小（不应该为空）
    if ($latestBackup.Length -gt 0) {
        Write-Host "备份文件有效"

        # 检查SQL文件头
        Get-Content $latestBackup.FullName -TotalCount 5
    } else {
        Write-Host "警告: 备份文件为空!" -ForegroundColor Red
    }
}
```

## 备份报告

```
## 数据库备份报告
时间: 2024-03-18 15:30

### 备份状态
| 项目 | 值 |
|------|-----|
| 最新备份 | backup_20240318_153000.zip |
| 备份大小 | 2.5 MB |
| 备份时间 | 2024-03-18 15:30 |

### 备份列表
| 文件名 | 大小 | 创建时间 |
|--------|------|----------|
| backup_20240318_153000.zip | 2.5 MB | 15:30 |
| backup_20240317_030000.zip | 2.4 MB | 03:00 |
| backup_20240316_030000.zip | 2.3 MB | 03:00 |

### 备份策略
- 保留天数: 7天
- 备份时间: 每日 03:00
- 存储位置: backups/

### 总结
- 备份状态: 正常
- 备份数量: 7
- 存储使用: 17.5 MB
```

## 常见问题

### 问题：备份失败
```bash
# 1. 检查容器是否运行
docker ps | Select-String -Pattern "<DB_CONTAINER>"

# 2. 检查磁盘空间
Get-PSDrive C | Select-Object Used, Free

# 3. 检查MySQL连接
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "SELECT 1;"

# 4. 查看MySQL日志
docker logs <DB_CONTAINER> --tail 20
```

### 问题：恢复失败
```bash
# 1. 检查备份文件是否存在
Get-ChildItem -Filter "backup_*.sql"

# 2. 验证备份文件完整性
$file = Get-ChildItem -Filter "backup_*.sql" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
Write-Host "文件大小: $($file.Length) bytes"

# 3. 检查数据库是否存在
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "SHOW DATABASES LIKE '<DB_NAME>';"
```