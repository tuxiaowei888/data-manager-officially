---
name: "测试运行"
description: "运行项目测试，包括API测试、单元测试和健康检查。当用户要求运行测试、测试系统或验证功能时调用。"
---

# 测试运行器

该技能用于运行各种测试，验证任何项目的系统功能。

## 测试类型

### 1. 快速健康检查
运行基本系统健康检查，验证服务是否正常运行。

### 2. API测试
测试所有API端点，包括：
- 认证（登录、注册、登出）
- CRUD操作
- 数据验证
- 错误处理

### 3. 集成测试
测试完整流程：
- 用户注册 → 登录 → 创建资源 → 处理 → 生成输出

## 测试前检查清单

```bash
# 1. 验证Python环境
python --version

# 2. 验证服务正在运行
curl http://localhost:8000/health

# 3. 验证数据库连接
docker ps | Select-String -Pattern "mysql"
```

## 使用方法

当用户要求运行测试时，执行：

### 步骤1：检查服务健康
```bash
# 检查服务是否在端口8000运行
netstat -ano | Select-String -Pattern ':8000.*LISTENING'

# 或
curl http://localhost:8000/health
```

### 步骤2：运行API测试
```bash
# 测试根端点
curl http://localhost:8000/

# 测试登录端点（示例）
curl -X POST "http://localhost:8000/api/v1/auth/login" `
  -H "Content-Type: application/x-www-form-urlencoded" `
  -d "username=admin&password=admin123"
```

### 步骤3：运行Python测试
```bash
# 使用pytest运行（如果可用）
python -m pytest tests/ -v

# 或运行特定测试文件
python tests/test_api.py

# 或运行快速测试
python tests/quick_test.py
```

### 步骤4：检查数据库
```bash
# 验证数据库连接
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "SHOW DATABASES;"

# 检查表
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "SHOW TABLES;"
```

## 配置变量

| 变量 | 描述 | 示例 |
|------|------|------|
| `SERVICE_PORT` | 服务端口（默认：8000） | 8000 |
| `DB_CONTAINER` | Docker容器名称 | my-mysql |
| `DB_USER` | 数据库用户 | root |
| `DB_PASSWORD` | 数据库密码 | 123456 |
| `DB_NAME` | 数据库名称 | myapp_db |

## 测试文件位置

| 文件 | 用途 |
|------|------|
| `tests/` | 测试目录 |
| `tests/quick_test.py` | 快速冒烟测试 |
| `tests/test_api.py` | API端点测试 |
| `test_*.py` | 单独测试文件 |

## 预期测试流程

1. **服务健康** - 验证服务在端口运行
2. **数据库健康** - 验证数据库容器运行中
3. **认证** - 测试登录（如适用）
4. **API端点** - 测试CRUD操作
5. **数据处理** - 测试核心业务逻辑

## 成功标准

所有测试应通过：
- HTTP 200/201 响应（成功操作）
- 有效的JSON响应
- 数据库连接保持
- 服务保持稳定

## 错误指示器

| 问题 | 症状 | 检查 |
|------|------|------|
| 服务宕机 | 端口未监听 | `netstat -ano \| grep 8000` |
| 数据库连接 | 连接被拒绝 | `docker ps \| grep mysql` |
| 认证失败 | 401未授权 | 检查凭据 |
| 导入错误 | ModuleNotFoundError | `pip list` |

## 故障排除

### 服务无响应
```bash
# 重启服务
python main.py

# 或使用uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 数据库连接失败
```bash
# 检查容器是否运行
docker ps

# 启动容器
docker start <DB_CONTAINER>
```

### 端口被占用
```bash
# 查找使用端口的进程
Get-NetTCPConnection -LocalPort 8000

# 终止进程
Stop-Process -Id <PID> -Force
```