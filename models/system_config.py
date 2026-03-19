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
