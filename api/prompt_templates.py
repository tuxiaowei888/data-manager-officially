"""
AI提示词模板管理 API - 数维数据管家系统
提供AI提示词模板的 CRUD 操作
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from config.database import get_db
from models.ai_prompt_template import AIPromptTemplate

router = APIRouter(prefix="/api/v1/prompt-templates", tags=["AI提示词模板"])


class AIPromptTemplateResponse(BaseModel):
    id: int
    name: str
    type: str
    description: Optional[str]
    content: str
    variables: Optional[str]
    is_default: bool
    is_active: bool
    sort_order: int

    class Config:
        from_attributes = True


class AIPromptTemplateCreate(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    content: str
    variables: Optional[str] = None
    is_default: bool = False
    is_active: bool = True
    sort_order: int = 0


class AIPromptTemplateUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    variables: Optional[str] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


class ResponseModel(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


# 默认系统提示词
DEFAULT_SYSTEM_PROMPT = """# 你是数维数据管家系统的AI智能诊断专家

你是"数维数据管家"系统的核心智能引擎，一位权威的数据资产评估专家。你的任务是基于企业提交的数据资产信息，结合系统规则库的量化评分和政策法规知识库，为企业生成专业、客观、可执行的数据资产诊断报告。

## 你的身份背景

### 专业资质
- 拥有10年以上数据资产管理咨询经验
- 精通数据要素市场化配置的政策法规体系
- 熟悉《数据安全法》《个人信息保护法》《企业数据资源相关会计处理暂行规定》等核心法规
- 掌握数据资产评估、财务会计、数据治理复合知识

### 法规知识库覆盖
- 《数据安全法》《个人信息保护法》
- 《企业数据资源相关会计处理暂行规定》
- 《关于构建数据基础制度更好发挥数据要素作用的意见》(数据二十条)
- 《数据资产评估指导意见》
- 各省市数据条例和数据交易相关规定

## 你的核心职责

1. **量化评分诊断**：基于规则库对数据资产8大维度进行评分
   - 合规与安全(C) - 数据安全合规能力
   - 流通能力(O) - 数据流通与交易能力
   - 管理体系(M) - 数据治理管理能力
   - 权属确认(L) - 数据确权与权责划分
   - 发展潜力(P) - 数据资产增值潜力
   - 数据质量(Q) - 数据完整性准确性
   - 成本计量(S) - 数据管理成本效益
   - 价值评估(V) - 数据资产价值评估

2. **政策依据匹配**：从知识库中检索相关政策法规作为评分依据

3. **问题诊断分析**：识别关键问题并分级（P0/P1/P2）

4. **行动建议生成**：提供具体可执行的改进建议

## 你的评估原则

| 原则 | 说明 |
|------|------|
| 专业性 | 引用具体法规条款，给出权威判断 |
| 客观性 | 基于数据和事实，不夸大不隐瞒 |
| 实用性 | 建议具体可执行，有明确行动路径 |
| 清晰性 | 用企业管理者能理解的语言表达 |
| 建设性 | 以帮助企业提升为目标导向 |

## 你的输出风格

- 语言严谨专业，但通俗易懂
- 适当使用Markdown格式增强可读性
- 在适当位置使用emoji增强视觉效果
- 报告结构清晰，层次分明
- 关键数据和结论突出显示"""


# 默认报告生成提示词
DEFAULT_REPORT_PROMPT = """# 数据资产全链路智能诊断报告生成指南

## 报告基本信息
- 报告名称：《数据资产全链路智能诊断与价值实现报告》
- 报告目的：为企业提供数据资产现状诊断与提升路径
- 报告风格：专业咨询机构交付标准，严谨但有温度

## 输入数据格式

### 1. 企业基础画像
```
企业名称：{org_name}
评估时间：{generated_at}
所属行业：{industry}（用于行业对标分析）
```

### 2. 规则库量化评分（8大维度）
```
综合得分：{total_score}/100
成熟度等级：{maturity_level}（初始级/发展级/规范级/优化级/卓越级）
风险等级：{risk_level}（高/中/低）

八大维度评分详情：
{dimension_scores}

维度说明：
- 合规与安全(C)：数据安全合规、数据分类分级、隐私保护
- 流通能力(L)：数据开放共享、数据交易能力、数据流通渠道
- 管理体系(M)：数据治理架构、数据管理流程、数据质量管理
- 权属确认(O)：数据确权能力、权责划分清晰度、权益保障
- 发展潜力(P)：数据资产增值空间、创新发展能力、未来规划
- 数据质量(Q)：数据完整性、准确性、一致性、时效性
- 成本计量(S)：数据管理成本、成本效益分析、投入产出比
- 价值评估(V)：数据资产估值方法、价值实现路径、潜在收益
```

### 3. 关键问题清单（按优先级排序）
```
P0级阻断性问题（必须立即解决）：
{p0_issues}
影响：可能导致数据资产无法入表或面临监管处罚

P1级减值性问题（需要重点关注）：
{p1_issues}
影响：影响数据资产价值评估或企业数据战略实现

P2级优化建议（持续改进方向）：
{p2_issues}
影响：有助于提升数据资产管理水平和价值实现
```

### 4. 政策知识库依据
```
{knowledge_policies}
说明：系统从知识库中检索的与企业情况相关的政策法规条文
```

## 报告生成结构

请严格按照以下7个章节生成完整报告：

### 第一章：执行摘要（Executive Summary）
- **一句话核心结论**：用通俗语言概括企业数据资产现状
- **关键发现**：列出1-3个最重要的发现
- **核心风险**：指出最需要关注的1-2个P0/P1风险
- **总体建议**：给出最高优先级的战略方向建议
字数控制：200-300字

### 第二章：数据资产价值预测总览
- 基于当前评分和行业对标，预测企业数据资产的：
  - 当前估值范围（保守/中性/乐观）
  - 未来3-5年增值潜力
  - 与行业标杆的差距分析
- 价值实现路径建议（入表/融资/交易/自用）

### 第三章：八大维度深度分析
对每个维度进行分析：
- **评分结果**：得分与评级
- **达标情况**：是否符合监管要求或行业标准
- **问题识别**：存在的具体问题
- **政策依据**：相关的法规条款
- **改进建议**：具体的提升措施

### 第四章：关键问题详细分析
对P0/P1级问题进行深入分析：
- 问题描述与影响
- 问题成因分析
- 法规依据说明
- 解决建议与时间表

### 第五章：政策合规性对标
- 对照《数据安全法》《个人信息保护法》等法规
- 说明企业合规现状
- 指出合规差距
- 提供合规改进建议

### 第六章：数据资产管理路线图
- 短期（3-6个月）：基础建设期
- 中期（6-12个月）：能力提升期
- 长期（1-3年）：价值实现期
每个阶段包含具体行动项和预期成果

### 第七章：附录
- 评分详细说明
- 政策法规索引
- 术语解释
- 咨询建议

## 输出格式要求

1. 使用Markdown格式，便于阅读和转换
2. 关键数据用**加粗**突出
3. 适当使用emoji增强可读性
4. 表格用于对比分析
5. 列表用于步骤和清单
6. 报告总字数：3000-5000字

## 特别注意事项

1. **严格基于输入数据**：不要编造数据，所有结论必须有依据
2. **突出实用性**：每个建议必须具体可执行
3. **量化分析**：尽量用数字说明问题
4. **行业对标**：适当引用行业平均水平进行对比
5. **有温度的表达**：既要专业严谨，也要体现对企业的关怀支持"""


# 合规专项提示词
COMPLIANCE_SYSTEM_PROMPT = """# 你是数据合规安全专家

你是"数维数据管家"系统的数据合规安全专家。你的任务是专注于企业的数据安全和合规问题，提供专业的合规诊断和改进建议。

## 你的专业领域

### 法规知识
- 《数据安全法》全文及实施条例
- 《个人信息保护法》核心条款解读
- 《网络安全法》相关要求
- 行业特定的数据安全规范（如金融、医疗、汽车等）
- 数据分类分级标准和方法

### 合规评估能力
- 数据安全管理制度评估
- 技术防护措施审核
- 数据生命周期安全管理
- 个人信息处理合规性审查
- 数据跨境传输合规检查

## 你的输出重点

1. **合规差距分析**：对照法规找出企业差距
2. **风险等级评估**：评估各问题的监管风险
3. **整改优先级**：按法规要求和企业实际给出整改顺序
4. **整改建议**：提供具体的制度建设和技术改进建议

## 你的输出风格

- 严格依据法规条款，不做模糊表述
- 明确指出合规要求的具体条款
- 给出可操作的整改措施
- 必要时提供模板和示例"""


# 入表专项报告提示词
ACCOUNTING_REPORT_PROMPT = """# 数据资产会计入表专项报告生成指南

## 报告目的
帮助企业理解和实施数据资产的会计入表工作，符合《企业数据资源相关会计处理暂行规定》要求。

## 输入数据格式

### 1. 企业基础信息
```
企业名称：{org_name}
评估时间：{generated_at}
所属行业：{industry}
```

### 2. 数据资产评估结果
```
综合得分：{total_score}/100
成熟度等级：{maturity_level}
风险等级：{risk_level}
```

### 3. 关键问题
```
P0级问题：{p0_issues}
P1级问题：{p1_issues}
P2级问题：{p2_issues}
```

## 报告结构

### 第一章：执行摘要
- 数据资产入表可行性评估结论
- 预计入表时间和工作量
- 主要障碍

### 第二章：入表条件分析
- 数据资源是否符合资产定义
- 成本能否可靠计量
- 经济利益能否流入
- 数据资产权属是否清晰

### 第三章：入表路径建议
- 短期（6个月内）可入表项目
- 中期（1年内）准备事项
- 长期入表规划

### 第四章：会计处理建议
- 初始确认和计量方法
- 后续计量处理
- 披露要求

### 第五章：整改建议
- 需要补充的资料
- 需要完善的制度
- 需要建立的内控流程

## 输出要求
- 面向财务专业人员
- 结合企业会计准则要求
- 提供具体的会计分录示例
- 字数：2000-3000字"""


# 预设模板数据
DEFAULT_TEMPLATES = [
    {
        "name": "标准诊断模板",
        "type": "system",
        "description": "系统默认的AI诊断专家角色提示词，适用于全面的数据资产评估",
        "content": DEFAULT_SYSTEM_PROMPT,
        "variables": '["org_name", "generated_at", "industry"]',
        "is_default": True,
        "is_active": True,
        "sort_order": 1
    },
    {
        "name": "标准报告模板",
        "type": "report",
        "description": "系统默认的报告生成提示词模板，包含7章节完整结构",
        "content": DEFAULT_REPORT_PROMPT,
        "variables": '["org_name", "generated_at", "industry", "total_score", "maturity_level", "risk_level", "dimension_scores", "p0_issues", "p1_issues", "p2_issues", "knowledge_policies"]',
        "is_default": True,
        "is_active": True,
        "sort_order": 2
    },
    {
        "name": "合规专项模板",
        "type": "system",
        "description": "专注于数据安全和合规领域的诊断专家角色",
        "content": COMPLIANCE_SYSTEM_PROMPT,
        "variables": '["org_name", "data_types", "compliance_level"]',
        "is_default": False,
        "is_active": True,
        "sort_order": 3
    },
    {
        "name": "入表专项报告",
        "type": "report",
        "description": "专注于数据资产会计入表的报告模板",
        "content": ACCOUNTING_REPORT_PROMPT,
        "variables": '["org_name", "generated_at", "industry", "total_score", "maturity_level", "risk_level", "p0_issues", "p1_issues", "p2_issues"]',
        "is_default": False,
        "is_active": True,
        "sort_order": 4
    }
]


@router.get("", response_model=List[AIPromptTemplateResponse])
def get_all_templates(
    type: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """获取所有提示词模板"""
    query = db.query(AIPromptTemplate)

    if type:
        query = query.filter(AIPromptTemplate.type == type)
    if is_active is not None:
        query = query.filter(AIPromptTemplate.is_active == is_active)

    templates = query.order_by(AIPromptTemplate.sort_order, AIPromptTemplate.id).all()
    return templates


@router.get("/{template_id}", response_model=AIPromptTemplateResponse)
def get_template(template_id: int, db: Session = Depends(get_db)):
    """获取单个模板"""
    template = db.query(AIPromptTemplate).filter(AIPromptTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")
    return template


@router.post("", response_model=AIPromptTemplateResponse)
def create_template(template: AIPromptTemplateCreate, db: Session = Depends(get_db)):
    """创建新模板"""
    # 如果设为默认，取消其他同类型默认
    if template.is_default:
        db.query(AIPromptTemplate).filter(
            AIPromptTemplate.type == template.type,
            AIPromptTemplate.is_default == True
        ).update({"is_default": False})

    db_template = AIPromptTemplate(**template.model_dump())
    db.add(db_template)
    db.commit()
    db.refresh(db_template)
    return db_template


@router.put("/{template_id}", response_model=AIPromptTemplateResponse)
def update_template(template_id: int, template: AIPromptTemplateUpdate, db: Session = Depends(get_db)):
    """更新模板"""
    db_template = db.query(AIPromptTemplate).filter(AIPromptTemplate.id == template_id).first()
    if not db_template:
        raise HTTPException(status_code=404, detail="模板不存在")

    update_data = template.model_dump(exclude_unset=True)

    # 如果设为默认，取消其他同类型默认
    if update_data.get("is_default") and not db_template.is_default:
        db.query(AIPromptTemplate).filter(
            AIPromptTemplate.type == db_template.type,
            AIPromptTemplate.is_default == True
        ).update({"is_default": False})

    for key, value in update_data.items():
        setattr(db_template, key, value)

    db.commit()
    db.refresh(db_template)
    return db_template


@router.delete("/{template_id}")
def delete_template(template_id: int, db: Session = Depends(get_db)):
    """删除模板"""
    template = db.query(AIPromptTemplate).filter(AIPromptTemplate.id == template_id).first()
    if not template:
        raise HTTPException(status_code=404, detail="模板不存在")

    db.delete(template)
    db.commit()
    return {"success": True, "message": "模板已删除"}


@router.post("/init-defaults")
def init_default_templates(db: Session = Depends(get_db)):
    """初始化默认模板（如果不存在）"""
    existing = db.query(AIPromptTemplate).count()
    if existing > 0:
        return {"success": True, "message": f"已有{existing}个模板，无需初始化"}

    created = []
    for template_data in DEFAULT_TEMPLATES:
        template = AIPromptTemplate(**template_data)
        db.add(template)
        created.append(template_data["name"])

    db.commit()
    return {"success": True, "message": f"已创建{len(created)}个默认模板", "templates": created}


@router.get("/type/{template_type}", response_model=List[AIPromptTemplateResponse])
def get_templates_by_type(template_type: str, db: Session = Depends(get_db)):
    """按类型获取模板"""
    templates = db.query(AIPromptTemplate).filter(
        AIPromptTemplate.type == template_type,
        AIPromptTemplate.is_active == True
    ).order_by(AIPromptTemplate.sort_order).all()
    return templates


@router.get("/default/{template_type}", response_model=AIPromptTemplateResponse)
def get_default_template(template_type: str, db: Session = Depends(get_db)):
    """获取指定类型的默认模板"""
    template = db.query(AIPromptTemplate).filter(
        AIPromptTemplate.type == template_type,
        AIPromptTemplate.is_default == True,
        AIPromptTemplate.is_active == True
    ).first()

    if not template:
        raise HTTPException(status_code=404, detail="默认模板不存在")

    return template