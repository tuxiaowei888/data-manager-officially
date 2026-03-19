import sys
sys.path.insert(0, '.')

print('=== 批量向量化所有文档 ===')

import chromadb
from config.database import SessionLocal
from models.knowledge_doc import KnowledgeDoc

# 初始化 ChromaDB
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="knowledge_policies")

print(f'当前向量库文档数: {collection.count()}')

# 获取所有文档
db = SessionLocal()
docs = db.query(KnowledgeDoc).filter(KnowledgeDoc.is_active == True).all()
print(f'数据库中有 {len(docs)} 个活跃文档')

total_chunks = 0
success_docs = 0

for doc in docs:
    if not doc.content or not doc.content.strip():
        print(f'跳过文档 {doc.id}: 内容为空')
        continue
    
    print(f'处理文档 {doc.id}: {doc.title[:30]}... (长度: {len(doc.content)})')
    
    # 分块
    content = doc.content
    chunk_size = 500
    chunk_overlap = 50
    chunks = []
    start = 0
    
    while start < len(content):
        end = min(start + chunk_size, len(content))
        
        # 尝试在标点处断开
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
    
    print(f'  分成 {len(chunks)} 个块')
    
    # 生成ID
    ids = [f"{doc.id}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"doc_id": doc.id, "chunk_index": i, "title": doc.title} for i in range(len(chunks))]
    
    # 添加到向量库
    try:
        collection.add(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        total_chunks += len(chunks)
        success_docs += 1
        print(f'  添加成功!')
    except Exception as e:
        print(f'  添加失败: {e}')

db.close()

print()
print('=== 处理完成 ===')
print(f'成功处理文档: {success_docs}')
print(f'总文本块数: {total_chunks}')
print(f'向量库文档数: {collection.count()}')

# 测试搜索
print()
print('=== 测试搜索 ===')
results = collection.query(
    query_texts=["数据安全"],
    n_results=3
)
print(f'搜索"数据安全"返回 {len(results["documents"][0])} 条结果')
for i, doc in enumerate(results["documents"][0][:2]):
    print(f'  {i+1}. {doc[:60]}...')
