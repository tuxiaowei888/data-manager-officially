---
name: 数据验证
description: 验证数据完整性和一致性。当用户要求验证数据、检查数据完整性或数据校验时调用。
---

# 数据验证

该技能用于验证数据库数据的完整性和一致性。

## 验证项目

| 验证项 | 说明 | 重要性 |
|--------|------|--------|
| 数据完整性 | 检查必填字段 | 高 |
| 数据一致性 | 检查关联关系 | 高 |
| 数据唯一性 | 检查唯一约束 | 高 |
| 数据格式 | 检查数据格式 | 中 |
| 数据范围 | 检查数值范围 | 中 |

## 验证步骤

### 步骤1：检查表结构
```bash
# 查看所有表
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "SHOW TABLES;"

# 查看表结构
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "DESCRIBE users;"

# 查看索引
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "SHOW INDEX FROM users;"
```

### 步骤2：检查数据完整性
```bash
# 检查必填字段是否为空
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SELECT 'users' as table_name, COUNT(*) as null_count
FROM users
WHERE username IS NULL OR email IS NULL;
"

# 检查所有表的空值
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SELECT
    TABLE_NAME,
    COLUMN_NAME,
    IS_NULLABLE,
    DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = '<DB_NAME>'
AND IS_NULLABLE = 'NO'
AND COLUMN_DEFAULT IS NULL;
"
```

### 步骤3：检查数据唯一性
```bash
# 检查重复数据
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SELECT username, COUNT(*) as count
FROM users
GROUP BY username
HAVING count > 1;
"

# 检查email重复
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SELECT email, COUNT(*) as count
FROM users
GROUP BY email
HAVING count > 1;
"
```

### 步骤4：检查数据一致性
```bash
# 检查外键关联
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SELECT 'orphan records' as issue, COUNT(*) as count
FROM evaluation_results er
LEFT JOIN users u ON er.user_id = u.id
WHERE u.id IS NULL;
"

# 检查孤立记录
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SELECT 'users' as table1, 'evaluation_results' as table2, 'user_id' as foreign_key, COUNT(*) as orphans
FROM evaluation_results
WHERE user_id NOT IN (SELECT id FROM users);
"
```

### 步骤5：检查数据格式
```bash
# 检查邮箱格式
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SELECT id, email
FROM users
WHERE email NOT LIKE '%@%.%'
AND email IS NOT NULL;
"

# 检查日期格式
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SELECT id, created_at
FROM users
WHERE created_at = '0000-00-00 00:00:00';
"
```

### 步骤6：检查数据范围
```bash
# 检查数值范围
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SELECT id, weight, risk_threshold
FROM rule_configs
WHERE weight < 0 OR weight > 1;
"

# 检查枚举值
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SELECT DISTINCT user_type
FROM users;
"
```

## 验证脚本

### 完整验证脚本
```python
def validate_all():
    from config.database import SessionLocal
    from models.user import User
    from models.rule_configs import RuleConfig

    db = SessionLocal()
    issues = []

    # 1. 检查用户必填字段
    users = db.query(User).all()
    for user in users:
        if not user.username:
            issues.append(f"用户ID {user.id} 用户名为空")
        if not user.email:
            issues.append(f"用户ID {user.id} 邮箱为空")

    # 2. 检查重复数据
    duplicate_usernames = db.query(User.username).group_by(User.username).having(db.func.count() > 1).all()
    if duplicate_usernames:
        issues.append(f"发现重复用户名: {duplicate_usernames}")

    # 3. 检查规则配置
    rules = db.query(RuleConfig).all()
    for rule in rules:
        if rule.weight < 0 or rule.weight > 1:
            issues.append(f"规则ID {rule.id} 权重超出范围: {rule.weight}")

    db.close()
    return issues
```

## 验证报告

```
## 数据验证报告
验证时间: 2024-03-18 15:30

### 表结构验证
| 表名 | 记录数 | 状态 |
|------|--------|------|
| users | 2 | ✓ |
| channels | 1 | ✓ |
| rule_configs | 18 | ✓ |
| evaluation_results | 0 | ✓ |

### 数据完整性
| 检查项 | 状态 | 发现 |
|--------|------|------|
| 必填字段 | ✓ 通过 | 0 |
| 空值检查 | ✓ 通过 | 0 |
| 外键关联 | ✓ 通过 | 0 |

### 数据唯一性
| 检查项 | 状态 | 发现 |
|--------|------|------|
| 用户名唯一 | ✓ 通过 | 0 |
| 邮箱唯一 | ✓ 通过 | 0 |

### 数据一致性
| 检查项 | 状态 | 发现 |
|--------|------|------|
| 外键关联 | ✓ 通过 | 0 |
| 孤立记录 | ✓ 通过 | 0 |

### 数据格式
| 检查项 | 状态 | 发现 |
|--------|------|------|
| 邮箱格式 | ✓ 通过 | 0 |
| 日期格式 | ✓ 通过 | 0 |

### 总结
- 总检查项: 25
- 通过: 25
- 失败: 0
- 状态: 全部通过 ✓
```

## 常见问题

### 问题：发现重复数据
```bash
# 1. 查找重复数据
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SELECT username, COUNT(*) as count
FROM users
GROUP BY username
HAVING count > 1;
"

# 2. 删除重复数据（保留ID最小的）
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
DELETE FROM users
WHERE id NOT IN (
    SELECT MIN(id)
    FROM users
    GROUP BY username
);
"
```

### 问题：发现空值
```bash
# 1. 查找空值
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SELECT id, username, email
FROM users
WHERE username IS NULL OR email IS NULL;
"

# 2. 更新空值
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
UPDATE users
SET username = CONCAT('user_', id)
WHERE username IS NULL;
"
```

### 问题：发现孤立记录
```bash
# 1. 查找孤立记录
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
SELECT *
FROM evaluation_results
WHERE user_id NOT IN (SELECT id FROM users);
"

# 2. 删除或修复孤立记录
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "
DELETE FROM evaluation_results
WHERE user_id NOT IN (SELECT id FROM users);
"
```