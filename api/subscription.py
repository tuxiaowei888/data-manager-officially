"""
订阅管理 API - 数维数据管家系统 V2.0
处理用户订阅升级、订阅信息查询和订阅计划管理
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime, timedelta

from config.database import get_db
from models.user import User
from models.system_config import SystemConfig
from api.auth import get_current_user
from schemas import ResponseModel
from services.subscription_service import (
    get_user_subscription_tier,
    check_user_can_evaluate,
    get_report_depth,
    get_subscription_plans,
    upgrade_subscription,
    get_user_subscription_info
)
from services.customer_scoring import calculate_customer_signals, get_customer_segmentation_stats

router = APIRouter(prefix="/api/v1/subscription", tags=["订阅管理"])


class SubscriptionPlanResponse(BaseModel):
    """订阅计划响应模型"""
    tier: str
    name: str
    description: str
    monthly_price: Optional[float]
    annual_price: Optional[float]
    features: List[str]
    daily_eval_limit: int
    report_depth: str
    dataset_limit: Optional[int]
    org_profile_limit: Optional[int]
    retention_days: int
    export_enabled: bool
    ai_analysis_enabled: bool
    priority_support: bool


class SubscriptionInfoResponse(BaseModel):
    """订阅信息响应模型"""
    current_tier: str
    effective_tier: str
    is_active: bool
    subscription_start_date: Optional[str]
    subscription_end_date: Optional[str]
    days_remaining: Optional[int]
    eval_count_used: int
    eval_count_limit: int
    eval_count_reset_date: str
    report_depth_allowed: str
    can_export_reports: bool
    dataset_limit: Optional[int]
    org_profile_limit: Optional[int]
    retention_days: int
    upgrade_available: bool
    upgrade_recommendation: Optional[str]


class SubscriptionUpgradeRequest(BaseModel):
    """订阅升级请求模型"""
    target_tier: str
    duration_days: int = 365  # 默认1年


class SubscriptionUpgradeResponse(BaseModel):
    """订阅升级响应模型"""
    success: bool
    message: str
    new_tier: str
    effective_date: str
    expiration_date: str
    transaction_id: Optional[str]
    features_unlocked: List[str]


class CustomerTierResponse(BaseModel):
    """客户分层响应模型"""
    tier_label: str
    tier_signals: Dict[str, float]
    metrics: Dict[str, Any]
    recommendations: List[str]
    calculated_at: str


@router.get("/plans", response_model=ResponseModel[List[SubscriptionPlanResponse]])
async def list_subscription_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取所有订阅计划"""
    plans_data = get_subscription_plans(db)
    
    # 转换为响应模型
    plans = []
    for tier, plan_data in plans_data.items():
        plans.append(SubscriptionPlanResponse(
            tier=tier,
            name=plan_data['name'],
            description=plan_data['description'],
            monthly_price=plan_data.get('monthly_price'),
            annual_price=plan_data.get('annual_price'),
            features=plan_data['features'],
            daily_eval_limit=plan_data['daily_eval_limit'],
            report_depth=plan_data['report_depth'],
            dataset_limit=plan_data.get('dataset_limit'),
            org_profile_limit=plan_data.get('org_profile_limit'),
            retention_days=plan_data['retention_days'],
            export_enabled=plan_data['export_enabled'],
            ai_analysis_enabled=plan_data['ai_analysis_enabled'],
            priority_support=plan_data['priority_support']
        ))
    
    return ResponseModel(
        code=200,
        message="获取成功",
        data=plans
    )


@router.get("/info", response_model=ResponseModel[SubscriptionInfoResponse])
async def get_subscription_info(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的订阅信息"""
    # 获取订阅信息
    info = get_user_subscription_info(current_user, db)
    
    # 计算升级建议
    upgrade_available = False
    upgrade_recommendation = None
    
    current_tier = info['current_tier']
    if current_tier == 'free':
        upgrade_available = True
        upgrade_recommendation = "升级到基础版，解锁更多评估次数和详细报告"
    elif current_tier == 'basic':
        upgrade_available = True
        upgrade_recommendation = "升级到专业版，获得无限制评估和行动方案报告"
    elif current_tier == 'pro':
        upgrade_available = True
        upgrade_recommendation = "升级到企业版，享受专属服务和多数据集分析"
    
    # 计算剩余天数
    days_remaining = None
    if info['subscription_end_date']:
        end_date = datetime.fromisoformat(info['subscription_end_date'].replace('Z', '+00:00'))
        days_remaining = (end_date.date() - datetime.now().date()).days
    
    response = SubscriptionInfoResponse(
        current_tier=info['current_tier'],
        effective_tier=info['effective_tier'],
        is_active=info['is_active'],
        subscription_start_date=info['subscription_start_date'],
        subscription_end_date=info['subscription_end_date'],
        days_remaining=days_remaining,
        eval_count_used=info['eval_count_used'],
        eval_count_limit=info['eval_count_limit'],
        eval_count_reset_date=info['eval_count_reset_date'],
        report_depth_allowed=info['report_depth'],
        can_export_reports=info['can_export'],
        dataset_limit=info.get('dataset_limit'),
        org_profile_limit=info.get('org_profile_limit'),
        retention_days=info['retention_days'],
        upgrade_available=upgrade_available,
        upgrade_recommendation=upgrade_recommendation
    )
    
    return ResponseModel(
        code=200,
        message="获取成功",
        data=response
    )


@router.get("/evaluation-status", response_model=ResponseModel[Dict[str, Any]])
async def get_evaluation_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取评估状态（剩余次数、限制等）"""
    result = check_user_can_evaluate(current_user, db)
    
    return ResponseModel(
        code=200,
        message="获取成功",
        data=result
    )


@router.post("/upgrade", response_model=ResponseModel[SubscriptionUpgradeResponse])
async def upgrade_user_subscription(
    upgrade_request: SubscriptionUpgradeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """升级用户订阅（模拟接口，实际需要支付集成）"""
    # 验证目标层级
    valid_tiers = ['basic', 'pro', 'enterprise']
    if upgrade_request.target_tier not in valid_tiers:
        raise HTTPException(
            status_code=400, 
            detail=f"无效的订阅层级，有效选项：{', '.join(valid_tiers)}"
        )
    
    # 检查当前层级
    current_tier = get_user_subscription_tier(current_user)
    tier_order = {'free': 0, 'basic': 1, 'pro': 2, 'enterprise': 3}
    
    # 只能升级到更高层级
    if tier_order.get(upgrade_request.target_tier, 0) <= tier_order.get(current_tier, 0):
        raise HTTPException(
            status_code=400,
            detail=f"只能升级到更高的订阅层级。当前层级：{current_tier}"
        )
    
    # 执行升级（模拟，实际需要支付处理）
    try:
        result = upgrade_subscription(
            user=current_user,
            new_tier=upgrade_request.target_tier,
            duration_days=upgrade_request.duration_days,
            db=db
        )
        
        if not result.get('success'):
            raise HTTPException(status_code=400, detail=result.get('message', '升级失败'))
        
        # 生成响应
        response = SubscriptionUpgradeResponse(
            success=True,
            message=result['message'],
            new_tier=upgrade_request.target_tier,
            effective_date=datetime.now().isoformat(),
            expiration_date=result['expiration_date'],
            transaction_id=result.get('transaction_id'),
            features_unlocked=result['features_unlocked']
        )
        
        return ResponseModel(
            code=200,
            message="订阅升级成功",
            data=response
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"升级过程中出错：{str(e)}")


@router.get("/customer-tier", response_model=ResponseModel[CustomerTierResponse])
async def get_customer_tier(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的客户分层信息"""
    # 计算客户分层信号
    result = calculate_customer_signals(current_user, db)
    
    response = CustomerTierResponse(
        tier_label=result['customer_tier_label'],
        tier_signals=result['customer_tier_signals'],
        metrics=result['metrics'],
        recommendations=result['recommendations'],
        calculated_at=result['calculated_at']
    )
    
    return ResponseModel(
        code=200,
        message="获取成功",
        data=response
    )


@router.get("/customer-segmentation-stats", response_model=ResponseModel[Dict[str, Any]])
async def get_customer_segmentation_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取客户分层统计信息（仅管理员）"""
    # 检查管理员权限
    if current_user.user_type != 'admin':
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 获取分层统计
    stats = get_customer_segmentation_stats(db)
    
    return ResponseModel(
        code=200,
        message="获取成功",
        data=stats
    )


@router.post("/refresh-customer-tiers", response_model=ResponseModel[Dict[str, Any]])
async def refresh_customer_tiers(
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """手动刷新客户分层（仅管理员，定时任务）"""
    # 检查管理员权限
    if current_user.user_type != 'admin':
        raise HTTPException(status_code=403, detail="需要管理员权限")
    
    # 执行批量更新
    from services.customer_scoring import batch_update_customer_tiers
    stats = batch_update_customer_tiers(db, limit)
    
    return ResponseModel(
        code=200,
        message=f"已处理 {stats['total_processed']} 个用户的分层更新",
        data=stats
    )