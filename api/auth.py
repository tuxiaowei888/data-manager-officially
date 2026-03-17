"""
用户认证 API
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext

from config.database import get_db
from models.user import User
from models.channel import Channel
from schemas.auth import (
    UserRegister, UserLogin, Token, UserInfo, UserResponse
)
from schemas import ResponseModel

router = APIRouter(prefix="/api/v1/auth", tags=["用户认证"])

# JWT 配置
import os
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-3x4mpl3-k3y")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7天

# 密码加密
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user


def check_admin(current_user: User = Depends(get_current_user)) -> User:
    """检查是否为管理员"""
    if current_user.user_type != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user


@router.post("/register", response_model=UserResponse, summary="用户注册")
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    用户注册（可选填写推荐码）
    
    - **username**: 用户名（必填，3-50 字符）
    - **password**: 密码（必填，至少 6 字符）
    - **email**: 邮箱（可选）
    - **phone**: 手机号（可选）
    - **referrer_code**: 推荐码（可选，填写后自动绑定渠道）
    """
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已被注册"
        )
    
    # 如果填写了推荐码，查找对应的渠道
    channel_id = None
    if user_data.referrer_code:
        channel = db.query(Channel).filter(
            Channel.channel_code == user_data.referrer_code
        ).first()
        if channel:
            channel_id = channel.id
        else:
            # 推荐码无效，但不阻止注册
            pass
    
    # 创建新用户
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        password_hash=hashed_password,
        email=user_data.email,
        phone=user_data.phone,
        referrer_code=user_data.referrer_code,
        channel_id=channel_id,
        user_type="client"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # 如果绑定了渠道，增加渠道的推荐用户数
    if channel_id:
        channel = db.query(Channel).get(channel_id)
        if channel:
            channel.referred_users_count += 1
            db.commit()
    
    return UserResponse(
        code=200,
        message="注册成功",
        data=UserInfo(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            phone=new_user.phone,
            user_type=new_user.user_type,
            is_vip=new_user.is_vip,
            referrer_code=new_user.referrer_code,
            channel_id=new_user.channel_id,
            created_at=new_user.created_at
        )
    )


@router.post("/login", response_model=Token, summary="用户登录")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    用户登录
    
    - **username**: 用户名
    - **password**: 密码
    
    返回 JWT Token，用于后续请求的身份验证
    """
    # 查找用户
    user = db.query(User).filter(User.username == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 检查用户是否启用
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用"
        )
    
    # 更新最后登录时间
    user.last_login_at = datetime.utcnow()
    db.commit()
    
    # 生成访问令牌
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user_type=user.user_type,
        username=user.username
    )


@router.get("/me", response_model=UserResponse, summary="获取当前用户信息")
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前登录用户的信息
    
    需要在请求头中携带有效的 JWT Token：
    ```
    Authorization: Bearer <your_token>
    ```
    """
    # 获取渠道名称
    channel_name = None
    if current_user.channel_id:
        channel = db.query(Channel).filter(Channel.id == current_user.channel_id).first()
        if channel:
            channel_name = channel.channel_name
    
    return UserResponse(
        code=200,
        message="success",
        data=UserInfo(
            id=current_user.id,
            username=current_user.username,
            email=current_user.email,
            phone=current_user.phone,
            user_type=current_user.user_type,
            is_vip=current_user.is_vip,
            referrer_code=current_user.referrer_code,
            channel_id=current_user.channel_id,
            channel_name=channel_name,
            last_login_at=current_user.last_login_at,
            created_at=current_user.created_at
        )
    )


@router.post("/logout", response_model=ResponseModel, summary="用户登出")
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    用户登出
    
    客户端只需删除本地存储的 Token 即可
    """
    # 这里可以添加 Token 黑名单逻辑（可选）
    return ResponseModel(
        code=200,
        message="登出成功"
    )
