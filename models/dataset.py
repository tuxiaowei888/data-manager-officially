"""
数据集模型 - 数维数据管家系统
表名：datasets
用途：存储用户的数据集信息，支持两级评估结构
"""
from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from config.database import Base


class Dataset(Base):
    """数据集模型 - 存储用户的数据集信息"""
    
    __tablename__ = "datasets"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True, comment="主键")
    
    # 用户关联
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    
    # 企业画像关联（可选）
    org_profile_id = Column(Integer, ForeignKey("org_profiles.id"), nullable=True, index=True, comment="企业画像ID")
    
    # 数据集基本信息
    dataset_name = Column(String(200), nullable=False, comment="数据集名称")
    dataset_type = Column(String(50), nullable=True, comment="数据集类型：core_ops/user_market/research/tech_dev/other")
    
    # 数据量信息
    data_volume_value = Column(Float, nullable=True, comment="数据量数值")
    data_volume_unit = Column(String(20), nullable=True, comment="数据量单位：万条/GB/TB")
    
    # 合规与安全信息
    contains_personal_info = Column(Boolean, default=False, comment="是否包含个人信息")
    desensitization_status = Column(String(50), nullable=True, comment="脱敏状态：full/partial/none")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关系定义
    user = relationship("User", backref="datasets")
    org_profile = relationship("OrgProfile", backref="datasets")
    
    # 评估结果关系（一对多）
    evaluation_results = relationship("EvaluationResult", back_populates="dataset", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Dataset(id={self.id}, name='{self.dataset_name}', user_id={self.user_id})>"
    
    @property
    def display_data_volume(self):
        """显示格式化的数据量"""
        if self.data_volume_value and self.data_volume_unit:
            return f"{self.data_volume_value} {self.data_volume_unit}"
        return "未设置"
    
    @property
    def dataset_type_display(self):
        """显示数据集类型"""
        type_map = {
            'core_ops': '核心运营',
            'user_market': '用户与市场',
            'research': '科研与公共服务',
            'tech_dev': '技术开发',
            'other': '其他'
        }
        return type_map.get(self.dataset_type, self.dataset_type or '未设置')
    
    @property
    def desensitization_status_display(self):
        """显示脱敏状态"""
        status_map = {
            'full': '已完全脱敏',
            'partial': '部分脱敏',
            'none': '未脱敏'
        }
        return status_map.get(self.desensitization_status, self.desensitization_status or '未设置')
    
    @property
    def personal_info_display(self):
        """显示个人信息状态"""
        return "是" if self.contains_personal_info else "否"