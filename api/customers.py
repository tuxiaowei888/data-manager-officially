"""
客户管理 API - 管理员专用
查看客户资料、表单记录、评估报告
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta
import io
import zipfile
import json

from config.database import get_db
from models.user import User
from models.evaluation_result import EvaluationResult
from api.auth import get_current_user
from schemas import ResponseModel

router = APIRouter(prefix="/api/v1/customers", tags=["客户管理"])


class CustomerBasic(BaseModel):
    id: int
    username: str
    email: Optional[str]
    phone: Optional[str]
    is_vip: bool
    vip_expire_date: Optional[str]
    is_active: bool
    channel_id: Optional[int]
    referrer_code: Optional[str]
    daily_eval_count: int
    created_at: Optional[str]
    last_login_at: Optional[str]


class CustomerDetail(CustomerBasic):
    total_evaluations: int
    avg_score: Optional[float]
    latest_score: Optional[float]
    latest_eval_at: Optional[str]
    is_high_value: bool = False


class EvaluationReport(BaseModel):
    id: int
    org_name: Optional[str]
    total_score: float
    risk_level: str
    created_at: Optional[str]


class CustomerStats(BaseModel):
    total_customers: int
    vip_customers: int
    active_today: int
    active_week: int
    active_month: int
    high_value_count: int


def check_admin(current_user: User = Depends(get_current_user)):
    if current_user.user_type != 'admin':
        raise HTTPException(status_code=403, detail="需要管理员权限")
    return current_user


@router.get("/stats", response_model=CustomerStats)
async def get_customer_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """获取客户统计数据"""
    total = db.query(User).filter(User.user_type == 'client').count()
    vip = db.query(User).filter(User.user_type == 'client', User.is_vip == True).count()
    
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    active_today = db.query(User).filter(
        User.user_type == 'client',
        User.daily_eval_date == today
    ).count()
    
    active_week = db.query(EvaluationResult).filter(
        EvaluationResult.created_at >= week_ago
    ).distinct(EvaluationResult.user_id).count()
    
    active_month = db.query(EvaluationResult).filter(
        EvaluationResult.created_at >= month_ago
    ).distinct(EvaluationResult.user_id).count()
    
    subquery = db.query(
        EvaluationResult.user_id,
        func.count(EvaluationResult.id).label('total_eval'),
        func.avg(EvaluationResult.total_score).label('avg_score')
    ).group_by(EvaluationResult.user_id).subquery()
    
    high_value = db.query(User).join(
        subquery, User.id == subquery.c.user_id, isouter=True
    ).filter(
        User.user_type == 'client',
        or_(
            User.is_vip == True,
            and_(subquery.c.total_eval >= 5, subquery.c.avg_score >= 60),
            subquery.c.total_eval >= 10
        )
    ).count()
    
    return CustomerStats(
        total_customers=total,
        vip_customers=vip,
        active_today=active_today,
        active_week=active_week,
        active_month=active_month,
        high_value_count=high_value
    )


@router.get("", response_model=List[CustomerDetail])
async def get_customers(
    keyword: Optional[str] = None,
    vip_status: Optional[str] = None,
    active_status: Optional[str] = None,
    register_time: Optional[str] = None,
    eval_count_range: Optional[str] = None,
    score_range: Optional[str] = None,
    risk_level: Optional[str] = None,
    high_value_only: bool = False,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """获取客户列表（支持多维度筛选）"""
    query = db.query(User).filter(User.user_type == 'client')
    
    if keyword:
        query = query.filter(
            or_(
                User.username.contains(keyword),
                User.email.contains(keyword),
                User.phone.contains(keyword)
            )
        )
    
    if vip_status == 'vip':
        query = query.filter(User.is_vip == True)
    elif vip_status == 'normal':
        query = query.filter(User.is_vip == False)
    
    if register_time:
        today = datetime.now().date()
        if register_time == 'today':
            query = query.filter(User.created_at >= today)
        elif register_time == 'week':
            query = query.filter(User.created_at >= today - timedelta(days=7))
        elif register_time == 'month':
            query = query.filter(User.created_at >= today - timedelta(days=30))
    
    users = query.order_by(User.id.asc()).offset((page - 1) * page_size).limit(page_size).all()
    
    results = []
    for u in users:
        evals = db.query(EvaluationResult).filter(EvaluationResult.user_id == u.id).all()
        total_eval = len(evals)
        avg_score = sum(e.total_score for e in evals) / total_eval if total_eval > 0 else None
        latest = evals[-1] if evals else None
        
        is_high_value = (
            u.is_vip or 
            (total_eval >= 5 and avg_score and avg_score >= 60) or 
            total_eval >= 10
        )
        
        if high_value_only and not is_high_value:
            continue
        
        results.append(CustomerDetail(
            id=u.id,
            username=u.username,
            email=u.email,
            phone=u.phone,
            is_vip=u.is_vip or False,
            vip_expire_date=u.vip_expire_date.strftime('%Y-%m-%d') if u.vip_expire_date else None,
            is_active=u.is_active,
            channel_id=u.channel_id,
            referrer_code=u.referrer_code,
            daily_eval_count=u.daily_eval_count or 0,
            created_at=u.created_at.strftime('%Y-%m-%d %H:%M') if u.created_at else None,
            last_login_at=u.last_login_at.strftime('%Y-%m-%d %H:%M') if u.last_login_at else None,
            total_evaluations=total_eval,
            avg_score=round(avg_score, 1) if avg_score else None,
            latest_score=latest.total_score if latest else None,
            latest_eval_at=latest.created_at.strftime('%Y-%m-%d %H:%M') if latest and latest.created_at else None,
            is_high_value=is_high_value
        ))
    
    return results


@router.get("/{user_id}", response_model=CustomerDetail)
async def get_customer_detail(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """获取客户详情"""
    u = db.query(User).filter(User.id == user_id, User.user_type == 'client').first()
    if not u:
        raise HTTPException(status_code=404, detail="客户不存在")
    
    evals = db.query(EvaluationResult).filter(EvaluationResult.user_id == u.id).all()
    total_eval = len(evals)
    avg_score = sum(e.total_score for e in evals) / total_eval if total_eval > 0 else None
    latest = evals[-1] if evals else None
    
    return CustomerDetail(
        id=u.id,
        username=u.username,
        email=u.email,
        phone=u.phone,
        is_vip=u.is_vip or False,
        vip_expire_date=u.vip_expire_date.strftime('%Y-%m-%d') if u.vip_expire_date else None,
        is_active=u.is_active,
        channel_id=u.channel_id,
        referrer_code=u.referrer_code,
        daily_eval_count=u.daily_eval_count or 0,
        created_at=u.created_at.strftime('%Y-%m-%d %H:%M') if u.created_at else None,
        last_login_at=u.last_login_at.strftime('%Y-%m-%d %H:%M') if u.last_login_at else None,
        total_evaluations=total_eval,
        avg_score=round(avg_score, 1) if avg_score else None,
        latest_score=latest.total_score if latest else None,
        latest_eval_at=latest.created_at.strftime('%Y-%m-%d %H:%M') if latest and latest.created_at else None
    )


@router.get("/{user_id}/reports", response_model=List[EvaluationReport])
async def get_customer_reports(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """获取客户的评估报告列表"""
    u = db.query(User).filter(User.id == user_id, User.user_type == 'client').first()
    if not u:
        raise HTTPException(status_code=404, detail="客户不存在")
    
    reports = db.query(EvaluationResult).filter(
        EvaluationResult.user_id == user_id
    ).order_by(EvaluationResult.created_at.desc()).all()
    
    return [
        EvaluationReport(
            id=r.id,
            org_name=r.org_name,
            total_score=r.total_score,
            risk_level=r.risk_level,
            created_at=r.created_at.strftime('%Y-%m-%d %H:%M') if r.created_at else None
        )
        for r in reports
    ]


@router.get("/{user_id}/reports/export")
async def export_all_reports(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """导出客户所有报告为ZIP文件"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    reports = db.query(EvaluationResult).filter(
        EvaluationResult.user_id == user_id
    ).order_by(EvaluationResult.created_at.desc()).all()
    
    if not reports:
        raise HTTPException(status_code=404, detail="暂无报告可导出")
    
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for i, report in enumerate(reports, 1):
            report_data = {
                "id": report.id,
                "org_name": report.org_name,
                "total_score": report.total_score,
                "risk_level": report.risk_level,
                "detail": report.detail_json,
                "created_at": report.created_at.strftime('%Y-%m-%d %H:%M') if report.created_at else None
            }
            
            json_content = json.dumps(report_data, ensure_ascii=False, indent=2)
            filename = f"report_{i}_{report.org_name or 'unnamed'}.json"
            zip_file.writestr(filename, json_content)
    
    zip_buffer.seek(0)
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={user.username}_reports.zip"
        }
    )


@router.get("/{user_id}/reports/{report_id}")
async def get_report_detail(
    user_id: int,
    report_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """获取报告详情"""
    report = db.query(EvaluationResult).filter(
        EvaluationResult.id == report_id,
        EvaluationResult.user_id == user_id
    ).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    return {
        "id": report.id,
        "user_id": report.user_id,
        "org_name": report.org_name,
        "total_score": report.total_score,
        "risk_level": report.risk_level,
        "detail": report.detail_json,
        "created_at": report.created_at.strftime('%Y-%m-%d %H:%M') if report.created_at else None
    }


@router.get("/{user_id}/reports/{report_id}/export")
async def export_single_report(
    user_id: int,
    report_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """导出单个报告为JSON文件"""
    report = db.query(EvaluationResult).filter(
        EvaluationResult.id == report_id,
        EvaluationResult.user_id == user_id
    ).first()
    
    if not report:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    report_data = {
        "id": report.id,
        "org_name": report.org_name,
        "total_score": report.total_score,
        "risk_level": report.risk_level,
        "detail": report.detail_json,
        "created_at": report.created_at.strftime('%Y-%m-%d %H:%M') if report.created_at else None
    }
    
    json_content = json.dumps(report_data, ensure_ascii=False, indent=2)
    json_bytes = json_content.encode('utf-8')
    
    return StreamingResponse(
        io.BytesIO(json_bytes),
        media_type="application/json",
        headers={
            "Content-Disposition": f"attachment; filename=report_{report_id}.json"
        }
    )


@router.get("/{user_id}/reports/export")
async def export_all_reports(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """导出客户所有报告为ZIP文件"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    reports = db.query(EvaluationResult).filter(
        EvaluationResult.user_id == user_id
    ).order_by(EvaluationResult.created_at.desc()).all()
    
    if not reports:
        raise HTTPException(status_code=404, detail="暂无报告可导出")
    
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for i, report in enumerate(reports, 1):
            report_data = {
                "id": report.id,
                "org_name": report.org_name,
                "total_score": report.total_score,
                "risk_level": report.risk_level,
                "detail": report.detail_json,
                "created_at": report.created_at.strftime('%Y-%m-%d %H:%M') if report.created_at else None
            }
            
            json_content = json.dumps(report_data, ensure_ascii=False, indent=2)
            filename = f"report_{i}_{report.org_name or 'unnamed'}.json"
            zip_file.writestr(filename, json_content)
    
    zip_buffer.seek(0)
    
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={user.username}_reports.zip"
        }
    )
