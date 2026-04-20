"""
Pydantic 模型 - 数维数据管家系统
用于请求/响应数据验证
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


# ============ 规则配置相关模型 ============

class RuleConfigBase(BaseModel):
    """规则配置基础模型"""
    dimension_code: str = Field(..., description="维度代码")
    rule_name: str = Field(..., description="规则名称")
    logic_expression: str = Field(..., description="计算逻辑表达式")
    weight: float = Field(..., ge=0.0, description="权重")
    risk_threshold: float = Field(..., ge=0.0, le=100.0, description="风险阈值")
    is_active: bool = Field(default=True, description="是否启用")


class RuleConfigCreate(RuleConfigBase):
    """创建规则配置请求模型"""
    pass


class RuleConfigUpdate(BaseModel):
    """更新规则配置请求模型"""
    dimension_code: Optional[str] = None
    rule_name: Optional[str] = None
    logic_expression: Optional[str] = None
    weight: Optional[float] = Field(None, ge=0.0, le=100.0)
    risk_threshold: Optional[float] = Field(None, ge=0.0, le=100.0)
    is_active: Optional[bool] = None


class RuleConfigResponse(RuleConfigBase):
    """规则配置响应模型"""
    id: int
    source_type: str
    version: int
    ai_prompt_context: Optional[str] = None
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# ============ 评价结果相关模型 ============

class EvaluationRequest(BaseModel):
    """评价请求模型"""
    user_id: int
    data: dict = Field(..., description="用户填报的数据")


class EvaluationDetail(BaseModel):
    """评价详情"""
    dimension_code: str
    rule_name: str
    score: float
    weight: float
    risk_level: str


class EvaluationResponse(BaseModel):
    """评价响应模型"""
    id: int
    user_id: int
    total_score: float
    risk_level: str
    detail_json: dict
    engine_version: str
    ai_analysis_log: Optional[dict] = None


# ============ 知识库相关模型 ============

class KnowledgeDocBase(BaseModel):
    """知识库文档基础模型"""
    title: str = Field(..., description="文档标题")
    content: Optional[str] = Field(None, description="文档内容")


class KnowledgeDocCreate(KnowledgeDocBase):
    """创建知识库文档请求模型"""
    category_id: Optional[int] = Field(None, description="目录分类ID")
    source: Optional[str] = Field(None, description="来源")


class KnowledgeDocResponse(BaseModel):
    """知识库文档响应模型"""
    id: int
    category_id: Optional[int] = None
    title: str
    content: Optional[str] = None
    source: Optional[str] = None
    is_active: bool = True
    created_at: Optional[str] = None
    
    class Config:
        from_attributes = True


# ============ 通用响应模型 ============

from typing import Generic, TypeVar

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    """通用响应模型"""
    code: int = 200
    message: str = ""
    data: Optional[T] = None
