"""
企业档案管理 API - 数维数据管家系统 V2.0
支持用户创建和管理企业档案，作为 2 层评估结构的第二层
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from config.database import get_db
from models.user import User
from models.org_profile import OrgProfile
from models.evaluation_result import EvaluationResult
from models.dataset import Dataset
from api.auth import get_current_user
from schemas import ResponseModel
from services.subscription_decorators import require_subscription_limit, check_duplicate_name

router = APIRouter(prefix="/api/v1/org-profiles", tags=["企业档案管理"])


class OrgProfileCreate(BaseModel):
    """创建企业档案请求模型"""
    company_name: str
    industry: Optional[str] = None
    company_size: Optional[str] = None
    annual_revenue: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    compliance_certifications: Optional[str] = None
    description: Optional[str] = None


class OrgProfileUpdate(BaseModel):
    """更新企业档案请求模型"""
    company_name: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    annual_revenue: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    compliance_certifications: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class OrgProfileResponse(BaseModel):
    """企业档案响应模型"""
    id: int
    user_id: int
    company_name: str
    industry: Optional[str]
    company_size: Optional[str]
    annual_revenue: Optional[str]
    contact_person: Optional[str]
    contact_email: Optional[str]
    contact_phone: Optional[str]
    address: Optional[str]
    website: Optional[str]
    compliance_certifications: Optional[str]
    description: Optional[str]
    is_active: bool
    created_at: str
    updated_at: Optional[str]
    
    # 关联信息
    evaluation_count: int = 0
    dataset_count: int = 0
    latest_evaluation: Optional[Dict[str, Any]] = None


class OrgProfileStats(BaseModel):
    """企业档案统计信息"""
    total_profiles: int
    active_profiles: int
    evaluations_by_profile: Dict[str, int]
    datasets_by_profile: Dict[str, int]


@router.post("/", response_model=ResponseModel[OrgProfileResponse])
@require_subscription_limit(max_org_profiles=1, error_message="订阅层级限制")
@check_duplicate_name(OrgProfile, name_field='company_name', error_message="企业名称已存在")
async def create_org_profile(
    profile_data: OrgProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新企业档案"""
    # 订阅限制检查已由装饰器处理
    
    # 创建企业档案
    profile = OrgProfile(
        user_id=current_user.id,
        company_name=profile_data.company_name,
        industry=profile_data.industry,
        company_size=profile_data.company_size,
        annual_revenue=profile_data.annual_revenue,
        contact_person=profile_data.contact_person,
        contact_email=profile_data.contact_email,
        contact_phone=profile_data.contact_phone,
        address=profile_data.address,
        website=profile_data.website,
        compliance_certifications=profile_data.compliance_certifications,
        description=profile_data.description,
        is_active=True,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    
    db.add(profile)
    db.commit()
    db.refresh(profile)
    
    return ResponseModel(
        code=200,
        message="企业档案创建成功",
        data=org_profile_to_response(profile, db)
    )


@router.get("/", response_model=ResponseModel[List[OrgProfileResponse]])
async def list_org_profiles(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    active_only: bool = Query(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户的企业档案列表"""
    query = db.query(OrgProfile).filter(OrgProfile.user_id == current_user.id)
    
    if active_only:
        query = query.filter(OrgProfile.is_active == True)
    
    profiles = query.order_by(desc(OrgProfile.created_at)).offset(skip).limit(limit).all()
    
    # 转换为响应模型
    profile_responses = [org_profile_to_response(profile, db) for profile in profiles]
    
    return ResponseModel(
        code=200,
        message="获取成功",
        data=profile_responses
    )


@router.get("/{profile_id}", response_model=ResponseModel[OrgProfileResponse])
async def get_org_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取企业档案详情"""
    profile = db.query(OrgProfile).filter(
        OrgProfile.id == profile_id,
        OrgProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="企业档案不存在或无权访问")
    
    return ResponseModel(
        code=200,
        message="获取成功",
        data=org_profile_to_response(profile, db)
    )


@router.put("/{profile_id}", response_model=ResponseModel[OrgProfileResponse])
async def update_org_profile(
    profile_id: int,
    update_data: OrgProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新企业档案信息"""
    profile = db.query(OrgProfile).filter(
        OrgProfile.id == profile_id,
        OrgProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="企业档案不存在或无权访问")
    
    # 更新字段
    update_dict = update_data.dict(exclude_unset=True)
    if 'company_name' in update_dict and update_dict['company_name'] != profile.company_name:
        # 检查名称是否重复
        existing = db.query(OrgProfile).filter(
            OrgProfile.user_id == current_user.id,
            OrgProfile.company_name == update_dict['company_name'],
            OrgProfile.id != profile_id
        ).first()
        
        if existing:
            raise HTTPException(status_code=400, detail="企业名称已存在")
    
    for key, value in update_dict.items():
        if value is not None:
            setattr(profile, key, value)
    
    profile.updated_at = datetime.now()
    db.commit()
    db.refresh(profile)
    
    return ResponseModel(
        code=200,
        message="企业档案更新成功",
        data=org_profile_to_response(profile, db)
    )


@router.delete("/{profile_id}", response_model=ResponseModel)
async def delete_org_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除企业档案（软删除）"""
    profile = db.query(OrgProfile).filter(
        OrgProfile.id == profile_id,
        OrgProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="企业档案不存在或无权访问")
    
    # 检查是否有评估记录
    eval_count = db.query(EvaluationResult).filter(
        EvaluationResult.org_profile_id == profile_id
    ).count()
    
    # 检查是否有关联的数据集
    dataset_count = db.query(Dataset).filter(
        Dataset.org_profile_id == profile_id
    ).count()
    
    if eval_count > 0 or dataset_count > 0:
        # 有评估记录或数据集，软删除
        profile.is_active = False
        profile.updated_at = datetime.now()
        message = "企业档案已禁用（存在关联记录）"
    else:
        # 无关联记录，物理删除
        db.delete(profile)
        message = "企业档案已删除"
    
    db.commit()
    
    return ResponseModel(
        code=200,
        message=message,
        data=None
    )


@router.get("/{profile_id}/evaluations", response_model=ResponseModel[List[Dict[str, Any]]])
async def get_org_profile_evaluations(
    profile_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取企业档案的评估记录"""
    # 验证企业档案权限
    profile = db.query(OrgProfile).filter(
        OrgProfile.id == profile_id,
        OrgProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="企业档案不存在或无权访问")
    
    # 获取评估记录
    evaluations = db.query(EvaluationResult).filter(
        EvaluationResult.org_profile_id == profile_id
    ).order_by(desc(EvaluationResult.created_at)).offset(skip).limit(limit).all()
    
    # 转换为响应格式
    eval_list = []
    for eval_result in evaluations:
        # 获取数据集信息
        dataset_name = None
        if eval_result.dataset_id:
            dataset = db.query(Dataset).filter(Dataset.id == eval_result.dataset_id).first()
            dataset_name = dataset.name if dataset else None
        
        eval_list.append({
            'id': eval_result.id,
            'report_id': eval_result.report_id,
            'total_score': eval_result.total_score,
            'risk_level': eval_result.risk_level,
            'created_at': eval_result.created_at.isoformat() if eval_result.created_at else None,
            'dataset_id': eval_result.dataset_id,
            'dataset_name': dataset_name,
            'subscription_tier': eval_result.subscription_tier
        })
    
    return ResponseModel(
        code=200,
        message="获取成功",
        data=eval_list
    )


@router.get("/{profile_id}/datasets", response_model=ResponseModel[List[Dict[str, Any]]])
async def get_org_profile_datasets(
    profile_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取企业档案关联的数据集"""
    # 验证企业档案权限
    profile = db.query(OrgProfile).filter(
        OrgProfile.id == profile_id,
        OrgProfile.user_id == current_user.id
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="企业档案不存在或无权访问")
    
    # 获取关联的数据集
    datasets = db.query(Dataset).filter(
        Dataset.org_profile_id == profile_id,
        Dataset.user_id == current_user.id
    ).order_by(desc(Dataset.created_at)).offset(skip).limit(limit).all()
    
    # 转换为响应格式
    dataset_list = []
    for dataset in datasets:
        # 获取评估统计
        eval_count = db.query(EvaluationResult).filter(
            EvaluationResult.dataset_id == dataset.id
        ).count()
        
        dataset_list.append({
            'id': dataset.id,
            'name': dataset.name,
            'dataset_type': dataset.dataset_type,
            'data_volume': dataset.data_volume,
            'is_active': dataset.is_active,
            'created_at': dataset.created_at.isoformat() if dataset.created_at else None,
            'evaluation_count': eval_count
        })
    
    return ResponseModel(
        code=200,
        message="获取成功",
        data=dataset_list
    )


@router.get("/stats/summary", response_model=ResponseModel[OrgProfileStats])
async def get_org_profile_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取企业档案统计摘要"""
    # 统计企业档案数量
    total_profiles = db.query(OrgProfile).filter(OrgProfile.user_id == current_user.id).count()
    active_profiles = db.query(OrgProfile).filter(
        OrgProfile.user_id == current_user.id,
        OrgProfile.is_active == True
    ).count()
    
    # 统计各企业档案的评估数量和数据集数量
    profiles = db.query(OrgProfile).filter(OrgProfile.user_id == current_user.id).all()
    evaluations_by_profile = {}
    datasets_by_profile = {}
    
    for profile in profiles:
        # 评估数量
        eval_count = db.query(EvaluationResult).filter(
            EvaluationResult.org_profile_id == profile.id
        ).count()
        
        evaluations_by_profile[profile.company_name] = eval_count
        
        # 数据集数量
        dataset_count = db.query(Dataset).filter(
            Dataset.org_profile_id == profile.id
        ).count()
        
        datasets_by_profile[profile.company_name] = dataset_count
    
    stats = OrgProfileStats(
        total_profiles=total_profiles,
        active_profiles=active_profiles,
        evaluations_by_profile=evaluations_by_profile,
        datasets_by_profile=datasets_by_profile
    )
    
    return ResponseModel(
        code=200,
        message="获取成功",
        data=stats
    )


def org_profile_to_response(profile: OrgProfile, db: Session) -> OrgProfileResponse:
    """将OrgProfile对象转换为响应模型"""
    # 获取评估统计
    evaluation_count = db.query(EvaluationResult).filter(
        EvaluationResult.org_profile_id == profile.id
    ).count()
    
    # 获取数据集统计
    dataset_count = db.query(Dataset).filter(
        Dataset.org_profile_id == profile.id
    ).count()
    
    latest_evaluation = None
    if evaluation_count > 0:
        latest = db.query(EvaluationResult).filter(
            EvaluationResult.org_profile_id == profile.id
        ).order_by(desc(EvaluationResult.created_at)).first()
        
        if latest:
            # 获取数据集信息
            dataset_name = None
            if latest.dataset_id:
                dataset = db.query(Dataset).filter(Dataset.id == latest.dataset_id).first()
                dataset_name = dataset.name if dataset else None
            
            latest_evaluation = {
                'id': latest.id,
                'report_id': latest.report_id,
                'total_score': latest.total_score,
                'risk_level': latest.risk_level,
                'created_at': latest.created_at.isoformat() if latest.created_at else None,
                'dataset_id': latest.dataset_id,
                'dataset_name': dataset_name
            }
    
    return OrgProfileResponse(
        id=profile.id,
        user_id=profile.user_id,
        company_name=profile.company_name,
        industry=profile.industry,
        company_size=profile.company_size,
        annual_revenue=profile.annual_revenue,
        contact_person=profile.contact_person,
        contact_email=profile.contact_email,
        contact_phone=profile.contact_phone,
        address=profile.address,
        website=profile.website,
        compliance_certifications=profile.compliance_certifications,
        description=profile.description,
        is_active=profile.is_active,
        created_at=profile.created_at.isoformat() if profile.created_at else None,
        updated_at=profile.updated_at.isoformat() if profile.updated_at else None,
        evaluation_count=evaluation_count,
        dataset_count=dataset_count,
        latest_evaluation=latest_evaluation
    )