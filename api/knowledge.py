"""
知识库管理 API - 数维数据管家系统
提供政策文档的上传、查询功能
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import threading
import time

from config.database import get_db
from models.knowledge_doc import KnowledgeDoc
from schemas import KnowledgeDocCreate, KnowledgeDocResponse, ResponseModel
from api.auth import check_admin
from models.user import User

router = APIRouter(prefix="/api/v1/knowledge", tags=["知识库管理"])

_vectorize_status = {
    "is_running": False,
    "total": 0,
    "processed": 0,
    "success": 0,
    "fail": 0,
    "skipped": 0,
    "start_time": None,
    "end_time": None,
    "error": None
}
_vectorize_lock = threading.Lock()

def _run_vectorize_task(doc_ids: list):
    global _vectorize_status
    from services.vector_store import vector_store
    from config.database import SessionLocal
    
    db = SessionLocal()
    try:
        for i, doc_id in enumerate(doc_ids):
            if not _vectorize_status["is_running"]:
                break
            
            doc = db.query(KnowledgeDoc).filter(KnowledgeDoc.id == doc_id).first()
            if not doc or not doc.content or not doc.content.strip():
                with _vectorize_lock:
                    _vectorize_status["skipped"] += 1
                    _vectorize_status["processed"] += 1
                continue
            
            try:
                added = vector_store.add_document(
                    doc_id=str(doc.id),
                    content=doc.content,
                    metadata={"title": doc.title, "category_id": doc.category_id}
                )
                with _vectorize_lock:
                    if added:
                        _vectorize_status["success"] += 1
                    else:
                        _vectorize_status["fail"] += 1
                    _vectorize_status["processed"] += 1
            except Exception as e:
                print(f"[Vectorize] 文档ID {doc.id} 处理失败: {e}")
                with _vectorize_lock:
                    _vectorize_status["fail"] += 1
                    _vectorize_status["processed"] += 1
    except Exception as e:
        with _vectorize_lock:
            _vectorize_status["error"] = str(e)
    finally:
        db.close()
        with _vectorize_lock:
            _vectorize_status["is_running"] = False
            _vectorize_status["end_time"] = time.time()


@router.get("")
def get_all_documents(
    category_id: Optional[int] = Query(None, description="目录分类ID"),
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    db: Session = Depends(get_db)
):
    """
    获取所有政策文档
    
    Args:
        category_id: 按目录分类筛选
        keyword: 按关键词搜索
    """
    query = db.query(KnowledgeDoc).filter(KnowledgeDoc.is_active == True)
    
    if category_id:
        query = query.filter(KnowledgeDoc.category_id == category_id)
    
    if keyword:
        query = query.filter(KnowledgeDoc.title.contains(keyword))
    
    docs = query.order_by(KnowledgeDoc.created_at.desc()).all()
    
    return [
        {
            "id": d.id,
            "category_id": d.category_id,
            "doc_type": d.doc_type,
            "title": d.title,
            "content": d.content[:500] + "..." if d.content and len(d.content) > 500 else d.content,
            "source": d.source,
            "is_active": d.is_active,
            "created_at": d.created_at.strftime('%Y-%m-%d %H:%M') if d.created_at else None
        }
        for d in docs
    ]


@router.get("/{doc_id}")
def get_document(doc_id: int, db: Session = Depends(get_db)):
    """
    获取单个文档详情
    
    Args:
        doc_id: 文档 ID
    """
    doc = db.query(KnowledgeDoc).filter(KnowledgeDoc.id == doc_id).first()
    
    if not doc:
        raise HTTPException(status_code=404, detail=f"文档不存在：{doc_id}")
    
    return {
        "id": doc.id,
        "category_id": doc.category_id,
        "doc_type": doc.doc_type,
        "title": doc.title,
        "content": doc.content,
        "source": doc.source,
        "is_active": doc.is_active,
        "created_at": doc.created_at.strftime('%Y-%m-%d %H:%M') if doc.created_at else None
    }


@router.post("")
def create_document(doc_data: KnowledgeDocCreate, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
    """
    创建政策文档
    
    管理员可以上传政策文档
    """
    doc = KnowledgeDoc(
        title=doc_data.title,
        category_id=doc_data.category_id,
        content=doc_data.content,
        source=doc_data.source,
        is_active=True
    )
    
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    from services.vector_store import vector_store
    if vector_store.is_available():
        vector_store.add_document(
            doc_id=str(doc.id),
            content=doc.content or "",
            metadata={"title": doc.title, "category_id": doc.category_id}
        )
    
    return {
        "id": doc.id,
        "category_id": doc.category_id,
        "title": doc.title,
        "content": doc.content[:500] + "..." if doc.content and len(doc.content) > 500 else doc.content,
        "source": doc.source,
        "is_active": doc.is_active,
        "created_at": doc.created_at.strftime('%Y-%m-%d %H:%M') if doc.created_at else None
    }


@router.delete("/{doc_id}", response_model=ResponseModel)
def delete_document(doc_id: int, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
    """
    删除政策文档
    
    Args:
        doc_id: 文档 ID
    """
    try:
        doc = db.query(KnowledgeDoc).filter(KnowledgeDoc.id == doc_id).first()
        
        if not doc:
            raise HTTPException(status_code=404, detail=f"文档不存在：{doc_id}")
        
        db.delete(doc)
        db.commit()
        
        from services.vector_store import vector_store
        if vector_store.is_available():
            vector_store.delete_document(str(doc_id))
        
        return ResponseModel(
            status="success",
            message=f"文档已删除：{doc_id}",
            data=None
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除失败：{str(e)}")


@router.post("/upload")
async def upload_document(
    title: str,
    file: UploadFile = File(...),
    category_id: Optional[int] = Query(None, description="目录分类ID"),
    doc_type: Optional[str] = Query(None, description="文档类型"),
    source: Optional[str] = Query(None, description="来源"),
    db: Session = Depends(get_db),
    admin: User = Depends(check_admin)
):
    """
    上传政策文档文件
    
    支持 .txt, .md, .doc, .docx, .pdf 格式
    
    Args:
        title: 文档标题
        file: 上传的文件
        category_id: 目录分类ID
        doc_type: 文档类型
        source: 来源
    """
    import io
    from PyPDF2 import PdfReader
    
    content = await file.read()
    filename = file.filename.lower() if file.filename else ""
    content_text = ""
    
    try:
        if filename.endswith('.pdf'):
            pdf_reader = PdfReader(io.BytesIO(content))
            for page in pdf_reader.pages:
                text = page.extract_text()
                if text:
                    content_text += text + "\n\n"
        elif filename.endswith('.docx') or filename.endswith('.doc'):
            try:
                from docx import Document
                doc = Document(io.BytesIO(content))
                for para in doc.paragraphs:
                    text = para.text.strip()
                    if text:
                        content_text += text + "\n\n"
            except ImportError:
                raise HTTPException(status_code=500, detail="服务器未安装python-docx库，无法解析Word文件")
        else:
            try:
                content_text = content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    content_text = content.decode('gbk')
                except:
                    content_text = content.decode('utf-8', errors='ignore')
                    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"文件解析失败：{str(e)}")
    
    if not content_text.strip():
        raise HTTPException(status_code=400, detail="文件内容为空或无法解析")
    
    doc = KnowledgeDoc(
        title=title,
        category_id=category_id,
        doc_type=doc_type,
        content=content_text,
        source=source or file.filename,
        is_active=True
    )
    
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    from services.vector_store import vector_store
    if vector_store.is_available():
        vector_store.add_document(
            doc_id=str(doc.id),
            content=content_text,
            metadata={"title": title, "category_id": category_id}
        )
    
    return {
        "id": doc.id,
        "category_id": doc.category_id,
        "doc_type": doc.doc_type,
        "title": doc.title,
        "content": doc.content[:500] + "..." if len(doc.content) > 500 else doc.content,
        "source": doc.source,
        "is_active": doc.is_active,
        "created_at": doc.created_at.strftime('%Y-%m-%d %H:%M') if doc.created_at else None
    }


@router.get("/search")
def search_documents(
    keyword: str,
    db: Session = Depends(get_db)
):
    """
    搜索政策文档
    
    V1.0 实现：简单的文本匹配
    V2.0 实现：语义检索
    
    Args:
        keyword: 搜索关键词
    """
    from services.vector_store import vector_store
    
    if vector_store.is_available():
        results = vector_store.search(keyword, top_k=10)
        return {
            "mode": "semantic",
            "results": results
        }
    
    docs = db.query(KnowledgeDoc).filter(
        KnowledgeDoc.content.like(f"%{keyword}%")
    ).all()
    
    return {
        "mode": "keyword",
        "results": docs
    }


@router.post("/vectorize-all", response_model=ResponseModel)
def vectorize_all_documents(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db), 
    admin: User = Depends(check_admin)
):
    """
    批量向量化所有知识库文档（异步后台任务）
    
    管理员操作：将数据库中所有文档批量添加到向量库
    此接口立即返回，实际处理在后台进行，可通过 /vectorize-status 查询进度
    
    Returns:
        任务启动状态
    """
    from services.vector_store import vector_store
    
    if not vector_store.is_available():
        return ResponseModel(
            status="warning",
            message="向量存储不可用，请先安装依赖并重启服务",
            data=None
        )
    
    global _vectorize_status
    
    with _vectorize_lock:
        if _vectorize_status["is_running"]:
            return ResponseModel(
                status="warning",
                message="已有向量化任务正在运行，请等待完成",
                data=_vectorize_status
            )
        
        docs = db.query(KnowledgeDoc).filter(KnowledgeDoc.is_active == True).all()
        doc_ids = [doc.id for doc in docs]
        
        _vectorize_status = {
            "is_running": True,
            "total": len(doc_ids),
            "processed": 0,
            "success": 0,
            "fail": 0,
            "skipped": 0,
            "start_time": time.time(),
            "end_time": None,
            "error": None
        }
    
    thread = threading.Thread(target=_run_vectorize_task, args=(doc_ids,))
    thread.daemon = True
    thread.start()
    
    return ResponseModel(
        status="success",
        message=f"向量化任务已启动，共 {len(doc_ids)} 个文档待处理",
        data={
            "total": len(doc_ids),
            "is_running": True
        }
    )


@router.get("/vectorize-status")
def get_vectorize_status():
    """
    获取批量向量化任务进度
    
    Returns:
        当前任务状态和进度
    """
    global _vectorize_status
    
    with _vectorize_lock:
        status_copy = _vectorize_status.copy()
    
    if status_copy["is_running"]:
        progress = 0
        if status_copy["total"] > 0:
            progress = round(status_copy["processed"] / status_copy["total"] * 100, 1)
        return {
            "is_running": True,
            "progress": progress,
            "total": status_copy["total"],
            "processed": status_copy["processed"],
            "success": status_copy["success"],
            "fail": status_copy["fail"],
            "skipped": status_copy["skipped"]
        }
    else:
        if status_copy["end_time"] and status_copy["total"] > 0:
            return {
                "is_running": False,
                "completed": True,
                "total": status_copy["total"],
                "success": status_copy["success"],
                "fail": status_copy["fail"],
                "skipped": status_copy["skipped"],
                "error": status_copy["error"]
            }
        else:
            return {
                "is_running": False,
                "completed": False,
                "message": "没有正在进行的向量化任务"
            }
