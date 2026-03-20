"""
评价服务 API - 数维数据管家系统
提供评价计算和结果查询功能
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
import json
import io
import traceback

from config.database import get_db
from api.auth import get_current_user
from models.user import User
from models.evaluation_result import EvaluationResult
from services.vip_service import check_user_can_evaluate, increment_eval_count, can_export_report

router = APIRouter(prefix="/api/v1/evaluation", tags=["评价服务"])


class EvaluateRequest(BaseModel):
    """评估请求"""
    form_data: Dict[str, Any]


class EvaluateResponse(BaseModel):
    """评估响应"""
    report_id: str
    org_name: str
    total_score: float
    maturity_level: str
    dimensions: List[Dict[str, Any]]
    p0_issues: List[Dict[str, Any]]
    p1_issues: List[Dict[str, Any]]
    p2_issues: List[Dict[str, Any]]
    risk_level: str
    generated_at: str


class VipStatusResponse(BaseModel):
    """VIP状态响应"""
    can_evaluate: bool
    remaining: int
    is_vip: bool
    message: str


@router.get("/vip-status", response_model=VipStatusResponse)
def get_vip_status(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取用户VIP状态和评估次数
    """
    return check_user_can_evaluate(current_user, db)


@router.post("/evaluate", response_model=EvaluateResponse)
def evaluate_form(
    request: EvaluateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    执行评估计算
    
    接收用户填写的表单数据，计算各维度得分，生成完整报告
    """
    vip_check = check_user_can_evaluate(current_user, db)
    
    if not vip_check['can_evaluate']:
        raise HTTPException(
            status_code=403,
            detail={
                'code': 'EVAL_LIMIT_EXCEEDED',
                'message': vip_check['message'],
                'is_vip': vip_check['is_vip'],
                'remaining': vip_check['remaining']
            }
        )
    
    from services.evaluation import EvaluationService
    
    service = EvaluationService(db)
    
    try:
        result = service.evaluate(
            form_data=request.form_data,
            user_id=current_user.id
        )
        
        increment_eval_count(current_user, db)
        
        return EvaluateResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"评估计算失败：{str(e)}")


@router.get("/{result_id}/download")
def download_evaluation_report(
    result_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    下载评估报告
    
    VIP用户可导出报告为PDF文件
    """
    from services.evaluation import EvaluationService
    from services.pdf_service import generate_report_pdf, generate_pdf_filename
    from urllib.parse import quote
    
    if not can_export_report(current_user):
        raise HTTPException(
            status_code=403,
            detail={
                'code': 'VIP_REQUIRED',
                'message': '该功能仅限VIP用户使用，请升级VIP后重试'
            }
        )
    
    service = EvaluationService(db)
    try:
        result = service.get_result(result_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    org_name = result.get('org_name', '未命名企业') or '未命名企业'
    detail_json = result.get('detail_json') or {}
    if not isinstance(detail_json, dict):
        detail_json = {}
    
    report_data = {
        "id": result_id,
        "org_name": org_name,
        "total_score": result.get('total_score', 0) or 0,
        "maturity_level": detail_json.get('maturity_level', ''),
        "risk_level": result.get('risk_level', '') or 'P2',
        "dimensions": detail_json.get('dimensions', []) or [],
        "p0_issues": detail_json.get('p0_issues', []) or [],
        "p1_issues": detail_json.get('p1_issues', []) or [],
        "generated_at": result.get('created_at', '') or ''
    }
    
    try:
        print(f"[PDF] 开始生成报告，report_data: {report_data}")
        pdf_file = generate_report_pdf(report_data)
        print(f"[PDF] PDF生成成功，大小: {len(pdf_file.getvalue())} bytes")
    except Exception as e:
        import sys
        exc_info = sys.exc_info()
        error_details = ''.join(traceback.format_exception(*exc_info))
        print(f"[PDF] 生成失败: {error_details}")
        raise HTTPException(status_code=500, detail=f"PDF生成失败：{type(e).__name__}: {str(e)}")
    
    filename = generate_pdf_filename(org_name, result_id)
    encoded_filename = quote(filename)
    
    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}"
        }
    )


@router.delete("/{result_id}")
def delete_evaluation_result(
    result_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除评价结果
    
    Args:
        result_id: 评价结果 ID
    """
    from services.evaluation import EvaluationService
    
    service = EvaluationService(db)
    
    try:
        service.delete_result(result_id)
        return {"message": "删除成功"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/history")
def get_evaluation_history(limit: int = 100, db: Session = Depends(get_db)):
    """
    获取所有评估历史记录（管理端用）

    Args:
        limit: 返回数量限制
    """
    from services.evaluation import EvaluationService

    service = EvaluationService(db)
    results = service.get_all_results(limit)

    return results


@router.get("/user/{user_id}/history")
def get_user_evaluation_history(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """
    获取用户评价历史
    
    Args:
        user_id: 用户 ID
        limit: 返回数量限制
    """
    from services.evaluation import EvaluationService
    
    service = EvaluationService(db)
    results = service.get_user_results(user_id, limit)
    
    return results


@router.get("/{result_id}")
def get_evaluation_result(result_id: int, db: Session = Depends(get_db)):
    """
    获取评价结果
    
    Args:
        result_id: 评价结果 ID
    """
    from services.evaluation import EvaluationService
    
    service = EvaluationService(db)
    
    try:
        result = service.get_result(result_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
