from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from config.database import Base


class User(Base):
    __tablename__ = "users"

    # 添加唯一约束：邮箱必须唯一（允许NULL）
    __table_args__ = (
        UniqueConstraint('email', name='idx_email_unique'),
    )

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), nullable=True, unique=True)
    phone = Column(String(20), nullable=True)
    referrer_code = Column(String(20), nullable=True, index=True)
    channel_id = Column(Integer, ForeignKey('channels.id'), nullable=True, index=True)
    user_type = Column(String(20), default='client')
    is_vip = Column(Boolean, default=False)
    vip_expire_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    daily_eval_count = Column(Integer, default=0)
    daily_eval_date = Column(Date, nullable=True)
    
    # 新增订阅相关字段
    subscription_tier = Column(String(20), default='free', comment='订阅档位：free/basic/pro/enterprise')
    subscription_start_date = Column(Date, nullable=True, comment='订阅开始日期')
    eval_count_used = Column(Integer, default=0, comment='本年度已使用评估次数')
    eval_count_reset_date = Column(Date, nullable=True, comment='评估次数重置日期')
    
    # 客户分层信号
    customer_tier_signal = Column(Integer, default=0, comment='客户分层信号分')
    customer_tier_label = Column(String(20), default='observer', comment='客户分层：high_value/nurturing/observer')
    last_signal_update = Column(DateTime, nullable=True, comment='信号分最后更新时间')

    channel = relationship("Channel", back_populates="users")
    
    @property
    def effective_subscription_tier(self):
        """获取有效的订阅档位（兼容旧is_vip字段）"""
        # 如果subscription_tier已设置，使用它
        if self.subscription_tier and self.subscription_tier != 'free':
            return self.subscription_tier
        
        # 否则根据is_vip判断
        if self.is_vip and self.vip_expire_date and self.vip_expire_date >= datetime.utcnow().date():
            return 'basic'  # 旧VIP用户默认映射为基础版
        return 'free'
    
    @property
    def is_subscription_active(self):
        """检查订阅是否有效"""
        if self.subscription_tier == 'free':
            return True  # 免费用户始终有效
            
        if self.subscription_start_date and self.vip_expire_date:
            # 检查VIP过期日期（兼容旧逻辑）
            return self.vip_expire_date >= datetime.utcnow().date()
            
        # 如果没有设置过期日期，检查订阅开始日期（假设年付）
        if self.subscription_start_date:
            # 假设订阅有效期为1年
            from datetime import timedelta
            expiry_date = self.subscription_start_date + timedelta(days=365)
            return expiry_date >= datetime.utcnow().date()
            
        return False
