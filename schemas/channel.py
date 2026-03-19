"""
渠道管理 Schema
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class ChannelCreate(BaseModel):
    """创建渠道请求"""
    channel_name: str = Field(..., min_length=1, max_length=100, description="渠道名称")
    channel_code: str = Field(..., min_length=1, max_length=20, description="渠道推荐码")
    contact_person: Optional[str] = Field(None, max_length=50, description="联系人")
    contact_phone: Optional[str] = Field(None, max_length=20, description="联系电话")


class ChannelUpdate(BaseModel):
    """更新渠道请求"""
    channel_name: Optional[str] = Field(None, max_length=100, description="渠道名称")
    contact_person: Optional[str] = Field(None, max_length=50, description="联系人")
    contact_phone: Optional[str] = Field(None, max_length=20, description="联系电话")
    is_active: Optional[bool] = Field(None, description="是否启用")


class ChannelData(BaseModel):
    """渠道数据"""
    id: int
    channel_name: str
    channel_code: str
    contact_person: Optional[str]
    contact_phone: Optional[str]
    referred_users_count: int = 0
    is_active: bool = True
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChannelResponse(BaseModel):
    """渠道响应"""
    code: int = 200
    message: str = "success"
    data: Optional[ChannelData] = None


class ChannelListResponse(BaseModel):
    """渠道列表响应"""
    code: int = 200
    message: str = "success"
    data: list = []
    total: int = 0
