import sys
sys.path.insert(0, '.')

print('=== 测试 ChromaDB 嵌入函数 ===')

import chromadb

# 创建客户端
client = chromadb.PersistentClient(path="./chroma_db")

# 获取或创建集合
collection = client.get_or_create_collection(name="test_collection")

# 测试添加文档
print('测试添加文档...')
try:
    collection.add(
        documents=["这是测试文档1", "这是测试文档2"],
        ids=["test1", "test2"]
    )
    print('添加成功!')
    print(f'集合文档数: {collection.count()}')
    
    # 测试查询
    print('测试查询...')
    results = collection.query(
        query_texts=["测试"],
        n_results=2
    )
    print(f'查询结果: {results}')
    
except Exception as e:
    print(f'错误: {e}')
    import traceback
    traceback.print_exc()

# 清理测试集合
try:
    client.delete_collection("test_collection")
    print('测试集合已清理')
except:
    pass
