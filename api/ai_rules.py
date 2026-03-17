"""
AI 规则生成 API - 数维数据管家系统
V2.0 预留接口，V1.0 阶段返回占位响应
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from schemas import ResponseModel
from typing import List

router = APIRouter(prefix="/api/v1/rules", tags=["AI 规则生成"])


@router.post("/ai-generate", response_model=ResponseModel)
async def ai_generate_rule(file: UploadFile = File(...)):
    """
    AI 生成规则 - V2.0 功能
    
    V1.0 阶段：接收文件参数，直接返回 "Coming Soon" 提示
    
    V2.0 规划：
    1. 用户上传 PDF 政策文档
    2. LLM 解析文档内容
    3. 自动生成 JSON 规则
    4. 提交审核
    """
    # V1.0 占位实现 - 不调用任何 LLM API
    return ResponseModel(
        status="coming_soon",
        message="V2.0 功能：AI 规则自动生成即将上线",
        data={
            "feature": "ai-generate",
            "version": "V2.0",
            "description": "上传政策文档后，AI 将自动解析并生成评价规则"
        }
    )


@router.post("/ai-batch-generate", response_model=ResponseModel)
async def ai_batch_generate_rules(files: List[UploadFile] = File(...)):
    """
    批量 AI 生成规则 - V2.0 功能
    
    V1.0 阶段：返回占位提示
    """
    return ResponseModel(
        status="coming_soon",
        message="V2.0 功能：批量 AI 规则生成即将上线",
        data={
            "feature": "ai-batch-generate",
            "version": "V2.0"
        }
    )


@router.get("/ai-status", response_model=ResponseModel)
def get_ai_generation_status():
    """
    获取 AI 生成状态 - V2.0 功能
    
    V1.0 阶段：返回占位提示
    """
    return ResponseModel(
        status="coming_soon",
        message="V2.0 功能：AI 生成状态查询即将上线",
        data={
            "feature": "ai-status",
            "version": "V2.0"
        }
    )
