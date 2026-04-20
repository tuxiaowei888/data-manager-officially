---
name: 数据迁移
description: 处理数据库迁移，包括结构更改、数据备份、恢复和数据转换。当用户想要迁移数据或更新数据库结构时调用。
---

# 数据迁移

该技能用于处理任何项目的数据库迁移、备份、恢复和数据转换。

## 必需配置

| 变量 | 描述 | 示例 |
|------|------|------|
| `DB_CONTAINER` | Docker容器名称 | `my-mysql` |
| `DB_NAME` | 数据库名称 | `myapp_db` |
| `DB_USER` | 数据库用户 | `root` |
| `DB_PASSWORD` | 数据库密码 | `mypassword` |
| `DB_PORT` | 数据库端口 | `3306` |

## 迁移类型

### 1. 结构迁移
更改数据库结构（表、列、索引）。

### 2. 数据迁移
在环境之间移动数据或转换数据。

### 3. 备份和恢复
创建备份和从备份恢复。

## 备份操作

### 创建完整备份
```bash
# 备份整个数据库
docker exec -it <DB_CONTAINER> mysqldump -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> > "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql"

# 验证备份已创建
Get-ChildItem -Filter "backup_*.sql" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

### 备份特定表
```bash
# 备份特定表
docker exec -it <DB_CONTAINER> mysqldump -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> table1 table2 > "partial_backup.sql"
```

### 从备份恢复
```bash
# 删除并重新创建数据库
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "DROP DATABASE IF EXISTS <DB_NAME>; CREATE DATABASE <DB_NAME>;"

# 从备份恢复
docker exec -i <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> < "backup_file.sql"
```

## 结构迁移

### 添加新表
```python
# 示例：添加新表
def migrate_add_table():
    from config.database import engine
    from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData

    metadata = MetaData()
    new_table = Table('new_table', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(100)),
        Column('created_at', DateTime)
    )
    metadata.create_all(engine)
```

### 添加新列
```python
# 向现有表添加新列
def migrate_add_column():
    from config.database import engine
    from sqlalchemy import text

    with engine.connect() as conn:
        conn.execute(text("ALTER TABLE users ADD COLUMN new_column VARCHAR(100)"))
        conn.commit()
```

### 创建索引
```python
# 向表添加索引
def migrate_add_index():
    from config.database import engine
    from sqlalchemy import text

    with engine.connect() as conn:
        conn.execute(text("CREATE INDEX idx_email ON users(email)"))
        conn.commit()
```

## 数据迁移脚本

### 导出数据到JSON
```python
def export_to_json(table_name):
    from config.database import SessionLocal
    from sqlalchemy import text

    db = SessionLocal()
    result = db.execute(text(f"SELECT * FROM {table_name}"))
    rows = result.fetchall()
    columns = result.keys()

    data = [dict(zip(columns, row)) for row in rows]

    import json
    with open(f'{table_name}_export.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False, default=str)

    db.close()
    return len(data)
```

### 从JSON导入数据
```python
def import_from_json(table_name, json_file):
    import json
    from config.database import SessionLocal
    from sqlalchemy import text

    with open(json_file, 'r') as f:
        data = json.load(f)

    db = SessionLocal()
    for item in data:
        columns = ', '.join(item.keys())
        placeholders = ', '.join([f':{k}' for k in item.keys()])
        query = text(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})")
        db.execute(query, item)

    db.commit()
    db.close()
    return len(data)
```

### 表之间传输数据
```python
def transfer_data(source_table, target_table, mapping):
    from config.database import SessionLocal
    from sqlalchemy import text

    db = SessionLocal()

    # 从源选择
    result = db.execute(text(f"SELECT * FROM {source_table}"))
    rows = result.fetchall()

    # 插入目标
    for row in rows:
        data = dict(zip(result.keys(), row))
        transformed = {k: data[v] for k, v in mapping.items()}

        columns = ', '.join(transformed.keys())
        placeholders = ', '.join([f':{k}' for k in transformed.keys()])
        query = text(f"INSERT INTO {target_table} ({columns}) VALUES ({placeholders})")
        db.execute(query, transformed)

    db.commit()
    db.close()
```

## 迁移检查清单

| 步骤 | 操作 | 验证 |
|------|------|------|
| 1 | 创建备份 | `ls *.sql` |
| 2 | 测试备份恢复 | `mysql < backup_test.sql` |
| 3 | 运行迁移 | `python migrate_xxx.py` |
| 4 | 验证结构 | `DESCRIBE table_name;` |
| 5 | 验证数据 | `SELECT COUNT(*) FROM table_name;` |
| 6 | 测试应用 | `curl localhost:8000/health` |

## 常见迁移任务

### 1. 重置测试数据
```bash
# 清除特定表
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "TRUNCATE TABLE evaluation_results;"
```

### 2. 更新配置
```bash
# 更新特定值
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "UPDATE config SET value='new_value' WHERE key='setting_name';"
```

### 3. 在数据库之间复制数据
```bash
# 从源导出
docker exec -it source-container mysqldump -u root -ppassword source_db > data.sql

# 导入到目标
docker exec -it target-container mysql -u root -ppassword target_db < data.sql
```

### 4. 重命名表
```python
def rename_table(old_name, new_name):
    from config.database import engine
    from sqlalchemy import text

    with engine.connect() as conn:
        conn.execute(text(f"RENAME TABLE {old_name} TO {new_name}"))
        conn.commit()
```

### 5. 删除列
```python
def drop_column(table_name, column_name):
    from config.database import engine
    from sqlalchemy import text

    with engine.connect() as conn:
        conn.execute(text(f"ALTER TABLE {table_name} DROP COLUMN {column_name}"))
        conn.commit()
```

## 回滚计划

始终准备回滚计划：

```bash
# 1. 迁移前，创建回滚脚本
docker exec -it <DB_CONTAINER> mysqldump -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> > rollback_backup.sql

# 2. 如果迁移失败，恢复
docker exec -i <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> < rollback_backup.sql
```

## 迁移报告

| 项目 | 之前 | 之后 | 状态 |
|------|------|------|------|
| 表 | X | X | ✓/✗ |
| 每表行数 | X | X | ✓/✗ |
| 索引 | X | X | ✓/✗ |
| 数据完整性 | OK | OK | ✓/✗ |

## 验证数据完整性

```bash
# 迁移前后统计行数
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "SELECT COUNT(*) FROM table_name;"

# 检查空值
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "SELECT * FROM table_name WHERE column IS NULL;"

# 检查数据类型
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "DESCRIBE table_name;"
```

## 数据库连接测试

```bash
# 测试MySQL连接
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "SELECT 1;"

# 列出数据库
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> -e "SHOW DATABASES;"

# 列出表
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "SHOW TABLES;"

# 检查表结构
docker exec -it <DB_CONTAINER> mysql -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> -e "DESCRIBE table_name;"
```

## 定时备份

对于生产环境，设置定时备份：

```bash
# 创建备份脚本
@echo off
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "datestamp=%dt:~0,8%"
set "timestamp=%dt:~8,6%"
docker exec -it <DB_CONTAINER> mysqldump -u <DB_USER> -p<DB_PASSWORD> <DB_NAME> > "backup_%datestamp%_%timestamp%.sql"
```

## 迁移安全规则

1. **迁移前始终备份**
2. **首先在预发布环境测试迁移**
3. **保持回滚计划就绪**
4. **记录所有更改**
5. **迁移后监控**
6. **验证数据完整性**