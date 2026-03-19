# -*- coding: utf-8 -*-
"""
批量向量化脚本 - 数维数据管家系统
自动处理所有知识库文档
"""
import sys
import os
import time

# 设置输出编码
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 50)
print("批量向量化脚本启动")
print("=" * 50)

# 1. 检查依赖
print("\n[1/4] 检查依赖...")
try:
    import chromadb
    print(f"  ✓ ChromaDB 版本: {chromadb.__version__}")
except ImportError:
    print("  ✗ ChromaDB 未安装，正在安装...")
    os.system("pip install chromadb -q")
    import chromadb

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    print("  ✓ SQLAlchemy 已安装")
except ImportError:
    print("  ✗ SQLAlchemy 未安装")
    sys.exit(1)

# 2. 连接数据库
print("\n[2/4] 连接数据库...")
sys.path.insert(0, '.')
from config.database import SessionLocal
from models.knowledge_doc import KnowledgeDoc

db = SessionLocal()
docs = db.query(KnowledgeDoc).filter(KnowledgeDoc.is_active == True).all()
print(f"  ✓ 找到 {len(docs)} 个活跃文档")

# 3. 初始化向量库
print("\n[3/4] 初始化向量库...")
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="knowledge_policies")
print(f"  ✓ 当前向量库文档数: {collection.count()}")

# 获取已处理的文档
existing_ids = set()
try:
    existing = collection.get()
    for id in existing['ids']:
        doc_id = id.split('_chunk_')[0]
        existing_ids.add(doc_id)
    print(f"  ✓ 已处理文档数: {len(existing_ids)}")
except:
    pass

# 4. 批量处理
print("\n[4/4] 批量向量化...")
success_count = 0
skip_count = 0
error_count = 0
total_chunks = 0

for doc in docs:
    if str(doc.id) in existing_ids:
        print(f"  跳过文档 {doc.id} (已处理)")
        skip_count += 1
        continue
    
    if not doc.content or not doc.content.strip():
        print(f"  跳过文档 {doc.id} (内容为空)")
        skip_count += 1
        continue
    
    title = doc.title[:25] + "..." if doc.title and len(doc.title) > 25 else doc.title
    print(f"  处理文档 {doc.id}: {title}")
    
    # 分块
    content = doc.content
    chunk_size = 500
    chunk_overlap = 50
    chunks = []
    start = 0
    
    while start < len(content):
        end = min(start + chunk_size, len(content))
        if end < len(content):
            last_punct = max(
                content.rfind('。', start, end),
                content.rfind('！', start, end),
                content.rfind('？', start, end),
                content.rfind('\n', start, end)
            )
            if last_punct > start + chunk_overlap:
                end = last_punct + 1
        chunk = content[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - chunk_overlap
        if start < 0:
            start = 0
        if start >= len(content):
            break
    
    # 添加到向量库
    try:
        ids = [f"{doc.id}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"doc_id": str(doc.id), "chunk_index": i, "title": doc.title or ""} for i in range(len(chunks))]
        
        collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        success_count += 1
        total_chunks += len(chunks)
        print(f"    ✓ 成功添加 {len(chunks)} 个文本块")
    except Exception as e:
        error_count += 1
        print(f"    ✗ 错误: {e}")

db.close()

# 结果
print("\n" + "=" * 50)
print("处理完成!")
print("=" * 50)
print(f"成功处理: {success_count} 个文档")
print(f"跳过: {skip_count} 个文档")
print(f"失败: {error_count} 个文档")
print(f"总文本块: {total_chunks}")
print(f"向量库总文档数: {collection.count()}")

# 测试搜索
if collection.count() > 0:
    print("\n测试搜索...")
    results = collection.query(query_texts=["数据安全"], n_results=3)
    print(f"搜索'数据安全'返回 {len(results['documents'][0])} 条结果")
    if results['documents'][0]:
        print(f"示例: {results['documents'][0][0][:50]}...")

print("\n向量化完成!")
