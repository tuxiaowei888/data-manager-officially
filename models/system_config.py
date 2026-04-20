"""
系统配置模型 - 存储系统运行参数
"""
from sqlalchemy import Column, Integer, String, Text
from config.database import Base


class SystemConfig(Base):
    """系统配置模型"""
    
    __tablename__ = "system_configs"
    
    id = Column(Integer, primary_key=True)
    config_key = Column(String(100), unique=True, nullable=False, index=True)
    config_value = Column(Text, nullable=True)
    description = Column(String(500), nullable=True)
    
    def __repr__(self):
        return f"<SystemConfig(key={self.config_key})>"


DEFAULT_CONFIGS = {
    # 旧版配置（保持兼容）
    "free_daily_eval_limit": {
        "value": "3",
        "description": "普通用户每日评估次数限制"
    },
    "vip_default_days": {
        "value": "30",
        "description": "VIP默认开通天数"
    },
    "free_report_retention_days": {
        "value": "7",
        "description": "普通用户报告保留天数"
    },
    "vip_report_retention_days": {
        "value": "36500",
        "description": "VIP用户报告保留天数（永久=36500天）"
    },
    "enable_vip_export": {
        "value": "true",
        "description": "是否启用VIP导出功能"
    },
    "enable_ai_analysis": {
        "value": "true",
        "description": "是否启用AI分析功能"
    },
    "system_name": {
        "value": "数维数据管家系统",
        "description": "系统名称"
    },
    "contact_email": {
        "value": "support@example.com",
        "description": "联系邮箱"
    },
    
    # V2.0 订阅四档体系配置
    # ======================= 体验版配置 =======================
    "free_eval_limit": {
        "value": "1",
        "description": "体验版年度评估次数限制"
    },
    "free_report_depth": {
        "value": "summary",
        "description": "体验版报告深度：summary/diagnosis/action_plan/full"
    },
    "free_report_retention": {
        "value": "7",
        "description": "体验版报告保留天数"
    },
    
    # ======================= 基础版配置 =======================
    "basic_eval_limit": {
        "value": "5",
        "description": "基础版年度评估次数限制"
    },
    "basic_report_depth": {
        "value": "diagnosis",
        "description": "基础版报告深度"
    },
    "basic_report_retention": {
        "value": "365",
        "description": "基础版报告保留天数（1年）"
    },
    "basic_pdf_export": {
        "value": "true",
        "description": "基础版是否允许PDF导出"
    },
    "basic_knowledge_access": {
        "value": "basic",
        "description": "基础版知识库访问权限：basic/full"
    },
    
    # ======================= 专业版配置 =======================
    "pro_eval_limit": {
        "value": "20",
        "description": "专业版年度评估次数限制"
    },
    "pro_report_depth": {
        "value": "action_plan",
        "description": "专业版报告深度"
    },
    "pro_report_retention": {
        "value": "730",
        "description": "专业版报告保留天数（2年）"
    },
    "pro_pdf_export": {
        "value": "true",
        "description": "专业版是否允许PDF导出"
    },
    "pro_knowledge_access": {
        "value": "full",
        "description": "专业版知识库访问权限"
    },
    "pro_industry_benchmark": {
        "value": "true",
        "description": "专业版是否启用行业对标功能"
    },
    "pro_valuation": {
        "value": "true",
        "description": "专业版是否启用估值计算功能"
    },
    
    # ======================= 企业版配置 =======================
    "enterprise_eval_limit": {
        "value": "-1",
        "description": "企业版年度评估次数限制（-1表示不限量）"
    },
    "enterprise_report_depth": {
        "value": "full",
        "description": "企业版报告深度"
    },
    "enterprise_report_retention": {
        "value": "-1",
        "description": "企业版报告保留天数（-1表示永久）"
    },
    "enterprise_pdf_export": {
        "value": "true",
        "description": "企业版是否允许PDF导出"
    },
    "enterprise_knowledge_access": {
        "value": "full",
        "description": "企业版知识库访问权限"
    },
    "enterprise_brand_custom": {
        "value": "true",
        "description": "企业版是否启用品牌定制功能"
    },
    "enterprise_api_access": {
        "value": "true",
        "description": "企业版是否启用API访问"
    },
    "enterprise_multi_dataset_overview": {
        "value": "true",
        "description": "企业版是否启用多数据集概览功能"
    }
}


def init_system_configs(db):
    """初始化系统配置"""
    for key, config in DEFAULT_CONFIGS.items():
        existing = db.query(SystemConfig).filter(SystemConfig.config_key == key).first()
        if not existing:
            new_config = SystemConfig(
                config_key=key,
                config_value=config["value"],
                description=config["description"]
            )
            db.add(new_config)
    db.commit()
