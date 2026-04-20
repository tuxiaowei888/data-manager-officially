# 转换 UTF-16 到 UTF-8 并提取知识库数据
import codecs

# 读取 UTF-16 LE 文件并转换为 UTF-8
with open('backups/shuwei_data_manager_20260320_235846.sql', 'r', encoding='utf-16-le') as f:
    content = f.read()

# 查找 knowledge_docs 的数据区域
start = content.find('LOCK TABLES `knowledge_docs` WRITE')
end = content.find('UNLOCK TABLES', start)
data_section = content[start:end]

# 写入转换后的文件
with open('backups/knowledge_docs_data.sql', 'w', encoding='utf-8') as f:
    f.write(data_section)

print(f'已提取并转换数据到 backups/knowledge_docs_data.sql')
print(f'文件大小: {len(data_section)} 字符')