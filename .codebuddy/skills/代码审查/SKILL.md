---
name: "代码审查"
description: "审查代码的的最佳实践、错误、安全问题和新能改进。当用户要求代码审查或合并更改前调用。"
---

# 代码审查器

该技能用于对任何Python/FastAPI项目进行全面的代码审查。

## 审查领域

### 1. 代码质量
- 适当的错误处理
- 代码结构和组织
- 命名规范
- 注释质量（避免不必要的注释）
- DRY原则（不要重复自己）
- 函数长度和复杂度

### 2. 安全性
- SQL注入漏洞
- 认证/授权问题
- 敏感数据泄露
- 输入验证
- 密码哈希
- 密钥管理

### 3. 性能
- 数据库查询优化
- 不必要的循环或迭代
- 内存泄漏
- 连接池使用
- 适用时的async/await使用

### 4. 最佳实践
- FastAPI最佳实践
- RESTful API设计
- 正确的HTTP状态码
- JSON响应一致性
- API版本控制
- 类型提示使用

## 使用方法

当用户要求代码审查时，执行：

### 步骤1：语法检查
```bash
# 检查Python文件语法错误
python -m py_compile <file.py>

# 检查目录中的所有Python文件
Get-ChildItem -Recurse -Filter "*.py" | ForEach-Object { python -m py_compile $_.FullName }
```

### 步骤2：基本代码检查
```bash
# 检查常见问题（需要flake8）
python -m flake8 api/ --select=E9,F63,F7,F82

# 或使用默认规则运行
python -m flake8 api/
```

### 步骤3：导入检查
```bash
# 验证所有导入工作
python -c "import api; print('所有导入正常')"
```

### 步骤4：安全扫描
```bash
# 检查硬编码密钥（基本）
Select-String -Path . -Pattern "password\s*=\s*['\"][^'\"]{8,}['\"]" -Recurse

# 检查SQL注入风险
Select-String -Path . -Pattern "\.execute\(|cursor\.execute\(" -Recurse
```

## 审查检查清单

| 类别 | 检查点 | 优先级 |
|------|--------|--------|
| 安全性 | 密码正确哈希 | 高 |
| 安全性 | SQL注入预防 | 高 |
| 安全性 | 输入验证 | 高 |
| 安全性 | 无硬编码密钥 | 高 |
| 性能 | 数据库索引 | 中 |
| 性能 | 查询优化 | 中 |
| 质量 | 错误处理 | 高 |
| 质量 | HTTP状态码 | 中 |
| 质量 | 响应一致性 | 中 |
| 质量 | 类型提示 | 低 |

## 常见问题

### 1. 缺少错误处理
```python
# 错误
def get_user(id):
    return db.query(User).filter(User.id == id).first()

# 正确
def get_user(id: int):
    try:
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        return user
    except Exception as e:
        logger.error(f"获取用户错误: {e}")
        raise HTTPException(status_code=500, detail="服务器内部错误")
```

### 2. 不安全的直接SQL
```python
# 错误
def query_db(sql):
    return cursor.execute(sql)

# 正确
def query_db(sql, params):
    return cursor.execute(sql, params)
```

### 3. 硬编码凭据
```python
# 错误
DATABASE_URL = "mysql://root:password@localhost:3306/db"

# 正确
DATABASE_URL = os.getenv("DATABASE_URL")
```

### 4. 缺少输入验证
```python
# 错误
def create_user(username, email):
    return User(username=username, email=email)

# 正确
def create_user(user_data: UserCreate):
    return User(username=user_data.username, email=user_data.email)
```

### 5. 无分页
```python
# 错误
def get_all_users():
    return db.query(User).all()

# 正确
def get_all_users(skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()
```

## 文件特定检查

### API文件
- 路由有正确的HTTP方法
- 定义了请求/响应模型
- 正确注入了依赖
- 记录了错误响应

### 模型文件
- 正确定义了关系
- 经常查询的列有索引
- 设置了默认值
- 处理了可空字段

### 服务文件
- 业务逻辑与路由分离
- 正确管理事务
- 捕获并记录了异常

## 输出格式

审查后，提供：

```
## 代码审查报告

### 发现的问题
| 严重性 | 位置 | 问题 | 建议 |
|--------|------|------|------|
| 高 | api/auth.py:45 | SQL注入风险 | 使用参数化查询 |
| 中 | api/users.py:23 | 缺少分页 | 添加skip/limit参数 |

### 摘要
- 总问题数: X
- 高优先级: X
- 中优先级: X
- 低优先级: X

### 建议
1. 立即修复高优先级问题
2. 在下一个迭代中审查中优先级问题
3. 考虑在未来改进中处理低优先级问题
```

## 审查文件

审查时重点关注：
- `api/` - API路由处理
- `models/` - 数据库模型
- `services/` - 业务逻辑
- `schemas/` - Pydantic模型
- `main.py` - 应用入口点

## 快速审查命令

```bash
# 统计代码行数
Get-ChildItem -Recurse -Include "*.py" | Get-Content | Measure-Object -Line

# 查找TODO注释
Select-String -Path . -Pattern "TODO|FIXME|HACK" -Recurse

# 检查print语句
Select-String -Path . -Pattern "print\(" -Recurse

# 查找大函数（>100行）
```