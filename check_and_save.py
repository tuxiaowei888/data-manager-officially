import chromadb
import sqlite3
import os
import json

output = []

output.append("=== 检查 ChromaDB 状态 ===")

# 检查数据库文件
db_path = "./chroma_db/chroma.sqlite3"
if os.path.exists(db_path):
    output.append(f"数据库文件存在: {db_path}")
    file_size = os.path.getsize(db_path)
    output.append(f"文件大小: {file_size} bytes")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    output.append(f"表: {[t[0] for t in tables]}")
    
    cursor.execute("SELECT id, name FROM collections;")
    collections = cursor.fetchall()
    output.append(f"集合: {collections}")
    
    conn.close()
else:
    output.append("数据库文件不存在")

# 使用 ChromaDB API
output.append("\n=== ChromaDB API ===")
client = chromadb.PersistentClient(path="./chroma_db")
collections = client.list_collections()
output.append(f"集合列表: {[c.name for c in collections]}")

for col in collections:
    output.append(f"\n集合: {col.name}")
    count = col.count()
    output.append(f"  文档数: {count}")
    
    if count > 0:
        result = col.get(limit=3)
        output.append(f"  示例文档ID: {result['ids'][:3]}")
        
        query_result = col.query(
            query_texts=["数据安全"],
            n_results=2
        )
        output.append(f"  搜索结果数: {len(query_result['documents'][0])}")
        if query_result['documents'][0]:
            output.append(f"  第一条结果: {query_result['documents'][0][0][:60]}...")

# 写入文件
with open("vector_status.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(output))

print("结果已写入 vector_status.txt")
