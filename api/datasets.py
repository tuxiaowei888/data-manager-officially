"""
数据集管理 API - 数维数据管家系统 V2.0
支持用户创建和管理数据集，作为 2 层评估结构的第一层
"""
from fastapi import APIRouter, HTTPException, Depends, Query, Body
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from config.database import get_db
from models.user import User
from models.dataset import Dataset
from models.evaluation_result import EvaluationResult
from api.auth import get_current_user
from schemas import ResponseModel
from services.subscription_decorators import require_subscription_limit, check_duplicate_name

router = APIRouter(prefix="/api/v1/datasets", tags=["数据集管理"])


class DatasetCreate(BaseModel):
    """创建数据集请求模型"""
    name: str
    dataset_type: str = "general"
    data_volume: Optional[str] = None
    data_format: Optional[str] = None
    security_level: Optional[str] = None
    description: Optional[str] = None


class DatasetUpdate(BaseModel):
    """更新数据集请求模型"""
    name: Optional[str] = None
    dataset_type: Optional[str] = None
    data_volume: Optional[str] = None
    data_format: Optional[str] = None
    security_level: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class DatasetResponse(BaseModel):
    """数据集响应模型"""
    id: int
    user_id: int
    name: str
    dataset_type: str
    data_volume: Optional[str]
    data_format: Optional[str]
    security_level: Optional[str]
    description: Optional[str]
    is_active: bool
    created_at: str
    updated_at: Optional[str]
    
    # 关联信息
    evaluation_count: int = 0
    latest_evaluation: Optional[Dict[str, Any]] = None


class DatasetStats(BaseModel):
    """数据集统计信息"""
    total_datasets: int
    active_datasets: int
    evaluations_by_dataset: Dict[str, int]


@router.post("/", response_model=ResponseModel[DatasetResponse])
@require_subscription_limit(max_datasets=3, error_message="订阅层级限制")
@check_duplicate_name(Dataset, name_field='name', error_message="数据集名称已存在")
async def create_dataset(
    dataset_data: DatasetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新数据集"""
    # 订阅限制检查已由装饰器处理
    
    # 创建数据集
    dataset = Dataset(
        user_id=current_user.id,
        name=dataset_data.name,
        dataset_type=dataset_data.dataset_type,
        data_volume=dataset_data.data_volume,
        data_format=dataset_data.data_format,
        security_level=dataset_data.security_level,
        description=dataset_data.description,
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    
    return ResponseModel(
        code=200,
        message="数据集创建成功",
        data=dataset_to_response(dataset, db)
    )


@router.get("/", response_model=ResponseModel[List[DatasetResponse]])
async def list_datasets(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    active_only: bool = Query(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户的数据集列表"""
    query = db.query(Dataset).filter(Dataset.user_id == current_user.id)
    
    if active_only:
        query = query.filter(Dataset.is_active == True)
    
    datasets = query.order_by(desc(Dataset.created_at)).offset(skip).limit(limit).all()
    
    # 转换为响应模型
    dataset_responses = [dataset_to_response(dataset, db) for dataset in datasets]
    
    return ResponseModel(
        code=200,
        message="获取成功",
        data=dataset_responses
    )


@router.get("/{dataset_id}", response_model=ResponseModel[DatasetResponse])
async def get_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取数据集详情"""
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.user_id == current_user.id
    ).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="数据集不存在或无权访问")
    
    return ResponseModel(
        code=200,
        message="获取成功",
        data=dataset_to_response(dataset, db)
    )


@router.put("/{dataset_id}", response_model=ResponseModel[DatasetResponse])
async def update_dataset(
    dataset_id: int,
    update_data: DatasetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新数据集信息"""
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.user_id == current_user.id
    ).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="数据集不存在或无权访问")
    
    # 更新字段
    update_dict = update_data.dict(exclude_unset=True)
    if 'name' in update_dict and update_dict['name'] != dataset.name:
        # 检查名称是否重复
        existing = db.query(Dataset).filter(
            Dataset.user_id == current_user.id,
            Dataset.name == update_dict['name'],
            Dataset.id != dataset_id
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="数据集名称已存在")
    
    for key, value in update_dict.items():
        if value is not None:
            setattr(dataset, key, value)
    
    dataset.updated_at = datetime.now()
    db.commit()
    db.refresh(dataset)
    
    return ResponseModel(
        code=200,
        message="数据集更新成功",
        data=dataset_to_response(dataset, db)
    )


@router.delete("/{dataset_id}", response_model=ResponseModel)
async def delete_dataset(
    dataset_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除数据集（软删除）"""
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.user_id == current_user.id
    ).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="数据集不存在或无权访问")
    
    # 检查是否有评估记录
    eval_count = db.query(EvaluationResult).filter(
        EvaluationResult.dataset_id == dataset_id
    ).count()
    
    if eval_count > 0:
        # 有评估记录，软删除
        dataset.is_active = False
        dataset.updated_at = datetime.now()
        message = "数据集已禁用（存在评估记录）"
    else:
        # 无评估记录，物理删除
        db.delete(dataset)
        message = "数据集已删除"
    
    db.commit()
    
    return ResponseModel(
        code=200,
        message=message,
        data=None
    )


@router.get("/{dataset_id}/evaluations", response_model=ResponseModel[List[Dict[str, Any]]])
async def get_dataset_evaluations(
    dataset_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取数据集的评估记录"""
    # 验证数据集权限
    dataset = db.query(Dataset).filter(
        Dataset.id == dataset_id,
        Dataset.user_id == current_user.id
    ).first()
    
    if not dataset:
        raise HTTPException(status_code=404, detail="数据集不存在或无权访问")
    
    # 获取评估记录
    evaluations = db.query(EvaluationResult).filter(
        EvaluationResult.dataset_id == dataset_id
    ).order_by(desc(EvaluationResult.created_at)).offset(skip).limit(limit).all()
    
    # 转换为响应格式
    eval_list = []
    for eval_result in evaluations:
        eval_list.append({
            'id': eval_result.id,
            'report_id': eval_result.report_id,
            'total_score': eval_result.total_score,
            'risk_level': eval_result.risk_level,
            'created_at': eval_result.created_at.isoformat() if eval_result.created_at else None,
            'org_profile_id': eval_result.org_profile_id,
            'subscription_tier': eval_result.subscription_tier
        })
    
    return ResponseModel(
        code=200,
        message="获取成功",
        data=eval_list
    )


@router.get("/stats/summary", response_model=ResponseModel[DatasetStats])
async def get_dataset_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取数据集统计摘要"""
    # 统计数据集数量
    total_datasets = db.query(Dataset).filter(Dataset.user_id == current_user.id).count()
    active_datasets = db.query(Dataset).filter(
        Dataset.user_id == current_user.id,
        Dataset.is_active == True
    ).count()
    
    # 统计各数据集的评估数量
    datasets = db.query(Dataset).filter(Dataset.user_id == current_user.id).all()
    evaluations_by_dataset = {}
    
    for dataset in datasets:
        eval_count = db.query(EvaluationResult).filter(
            EvaluationResult.dataset_id == dataset.id
        ).count()
        
        evaluations_by_dataset[dataset.name] = eval_count
    
    stats = DatasetStats(
        total_datasets=total_datasets,
        active_datasets=active_datasets,
        evaluations_by_dataset=evaluations_by_dataset
    )
    
    return ResponseModel(
        code=200,
        message="获取成功",
        data=stats
    )


def dataset_to_response(dataset: Dataset, db: Session) -> DatasetResponse:
    """将Dataset对象转换为响应模型"""
    # 获取评估统计
    evaluation_count = db.query(EvaluationResult).filter(
        EvaluationResult.dataset_id == dataset.id
    ).count()
    
    latest_evaluation = None
    if evaluation_count > 0:
        latest = db.query(EvaluationResult).filter(
            EvaluationResult.dataset_id == dataset.id
        ).order_by(desc(EvaluationResult.created_at)).first()
        
        if latest:
            latest_evaluation = {
                'id': latest.id,
                'report_id': latest.report_id,
                'total_score': latest.total_score,
                'risk_level': latest.risk_level,
                'created_at': latest.created_at.isoformat() if latest.created_at else None
            }
    
    return DatasetResponse(
        id=dataset.id,
        user_id=dataset.user_id,
        name=dataset.name,
        dataset_type=dataset.dataset_type,
        data_volume=dataset.data_volume,
        data_format=dataset.data_format,
        security_level=dataset.security_level,
        description=dataset.description,
        is_active=dataset.is_active,
        created_at=dataset.created_at.isoformat() if dataset.created_at else None,
        updated_at=dataset.updated_at.isoformat() if dataset.updated_at else None,
        evaluation_count=evaluation_count,
        latest_evaluation=latest_evaluation
    )