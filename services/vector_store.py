"""
向量存储服务 - 数维数据管家系统
功能：
1. 文档向量化
2. 语义检索
3. Chroma 向量数据库管理
"""
import os
from typing import List, Dict, Any, Optional
from pathlib import Path

try:
    import chromadb
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False


class VectorStore:
    """向量存储服务 - 基于Chroma"""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        初始化向量存储
        
        Args:
            persist_directory: 向量数据库持久化目录
        """
        self.persist_directory = persist_directory
        self.collection_name = "knowledge_policies"
        self.client = None
        self.collection = None
        self._initialized = False
        
        if CHROMA_AVAILABLE:
            self._init_chroma()
    
    def _init_chroma(self):
        """初始化Chroma客户端和集合"""
        if not CHROMA_AVAILABLE:
            print("[VectorStore] ChromaDB 未安装")
            return
        
        try:
            Path(self.persist_directory).mkdir(exist_ok=True, parents=True)
            
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name
            )
            
            self._initialized = True
            print(f"[VectorStore] 初始化成功，集合: {self.collection_name}")
            
        except Exception as e:
            print(f"[VectorStore] 初始化失败: {e}")
            self._initialized = False
            self.collection = None
    
    def is_available(self) -> bool:
        """检查向量存储是否可用"""
        return CHROMA_AVAILABLE and self.collection is not None and self._initialized
    
    def add_document(
        self,
        doc_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ) -> bool:
        """
        添加文档到向量库
        
        Args:
            doc_id: 文档ID
            content: 文档内容
            metadata: 元数据
            chunk_size: 文本块大小
            chunk_overlap: 块重叠大小
        
        Returns:
            是否成功
        """
        if not self.is_available():
            print("[VectorStore] 向量存储不可用，无法添加文档")
            return False
        
        try:
            chunks = self._split_text(content, chunk_size, chunk_overlap)
            
            if not chunks:
                print(f"[VectorStore] 文档 {doc_id} 内容为空，跳过")
                return False
            
            ids = [f"{doc_id}_chunk_{i}" for i in range(len(chunks))]
            metadatas = [
                {
                    "doc_id": doc_id,
                    "chunk_index": i,
                    **(metadata or {})
                }
                for i in range(len(chunks))
            ]
            
            self.collection.add(
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"[VectorStore] 成功添加文档 {doc_id}，共 {len(chunks)} 个文本块")
            return True
        except Exception as e:
            print(f"[VectorStore] 添加文档失败: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        语义检索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            filter_metadata: 元数据过滤
        
        Returns:
            检索结果列表
        """
        if not self.is_available():
            return []
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                where=filter_metadata
            )
            
            documents = results.get('documents', [[]])[0]
            metadatas = results.get('metadatas', [[]])[0]
            distances = results.get('distances', [[]])[0]
            
            output = []
            for i, doc in enumerate(documents):
                output.append({
                    'content': doc,
                    'metadata': metadatas[i] if i < len(metadatas) else {},
                    'distance': distances[i] if i < len(distances) else 0.0,
                    'relevance': 1.0 - (distances[i] if i < len(distances) else 0.0)
                })
            
            return output
        except Exception as e:
            print(f"[VectorStore] 检索失败: {e}")
            return []
    
    def delete_document(self, doc_id: str) -> bool:
        """
        删除文档
        
        Args:
            doc_id: 文档ID
        
        Returns:
            是否成功
        """
        if not self.is_available():
            return False
        
        try:
            self.collection.delete(
                where={"doc_id": doc_id}
            )
            return True
        except Exception as e:
            print(f"[VectorStore] 删除文档失败: {e}")
            return False
    
    def get_document_count(self) -> int:
        """获取文档数量"""
        if not self.is_available():
            return 0
        try:
            return self.collection.count()
        except:
            return 0
    
    def _split_text(
        self,
        text: str,
        chunk_size: int,
        chunk_overlap: int
    ) -> List[str]:
        """
        简单文本分块
        
        Args:
            text: 输入文本
            chunk_size: 块大小
            chunk_overlap: 重叠大小
        
        Returns:
            文本块列表
        """
        if not text or len(text.strip()) == 0:
            return []
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = min(start + chunk_size, text_length)
            
            if end < text_length:
                last_punct = max(
                    text.rfind('。', start, end),
                    text.rfind('！', start, end),
                    text.rfind('？', start, end),
                    text.rfind('\n', start, end)
                )
                if last_punct > start + chunk_overlap:
                    end = last_punct + 1
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - chunk_overlap
            if start < 0:
                start = 0
            if start <= 0 and end >= text_length:
                break
        
        return chunks


vector_store = VectorStore()
