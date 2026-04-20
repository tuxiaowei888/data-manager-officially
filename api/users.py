"""
用户管理 API - 管理员专用
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from config.database import get_db
from models.user import User
from api.auth import get_current_user, get_password_hash
from schemas import ResponseModel

router = APIRouter(prefix="/api/v1/users", tags=["用户管理"])


class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    phone: Optional[str] = None
    user_type: str = "client"


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    user_type: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: Optional[str]
    phone: Optional[str]
    user_type: str
    is_vip: bool
    vip_expire_date: Optional[str] = None
    is_active: bool
    daily_eval_count: int = 0
    created_at: Optional[str]


class VipSetRequest(BaseModel):
    days: int = 30


def check_admin(current_user: User = Depends(get_current_user)):
    """检查是否为管理员"""
    if current_user.user_type != 'admin':
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return current_user


@router.get("")
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """
    获取用户列表
    
    - **skip**: 跳过前N条记录（默认0）
    - **limit**: 返回最大记录数（默认100，最大1000）
    """
    # 限制最大返回数量
    limit = min(limit, 1000)
    
    # 获取总数
    total = db.query(User).count()
    
    # 获取分页数据
    users = db.query(User).order_by(User.id.asc()).offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": [
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "phone": u.phone,
                "user_type": u.user_type,
                "is_vip": u.is_vip,
                "vip_expire_date": u.vip_expire_date.strftime('%Y-%m-%d') if u.vip_expire_date else None,
                "is_active": u.is_active,
                "daily_eval_count": u.daily_eval_count or 0,
                "created_at": u.created_at.strftime('%Y-%m-%d %H:%M') if u.created_at else None
            }
            for u in users
        ]
    }


@router.post("", response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """创建用户"""
    existing = db.query(User).filter(User.username == user_data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    new_user = User(
        username=user_data.username,
        password_hash=get_password_hash(user_data.password),
        email=user_data.email,
        phone=user_data.phone,
        user_type=user_data.user_type,
        is_active=True
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        phone=new_user.phone,
        user_type=new_user.user_type,
        is_vip=new_user.is_vip,
        is_active=new_user.is_active,
        created_at=new_user.created_at.strftime('%Y-%m-%d %H:%M') if new_user.created_at else None
    )


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """更新用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if user_data.username:
        user.username = user_data.username
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.phone is not None:
        user.phone = user_data.phone
    if user_data.user_type:
        user.user_type = user_data.user_type
    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)
    
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        phone=user.phone,
        user_type=user.user_type,
        is_vip=user.is_vip,
        is_active=user.is_active,
        created_at=user.created_at.strftime('%Y-%m-%d %H:%M') if user.created_at else None
    )


@router.post("/{user_id}/toggle", response_model=ResponseModel)
async def toggle_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """启用/禁用用户"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="不能禁用自己的账号")
    
    user.is_active = not user.is_active
    db.commit()
    
    return ResponseModel(
        code=200,
        message=f"用户已{'启用' if user.is_active else '禁用'}"
    )


@router.delete("/{user_id}", response_model=ResponseModel)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """删除用户"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="不能删除自己的账号")
    
    db.delete(user)
    db.commit()
    
    return ResponseModel(status="success", message="用户已删除")


@router.post("/{user_id}/vip", response_model=ResponseModel)
async def set_user_vip(
    user_id: int,
    data: VipSetRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """设置用户VIP"""
    from services.vip_service import set_user_vip as set_vip
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    set_vip(user, data.days, db)
    
    return ResponseModel(
        status="success",
        message=f"已为用户 {user.username} 开通VIP {data.days} 天"
    )


@router.delete("/{user_id}/vip", response_model=ResponseModel)
async def revoke_user_vip(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """取消用户VIP"""
    try:
        from services.vip_service import revoke_user_vip as revoke_vip_func

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")

        revoke_vip_func(user, db)

        return ResponseModel(
            status="success",
            message=f"已取消用户 {user.username} 的VIP"
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"取消VIP失败: {str(e)}")
