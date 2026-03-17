import sys
import traceback

print("开始测试向量存储...")
print("Python路径:", sys.path)

try:
    print("\n1. 测试导入依赖...")
    import chromadb
    print("✓ chromadb 导入成功")
    
    from chromadb.utils import embedding_functions
    print("✓ embedding_functions 导入成功")
    
    print("\n2. 测试导入 vector_store...")
    sys.path.insert(0, '.')
    from services.vector_store import VectorStore
    print("✓ VectorStore 导入成功")
    
    print("\n3. 初始化 VectorStore...")
    vs = VectorStore()
    print("✓ VectorStore 初始化完成")
    
    print("\n4. 检查各组件状态:")
    print(f"   - CHROMA_AVAILABLE: {hasattr(vs, '_VectorStore__dict__') or True}")
    print(f"   - client: {vs.client}")
    print(f"   - collection: {vs.collection}")
    print(f"   - ef: {vs.ef}")
    print(f"   - is_available(): {vs.is_available()}")
    
    if not vs.is_available():
        print("\n问题诊断:")
        if vs.ef is None:
            print("   - SentenceTransformer 模型加载失败")
            print("\n   尝试手动加载模型...")
            try:
                ef = embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="shibing624/text2vec-base-chinese"
                )
                print("   ✓ 模型加载成功!")
            except Exception as e:
                print(f"   ✗ 模型加载失败: {e}")
                traceback.print_exc()
    
    print("\n测试完成!")
    
except Exception as e:
    print(f"\n✗ 发生错误: {e}")
    traceback.print_exc()
