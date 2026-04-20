import pymysql
import re

with open('backups/shuwei_data_manager_20260320_235846.sql', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-16-le', errors='ignore')

# 使用正则精确匹配
match = re.search(r'LOCK TABLES `knowledge_docs` WRITE;(.+?)UNLOCK TABLES', content, re.DOTALL)
if match:
    data_section = match.group(1)
    print(f'数据区域长度: {len(data_section)}')

    # 连接数据库 - 使用安全的数据库连接
    from config.script_db import get_pymysql_connection
    conn = get_pymysql_connection()
    # 设置SQL模式
    cursor = conn.cursor()
    cursor.execute("SET SESSION sql_mode='NO_ENGINE_SUBSTITUTION'")

    # 删除现有数据
    cursor.execute('DELETE FROM knowledge_docs')

    # 解析 VALUES
    values_match = re.search(r'INSERT INTO `knowledge_docs` VALUES (.+?);', data_section, re.DOTALL)
    if values_match:
        values_str = values_match.group(1)
        print(f'VALUES 长度: {len(values_str)}')

        # 解析记录
        records = []
        current = ""
        depth = 0
        in_string = False
        escape_next = False

        for char in values_str:
            if escape_next:
                current += char
                escape_next = False
                continue
            if char == '\\':
                escape_next = True
                continue
            if char == "'" and not escape_next:
                in_string = not in_string
                current += char
                continue
            if not in_string:
                if char == '(':
                    depth += 1
                    if depth == 1:
                        current = "("
                        continue
                elif char == ')':
                    depth -= 1
                    if depth == 0:
                        current += ")"
                        records.append(current)
                        current = ""
                        continue
                elif char == ',' and depth == 0:
                    continue
            current += char

        print(f'解析出 {len(records)} 条记录')

        # 解析并插入
        parsed = []
        for record in records:
            inner = record.strip()[1:-1]
            parts = []
            current_part = ""
            in_str = False
            esc = False

            for c in inner:
                if esc:
                    current_part += c
                    esc = False
                    continue
                if c == '\\':
                    esc = True
                    continue
                if c == "'":
                    in_str = not in_str
                    current_part += c
                    continue
                if c == ',' and not in_str:
                    parts.append(current_part.strip())
                    current_part = ""
                    continue
                current_part += c
            if current_part.strip():
                parts.append(current_part.strip())

            if len(parts) >= 7:
                try:
                    rec = (
                        int(parts[0]),
                        int(parts[1]) if parts[1] != 'NULL' else None,
                        parts[2].strip("'") if len(parts) > 2 else '',
                        parts[3].strip("'") if len(parts) > 3 else '',
                        parts[4].strip("'") if len(parts) > 4 else '',
                        parts[5].strip("'") if len(parts) > 5 else '1',
                        parts[6].strip("'") if len(parts) > 6 and parts[6].strip() != 'NULL' else None
                    )
                    parsed.append(rec)
                    print(f'  ID {rec[0]}: {rec[2][:30]}...')
                except Exception as e:
                    print(f'解析错误: {e}')

        if parsed:
            cursor.executemany(
                "INSERT INTO knowledge_docs (id, category_id, title, content, source, is_active, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                parsed
            )
            conn.commit()
            print(f'插入成功 {len(parsed)} 条!')

    # 验证
    cursor.execute('SELECT COUNT(*) FROM knowledge_docs')
    print(f'恢复后记录数: {cursor.fetchone()[0]}')

    cursor.close()
    conn.close()
else:
    print('未找到 knowledge_docs 数据')