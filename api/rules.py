"""
规则管理 API - 数维数据管家系统
提供规则的 CRUD 操作
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from config.database import get_db
from models.rule_config import RuleConfig, DIMENSIONS
from schemas import RuleConfigCreate, RuleConfigUpdate, RuleConfigResponse, ResponseModel
from api.auth import check_admin
from models.user import User

router = APIRouter(prefix="/api/v1/rules", tags=["规则管理"])


class DimensionInfo(BaseModel):
    code: str
    name: str
    color: str
    weight: int


def validate_expression(expression: str) -> dict:
    """验证逻辑表达式语法"""
    from simpleeval import EvalWithCompoundTypes
    
    safe_funcs = {'min': min, 'max': max, 'sum': sum, 'abs': abs, 'round': round}
    safe_names = {'True': True, 'False': False, 'None': None}
    
    test_data = {
        'compliance_score': 80, 'quality_score': 75, 'value_score': 70,
        'management_score': 65, 'circulation_score': 60, 'potential_score': 55,
        'total_records': 1000, 'valid_records': 950, 'error_count': 50,
        'data_sources': 5, 'api_calls': 100, 'storage_size': 10000
    }
    
    try:
        evaluator = EvalWithCompoundTypes(functions=safe_funcs, names={**safe_names, **test_data})
        result = evaluator.eval(expression)
        return {'valid': True, 'result': result}
    except Exception as e:
        return {'valid': False, 'error': str(e)}


@router.get("/dimensions", response_model=List[DimensionInfo])
def get_dimensions():
    """获取所有维度信息"""
    return [
        DimensionInfo(code=code, **info)
        for code, info in DIMENSIONS.items()
    ]


@router.get("")
def get_all_rules(
    dimension: Optional[str] = None,
    is_active: Optional[bool] = None,
    keyword: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    sort_by: str = Query("id", regex="^(id|dimension_code|weight|risk_threshold|created_at)$"),
    sort_order: str = Query("asc", regex="^(asc|desc)$"),
    db: Session = Depends(get_db)
):
    """获取所有规则（支持分页、排序、筛选）"""
    query = db.query(RuleConfig).filter(RuleConfig.is_deleted == False)
    
    if dimension:
        query = query.filter(RuleConfig.dimension_code == dimension)
    if is_active is not None:
        query = query.filter(RuleConfig.is_active == is_active)
    if keyword:
        query = query.filter(RuleConfig.rule_name.contains(keyword))
    
    sort_column = getattr(RuleConfig, sort_by, RuleConfig.id)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    total = query.count()
    rules = query.offset((page - 1) * page_size).limit(page_size).all()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "data": rules
    }


@router.get("/active", response_model=List[RuleConfigResponse])
def get_active_rules(db: Session = Depends(get_db)):
    """获取所有活跃规则"""
    return db.query(RuleConfig).filter(
        RuleConfig.is_active == True,
        RuleConfig.is_deleted == False
    ).all()


@router.get("/{rule_id}", response_model=RuleConfigResponse)
def get_rule(rule_id: int, db: Session = Depends(get_db)):
    """获取单个规则详情"""
    rule = db.query(RuleConfig).filter(
        RuleConfig.id == rule_id,
        RuleConfig.is_deleted == False
    ).first()
    
    if not rule:
        raise HTTPException(status_code=404, detail=f"规则不存在：{rule_id}")
    
    return rule


@router.post("", response_model=RuleConfigResponse)
def create_rule(rule_data: RuleConfigCreate, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
    """创建新规则"""
    if rule_data.dimension_code not in DIMENSIONS:
        raise HTTPException(status_code=400, detail=f"无效的维度代码：{rule_data.dimension_code}")
    
    validation = validate_expression(rule_data.logic_expression)
    if not validation['valid']:
        raise HTTPException(status_code=400, detail=f"表达式语法错误：{validation['error']}")
    
    rule = RuleConfig(
        dimension_code=rule_data.dimension_code,
        rule_name=rule_data.rule_name,
        logic_expression=rule_data.logic_expression,
        weight=rule_data.weight,
        risk_threshold=rule_data.risk_threshold,
        is_active=rule_data.is_active,
        source_type='manual',
        version=1
    )
    
    db.add(rule)
    db.commit()
    db.refresh(rule)
    
    return rule


@router.put("/{rule_id}", response_model=RuleConfigResponse)
def update_rule(rule_id: int, rule_data: RuleConfigUpdate, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
    """更新规则配置"""
    rule = db.query(RuleConfig).filter(
        RuleConfig.id == rule_id,
        RuleConfig.is_deleted == False
    ).first()
    
    if not rule:
        raise HTTPException(status_code=404, detail=f"规则不存在：{rule_id}")
    
    if rule_data.logic_expression:
        validation = validate_expression(rule_data.logic_expression)
        if not validation['valid']:
            raise HTTPException(status_code=400, detail=f"表达式语法错误：{validation['error']}")
    
    update_data = rule_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rule, field, value)
    
    rule.version += 1
    
    db.commit()
    db.refresh(rule)
    
    return rule


@router.delete("/{rule_id}", response_model=ResponseModel)
def delete_rule(rule_id: int, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
    """删除规则（软删除）"""
    rule = db.query(RuleConfig).filter(
        RuleConfig.id == rule_id,
        RuleConfig.is_deleted == False
    ).first()
    
    if not rule:
        raise HTTPException(status_code=404, detail=f"规则不存在：{rule_id}")
    
    rule.is_deleted = True
    rule.is_active = False
    db.commit()
    
    return ResponseModel(status="success", message=f"规则已删除：{rule_id}", data=None)


@router.post("/{rule_id}/toggle", response_model=RuleConfigResponse)
def toggle_rule_status(rule_id: int, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
    """切换规则启用状态"""
    rule = db.query(RuleConfig).filter(
        RuleConfig.id == rule_id,
        RuleConfig.is_deleted == False
    ).first()
    
    if not rule:
        raise HTTPException(status_code=404, detail=f"规则不存在：{rule_id}")
    
    rule.is_active = not rule.is_active
    rule.version += 1
    
    db.commit()
    db.refresh(rule)
    
    return rule


@router.post("/{rule_id}/validate")
def validate_rule_expression(rule_id: int, db: Session = Depends(get_db)):
    """验证规则表达式"""
    rule = db.query(RuleConfig).filter(
        RuleConfig.id == rule_id,
        RuleConfig.is_deleted == False
    ).first()
    
    if not rule:
        raise HTTPException(status_code=404, detail=f"规则不存在：{rule_id}")
    
    validation = validate_expression(rule.logic_expression)
    
    return {
        "rule_id": rule_id,
        "rule_name": rule.rule_name,
        "expression": rule.logic_expression,
        "is_valid": validation['valid'],
        "error": validation.get('error'),
        "test_result": validation.get('result')
    }
