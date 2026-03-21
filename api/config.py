"""
系统配置 API - 管理员专用
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from config.database import get_db
from models.user import User
from models.system_config import SystemConfig, init_system_configs
from api.auth import get_current_user
from schemas import ResponseModel

router = APIRouter(prefix="/api/v1/config", tags=["系统配置"])


class ConfigItem(BaseModel):
    key: str
    value: str
    description: Optional[str] = None


class VipLimitsUpdate(BaseModel):
    free_daily_eval_limit: Optional[int] = None
    vip_default_days: Optional[int] = None
    free_report_retention_days: Optional[int] = None
    vip_report_retention_days: Optional[int] = None
    enable_vip_export: Optional[bool] = None


def check_admin(current_user: User = Depends(get_current_user)):
    """检查是否为管理员"""
    if current_user.user_type != 'admin':
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return current_user


def get_config_value(db: Session, key: str, default: str) -> str:
    """获取配置值"""
    config = db.query(SystemConfig).filter(SystemConfig.config_key == key).first()
    return config.config_value if config else default


@router.get("", response_model=List[ConfigItem])
async def get_all_configs(
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """获取所有系统配置"""
    init_system_configs(db)
    
    configs = db.query(SystemConfig).all()
    
    return [
        ConfigItem(
            key=c.config_key,
            value=c.config_value or "",
            description=c.description
        )
        for c in configs
    ]


@router.get("/vip/limits", response_model=dict)
async def get_vip_limits(
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """获取VIP限制配置"""
    return {
        "free_daily_eval_limit": int(get_config_value(db, "free_daily_eval_limit", "3")),
        "vip_default_days": int(get_config_value(db, "vip_default_days", "30")),
        "free_report_retention_days": int(get_config_value(db, "free_report_retention_days", "7")),
        "vip_report_retention_days": int(get_config_value(db, "vip_report_retention_days", "36500")),
        "enable_vip_export": get_config_value(db, "enable_vip_export", "true").lower() == "true"
    }


@router.put("/vip/limits", response_model=ResponseModel)
async def update_vip_limits(
    data: VipLimitsUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """更新VIP限制配置"""
    mappings = {
        "free_daily_eval_limit": data.free_daily_eval_limit,
        "vip_default_days": data.vip_default_days,
        "free_report_retention_days": data.free_report_retention_days,
        "vip_report_retention_days": data.vip_report_retention_days,
        "enable_vip_export": data.enable_vip_export
    }
    
    for key, value in mappings.items():
        if value is None:
            continue
        
        config = db.query(SystemConfig).filter(SystemConfig.config_key == key).first()
        if config:
            if isinstance(value, bool):
                config.config_value = "true" if value else "false"
            else:
                config.config_value = str(value)
    
    db.commit()
    
    return ResponseModel(status="success", message="配置已更新")


@router.put("/{key}", response_model=ConfigItem)
async def update_config(
    key: str,
    value: str,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """更新单个配置项"""
    config = db.query(SystemConfig).filter(SystemConfig.config_key == key).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="配置项不存在")
    
    config.config_value = value
    db.commit()
    db.refresh(config)
    
    return ConfigItem(
        key=config.config_key,
        value=config.config_value or "",
        description=config.description
    )
