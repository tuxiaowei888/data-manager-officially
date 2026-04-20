---
name: 安全检查
description: 安全漏洞扫描和检查。当用户要求安全检查、漏洞扫描或安全审计时调用。
---

# 安全检查

该技能用于进行安全漏洞扫描和检查。

## 安全检查项

| 检查项 | 说明 | 重要性 |
|--------|------|--------|
| SQL注入 | 检查SQL注入漏洞 | 高 |
| XSS攻击 | 检查跨站脚本漏洞 | 高 |
| 密码安全 | 检查密码强度和加密 | 高 |
| 敏感数据 | 检查敏感信息泄露 | 高 |
| API安全 | 检查API认证和授权 | 高 |
| 依赖漏洞 | 检查已知安全漏洞 | 中 |

## 检查步骤

### 步骤1：代码安全扫描
```bash
# 检查硬编码密码
Select-String -Path . -Pattern "password\s*=\s*['\"][^'\"]{8,}['\"]" -Recurse

# 检查SQL拼接
Select-String -Path . -Pattern "\.execute\(|cursor\.execute\(|conn\.execute\(" -Recurse

# 检查危险函数使用
Select-String -Path . -Pattern "eval\(|exec\(|compile\(" -Recurse
```

### 步骤2：认证安全检查
```bash
# 检查JWT密钥是否安全
Select-String -Path . -Pattern "SECRET_KEY\s*=\s*['\"]" -Recurse

# 检查密码哈希
Select-String -Path . -Pattern "bcrypt|hashpw|hash" -Recurse

# 检查认证中间件
Select-String -Path . -Pattern "OAuth2PasswordBearer|Depends.*auth" -Recurse
```

### 步骤3：依赖漏洞检查
```bash
# 检查已知漏洞的包
pip list | Select-String -Pattern "requests|urllib"

# 安装安全检查工具
pip install safety

# 运行安全检查
safety check

# 或使用pip-audit
pip install pip-audit
pip-audit
```

### 步骤4：API安全检查
```bash
# 检查是否暴露敏感端点
Select-String -Path api/ -Pattern "/admin|/debug|/status" -Recurse

# 检查CORS配置
Select-String -Path . -Pattern "CORSMiddleware|CORS" -Recurse

# 检查rate limiting
Select-String -Path . -Pattern "rate_limit|throttle" -Recurse
```

### 步骤5：数据库安全检查
```bash
# 检查数据库连接是否使用SSL
Select-String -Path config/ -Pattern "ssl=true|use_ssl" -Recurse

# 检查是否使用root用户
Select-String -Path config/ -Pattern "MYSQL_ROOT_PASSWORD" -Recurse

# 检查是否暴露数据库端口
Select-String -Path . -Pattern "3306|5432|27017" -Recurse
```

## 常见漏洞

### 1. SQL注入
```python
# 错误：直接拼接SQL
def query_db(sql):
    return cursor.execute(sql)

# 正确：使用参数化查询
def query_db(sql, params):
    return cursor.execute(sql, params)
```

### 2. XSS攻击
```python
# 错误：直接输出用户输入
return f"<div>{user_input}</div>"

# 正确：转义输出
from markupsafe import escape
return f"<div>{escape(user_input)}</div>"
```

### 3. 密码安全
```python
# 错误：明文存储
user.password = plain_password

# 正确：使用bcrypt哈希
import bcrypt
user.password = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())
```

### 4. JWT安全
```python
# 错误：弱密钥
SECRET_KEY = "123456"

# 正确：强密钥
import secrets
SECRET_KEY = secrets.token_urlsafe(32)
```

## 安全报告

```
## 安全检查报告
检查时间: 2024-03-18 15:30

### 代码安全
| 检查项 | 状态 | 发现 |
|--------|------|------|
| 硬编码密码 | ✓ 通过 | 0 |
| SQL注入 | ✓ 通过 | 0 |
| 危险函数 | ✓ 通过 | 0 |

### 认证安全
| 检查项 | 状态 | 发现 |
|--------|------|------|
| JWT密钥 | ✓ 安全 | - |
| 密码哈希 | ✓ 安全 | - |
| 认证中间件 | ✓ 存在 | - |

### 依赖安全
| 检查项 | 状态 | 发现 |
|--------|------|------|
| 已知漏洞 | ✓ 无 | 0 |
| 过期依赖 | ⚠️ 需更新 | 2 |

### API安全
| 检查项 | 状态 | 发现 |
|--------|------|------|
| 敏感端点 | ✓ 未暴露 | - |
| CORS配置 | ✓ 安全 | - |
| Rate Limiting | ✓ 已配置 | - |

### 总结
- 总检查项: 15
- 通过: 13
- 警告: 2
- 失败: 0

### 建议
1. 更新 2 个过期依赖
2. 考虑添加请求日志记录
3. 定期进行安全扫描
```

## 故障排除

### 发现SQL注入漏洞
```bash
# 1. 查找所有原始SQL执行
Select-String -Path api/ -Pattern "\.execute\(" -Recurse

# 2. 替换为参数化查询
# 使用 SQLAlchemy ORM 或 参数化查询

# 3. 重新测试
```

### 发现硬编码密码
```bash
# 1. 查找所有密码配置
Select-String -Path . -Pattern "password\s*=\s*['\"]" -Recurse

# 2. 替换为环境变量
# 错误: password = "123456"
# 正确: password = os.getenv("DB_PASSWORD")

# 3. 添加到.env文件（不提交到Git）
```

### 发现依赖漏洞
```bash
# 1. 查看具体漏洞
safety check --json

# 2. 更新有漏洞的包
pip install --upgrade package_name

# 3. 重新检查
safety check
```