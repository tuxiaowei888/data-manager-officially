import sys
sys.path.insert(0, '.')

print('=== 开始批量向量化 ===')

from config.database import SessionLocal
from models.knowledge_doc import KnowledgeDoc
from services.vector_store import vector_store

if not vector_store.is_available():
    print('向量存储不可用，退出')
    sys.exit(1)

print('向量存储可用')

db = SessionLocal()
docs = db.query(KnowledgeDoc).filter(KnowledgeDoc.is_active == True).all()
print(f'找到 {len(docs)} 个文档待处理')

success_count = 0
fail_count = 0
skipped_count = 0

for doc in docs:
    if not doc.content or not doc.content.strip():
        print(f'跳过文档 {doc.id}: 内容为空')
        skipped_count += 1
        continue
    
    try:
        title_preview = doc.title[:30] if doc.title else '无标题'
        print(f'处理文档 {doc.id}: {title_preview}...')
        
        added = vector_store.add_document(
            doc_id=str(doc.id),
            content=doc.content,
            metadata={'title': doc.title, 'category_id': doc.category_id}
        )
        if added:
            success_count += 1
            print(f'  成功')
        else:
            fail_count += 1
            print(f'  失败')
    except Exception as e:
        fail_count += 1
        print(f'  错误: {e}')
        import traceback
        traceback.print_exc()

db.close()

print()
print('=== 处理完成 ===')
print(f'成功: {success_count}')
print(f'失败: {fail_count}')
print(f'跳过: {skipped_count}')
print(f'向量库总文档数: {vector_store.get_document_count()}')
