import sys
sys.path.insert(0, '.')

print('=== 检查文档内容 ===')

from config.database import SessionLocal
from models.knowledge_doc import KnowledgeDoc

db = SessionLocal()
docs = db.query(KnowledgeDoc).filter(KnowledgeDoc.is_active == True).all()

for doc in docs:
    content_len = len(doc.content) if doc.content else 0
    print(f'文档 {doc.id}: {doc.title[:30]}... - 内容长度: {content_len}')

db.close()

print()
print('=== 直接测试添加 ===')

import chromadb
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="knowledge_policies")

print(f'当前文档数: {collection.count()}')

# 取第一个文档测试
db = SessionLocal()
doc = db.query(KnowledgeDoc).filter(KnowledgeDoc.id == 6).first()
if doc and doc.content:
    print(f'处理文档 6, 内容长度: {len(doc.content)}')
    
    # 分块
    content = doc.content
    chunk_size = 500
    chunks = []
    start = 0
    while start < len(content):
        end = min(start + chunk_size, len(content))
        chunk = content[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end
    
    print(f'分成 {len(chunks)} 个块')
    
    # 只添加前3个块测试
    test_chunks = chunks[:3]
    ids = [f"6_chunk_{i}" for i in range(len(test_chunks))]
    
    print(f'添加 {len(test_chunks)} 个测试块...')
    collection.add(
        documents=test_chunks,
        ids=ids
    )
    print(f'添加后文档数: {collection.count()}')

db.close()
