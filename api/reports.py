"""
报告管理 API - 管理员专用
提供评估报告的查询、筛选、导出功能
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
from urllib.parse import quote

from config.database import get_db
from models.user import User
from models.evaluation_result import EvaluationResult
from api.auth import check_admin
from schemas import ResponseModel
from services.pdf_service import generate_pdf_filename

router = APIRouter(prefix="/api/v1/reports", tags=["报告管理"])


class ReportListItem(BaseModel):
    id: int
    user_id: int
    username: Optional[str]
    user_email: Optional[str]
    org_name: Optional[str]
    total_score: float
    risk_level: str
    created_at: Optional[str]


class ReportDetail(BaseModel):
    id: int
    user_id: int
    username: Optional[str]
    user_email: Optional[str]
    org_name: Optional[str]
    total_score: float
    risk_level: str
    detail: Optional[dict]
    created_at: Optional[str]


@router.get("", response_model=List[ReportListItem])
async def get_all_reports(
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """获取所有评估报告列表"""
    results = db.query(
        EvaluationResult.id,
        EvaluationResult.user_id,
        User.username,
        User.email.label('user_email'),
        EvaluationResult.org_name,
        EvaluationResult.total_score,
        EvaluationResult.risk_level,
        EvaluationResult.created_at
    ).join(
        User, EvaluationResult.user_id == User.id
    ).order_by(
        EvaluationResult.created_at.desc()
    ).all()
    
    return [
        ReportListItem(
            id=r.id,
            user_id=r.user_id,
            username=r.username,
            user_email=r.user_email,
            org_name=r.org_name,
            total_score=r.total_score,
            risk_level=r.risk_level,
            created_at=r.created_at.strftime('%Y-%m-%d %H:%M') if r.created_at else None
        )
        for r in results
    ]


@router.get("/{report_id}", response_model=ReportDetail)
async def get_report_detail(
    report_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """获取报告详情"""
    result = db.query(
        EvaluationResult.id,
        EvaluationResult.user_id,
        User.username,
        User.email.label('user_email'),
        EvaluationResult.org_name,
        EvaluationResult.total_score,
        EvaluationResult.risk_level,
        EvaluationResult.detail_json,
        EvaluationResult.created_at
    ).join(
        User, EvaluationResult.user_id == User.id
    ).filter(
        EvaluationResult.id == report_id
    ).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    return ReportDetail(
        id=result.id,
        user_id=result.user_id,
        username=result.username,
        user_email=result.user_email,
        org_name=result.org_name,
        total_score=result.total_score,
        risk_level=result.risk_level,
        detail=result.detail_json,
        created_at=result.created_at.strftime('%Y-%m-%d %H:%M') if result.created_at else None
    )


@router.get("/{report_id}/export")
async def export_single_report(
    report_id: int,
    format: str = Query("json", description="导出格式: json/excel/pdf"),
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """导出单个报告"""
    result = db.query(
        EvaluationResult.id,
        EvaluationResult.user_id,
        User.username,
        User.email.label('user_email'),
        EvaluationResult.org_name,
        EvaluationResult.total_score,
        EvaluationResult.risk_level,
        EvaluationResult.detail_json,
        EvaluationResult.created_at
    ).join(
        User, EvaluationResult.user_id == User.id
    ).filter(
        EvaluationResult.id == report_id
    ).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="报告不存在")
    
    report_data = {
        "id": result.id,
        "org_name": result.org_name,
        "total_score": result.total_score,
        "risk_level": result.risk_level,
        "detail": result.detail_json,
        "created_at": result.created_at.strftime('%Y-%m-%d %H:%M') if result.created_at else None
    }
    
    if format == "json":
        filename = generate_pdf_filename(result.org_name, report_id, 'json')
        json_content = json.dumps(report_data, ensure_ascii=False, indent=2)
        return StreamingResponse(
            io.BytesIO(json_content.encode('utf-8')),
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(filename)}"}
        )
    elif format == "excel":
        filename = generate_pdf_filename(result.org_name, report_id, 'xlsx')
        return generate_excel_report([report_data], filename)
    elif format == "pdf":
        filename = generate_pdf_filename(result.org_name, report_id)
        encoded_filename = quote(filename)
        return generate_pdf_report(report_data, encoded_filename)
    else:
        raise HTTPException(status_code=400, detail="不支持的导出格式")


@router.get("/export")
async def export_reports(
    ids: str = Query(..., description="报告ID列表，逗号分隔"),
    format: str = Query("json", description="导出格式: json/excel/pdf"),
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """批量导出报告"""
    try:
        report_ids = [int(id.strip()) for id in ids.split(',')]
    except:
        raise HTTPException(status_code=400, detail="无效的报告ID列表")
    
    results = db.query(
        EvaluationResult.id,
        EvaluationResult.user_id,
        User.username,
        EvaluationResult.org_name,
        EvaluationResult.total_score,
        EvaluationResult.risk_level,
        EvaluationResult.detail_json,
        EvaluationResult.created_at
    ).join(
        User, EvaluationResult.user_id == User.id
    ).filter(
        EvaluationResult.id.in_(report_ids)
    ).all()
    
    if not results:
        raise HTTPException(status_code=404, detail="未找到报告")
    
    reports_data = [
        {
            "id": r.id,
            "org_name": r.org_name,
            "total_score": r.total_score,
            "risk_level": r.risk_level,
            "detail": r.detail_json,
            "created_at": r.created_at.strftime('%Y-%m-%d %H:%M') if r.created_at else None
        }
        for r in results
    ]
    
    if format == "json":
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for report in reports_data:
                json_content = json.dumps(report, ensure_ascii=False, indent=2)
                filename = generate_pdf_filename(report.get('org_name', '未命名企业'), report['id'], 'json')
                zip_file.writestr(filename, json_content)
        
        zip_buffer.seek(0)
        date_str = datetime.now().strftime('%Y%m%d')
        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename*=UTF-8''%E6%95%B0%E6%8D%AE%E8%B5%84%E4%BA%A7%E8%AF%84%E4%BC%B0%E6%8A%A5%E5%91%8A%E5%AF%BC%E5%87%BA_{date_str}.zip"}
        )
    elif format == "excel":
        date_str = datetime.now().strftime('%Y%m%d')
        filename = f"数据资产评估报告导出_{date_str}.xlsx"
        return generate_excel_report(reports_data, filename)
    elif format == "pdf":
        return generate_pdf_reports_zip(reports_data)
    else:
        raise HTTPException(status_code=400, detail="不支持的导出格式")


def generate_excel_report(reports: list, filename: str):
    """生成Excel格式报告"""
    try:
        import pandas as pd
        
        rows = []
        for r in reports:
            row = {
                "报告ID": r["id"],
                "企业名称": r["org_name"] or "未命名",
                "总分": r["total_score"],
                "风险等级": {"P0": "高风险", "P1": "中风险", "P2": "低风险"}.get(r["risk_level"], r["risk_level"]),
                "评估时间": r["created_at"]
            }
            
            if r.get("detail") and r["detail"].get("dimensions"):
                for d in r["detail"]["dimensions"]:
                    row[f"维度-{d['name']}"] = d.get("score", "-")
            
            rows.append(row)
        
        df = pd.DataFrame(rows)
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='评估报告')
        
        output.seek(0)
        return StreamingResponse(
            output,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename*=UTF-8''{quote(filename)}"}
        )
    except ImportError:
        raise HTTPException(status_code=500, detail="Excel导出功能需要安装pandas和openpyxl库")


def generate_pdf_report(report: dict, filename: str):
    """生成PDF格式报告"""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib import colors
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        
        output = io.BytesIO()
        doc = SimpleDocTemplate(output, pagesize=A4)
        styles = getSampleStyleSheet()
        
        elements = []
        
        title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=18, spaceAfter=20)
        elements.append(Paragraph(f"评估报告 - {report.get('org_name', '未命名企业')}", title_style))
        elements.append(Spacer(1, 20))
        
        info_data = [
            ["企业名称", report.get("org_name", "-")],
            ["总分", str(report.get("total_score", "-"))],
            ["风险等级", {"P0": "高风险", "P1": "中风险", "P2": "低风险"}.get(report.get("risk_level"), "-")],
            ["评估时间", report.get("created_at", "-")]
        ]
        
        info_table = Table(info_data, colWidths=[100, 300])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 20))
        
        if report.get("detail") and report["detail"].get("dimensions"):
            elements.append(Paragraph("维度评分", styles['Heading2']))
            elements.append(Spacer(1, 10))
            
            dim_data = [["维度名称", "评分"]]
            for d in report["detail"]["dimensions"]:
                dim_data.append([d.get("name", "-"), str(d.get("score", "-"))])
            
            dim_table = Table(dim_data, colWidths=[200, 100])
            dim_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(dim_table)
        
        doc.build(elements)
        output.seek(0)
        
        return StreamingResponse(
            output,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename*=UTF-8''{filename}"}
        )
    except ImportError:
        raise HTTPException(status_code=500, detail="PDF导出功能需要安装reportlab库")


def generate_pdf_reports_zip(reports: list):
    """生成多个PDF报告的ZIP压缩包"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for report in reports:
            try:
                filename = generate_pdf_filename(report.get('org_name', '未命名企业'), report['id'])
                pdf_response = generate_pdf_report(report, quote(filename))
                pdf_content = pdf_response.body_iterator
                if hasattr(pdf_content, 'read'):
                    content = pdf_content.read()
                else:
                    content = b''.join([chunk for chunk in pdf_content])
                
                zip_file.writestr(filename, content)
            except Exception as e:
                continue
    
    zip_buffer.seek(0)
    date_str = datetime.now().strftime('%Y%m%d')
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename*=UTF-8''%E6%95%B0%E6%8D%AE%E8%B5%84%E4%BA%A7%E8%AF%84%E4%BC%B0%E6%8A%A5%E5%91%8A%E5%AF%BC%E5%87%BA_{date_str}.zip"}
    )
