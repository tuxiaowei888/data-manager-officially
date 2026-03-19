# -*- coding: utf-8 -*-
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

print("开始向量化...")

import chromadb
sys.path.insert(0, '.')
from config.database import SessionLocal
from models.knowledge_doc import KnowledgeDoc

# 初始化
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="knowledge_policies")

# 获取已处理的文档
existing_ids = set()
try:
    existing = collection.get()
    for id in existing['ids']:
        doc_id = id.split('_chunk_')[0]
        existing_ids.add(doc_id)
except:
    pass

print(f"已处理文档: {existing_ids}")
print(f"当前文档数: {collection.count()}")

# 获取数据库文档
db = SessionLocal()
docs = db.query(KnowledgeDoc).filter(KnowledgeDoc.is_active == True).all()
print(f"待处理文档: {len(docs)}")

# 处理每个文档
for doc in docs:
    if str(doc.id) in existing_ids:
        print(f"跳过 {doc.id}")
        continue
    
    if not doc.content:
        print(f"跳过 {doc.id} (空)")
        continue
    
    print(f"处理 {doc.id}: {doc.title[:20]}...")
    
    # 简单分块
    chunks = []
    text = doc.content
    for i in range(0, len(text), 500):
        chunk = text[i:i+500].strip()
        if chunk:
            chunks.append(chunk)
    
    # 添加到向量库
    ids = [f"{doc.id}_chunk_{j}" for j in range(len(chunks))]
    metadatas = [{"doc_id": str(doc.id), "title": doc.title or ""} for j in range(len(chunks))]
    
    try:
        collection.add(documents=chunks, ids=ids, metadatas=metadatas)
        print(f"  成功: {len(chunks)} 块")
    except Exception as e:
        print(f"  失败: {e}")

db.close()
print(f"\n完成! 总文档数: {collection.count()}")

# 测试搜索
results = collection.query(query_texts=["数据安全"], n_results=2)
print(f"搜索测试: {len(results['documents'][0])} 条结果")
