"""
知识库文档模型 - 数维数据管家系统
表名：knowledge_docs
用途：存储政策文档及其元数据
"""
from sqlalchemy import Column, Integer, String, Boolean, Text, JSON, TIMESTAMP, ForeignKey
from config.database import Base


class KnowledgeDoc(Base):
    """知识库文档模型 - V1.0 核心表，包含 V2.0 预留字段"""
    
    __tablename__ = "knowledge_docs"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键")
    category_id = Column(Integer, ForeignKey('knowledge_categories.id'), nullable=True, comment="目录分类ID")
    doc_type = Column(String(50), nullable=True, comment="文档类型")
    title = Column(String(500), nullable=False, comment="文档标题")
    content = Column(Text, nullable=True, comment="文档内容文本")
    tags = Column(JSON, nullable=True, comment="标签")
    source = Column(String(200), nullable=True, comment="来源")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(TIMESTAMP, nullable=True, comment="创建时间")
    updated_at = Column(TIMESTAMP, nullable=True, comment="更新时间")
    
    def __repr__(self):
        return f"<KnowledgeDoc(id={self.id}, title={self.title})>"
