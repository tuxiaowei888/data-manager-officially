"""
知识库目录分类 API - 数维数据管家系统
提供目录分类的 CRUD 操作
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from config.database import get_db
from models.knowledge_category import KnowledgeCategory, DEFAULT_CATEGORIES
from models.knowledge_doc import KnowledgeDoc
from schemas import ResponseModel
from api.auth import check_admin
from models.user import User

router = APIRouter(prefix="/api/v1/knowledge-categories", tags=["知识库目录"])


class CategoryCreate(BaseModel):
    name: str
    parent_id: Optional[int] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    sort_order: Optional[int] = 0


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    description: Optional[str]
    icon: Optional[str]
    sort_order: int
    is_active: bool
    doc_count: int = 0

    class Config:
        from_attributes = True


@router.get("", response_model=List[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db)):
    """获取所有目录分类"""
    categories = db.query(KnowledgeCategory).order_by(KnowledgeCategory.sort_order).all()
    
    results = []
    for c in categories:
        # 统计该分类下的文档数量
        doc_count = db.query(KnowledgeDoc).filter(KnowledgeDoc.category_id == c.id).count()
        
        results.append(CategoryResponse(
            id=c.id,
            name=c.name,
            parent_id=c.parent_id,
            description=c.description,
            icon=c.icon,
            sort_order=c.sort_order,
            is_active=c.is_active,
            doc_count=doc_count
        ))
    
    return results


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """获取单个目录分类"""
    c = db.query(KnowledgeCategory).filter(KnowledgeCategory.id == category_id).first()
    
    if not c:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    doc_count = db.query(KnowledgeDoc).filter(KnowledgeDoc.category_id == c.id).count()
    
    return CategoryResponse(
        id=c.id,
        name=c.name,
        parent_id=c.parent_id,
        description=c.description,
        icon=c.icon,
        sort_order=c.sort_order,
        is_active=c.is_active,
        doc_count=doc_count
    )


@router.post("", response_model=CategoryResponse)
def create_category(data: CategoryCreate, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
    """创建目录分类"""
    category = KnowledgeCategory(
        name=data.name,
        parent_id=data.parent_id,
        description=data.description,
        icon=data.icon,
        sort_order=data.sort_order
    )
    
    db.add(category)
    db.commit()
    db.refresh(category)
    
    return get_category(category.id, db)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
    """更新目录分类"""
    category = db.query(KnowledgeCategory).filter(KnowledgeCategory.id == category_id).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    db.commit()
    db.refresh(category)
    
    return get_category(category_id, db)


@router.delete("/{category_id}", response_model=ResponseModel)
def delete_category(category_id: int, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
    """删除目录分类"""
    category = db.query(KnowledgeCategory).filter(KnowledgeCategory.id == category_id).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="分类不存在")
    
    # 检查是否有文档使用该分类
    doc_count = db.query(KnowledgeDoc).filter(KnowledgeDoc.category_id == category_id).count()
    if doc_count > 0:
        raise HTTPException(status_code=400, detail=f"该分类下有 {doc_count} 个文档，请先移动或删除文档")
    
    db.delete(category)
    db.commit()
    
    return ResponseModel(status="success", message="分类已删除", data=None)


@router.post("/init-defaults")
def init_default_categories(db: Session = Depends(get_db)):
    """初始化默认分类"""
    existing = db.query(KnowledgeCategory).count()
    if existing > 0:
        return {"status": "skipped", "message": "分类已存在，跳过初始化"}
    
    for i, cat in enumerate(DEFAULT_CATEGORIES, 1):
        category = KnowledgeCategory(
            name=cat["name"],
            icon=cat.get("icon"),
            description=cat.get("description"),
            sort_order=i
        )
        db.add(category)
    
    db.commit()
    
    return {"status": "success", "message": f"已创建 {len(DEFAULT_CATEGORIES)} 个默认分类"}
