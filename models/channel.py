"""
渠道模型
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from config.database import Base


class Channel(Base):
    """渠道表"""
    __tablename__ = "channels"
    
    id = Column(Integer, primary_key=True, index=True, comment="渠道 ID")
    channel_name = Column(String(100), nullable=False, comment="渠道名称")
    channel_code = Column(String(20), unique=True, nullable=False, index=True, comment="推荐码")
    contact_person = Column(String(50), comment="联系人")
    contact_phone = Column(String(20), comment="联系电话")
    referred_users_count = Column(Integer, default=0, comment="推荐用户总数")
    is_active = Column(Boolean, default=True, comment="是否启用")
    remark = Column(Text, comment="备注")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关联用户
    users = relationship("User", back_populates="channel")
