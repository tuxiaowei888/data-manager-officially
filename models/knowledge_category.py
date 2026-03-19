"""
知识库目录分类模型 - 数维数据管家系统
表名：knowledge_categories
用途：管理知识库文档的分类目录
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from config.database import Base


class KnowledgeCategory(Base):
    """知识库目录分类模型"""
    
    __tablename__ = "knowledge_categories"
    
    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(100), nullable=False, comment="目录名称")
    
    parent_id = Column(Integer, nullable=True, comment="父目录ID，NULL表示根目录")
    
    description = Column(Text, nullable=True, comment="目录描述")
    
    icon = Column(String(50), nullable=True, comment="目录图标")
    
    sort_order = Column(Integer, default=0, comment="排序顺序")
    
    is_active = Column(Boolean, default=True, comment="是否启用")
    
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<KnowledgeCategory(id={self.id}, name={self.name})>"


# 预设目录分类
DEFAULT_CATEGORIES = [
    {"name": "政策法规", "icon": "bi bi-bank", "description": "国家及地方数据相关政策法规"},
    {"name": "行业标准", "icon": "bi bi-file-earmark-text", "description": "数据管理相关行业标准"},
    {"name": "操作指南", "icon": "bi bi-book", "description": "数据资产评估操作指南"},
    {"name": "案例参考", "icon": "bi bi-journal-text", "description": "典型案例分析参考"},
]
