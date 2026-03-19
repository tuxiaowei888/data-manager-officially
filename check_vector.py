import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="knowledge_policies")

count = collection.count()
print(f'向量库文档数: {count}')

if count > 0:
    results = collection.query(
        query_texts=["数据安全"],
        n_results=3
    )
    print(f'搜索结果数: {len(results["documents"][0])}')
    for i, doc in enumerate(results["documents"][0]):
        print(f'{i+1}. {doc[:80]}...')
