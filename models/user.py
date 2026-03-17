from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from datetime import datetime

from config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), nullable=True)
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

    channel = relationship("Channel", back_populates="users")
