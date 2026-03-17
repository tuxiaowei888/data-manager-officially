"""
渠道管理 API
"""
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from models.channel import Channel
from models.user import User
from schemas.channel import ChannelCreate, ChannelUpdate, ChannelResponse, ChannelListResponse

router = APIRouter(prefix="/api/v1/channels", tags=["渠道管理"])


@router.get("", response_model=ChannelListResponse, summary="获取所有渠道列表")
async def get_all_channels(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取所有渠道列表
    
    - **skip**: 跳过记录数（分页）
    - **limit**: 返回记录数（默认 100）
    """
    channels = db.query(Channel).offset(skip).limit(limit).all()
    total = db.query(Channel).count()
    
    return ChannelListResponse(
        code=200,
        message="success",
        data=[
            {
                "id": c.id,
                "channel_name": c.channel_name,
                "channel_code": c.channel_code,
                "contact_person": c.contact_person,
                "contact_phone": c.contact_phone,
                "referred_users_count": c.referred_users_count,
                "is_active": c.is_active,
                "created_at": c.created_at
            }
            for c in channels
        ],
        total=total
    )


@router.get("/{channel_id}", response_model=ChannelResponse, summary="获取渠道详情")
async def get_channel(
    channel_id: int,
    db: Session = Depends(get_db)
):
    """
    根据 ID 获取渠道详细信息
    """
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="渠道不存在"
        )
    
    return ChannelResponse(
        code=200,
        message="success",
        data={
            "id": channel.id,
            "channel_name": channel.channel_name,
            "channel_code": channel.channel_code,
            "contact_person": channel.contact_person,
            "contact_phone": channel.contact_phone,
            "referred_users_count": channel.referred_users_count,
            "is_active": channel.is_active,
            "created_at": channel.created_at
        }
    )


@router.post("", response_model=ChannelResponse, summary="创建新渠道")
async def create_channel(
    channel_data: ChannelCreate,
    db: Session = Depends(get_db)
):
    """
    创建新的渠道
    
    - **channel_name**: 渠道名称（必填）
    - **channel_code**: 渠道推荐码（必填，唯一）
    - **contact_person**: 联系人（可选）
    - **contact_phone**: 联系电话（可选）
    """
    # 检查推荐码是否已存在
    existing = db.query(Channel).filter(
        Channel.channel_code == channel_data.channel_code
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="推荐码已存在"
        )
    
    # 创建新渠道
    new_channel = Channel(
        channel_name=channel_data.channel_name,
        channel_code=channel_data.channel_code,
        contact_person=channel_data.contact_person,
        contact_phone=channel_data.contact_phone,
        is_active=True
    )
    
    db.add(new_channel)
    db.commit()
    db.refresh(new_channel)
    
    return ChannelResponse(
        code=201,
        message="渠道创建成功",
        data={
            "id": new_channel.id,
            "channel_name": new_channel.channel_name,
            "channel_code": new_channel.channel_code,
            "contact_person": new_channel.contact_person,
            "contact_phone": new_channel.contact_phone,
            "referred_users_count": new_channel.referred_users_count,
            "is_active": new_channel.is_active,
            "created_at": new_channel.created_at
        }
    )


@router.put("/{channel_id}", response_model=ChannelResponse, summary="更新渠道信息")
async def update_channel(
    channel_id: int,
    channel_data: ChannelUpdate,
    db: Session = Depends(get_db)
):
    """
    更新渠道信息
    
    可以更新：
    - 渠道名称
    - 联系人
    - 联系电话
    - 是否启用
    """
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="渠道不存在"
        )
    
    # 更新字段
    if channel_data.channel_name is not None:
        channel.channel_name = channel_data.channel_name
    if channel_data.contact_person is not None:
        channel.contact_person = channel_data.contact_person
    if channel_data.contact_phone is not None:
        channel.contact_phone = channel_data.contact_phone
    if channel_data.is_active is not None:
        channel.is_active = channel_data.is_active
    
    db.commit()
    db.refresh(channel)
    
    return ChannelResponse(
        code=200,
        message="渠道更新成功",
        data={
            "id": channel.id,
            "channel_name": channel.channel_name,
            "channel_code": channel.channel_code,
            "contact_person": channel.contact_person,
            "contact_phone": channel.contact_phone,
            "referred_users_count": channel.referred_users_count,
            "is_active": channel.is_active,
            "created_at": channel.created_at
        }
    )


@router.delete("/{channel_id}", response_model=ChannelResponse, summary="删除渠道")
async def delete_channel(
    channel_id: int,
    db: Session = Depends(get_db)
):
    """
    删除渠道（软删除，禁用渠道）
    """
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="渠道不存在"
        )
    
    # 检查是否有推荐用户
    if channel.referred_users_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"该渠道已有{channel.referred_users_count}个推荐用户，无法删除"
        )
    
    # 禁用渠道
    channel.is_active = False
    db.commit()
    
    return ChannelResponse(
        code=200,
        message="渠道已删除",
        data={
            "id": channel.id,
            "channel_name": channel.channel_name,
            "channel_code": channel.channel_code,
            "contact_person": channel.contact_person,
            "contact_phone": channel.contact_phone,
            "referred_users_count": channel.referred_users_count,
            "is_active": channel.is_active,
            "created_at": channel.created_at
        }
    )


@router.get("/{channel_id}/users", response_model=ChannelListResponse, summary="获取渠道推荐的用户列表")
async def get_channel_users(
    channel_id: int,
    db: Session = Depends(get_db)
):
    """
    获取该渠道推荐的所有用户列表
    """
    channel = db.query(Channel).filter(Channel.id == channel_id).first()
    
    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="渠道不存在"
        )
    
    users = db.query(User).filter(User.channel_id == channel_id).all()
    
    return ChannelListResponse(
        code=200,
        message="success",
        data=[
            {
                "id": u.id,
                "username": u.username,
                "email": u.email,
                "phone": u.phone,
                "referrer_code": u.referrer_code,
                "user_type": u.user_type,
                "is_vip": u.is_vip,
                "created_at": u.created_at
            }
            for u in users
        ],
        total=len(users)
    )
