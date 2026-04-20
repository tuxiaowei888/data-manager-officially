"""
订阅权限装饰器 - 数维数据管家系统 V2.0
用于统一处理订阅层级相关的权限检查
"""
from functools import wraps
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional, Callable

from config.database import get_db
from models.user import User
from api.auth import get_current_user
from services.subscription_service import get_user_subscription_tier


def require_subscription_limit(
    max_datasets: Optional[int] = None,
    max_org_profiles: Optional[int] = None,
    error_message: str = "订阅层级限制，请升级订阅"
):
    """
    订阅限制装饰器
    
    Args:
        max_datasets: 最大数据集数量
        max_org_profiles: 最大企业档案数量
        error_message: 错误提示信息
        
    Usage:
        @router.post("/")
        @require_subscription_limit(max_datasets=3)
        async def create_dataset(...):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), **kwargs):
            tier = get_user_subscription_tier(current_user)
            
            # 检查数据集限制
            if max_datasets is not None:
                from models.dataset import Dataset
                dataset_count = db.query(Dataset).filter(
                    Dataset.user_id == current_user.id,
                    Dataset.is_active == True
                ).count()
                
                if dataset_count >= max_datasets:
                    raise HTTPException(
                        status_code=403,
                        detail=f"{error_message}（当前层级最多创建{max_datasets}个数据集）"
                    )
            
            # 检查企业档案限制
            if max_org_profiles is not None:
                from models.org_profile import OrgProfile
                profile_count = db.query(OrgProfile).filter(
                    OrgProfile.user_id == current_user.id,
                    OrgProfile.is_active == True
                ).count()
                
                if profile_count >= max_org_profiles:
                    raise HTTPException(
                        status_code=403,
                        detail=f"{error_message}（当前层级最多创建{max_org_profiles}个企业档案）"
                    )
            
            return await func(*args, db=db, current_user=current_user, **kwargs)
        return wrapper
    return decorator


def require_tier(required_tiers: list, error_message: str = "需要更高的订阅层级"):
    """
    订阅层级要求装饰器
    
    Args:
        required_tiers: 允许的订阅层级列表
        error_message: 错误提示信息
        
    Usage:
        @router.get("/premium")
        @require_tier(['pro', 'enterprise'])
        async def premium_feature(...):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), **kwargs):
            tier = get_user_subscription_tier(current_user)
            
            if tier not in required_tiers:
                tier_names = {
                    'free': '免费版',
                    'basic': '基础版',
                    'pro': '专业版',
                    'enterprise': '企业版'
                }
                required_names = ' 或 '.join([tier_names.get(t, t) for t in required_tiers])
                raise HTTPException(
                    status_code=403,
                    detail=f"{error_message}（需要{required_names}）"
                )
            
            return await func(*args, db=db, current_user=current_user, **kwargs)
        return wrapper
    return decorator


def check_duplicate_name(
    model_class,
    name_field: str = 'name',
    error_message: str = "名称已存在"
):
    """
    检查重复名称的装饰器
    
    Args:
        model_class: SQLAlchemy 模型类
        name_field: 名称字段名
        error_message: 错误提示信息
        
    Usage:
        @router.post("/")
        @check_duplicate_name(Dataset, name_field='name', error_message='数据集名称已存在')
        async def create_dataset(dataset_data: DatasetCreate, ...):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, db: Session = Depends(get_db), current_user: User = Depends(get_current_user), **kwargs):
            # 从参数中获取名称
            # 支持 DatasetCreate 等 Pydantic 模型或 dict
            request_data = kwargs.get('dataset_data') or kwargs.get('profile_data') or kwargs.get('data')
            
            if request_data and hasattr(request_data, name_field):
                name_value = getattr(request_data, name_field)
                
                # 检查是否重复
                existing = db.query(model_class).filter(
                    model_class.user_id == current_user.id,
                    getattr(model_class, name_field) == name_value
                ).first()
                
                if existing:
                    raise HTTPException(status_code=400, detail=error_message)
            
            return await func(*args, db=db, current_user=current_user, **kwargs)
        return wrapper
    return decorator
