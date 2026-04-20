---
name: 环境检查
description: 检查开发环境配置是否正确。当用户要求检查环境、验证配置或排查问题时调用。
---

# 环境检查

该技能用于检查开发环境配置是否正确。

## 检查项目

| 检查项 | 说明 | 重要性 |
|--------|------|--------|
| Python版本 | Python >= 3.9 | 高 |
| Docker | Docker是否运行 | 高 |
| 数据库连接 | MySQL是否正常 | 高 |
| 依赖安装 | 核心依赖是否完整 | 高 |
| 端口占用 | 服务端口是否冲突 | 中 |
| 环境变量 | 配置是否正确 | 中 |

## 检查步骤

### 步骤1：检查Python环境
```bash
# 检查Python版本
python --version

# 检查pip版本
pip --version

# 检查Python路径
Get-Command python | Select-Object Source
```

### 步骤2：检查Docker环境
```bash
# 检查Docker版本
docker --version

# 检查Docker是否运行
docker ps

# 检查Docker容器
docker ps -a
```

### 步骤3：检查数据库连接
```bash
# 测试MySQL连接
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "SELECT 1;"

# 检查数据库列表
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "SHOW DATABASES;"

# 检查特定数据库
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "SHOW TABLES;"
```

### 步骤4：检查依赖安装
```bash
# 检查核心依赖
pip list | Select-String -Pattern "fastapi|uvicorn|sqlalchemy|pymysql"

# 检查所有已安装的包
pip list

# 检查requirements.txt
Test-Path requirements.txt
```

### 步骤5：检查服务端口
```bash
# 检查端口8000
netstat -ano | Select-String -Pattern ':8000.*LISTENING'

# 检查端口3306
netstat -ano | Select-String -Pattern ':3306.*LISTENING'

# 查看所有Python进程
Get-Process python | Select-Object Id, ProcessName, CPU, WorkingSet
```

### 步骤6：检查环境变量
```bash
# 检查.env文件
Test-Path .env

# 查看环境变量
Get-ChildItem Env:

# 检查数据库URL配置
(Get-Content .env -ErrorAction SilentlyContinue) -match "DATABASE"
```

## 环境验证清单

| 检查项 | 状态 | 预期值 |
|--------|------|--------|
| Python版本 | ✓/✗ | >= 3.9 |
| pip版本 | ✓/✗ | 最新版 |
| Docker版本 | ✓/✗ | >= 20.10 |
| MySQL容器 | ✓/✗ | 运行中 |
| 数据库连接 | ✓/✗ | 连接成功 |
| 核心依赖 | ✓/✗ | 已安装 |
| 服务端口 | ✓/✗ | 未被占用 |
| .env配置 | ✓/✗ | 文件存在 |

## 快速检查脚本

```bash
# 一键环境检查
Write-Host "=== 环境检查 ===" -ForegroundColor Green

# Python
Write-Host "Python: " -NoNewline
python --version

# Docker
Write-Host "Docker: " -NoNewline
docker --version

# MySQL容器
Write-Host "MySQL容器: " -NoNewline
docker ps | Select-String -Pattern "<DB_CONTAINER>"

# 端口
Write-Host "端口8000: " -NoNewline
netstat -ano | Select-String -Pattern ':8000.*LISTENING'

# 依赖
Write-Host "核心依赖: " -NoNewline
pip list | Select-String -Pattern "fastapi"
```

## 常见问题

### 问题：Python版本过低
```bash
# 升级Python（需要手动下载）
# https://www.python.org/downloads/
```

### 问题：Docker未运行
```bash
# 启动Docker Desktop
Start-Process "Docker Desktop"

# 或重启Docker服务
Restart-Service docker
```

### 问题：数据库连接失败
```bash
# 检查容器是否运行
docker ps | Select-String -Pattern "mysql"

# 启动容器
docker start <DB_CONTAINER>

# 检查容器日志
docker logs <DB_CONTAINER>
```

### 问题：端口被占用
```bash
# 查找占用端口的进程
Get-NetTCPConnection -LocalPort 8000

# 终止进程
Stop-Process -Id <PID> -Force
```

### 问题：依赖缺失
```bash
# 重新安装依赖
pip install -r requirements.txt
```

## 输出报告

```
## 环境检查报告
检查时间: 2024-03-18 15:30

### Python环境
- 版本: 3.11.5 ✓
- pip: 24.0 ✓

### Docker环境
- 版本: 24.0.1 ✓
- 容器状态: 运行中 ✓

### 数据库
- 容器: my-mysql ✓
- 数据库: shuwei_data_manager ✓
- 表数量: 8 ✓

### 依赖
- fastapi: 0.135.1 ✓
- uvicorn: 0.42.0 ✓
- sqlalchemy: 2.0.48 ✓

### 服务
- 端口8000: 未被占用 ✓
- 服务状态: 未运行

### 总结
- 检查项: 15
- 通过: 14
- 失败: 1
- 状态: 需要修复
```