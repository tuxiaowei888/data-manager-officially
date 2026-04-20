---
name: "项目初始化"
description: "初始化项目环境，包括Docker容器、数据库设置、依赖安装和服务启动。当用户想要从头设置项目或克隆后设置时调用。"
---

# 项目初始化

该技能用于从头初始化Python/FastAPI项目。

## 必需配置

运行前，请为项目确定以下值：

| 变量 | 描述 | 示例 |
|------|------|------|
| `PROJECT_PATH` | 项目目录路径 | `E:\myproject` |
| `DB_CONTAINER` | Docker容器名称 | `my-mysql` |
| `DB_NAME` | 数据库名称 | `myapp_db` |
| `DB_USER` | 数据库用户 | `root` |
| `DB_PASSWORD` | 数据库密码 | `mypassword` |
| `DB_PORT` | 数据库端口 | `3306` |
| `SERVICE_PORT` | 服务端口 | `8000` |
| `MAIN_FILE` | 入口文件 | `main.py` |

## 初始化步骤

### 步骤1：检查前置条件
```bash
# 检查Python版本（需要3.9+）
python --version

# 检查Docker
docker --version

# 验证Docker正在运行
docker ps
```

### 步骤2：导航到项目
```bash
# 切换到项目目录
cd <PROJECT_PATH>

# 或设置工作目录
Set-Location <PROJECT_PATH>
```

### 步骤3：启动Docker服务
```bash
# 检查容器是否存在
docker ps -a | Select-String -Pattern "<DB_CONTAINER>"

# 启动现有容器
docker start <DB_CONTAINER>

# 或创建新容器（MySQL示例）
docker run --name <DB_CONTAINER> -e MYSQL_ROOT_PASSWORD=<DB_PASSWORD> -p <DB_PORT>:3306 -d mysql:8.0
```

### 步骤4：验证容器
```bash
# 验证容器正在运行
docker ps | Select-String -Pattern "<DB_CONTAINER>"

# 测试数据库连接
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "SELECT 1;"
```

### 步骤5：安装依赖
```bash
# 检查requirements.txt是否存在
Test-Path requirements.txt

# 从requirements.txt安装
pip install -r requirements.txt

# 或安装核心依赖
pip install fastapi uvicorn sqlalchemy pymysql pydantic

# 验证安装
pip list
```

### 步骤6：配置环境
```bash
# 检查.env.example
Test-Path .env.example

# 复制并配置环境
if (Test-Path .env.example) {
    Copy-Item .env.example .env
}

# 使用正确值编辑.env
# DATABASE_URL=mysql+pymysql://<DB_USER>:<DB_PASSWORD>@localhost:<DB_PORT>/<DB_NAME>
```

### 步骤7：初始化数据库
```bash
# 运行数据库初始化脚本
python scripts/init_db.py

# 或运行完整初始化
python scripts/full_init_db.py

# 验证表已创建
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "USE <DB_NAME>; SHOW TABLES;"
```

### 步骤8：启动服务
```bash
# 启动FastAPI服务
python <MAIN_FILE>

# 或直接使用uvicorn
uvicorn main:app --host 0.0.0.0 --port <SERVICE_PORT>
```

## 验证检查清单

| 步骤 | 检查 | 命令 |
|------|------|------|
| Python | 版本3.9+ | `python --version` |
| Docker | 容器运行中 | `docker ps \| grep <DB_CONTAINER>` |
| 依赖 | 全部安装 | `pip list` |
| 数据库 | 表存在 | `SHOW TABLES;` |
| 服务 | 端口监听 | `netstat -ano \| grep <SERVICE_PORT>` |
| API | 健康检查 | `curl http://localhost:<SERVICE_PORT>/health` |

## 预期输出

初始化成功后：

```
============================================================
项目初始化完成
============================================================
✓ Python版本: X.X.X
✓ Docker运行正常
✓ 数据库容器: <DB_CONTAINER>
✓ 依赖已安装
✓ 数据库表已创建
✓ 服务运行在 http://localhost:<SERVICE_PORT>
============================================================
```

## 故障排除

### 问题：Docker未运行
```bash
# 启动Docker Desktop或Docker服务
Start-Service docker

# 或重启Docker
Restart-Service docker
```

### 问题：MySQL容器无法启动
```bash
# 删除并重新创建
docker rm <DB_CONTAINER>
docker run --name <DB_CONTAINER> -e MYSQL_ROOT_PASSWORD=<DB_PASSWORD> -p <DB_PORT>:3306 -d mysql:8.0
```

### 问题：端口已被占用
```bash
# 查找使用端口的进程
Get-NetTCPConnection -LocalPort <SERVICE_PORT>

# 终止进程
Stop-Process -Id <PID> -Force
```

### 问题：依赖安装失败
```bash
# 尝试使用--user标志
pip install -r requirements.txt --user

# 或使用虚拟环境
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 问题：数据库连接失败
```bash
# 检查MySQL是否运行
docker ps | Select-String -Pattern "mysql"

# 检查日志
docker logs <DB_CONTAINER>

# 手动测试连接
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD>
```

### 问题：导入错误
```bash
# 重新安装所有依赖
pip uninstall -y -r requirements.txt
pip install -r requirements.txt

# 或检查Python路径
python -c "import sys; print(sys.path)"
```

## 常见项目结构

### FastAPI项目
```
project/
├── main.py           # 入口点
├── api/              # API路由
├── models/           # SQLAlchemy模型
├── schemas/          # Pydantic模型
├── services/         # 业务逻辑
├── config/           # 配置
│   └── database.py  # 数据库连接
├── scripts/          # 工具脚本
│   └── init_db.py  # 数据库初始化
├── requirements.txt
└── .env
```

### Django项目
```
project/
├── manage.py
├── project/
│   ├── settings.py
│   └── urls.py
├── app/
│   ├── models.py
│   └── views.py
└── requirements.txt
```

## 环境变量模板

创建 `.env` 文件：

```env
# 数据库
DATABASE_URL=mysql+pymysql://<DB_USER>:<DB_PASSWORD>@localhost:<DB_PORT>/<DB_NAME>

# 安全
SECRET_KEY=your-secret-key-change-in-production

# 应用
APP_NAME=MyApp
ENVIRONMENT=development
DEBUG=true

# 服务
SERVICE_PORT=<SERVICE_PORT>
```