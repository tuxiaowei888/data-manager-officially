---
name: "自动化部署"
description: "自动化部署过程，包括构建、测试和部署应用程序。当用户想要部署应用程序或发布更改时调用。"
---

# 部署自动化

该技能用于处理任何Python/FastAPI应用程序的部署过程。

## 必需配置

| 变量 | 描述 | 示例 |
|------|------|------|
| `PROJECT_PATH` | 项目目录 | `E:\myproject` |
| `DB_CONTAINER` | Docker容器名称 | `my-mysql` |
| `DB_NAME` | 数据库名称 | `myapp_db` |
| `DB_USER` | 数据库用户 | `root` |
| `DB_PASSWORD` | 数据库密码 | `mypassword` |
| `SERVICE_PORT` | 服务端口 | `8000` |
| `MAIN_FILE` | 入口文件 | `main.py` |
| `ENVIRONMENT` | dev/staging/prod | `production` |

## 部署模式

### 1. 开发环境部署
用于本地开发和测试。
- 无需备份
- 直接重启
- 启用调试

### 2. 预发布环境部署
用于预发布测试。
- 部署前备份
- 部署后测试
- 限制访问

### 3. 生产环境部署
用于线上生产环境。
- 部署前完整备份
- 回滚计划就绪
- 启用监控

## 部署前检查清单

```bash
# 1. 检查当前服务状态
netstat -ano | Select-String -Pattern '<SERVICE_PORT>.*LISTENING'

# 2. 验证数据库备份存在
Test-Path "backup_$(Get-Date -Format 'yyyyMMdd').sql"

# 3. 检查Git状态（如果使用Git）
git status

# 4. 验证所有测试通过
python -m pytest tests/ -v
```

## 部署步骤

### 步骤1：创建备份
```bash
# 创建数据库备份
docker exec -it <DB_CONTAINER> mysqldump -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> > "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql"

# 验证备份已创建
Get-ChildItem -Filter "backup_*.sql" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

### 步骤2：拉取最新代码（如使用Git）
```bash
# 从远程拉取
git pull origin main

# 或检出特定版本
git checkout <version_tag>
```

### 步骤3：安装依赖
```bash
# 安装/更新依赖
pip install -r requirements.txt

# 验证安装
pip list
```

### 步骤4：运行数据库迁移
```bash
# 运行迁移脚本
python scripts/migrate.py

# 或初始化数据库
python scripts/init_db.py

# 验证结构
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "USE <DB_NAME>; SHOW TABLES;"
```

### 步骤5：停止当前服务
```bash
# 查找使用端口的进程
$process = Get-NetTCPConnection -LocalPort <SERVICE_PORT> | Select-Object -First 1

# 终止进程
if ($process) {
    Stop-Process -Id $process.OwningProcess -Force
}

# 等待清理
Start-Sleep -Seconds 2
```

### 步骤6：启动新服务
```bash
# 在后台启动服务
Start-Process python -ArgumentList "<MAIN_FILE>" -NoNewWindow -PassThru

# 等待启动
Start-Sleep -Seconds 3
```

### 步骤7：验证部署
```bash
# 检查服务健康
curl http://localhost:<SERVICE_PORT>/health

# 检查端口监听
netstat -ano | Select-String -Pattern '<SERVICE_PORT>.*LISTENING'

# 检查日志
# （查看终端输出）
```

## 回滚程序

如果部署失败：

### 步骤1：停止当前服务
```bash
# 查找并停止
Get-NetTCPConnection -LocalPort <SERVICE_PORT> | Stop-Process -Force
```

### 步骤2：恢复数据库
```bash
# 查找最新备份
$backup = Get-ChildItem -Filter "backup_*.sql" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

# 恢复数据库
docker exec -i <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> < $backup.FullName
```

### 步骤3：还原代码（如使用Git）
```bash
# 还原到之前的版本
git revert HEAD

# 或检出之前的提交
git checkout <previous_commit_hash>
```

### 步骤4：重启服务
```bash
# 启动之前的版本
Start-Process python -ArgumentList "<MAIN_FILE>" -NoNewWindow
```

## 部署报告

创建部署报告：

```
## 部署报告
日期: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
环境: <ENVIRONMENT>

### 部署前
- 备份已创建: 是/否
- 测试通过: 是/否
- 代码版本: <git_hash>

### 部署
- 状态: 成功/失败
- 耗时: X分钟

### 部署后
- 服务健康: 正常/错误
- 数据库: 已连接/已断开
- API响应: 200/错误

### 回滚
- 需要: 是/否
- 状态: 成功/失败
```

## 环境变量

| 变量 | 描述 | 默认值 |
|------|------|--------|
| `DATABASE_URL` | MySQL连接字符串 | mysql+pymysql://user:pass@localhost:3306/db |
| `SECRET_KEY` | JWT密钥 | change-in-production |
| `ENVIRONMENT` | dev/staging/prod | dev |
| `DEBUG` | 调试模式 | false |

## 监控

部署后，监控：

```bash
# 服务日志
# 查看终端输出

# 错误日志
Select-String -Path "*.log" -Pattern "ERROR"

# 数据库连接
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "SHOW PROCESSLIST;"

# API响应时间
Measure-Command { Invoke-WebRequest -Uri "http://localhost:<SERVICE_PORT>/health" }
```

## Git部署（可选）

```bash
# 提交更改
git add .
git commit -m "部署: $(Get-Date -Format 'yyyyMMdd_HHmmss')"

# 推送到远程
git push origin main

# 在服务器上：拉取并重启
git pull origin main
Restart-Service python
```

## 健康检查端点

| 端点 | 用途 | 预期响应 |
|------|------|----------|
| `/health` | 服务健康 | `{"status": "healthy"}` |
| `/` | 根信息 | 服务信息 |
| `/docs` | API文档 | HTML页面 |

## 快速部署命令

```bash
# 一键部署
cd <PROJECT_PATH>; pip install -r requirements.txt; Get-NetTCPConnection -LocalPort <SERVICE_PORT> | Stop-Process -Force; Start-Process python -ArgumentList "<MAIN_FILE>" -NoNewWindow
```