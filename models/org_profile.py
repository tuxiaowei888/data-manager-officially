"""
企业画像模型 - 数维数据管家系统
表名：org_profiles
用途：存储企业的基本信息，支持两级评估结构的第一级
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from config.database import Base


class OrgProfile(Base):
    """企业画像模型 - 存储企业基本信息"""
    
    __tablename__ = "org_profiles"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True, comment="主键")
    
    # 用户关联
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户ID")
    
    # 企业基本信息
    org_name = Column(String(200), nullable=True, comment="企业名称")
    industry = Column(String(100), nullable=True, comment="行业")
    company_size = Column(String(50), nullable=True, comment="企业规模")
    
    # 数据能力
    data_team_status = Column(String(50), nullable=True, comment="数据团队状况")
    
    # 安全与合规
    security_certs = Column(JSON, nullable=True, comment="安全认证（JSON数组）")
    data_security_measures = Column(String(100), nullable=True, comment="数据安全措施")
    compliance_history = Column(String(100), nullable=True, comment="合规历史")
    
    # 联系人信息
    contact_name = Column(String(100), nullable=True, comment="联系人姓名")
    contact_phone = Column(String(20), nullable=True, comment="联系电话")
    contact_email = Column(String(100), nullable=True, comment="联系邮箱")
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关系定义
    user = relationship("User", backref="org_profiles")
    
    # 数据集关系（一对多）
    datasets = relationship("Dataset", back_populates="org_profile", cascade="all, delete-orphan")
    
    # 评估结果关系（一对多）
    evaluation_results = relationship("EvaluationResult", back_populates="org_profile", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<OrgProfile(id={self.id}, org_name='{self.org_name}', user_id={self.user_id})>"
    
    @property
    def company_size_display(self):
        """显示企业规模"""
        size_map = {
            'micro': '微型企业（<10人）',
            'small': '小型企业（10-50人）',
            'medium': '中型企业（50-250人）',
            'large': '大型企业（>250人）'
        }
        return size_map.get(self.company_size, self.company_size or '未设置')
    
    @property
    def data_team_display(self):
        """显示数据团队状况"""
        team_map = {
            'none': '无专门团队',
            'part_time': '兼职人员',
            'small_team': '小型团队（<5人）',
            'dedicated_dept': '专门部门（>5人）',
            'full_department': '完整数据部门'
        }
        return team_map.get(self.data_team_status, self.data_team_status or '未设置')
    
    @property
    def has_security_certs(self):
        """检查是否有安全认证"""
        if not self.security_certs:
            return False
        if isinstance(self.security_certs, list):
            return len(self.security_certs) > 0
        return bool(self.security_certs)
    
    @property
    def security_certs_display(self):
        """显示安全认证"""
        if not self.security_certs:
            return "无"
        if isinstance(self.security_certs, list):
            return "、".join(self.security_certs)
        return str(self.security_certs)