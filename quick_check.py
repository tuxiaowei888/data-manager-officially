import chromadb
import sys

try:
    client = chromadb.PersistentClient(path="./chroma_db")
    col = client.get_collection("knowledge_policies")
    count = col.count()
    
    with open("result.txt", "w") as f:
        f.write(f"Count: {count}\n")
        
        if count > 0:
            result = col.get(limit=5)
            f.write(f"IDs: {result['ids']}\n")
            
            # 搜索测试
            query_result = col.query(query_texts=["数据安全"], n_results=3)
            f.write(f"Search results: {len(query_result['documents'][0])}\n")
            if query_result['documents'][0]:
                f.write(f"First: {query_result['documents'][0][0][:100]}\n")
    
    print("Done")
except Exception as e:
    with open("result.txt", "w") as f:
        f.write(f"Error: {e}\n")
    print(f"Error: {e}")
