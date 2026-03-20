"""
AI配置管理 API - 数维数据管家系统
提供AI配置的 CRUD 操作
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from config.database import get_db
from models.ai_config import AIConfig, AI_PROVIDERS, DEFAULT_REPORT_PROMPT
from services.ai_service import AIService
from schemas import ResponseModel
from api.auth import check_admin
from models.user import User

router = APIRouter(prefix="/api/v1/ai", tags=["AI管理"])


class AIConfigCreate(BaseModel):
    config_name: str
    provider: str
    api_key: Optional[str] = None
    api_base_url: Optional[str] = None
    model_name: str
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 4096
    system_prompt: Optional[str] = None
    report_prompt_template: Optional[str] = None
    is_active: Optional[bool] = True
    is_default: Optional[bool] = False


class AIConfigUpdate(BaseModel):
    config_name: Optional[str] = None
    provider: Optional[str] = None
    api_key: Optional[str] = None
    api_base_url: Optional[str] = None
    model_name: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    system_prompt: Optional[str] = None
    report_prompt_template: Optional[str] = None
    is_active: Optional[bool] = None
    is_default: Optional[bool] = None


class AIConfigResponse(BaseModel):
    id: int
    config_name: str
    provider: str
    api_key_masked: str
    api_base_url: Optional[str]
    model_name: str
    temperature: Optional[float]
    max_tokens: Optional[int]
    system_prompt: Optional[str]
    report_prompt_template: Optional[str]
    is_active: bool
    is_default: bool

    class Config:
        from_attributes = True


@router.get("/providers")
def get_providers():
    """获取支持的AI提供商列表"""
    return AI_PROVIDERS


@router.get("", response_model=List[AIConfigResponse])
def get_all_configs(db: Session = Depends(get_db)):
    """获取所有AI配置"""
    configs = db.query(AIConfig).order_by(AIConfig.id).all()
    
    results = []
    for c in configs:
        # 安全地掩码API密钥
        api_key_masked = ""
        if c.api_key:
            key_len = len(c.api_key)
            if key_len > 12:
                api_key_masked = c.api_key[:8] + "****" + c.api_key[-4:]
            elif key_len > 4:
                api_key_masked = c.api_key[:2] + "****" + c.api_key[-2:]
            else:
                api_key_masked = "****"
        
        results.append(AIConfigResponse(
            id=c.id,
            config_name=c.config_name,
            provider=c.provider,
            api_key_masked=api_key_masked,
            api_base_url=c.api_base_url,
            model_name=c.model_name,
            temperature=c.temperature,
            max_tokens=c.max_tokens,
            system_prompt=c.system_prompt,
            report_prompt_template=c.report_prompt_template,
            is_active=c.is_active,
            is_default=c.is_default
        ))
    
    return results


@router.get("/default-template")
def get_default_template():
    """获取默认提示词模板"""
    from models.ai_config import DEFAULT_SYSTEM_PROMPT, DEFAULT_REPORT_PROMPT
    return {
        "system_prompt": DEFAULT_SYSTEM_PROMPT,
        "report_template": DEFAULT_REPORT_PROMPT
    }


@router.get("/{config_id}", response_model=AIConfigResponse)
def get_config(config_id: int, db: Session = Depends(get_db)):
    """获取单个AI配置"""
    config = db.query(AIConfig).filter(AIConfig.id == config_id).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    
    api_key_masked = ""
    if config.api_key:
        api_key_masked = config.api_key[:8] + "****" + config.api_key[-4:] if len(config.api_key) > 12 else "****"
    
    return AIConfigResponse(
        id=config.id,
        config_name=config.config_name,
        provider=config.provider,
        api_key_masked=api_key_masked,
        api_base_url=config.api_base_url,
        model_name=config.model_name,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        system_prompt=config.system_prompt,
        report_prompt_template=config.report_prompt_template,
        is_active=config.is_active,
        is_default=config.is_default
    )


@router.put("/{config_id}", response_model=AIConfigResponse)
def update_config(config_id: int, config_data: AIConfigUpdate, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
    """更新AI配置"""
    config = db.query(AIConfig).filter(AIConfig.id == config_id).first()

    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")

    update_data = config_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(config, field, value)

    db.commit()
    db.refresh(config)

    api_key_masked = ""
    if config.api_key:
        api_key_masked = config.api_key[:8] + "****" + config.api_key[-4:] if len(config.api_key) > 12 else "****"

    return AIConfigResponse(
        id=config.id,
        config_name=config.config_name,
        provider=config.provider,
        model_name=config.model_name,
        api_key_masked=api_key_masked,
        api_base_url=config.api_base_url,
        temperature=config.temperature,
        max_tokens=config.max_tokens,
        system_prompt=config.system_prompt,
        report_prompt_template=config.report_prompt_template,
        is_active=config.is_active,
        is_default=config.is_default
    )


@router.post("", response_model=AIConfigResponse)
def create_config(config_data: AIConfigCreate, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
    """创建AI配置"""
    if config_data.provider not in AI_PROVIDERS:
        raise HTTPException(status_code=400, detail=f"不支持的AI提供商: {config_data.provider}")
    
    if config_data.is_default:
        db.query(AIConfig).update({AIConfig.is_default: False})
    
    config = AIConfig(
        config_name=config_data.config_name,
        provider=config_data.provider,
        api_key=config_data.api_key,
        api_base_url=config_data.api_base_url or AI_PROVIDERS[config_data.provider]["default_url"],
        model_name=config_data.model_name,
        temperature=config_data.temperature,
        max_tokens=config_data.max_tokens,
        system_prompt=config_data.system_prompt,
        report_prompt_template=config_data.report_prompt_template,
        is_active=config_data.is_active,
        is_default=config_data.is_default
    )
    
    db.add(config)
    db.commit()
    db.refresh(config)
    
    return get_config(config.id, db)


@router.put("/{config_id}", response_model=AIConfigResponse)
def update_config(config_id: int, config_data: AIConfigUpdate, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
    """更新AI配置"""
    config = db.query(AIConfig).filter(AIConfig.id == config_id).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    
    if config_data.is_default:
        db.query(AIConfig).filter(AIConfig.id != config_id).update({AIConfig.is_default: False})
    
    update_data = config_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(config, field, value)
    
    db.commit()
    db.refresh(config)
    
    return get_config(config.id, db)


@router.delete("/{config_id}", response_model=ResponseModel)
def delete_config(config_id: int, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
    """删除AI配置"""
    config = db.query(AIConfig).filter(AIConfig.id == config_id).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    
    db.delete(config)
    db.commit()
    
    return ResponseModel(status="success", message="配置已删除", data=None)


@router.post("/{config_id}/test")
def test_config(config_id: int, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
    """测试AI配置连接"""
    ai_service = AIService(db)
    result = ai_service.test_connection(config_id)
    
    return result


@router.post("/{config_id}/set-default")
def set_default_config(config_id: int, db: Session = Depends(get_db), admin: User = Depends(check_admin)):
    """设置默认AI配置"""
    config = db.query(AIConfig).filter(AIConfig.id == config_id).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="配置不存在")
    
    db.query(AIConfig).update({AIConfig.is_default: False})
    config.is_default = True
    config.is_active = True
    db.commit()
    
    return {"status": "success", "message": f"已将 {config.config_name} 设为默认配置"}
