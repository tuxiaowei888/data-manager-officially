"""
权限配置管理 API - 数维数据管家系统
提供普通用户和VIP用户权限配置
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from config.database import get_db
from api.auth import check_admin
from models.user import User

router = APIRouter(prefix="/api/v1/permissions", tags=["权限配置"])


class PermissionConfigResponse(BaseModel):
    id: int
    config_key: str
    config_value: str
    description: Optional[str]

    class Config:
        from_attributes = True


class PermissionConfigUpdate(BaseModel):
    config_key: Optional[str] = None
    config_value: str


class PermissionConfigBatchUpdate(BaseModel):
    configs: List[PermissionConfigUpdate]


class AllPermissionsResponse(BaseModel):
    user_permissions: dict
    vip_permissions: dict
    vip_defaults: dict


@router.get("", response_model=AllPermissionsResponse)
def get_all_permissions(db: Session = Depends(get_db)):
    """获取所有权限配置"""
    from models.system_config import SystemConfig

    configs = db.query(SystemConfig).all()
    config_dict = {c.config_key: c.config_value for c in configs}

    user_permissions = {
        "eval_limit": int(config_dict.get("user_eval_limit", 3)),
        "knowledge_view": config_dict.get("user_knowledge_view", "0") == "1",
        "report_view": config_dict.get("user_report_view", "1") == "1",
        "report_download": config_dict.get("user_report_download", "0") == "1",
    }

    vip_permissions = {
        "eval_limit": int(config_dict.get("vip_eval_limit", 30)),
        "knowledge_view": config_dict.get("vip_knowledge_view", "1") == "1",
        "report_download": config_dict.get("vip_report_download", "1") == "1",
        "priority_queue": config_dict.get("vip_priority_queue", "1") == "1",
        "report_save_limit": int(config_dict.get("vip_report_save_limit", 30)),
    }

    vip_defaults = {
        "monthly_days": int(config_dict.get("vip_default_monthly_days", 30)),
        "yearly_days": int(config_dict.get("vip_default_yearly_days", 365)),
        "expire_action": config_dict.get("vip_expire_action", "keep"),
        "renewal_reminder_days": int(config_dict.get("vip_renewal_reminder_days", 3)),
    }

    return {
        "user_permissions": user_permissions,
        "vip_permissions": vip_permissions,
        "vip_defaults": vip_defaults
    }


@router.get("/all", response_model=List[PermissionConfigResponse])
def get_all_configs(db: Session = Depends(get_db)):
    """获取所有配置项"""
    from models.system_config import SystemConfig

    configs = db.query(SystemConfig).all()
    return configs


@router.get("/{config_key}", response_model=PermissionConfigResponse)
def get_config(config_key: str, db: Session = Depends(get_db)):
    """获取单个配置"""
    from models.system_config import SystemConfig

    config = db.query(SystemConfig).filter(SystemConfig.config_key == config_key).first()
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    return config


@router.put("/{config_key}")
def update_config(
    config_key: str,
    config: PermissionConfigUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """更新单个配置"""
    from models.system_config import SystemConfig

    db_config = db.query(SystemConfig).filter(SystemConfig.config_key == config_key).first()
    if not db_config:
        raise HTTPException(status_code=404, detail="配置不存在")

    db_config.config_value = config.config_value
    db.commit()

    return {"success": True, "message": f"配置 {config_key} 已更新"}


@router.put("/batch")
def update_configs_batch(
    configs: PermissionConfigBatchUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """批量更新配置"""
    from models.system_config import SystemConfig

    updated_keys = []
    for item in configs.configs:
        db_config = db.query(SystemConfig).filter(SystemConfig.config_key == item.config_key).first()
        if db_config:
            db_config.config_value = item.config_value
            updated_keys.append(item.config_key)

    db.commit()

    return {"success": True, "message": f"已更新 {len(updated_keys)} 个配置项", "updated": updated_keys}


@router.post("/init-defaults")
def init_default_permissions(
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """初始化默认权限配置"""
    from models.system_config import SystemConfig

    default_configs = [
        ("user_eval_limit", "3", "普通用户每月评估次数"),
        ("user_knowledge_view", "0", "普通用户知识库查看权限"),
        ("user_report_view", "1", "普通用户报告查看权限"),
        ("user_report_download", "0", "普通用户报告下载权限"),
        ("vip_eval_limit", "30", "VIP用户每月评估次数"),
        ("vip_knowledge_view", "1", "VIP知识库查看权限"),
        ("vip_report_download", "1", "VIP报告下载权限"),
        ("vip_priority_queue", "1", "VIP优先队列权限"),
        ("vip_report_save_limit", "30", "VIP历史报告保存数"),
        ("vip_default_monthly_days", "30", "月度VIP默认天数"),
        ("vip_default_yearly_days", "365", "年度VIP默认天数"),
        ("vip_expire_action", "keep", "VIP到期处理策略"),
        ("vip_renewal_reminder_days", "3", "VIP续费提醒天数"),
    ]

    created = []
    for key, value, desc in default_configs:
        existing = db.query(SystemConfig).filter(SystemConfig.config_key == key).first()
        if not existing:
            config = SystemConfig(config_key=key, config_value=value, description=desc)
            db.add(config)
            created.append(key)

    db.commit()

    return {"success": True, "message": f"已创建 {len(created)} 个默认配置项", "created": created}