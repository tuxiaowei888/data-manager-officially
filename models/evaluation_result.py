"""
评价结果模型 - 数维数据管家系统
表名：evaluation_results
用途：存储用户评价计算的结果
"""
import uuid
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base


def generate_report_id():
    """生成报告ID"""
    return f"RPT{uuid.uuid4().hex[:12].upper()}"


class EvaluationResult(Base):
    """评价结果模型 - V1.0 核心表，包含 V2.0 预留字段"""
    
    __tablename__ = "evaluation_results"
    
    # 主键
    id = Column(Integer, primary_key=True, index=True, comment="主键")
    
    # 用户 ID
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True, comment="用户 ID")
    
    # 数据集关联（新增V2.0订阅体系）
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=True, index=True, comment="数据集ID")
    
    # 企业画像关联（新增V2.0订阅体系）
    org_profile_id = Column(Integer, ForeignKey("org_profiles.id"), nullable=True, index=True, comment="企业画像ID")
    
    # 评估时的订阅档位（新增V2.0订阅体系）
    subscription_tier = Column(String(20), default='free', comment="评估时的订阅档位")
    
    # 报告 ID（唯一标识）
    report_id = Column(String(100), nullable=False, default=generate_report_id, unique=True, index=True, comment="报告唯一ID")
    
    # 机构名称
    org_name = Column(String(200), nullable=True, comment="机构名称")
    
    # 总分
    total_score = Column(Float, nullable=False, comment="总分")
    
    # 成熟度等级
    maturity_level = Column(String(50), nullable=True, comment="成熟度等级")
    
    # 各维度得分
    compliance_score = Column(Float, nullable=True, comment="合规性得分")
    quality_score = Column(Float, nullable=True, comment="数据质量得分")
    rights_score = Column(Float, nullable=True, comment="权属确认得分")
    value_score = Column(Float, nullable=True, comment="价值评估得分")
    cost_score = Column(Float, nullable=True, comment="成本计量得分")
    
    # 问题列表
    p0_issues = Column(JSON, nullable=True, comment="P0级问题列表")
    p1_issues = Column(JSON, nullable=True, comment="P1级问题列表")
    p2_issues = Column(JSON, nullable=True, comment="P2级问题列表")
    
    # 报告数据
    report_data = Column(JSON, nullable=True, comment="完整报告数据")
    
    # 报告文件URL
    report_pdf_url = Column(String(500), nullable=True, comment="PDF报告URL")
    report_word_url = Column(String(500), nullable=True, comment="Word报告URL")
    
    # 最高风险等级 (P0/P1/P2)
    risk_level = Column(String(10), nullable=False, comment="风险等级")
    
    # 各维度得分详情
    detail_json = Column(JSON, nullable=False, comment="各维度得分详情")
    
    # V2.0 预留：记录计算时使用的引擎版本
    engine_version = Column(String(50), default='v1_static', comment="计算引擎版本")
    
    # V2.0 预留：存储 AI 推导过程，V1.0 留空
    ai_analysis_log = Column(JSON, nullable=True, comment="AI 分析日志")
    
    # 创建时间
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    # 关联定义
    user = relationship("User", backref="evaluation_results")
    dataset = relationship("Dataset", back_populates="evaluation_results")
    org_profile = relationship("OrgProfile", back_populates="evaluation_results")
    
    def __repr__(self):
        return f"<EvaluationResult(id={self.id}, report_id={self.report_id}, score={self.total_score})>"
