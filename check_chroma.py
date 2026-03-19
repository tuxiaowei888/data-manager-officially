import chromadb
import sqlite3
import os

print("=== 检查 ChromaDB 状态 ===")

# 检查数据库文件
db_path = "./chroma_db/chroma.sqlite3"
if os.path.exists(db_path):
    print(f"数据库文件存在: {db_path}")
    file_size = os.path.getsize(db_path)
    print(f"文件大小: {file_size} bytes")
    
    # 直接查询SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 查询表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"表: {[t[0] for t in tables]}")
    
    # 查询集合
    cursor.execute("SELECT id, name FROM collections;")
    collections = cursor.fetchall()
    print(f"集合: {collections}")
    
    conn.close()
else:
    print("数据库文件不存在")

# 使用 ChromaDB API
print("\n=== ChromaDB API ===")
client = chromadb.PersistentClient(path="./chroma_db")
collections = client.list_collections()
print(f"集合列表: {[c.name for c in collections]}")

for col in collections:
    print(f"\n集合: {col.name}")
    count = col.count()
    print(f"  文档数: {count}")
    
    if count > 0:
        # 获取一些文档
        result = col.get(limit=3)
        print(f"  示例文档ID: {result['ids'][:3]}")
        
        # 测试搜索
        query_result = col.query(
            query_texts=["数据安全"],
            n_results=2
        )
        print(f"  搜索结果数: {len(query_result['documents'][0])}")
        if query_result['documents'][0]:
            print(f"  第一条结果: {query_result['documents'][0][0][:60]}...")
