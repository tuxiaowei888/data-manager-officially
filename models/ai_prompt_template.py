"""
AI提示词模板模型
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from config.database import Base

class AIPromptTemplate(Base):
    """AI提示词模板"""
    __tablename__ = "ai_prompt_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="模板名称")
    type = Column(String(20), nullable=False, comment="模板类型: system/system_prompt/report/report_prompt")
    description = Column(Text, nullable=True, comment="模板描述")
    content = Column(Text, nullable=False, comment="模板内容")
    variables = Column(Text, nullable=True, comment="模板变量JSON数组")
    is_default = Column(Boolean, default=False, comment="是否默认模板")
    is_active = Column(Boolean, default=True, comment="是否启用")
    sort_order = Column(Integer, default=0, comment="排序顺序")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<AIPromptTemplate(id={self.id}, name={self.name}, type={self.type})>"