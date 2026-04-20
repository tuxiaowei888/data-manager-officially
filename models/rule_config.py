"""
规则配置模型 - 数维数据管家系统
表名：rule_configs
用途：存储所有评价指标的逻辑、权重和阈值
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from sqlalchemy.sql import func
from config.database import Base


DIMENSIONS = {
    "C": {"name": "合规与安全", "color": "#FF6B6B", "weight": 20},
    "Q": {"name": "数据质量", "color": "#4ECDC4", "weight": 15},
    "O": {"name": "权属确认", "color": "#96CEB4", "weight": 15},
    "V": {"name": "价值评估", "color": "#45B7D1", "weight": 20},
    "M": {"name": "管理体系", "color": "#9B59B6", "weight": 10},
    "L": {"name": "流通能力", "color": "#FFEAA7", "weight": 10},
    "P": {"name": "发展潜力", "color": "#DDA0DD", "weight": 5},
    "S": {"name": "成本计量", "color": "#3498DB", "weight": 5}
}


class RuleConfig(Base):
    """规则配置模型 - V1.0 核心表，包含 V2.0 预留字段"""
    
    __tablename__ = "rule_configs"
    
    id = Column(Integer, primary_key=True, index=True, comment="主键")
    
    dimension_code = Column(String(50), nullable=False, index=True, comment="维度代码")
    
    rule_name = Column(String(200), nullable=False, comment="规则名称")
    
    rule_description = Column(Text, nullable=True, comment="规则描述")
    
    logic_expression = Column(Text, nullable=False, comment="计算逻辑字符串")
    
    weight = Column(Float, nullable=False, default=1.0, comment="权重(百分比)")
    
    risk_threshold = Column(Float, nullable=False, default=60.0, comment="风险触发阈值")
    
    is_active = Column(Boolean, default=True, comment="是否启用")
    
    is_deleted = Column(Boolean, default=False, comment="是否删除(软删除)")
    
    source_type = Column(String(20), default='manual', comment="规则来源：manual/ai_generated/imported")
    
    version = Column(Integer, default=1, comment="规则版本号")
    
    ai_prompt_context = Column(Text, nullable=True, comment="AI生成规则的上下文")
    
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<RuleConfig(id={self.id}, name={self.rule_name}, dimension={self.dimension_code})>"
