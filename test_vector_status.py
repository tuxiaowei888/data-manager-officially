import sys
sys.path.insert(0, '.')

from services.vector_store import vector_store

print('向量库文档数量:', vector_store.get_document_count())

# 测试搜索
results = vector_store.search('数据安全', top_k=3)
print('搜索结果数量:', len(results))
for i, r in enumerate(results[:2]):
    content = r.get('content', '')[:50]
    print(f'  {i+1}. {content}...')
