import pymysql

# 使用 UTF-16 LE 编码读取备份文件
with open('backups/shuwei_data_manager_20260320_235846.sql', 'r', encoding='utf-16-le') as f:
    content = f.read()

# 提取 CREATE TABLE 语句
start = content.find('CREATE TABLE `knowledge_docs`')
end = content.find(';', start)
create_table = content[start:end+1]

print('CREATE TABLE 语句:')
print(create_table[:500] + '...')

# 连接数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='shuwei_data_manager',
    charset='utf8mb4'
)
cursor = conn.cursor()

# 创建表
cursor.execute(create_table)
print('\n表创建成功!')

conn.commit()

# 验证
cursor.execute('SHOW TABLES LIKE "knowledge_docs"')
print('knowledge_docs 表已创建:', cursor.fetchone() is not None)

cursor.close()
conn.close()