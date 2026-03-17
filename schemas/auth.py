"""
用户认证 Schema
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserRegister(BaseModel):
    """用户注册请求"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, max_length=100, description="密码")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    referrer_code: Optional[str] = Field(None, max_length=20, description="推荐码")


class UserLogin(BaseModel):
    """用户登录请求"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")


class Token(BaseModel):
    """访问令牌"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600
    user_type: Optional[str] = "client"
    username: Optional[str] = None


class TokenData(BaseModel):
    """Token 数据"""
    username: Optional[str] = None
    user_id: Optional[int] = None


class UserInfo(BaseModel):
    """用户信息响应"""
    id: int
    username: str
    email: Optional[str] = None
    phone: Optional[str] = None
    user_type: str
    is_vip: bool
    referrer_code: Optional[str] = None
    channel_id: Optional[int] = None
    channel_name: Optional[str] = None
    last_login_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """用户响应"""
    code: int = 200
    message: str = "success"
    data: Optional[UserInfo] = None
