# 数维数据管家系统 (ShuWei Data Manager)

## 系统规格说明书 (System Specification Document)

| 版本 | 日期 | 作者 | 状态 |
|------|------|------|------|
| 1.0.0 | 2026-03-25 | 数维创擎 | 草稿 |

---

## 1. 项目概述

### 1.1 项目背景

数维数据管家系统是一款**SaaS 化数据资产评价平台**，旨在为企业提供专业、权威、可落地的数据资产评估服务。系统基于国家数据要素市场化政策，结合《数据安全法》《个人信息保护法》《企业数据资源相关会计处理暂行规定》等法规，构建了一套完整的数据资产评价体系。

### 1.2 项目目标

- **核心价值**: 帮助企业实现从"合规"到"入表"再到"融资/交易"的全链路数据资产管理
- **目标用户**: 需要进行数据资产评价的企业客户、渠道合作伙伴、系统管理员
- **核心功能**: 规则化评分、AI智能报告生成、知识库检索、VIP会员管理

### 1.3 系统范围

```
┌─────────────────────────────────────────────────────────────┐
│                        数维数据管家系统                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Web管理后台  │  │  微信小程序  │  │   FastAPI REST API  │  │
│  │  (admin-new) │  │ (miniprogram)│  │      (Backend)      │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│           │              │                   │              │
│           └──────────────┴───────────────────┘              │
│                          │                                   │
│                    MySQL Database                            │
│                  (Docker Container)                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 技术架构

### 2.1 技术栈概览

| 层级 | 技术选型 | 说明 |
|------|----------|------|
| **后端框架** | FastAPI 0.109+ | 高性能异步Python Web框架 |
| **数据库** | MySQL 8.0 (Docker: my-mysql) | 关系型数据存储 |
| **ORM** | SQLAlchemy 2.0 | 数据库抽象层 |
| **认证** | JWT (PyJWT) + bcrypt | 无状态认证 |
| **向量存储** | ChromaDB | 知识库向量检索 ✅ 已集成 |
| **AI服务** | 多Provider支持 | OpenAI/Anthropic/智谱/通义千问/DeepSeek |
| **前端** | 原生HTML/CSS/JS | 轻量级管理后台 |
| **小程序** | 微信小程序 | 客户评估入口 |
| **PDF生成** | ReportLab | 报告文档导出 |

### 2.2 项目结构

```
e:\数维创擎\代码库\数维数据管家系统/
│
├── main.py                      # FastAPI 应用入口
├── config/
│   ├── database.py              # 数据库连接配置
│   └── logging_config.py        # 日志配置
│
├── models/                       # SQLAlchemy 数据模型
│   ├── user.py                   # 用户模型
│   ├── channel.py                # 渠道模型
│   ├── rule_config.py            # 规则配置模型
│   ├── evaluation_result.py      # 评价结果模型
│   ├── knowledge_doc.py          # 知识库文档模型
│   ├── knowledge_category.py     # 知识库分类模型
│   ├── ai_config.py              # AI配置模型
│   ├── ai_prompt_template.py     # AI提示词模板模型
│   └── system_config.py          # 系统配置模型
│
├── api/                          # REST API 路由
│   ├── auth.py                   # 认证API
│   ├── rules.py                  # 规则管理API
│   ├── evaluation.py             # 评价服务API
│   ├── knowledge.py              # 知识库API
│   ├── reports.py                # 报告API
│   ├── users.py                  # 用户管理API
│   ├── customers.py              # 客户管理API
│   ├── channel.py                # 渠道API
│   ├── ai_config.py              # AI配置API
│   ├── ai_rules.py               # AI规则API
│   └── permissions.py            # 权限API
│
├── schemas/                      # Pydantic 数据模型
│   ├── auth.py
│   └── __init__.py
│
├── services/                     # 业务逻辑层
│   ├── evaluation.py             # 评价计算服务
│   ├── rule_calculator.py        # 规则计算引擎
│   ├── vip_service.py            # VIP服务
│   ├── ai_service.py             # AI服务
│   ├── pdf_service.py            # PDF生成服务
│   ├── report_generator.py       # 报告生成服务
│   ├── vector_store.py           # 向量存储服务
│   └── policy_retriever.py       # 政策检索服务
│
├── frontend/                     # Web 管理后台
│   ├── admin-new/                # 新版管理后台
│   │   ├── pages/                # 页面模块
│   │   ├── css/                  # 样式文件
│   │   └── js/                   # 脚本文件
│   ├── admin.html                # 管理后台首页
│   ├── login.html                # 登录页面
│   ├── home.html                 # 用户首页
│   ├── rules.html                # 规则库页面
│   ├── knowledge.html            # 知识库页面
│   └── ...                       # 其他HTML页面
│
├── miniprogram/                  # 微信小程序
│   ├── app.js                    # 小程序入口
│   ├── app.json                  # 小程序配置
│   ├── api/
│   │   └── api.js               # API封装
│   └── pages/
│       ├── index/                # 首页/登录
│       ├── form/                 # 评估表单
│       ├── report/               # 报告查看
│       └── profile/              # 个人中心
│
├── scripts/                      # 工具脚本
│   ├── full_init_db.py          # 数据库初始化
│   ├── init_knowledge_categories.py
│   └── create_admin.py
│
├── .trae/skills/                # AI助手技能库
│   ├── miniprogram-*/           # 小程序开发技能
│   ├── ui-ux-pro-max/           # UI/UX设计技能
│   └── ...                       # 其他辅助技能
│
└── tests/                        # 测试文件
    ├── test_api.py
    └── quick_test.py
```

---

## 3. 数据库设计

### 3.1 实体关系图 (ERD)

```
┌─────────────────┐       ┌─────────────────┐
│    channels     │       │     users       │
│─────────────────│       │─────────────────│
│ id (PK)         │◄──────│ channel_id (FK) │
│ channel_name    │       │ id (PK)         │
│ channel_code    │       │ username        │
│ contact_person  │       │ password_hash   │
│ contact_phone   │       │ email           │
│ referred_users  │       │ user_type       │
│ is_active       │       │ is_vip          │
└─────────────────┘       │ vip_expire_date │
                          │ daily_eval_count│
                          │ daily_eval_date │
                          └────────┬────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
                    ▼              ▼              ▼
         ┌─────────────────┐ ┌───────────┐ ┌─────────────────┐
         │ evaluation_     │ │ ai_configs│ │ai_prompt_templa │
         │ results         │ │           │ │tes              │
         │─────────────────│ │───────────│ │─────────────────│
         │ id (PK)         │ │ id (PK)   │ │ id (PK)         │
         │ user_id (FK)    │ │ config_   │ │ name            │
         │ report_id       │ │ name      │ │ type            │
         │ org_name        │ │ provider  │ │ content         │
         │ total_score     │ │ api_key   │ │ is_default      │
         │ maturity_level  │ │ model_    │ │ is_active       │
         │ risk_level      │ │ name      │ └─────────────────┘
         │ detail_json     │ │ is_active │
         │ report_pdf_url │ │ is_default│
         └─────────────────┘ └───────────┘
                    │
                    ▼
         ┌─────────────────────────────────┐
         │         rule_configs           │
         │─────────────────────────────────│
         │ id (PK)                        │
         │ dimension_code                 │
         │ rule_name                      │
         │ logic_expression               │
         │ weight                         │
         │ risk_threshold                 │
         │ is_active                      │
         │ is_deleted                     │
         │ source_type                    │
         │ version                        │
         └─────────────────────────────────┘

         ┌─────────────────────────────────┐
         │       knowledge_docs           │
         │─────────────────────────────────│
         │ id (PK)                        │
         │ category_id (FK)               │
         │ title                          │
         │ content                        │
         │ doc_type                       │
         │ tags (JSON)                    │
         │ source                         │
         │ is_active                      │
         └─────────────────────────────────┘
                    ▲
                    │
         ┌─────────────────────────────────┐
         │    knowledge_categories         │
         │─────────────────────────────────│
         │ id (PK)                        │
         │ name                           │
         │ parent_id                       │
         │ description                    │
         │ icon                           │
         │ sort_order                     │
         │ is_active                      │
         └─────────────────────────────────┘
```

### 3.2 数据表详细说明

#### 3.2.1 users (用户表)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INT | PK, AUTO_INCREMENT | 用户ID |
| username | VARCHAR(50) | UNIQUE, NOT NULL | 用户名 |
| password_hash | VARCHAR(255) | NOT NULL | 密码哈希(bcrypt) |
| email | VARCHAR(100) | UNIQUE, NULL | 邮箱 |
| phone | VARCHAR(20) | NULL | 手机号 |
| referrer_code | VARCHAR(20) | INDEX, NULL | 推荐码 |
| channel_id | INT | FK -> channels.id, NULL | 渠道ID |
| user_type | VARCHAR(20) | DEFAULT 'client' | 用户类型: client/admin |
| is_vip | BOOLEAN | DEFAULT FALSE | 是否VIP |
| vip_expire_date | DATE | NULL | VIP过期日期 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否启用 |
| last_login_at | DATETIME | NULL | 最后登录时间 |
| daily_eval_count | INT | DEFAULT 0 | 每日评估计数 |
| daily_eval_date | DATE | NULL | 每日评估日期 |
| created_at | DATETIME | DEFAULT NOW() | 创建时间 |
| updated_at | DATETIME | ON UPDATE NOW() | 更新时间 |

#### 3.2.2 channels (渠道表)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INT | PK | 渠道ID |
| channel_name | VARCHAR(100) | NOT NULL | 渠道名称 |
| channel_code | VARCHAR(20) | UNIQUE, INDEX | 推荐码 |
| contact_person | VARCHAR(50) | NULL | 联系人 |
| contact_phone | VARCHAR(20) | NULL | 联系电话 |
| referred_users_count | INT | DEFAULT 0 | 推荐用户数 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否启用 |
| remark | TEXT | NULL | 备注 |
| created_at | DATETIME | DEFAULT NOW() | 创建时间 |
| updated_at | DATETIME | ON UPDATE NOW() | 更新时间 |

#### 3.2.3 rule_configs (规则配置表)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INT | PK | 规则ID |
| dimension_code | VARCHAR(50) | INDEX, NOT NULL | 维度代码 |
| rule_name | VARCHAR(200) | NOT NULL | 规则名称 |
| rule_description | TEXT | NULL | 规则描述 |
| logic_expression | TEXT | NOT NULL | 计算逻辑表达式 |
| weight | FLOAT | NOT NULL, DEFAULT 1.0 | 权重(百分比) |
| risk_threshold | FLOAT | NOT NULL, DEFAULT 60.0 | 风险触发阈值 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否启用 |
| is_deleted | BOOLEAN | DEFAULT FALSE | 软删除标记 |
| source_type | VARCHAR(20) | DEFAULT 'manual' | 来源: manual/ai_generated/imported |
| version | INT | DEFAULT 1 | 版本号 |
| ai_prompt_context | TEXT | NULL | AI生成上下文 |
| created_at | DATETIME | DEFAULT NOW() | 创建时间 |
| updated_at | DATETIME | ON UPDATE NOW() | 更新时间 |

#### 3.2.4 evaluation_results (评价结果表)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INT | PK | 结果ID |
| user_id | INT | FK -> users.id, INDEX | 用户ID |
| report_id | VARCHAR(100) | UNIQUE, INDEX | 报告唯一ID |
| org_name | VARCHAR(200) | NULL | 机构名称 |
| total_score | FLOAT | NOT NULL | 总分 |
| maturity_level | VARCHAR(50) | NULL | 成熟度等级 |
| compliance_score | FLOAT | NULL | 合规性得分 |
| quality_score | FLOAT | NULL | 数据质量得分 |
| rights_score | FLOAT | NULL | 权属确认得分 |
| value_score | FLOAT | NULL | 价值评估得分 |
| cost_score | FLOAT | NULL | 成本计量得分 |
| p0_issues | JSON | NULL | P0级问题列表 |
| p1_issues | JSON | NULL | P1级问题列表 |
| p2_issues | JSON | NULL | P2级问题列表 |
| detail_json | JSON | NOT NULL | 各维度得分详情 |
| risk_level | VARCHAR(10) | NOT NULL | 风险等级 |
| report_pdf_url | VARCHAR(500) | NULL | PDF报告URL |
| report_word_url | VARCHAR(500) | NULL | Word报告URL |
| engine_version | VARCHAR(50) | DEFAULT 'v1_static' | 计算引擎版本 |
| ai_analysis_log | JSON | NULL | AI分析日志(V2.0预留) |
| created_at | DATETIME | DEFAULT NOW() | 创建时间 |

#### 3.2.5 knowledge_docs (知识库文档表)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INT | PK | 文档ID |
| category_id | INT | FK -> knowledge_categories.id | 分类ID |
| display_order | INT | DEFAULT 0 | 显示排序 |
| doc_type | VARCHAR(50) | NULL | 文档类型 |
| title | VARCHAR(500) | NOT NULL | 文档标题 |
| content | TEXT | NULL | 文档内容 |
| tags | JSON | NULL | 标签数组 |
| source | VARCHAR(200) | NULL | 来源 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否启用 |
| created_at | TIMESTAMP | NULL | 创建时间 |
| updated_at | TIMESTAMP | NULL | 更新时间 |

#### 3.2.6 knowledge_categories (知识库分类表)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INT | PK | 分类ID |
| name | VARCHAR(100) | NOT NULL | 分类名称 |
| parent_id | INT | NULL | 父分类ID |
| description | TEXT | NULL | 分类描述 |
| icon | VARCHAR(50) | NULL | 分类图标 |
| sort_order | INT | DEFAULT 0 | 排序顺序 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否启用 |
| created_at | DATETIME | DEFAULT NOW() | 创建时间 |
| updated_at | DATETIME | ON UPDATE NOW() | 更新时间 |

#### 3.2.7 ai_configs (AI配置表)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INT | PK | 配置ID |
| config_name | VARCHAR(100) | NOT NULL | 配置名称 |
| provider | VARCHAR(50) | NOT NULL | AI提供商 |
| api_key | VARCHAR(255) | NULL | API密钥 |
| api_base_url | VARCHAR(255) | NULL | API基础URL |
| model_name | VARCHAR(100) | NOT NULL | 模型名称 |
| temperature | FLOAT | DEFAULT 0.7 | 温度参数 |
| max_tokens | INT | DEFAULT 4096 | 最大token数 |
| system_prompt | TEXT | NULL | 系统提示词 |
| report_prompt_template | TEXT | NULL | 报告生成提示词模板 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否启用 |
| is_default | BOOLEAN | DEFAULT FALSE | 是否默认配置 |
| created_at | DATETIME | DEFAULT NOW() | 创建时间 |
| updated_at | DATETIME | ON UPDATE NOW() | 更新时间 |

#### 3.2.8 ai_prompt_templates (AI提示词模板表)

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | INT | PK | 模板ID |
| name | VARCHAR(100) | NOT NULL | 模板名称 |
| type | VARCHAR(20) | NOT NULL | 模板类型 |
| description | TEXT | NULL | 模板描述 |
| content | TEXT | NOT NULL | 模板内容 |
| variables | TEXT | NULL | 模板变量JSON |
| is_default | BOOLEAN | DEFAULT FALSE | 是否默认 |
| is_active | BOOLEAN | DEFAULT TRUE | 是否启用 |
| sort_order | INT | DEFAULT 0 | 排序顺序 |
| created_at | DATETIME | DEFAULT NOW() | 创建时间 |
| updated_at | DATETIME | ON UPDATE NOW() | 更新时间 |

---

## 4. API 接口规范

### 4.1 API 基础信息

- **Base URL**: `http://localhost:8000/api/v1`
- **认证方式**: JWT Bearer Token
- **内容类型**: `application/json`
- **文档地址**: `/docs` (Swagger UI) | `/redoc` (ReDoc)

### 4.2 认证接口

#### POST /auth/register - 用户注册

**Request:**
```json
{
  "username": "string (3-50字符)",
  "password": "string (最少6字符)",
  "email": "string (可选)",
  "phone": "string (可选)",
  "referrer_code": "string (可选)"
}
```

**Response (200):**
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "user_type": "client",
    "is_vip": false,
    "referrer_code": "CODE123",
    "channel_id": 1,
    "created_at": "2026-03-25T10:00:00"
  }
}
```

#### POST /auth/login - 用户登录

**Request (Form Data):**
```
username: string
password: string
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 604800,
  "user_type": "client",
  "username": "testuser"
}
```

#### GET /auth/me - 获取当前用户信息

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "phone": "13800138000",
    "user_type": "client",
    "is_vip": true,
    "channel_id": 1,
    "channel_name": "渠道A",
    "last_login_at": "2026-03-25T10:00:00",
    "created_at": "2026-03-01T00:00:00"
  }
}
```

### 4.3 评价服务接口

#### GET /evaluation/vip-status - 获取VIP状态

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "can_evaluate": true,
  "remaining": 5,
  "is_vip": true,
  "message": "今日剩余评估次数: 5"
}
```

#### POST /evaluation/evaluate - 执行评估

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "form_data": {
    "org_name": "测试企业",
    "industry": "互联网",
    "data_volume": 1000000,
    "compliance_score": 80,
    "quality_score": 75,
    ...
  }
}
```

**Response (200):**
```json
{
  "report_id": "RPTABC123DEF456",
  "org_name": "测试企业",
  "total_score": 78.5,
  "maturity_level": "L3-规范级",
  "dimensions": [
    {
      "code": "C",
      "name": "合规与安全",
      "score": 82.0,
      "weight": 20,
      "issues": []
    }
  ],
  "p0_issues": [],
  "p1_issues": [
    {
      "rule_name": "数据分类分级",
      "description": "企业未建立完善的数据分类分级制度",
      "suggestion": "建议参照《数据安全法》建立分类分级制度"
    }
  ],
  "p2_issues": [],
  "risk_level": "P1",
  "generated_at": "2026-03-25T10:30:00"
}
```

#### GET /evaluation/{result_id} - 获取评估结果

#### GET /evaluation/{result_id}/download - 下载PDF报告

#### GET /evaluation/history - 获取评估历史

#### DELETE /evaluation/{result_id} - 删除评估结果

### 4.4 规则管理接口

#### GET /rules/dimensions - 获取所有维度

**Response (200):**
```json
[
  {"code": "C", "name": "合规与安全", "color": "#FF6B6B", "weight": 20},
  {"code": "Q", "name": "数据质量", "color": "#4ECDC4", "weight": 15},
  {"code": "O", "name": "权属确认", "color": "#96CEB4", "weight": 15},
  {"code": "V", "name": "价值评估", "color": "#45B7D1", "weight": 20},
  {"code": "M", "name": "管理体系", "color": "#9B59B6", "weight": 10},
  {"code": "L", "name": "流通能力", "color": "#FFEAA7", "weight": 10},
  {"code": "P", "name": "发展潜力", "color": "#DDA0DD", "weight": 5},
  {"code": "S", "name": "成本计量", "color": "#3498DB", "weight": 5}
]
```

#### GET /rules - 获取规则列表 (分页)

**Query Parameters:**
- `dimension`: 维度代码筛选
- `is_active`: 是否启用筛选
- `keyword`: 关键词搜索
- `page`: 页码 (默认1)
- `page_size`: 每页数量 (默认50)
- `sort_by`: 排序字段
- `sort_order`: 排序方向 (asc/desc)

#### POST /rules - 创建规则 (Admin)

#### PUT /rules/{rule_id} - 更新规则 (Admin)

#### DELETE /rules/{rule_id} - 删除规则 (Admin)

#### POST /rules/{rule_id}/toggle - 切换启用状态 (Admin)

#### POST /rules/{rule_id}/validate - 验证规则表达式

### 4.5 知识库接口

#### GET /knowledge - 获取文档列表

#### GET /knowledge/{doc_id} - 获取文档详情

#### POST /knowledge - 创建文档 (Admin)

#### PUT /knowledge/{doc_id} - 更新文档 (Admin)

#### DELETE /knowledge/{doc_id} - 删除文档 (Admin)

#### GET /knowledge/categories - 获取分类列表

### 4.6 AI配置接口

#### GET /ai-config - 获取AI配置列表

#### POST /ai-config - 创建AI配置 (Admin)

#### PUT /ai-config/{config_id} - 更新AI配置 (Admin)

#### DELETE /ai-config/{config_id} - 删除AI配置 (Admin)

### 4.7 错误响应格式

```json
{
  "detail": {
    "code": "ERROR_CODE",
    "message": "错误描述信息",
    "field": "具体字段(可选)"
  }
}
```

**常见错误码:**

| HTTP Status | Code | 说明 |
|-------------|------|------|
| 400 | BAD_REQUEST | 请求参数错误 |
| 401 | UNAUTHORIZED | 未授权/Token无效 |
| 403 | FORBIDDEN | 权限不足 |
| 404 | NOT_FOUND | 资源不存在 |
| 429 | RATE_LIMITED | 请求过于频繁 |
| 500 | INTERNAL_ERROR | 服务器内部错误 |

---

## 5. 核心业务逻辑

### 5.1 八维评价体系

系统采用**八维评价模型**对数据资产进行全面评估：

| 维度代码 | 维度名称 | 权重 | 说明 |
|----------|----------|------|------|
| C | 合规与安全 | 20% | 数据安全合规性 |
| Q | 数据质量 | 15% | 数据完整性、准确性 |
| O | 权属确认 | 15% | 数据确权法律依据 |
| V | 价值评估 | 20% | 数据资产价值 |
| M | 管理体系 | 10% | 数据管理制度 |
| L | 流通能力 | 10% | 数据流通可行性 |
| P | 发展潜力 | 5% | 数据增长潜力 |
| S | 成本计量 | 5% | 数据成本核算 |

### 5.2 成熟度等级

| 等级 | 分数区间 | 说明 |
|------|----------|------|
| L1-初始级 | 0-40 | 仅有基本数据管理 |
| L2-管理级 | 40-60 | 建立初步管理制度 |
| L3-规范级 | 60-75 | 规范化管理体系 |
| L4-优化级 | 75-90 | 持续优化改进 |
| L5-卓越级 | 90-100 | 行业标杆 |

### 5.3 风险等级

| 风险等级 | 说明 | 触发条件 |
|----------|------|----------|
| P0 | 阻断性风险 | 存在P0级问题 |
| P1 | 减值性风险 | 存在P1级问题，无P0 |
| P2 | 建议性风险 | 仅存在P2级问题 |
| Pass | 无风险 | 无任何问题 |

### 5.4 VIP权益体系

| 权益 | 普通用户 | VIP用户 |
|------|----------|---------|
| 每日评估次数 | 3次 | 不限 |
| 报告导出 | 不可 | 可导出PDF |
| 历史记录 | 最近10条 | 全部 |
| AI分析报告 | 基础版 | 增强版 |
| 渠道推广 | 不可 | 可获得推荐码 |

---

## 6. 前端架构

### 6.1 Web管理后台

**技术栈:** 原生 HTML5 + CSS3 + JavaScript (无框架)

**主要页面:**

| 页面 | 路由 | 功能 |
|------|------|------|
| 登录 | /login.html | 用户登录 |
| 注册 | /register.html | 用户注册 |
| 管理后台 | /admin-new/index.html | 主控制台 |
| 规则管理 | /admin-new/pages/rules.html | 规则CRUD |
| 知识库 | /admin-new/pages/knowledge.html | 知识库管理 |
| 用户管理 | /admin-new/pages/users.html | 用户管理 |
| 客户管理 | /admin-new/pages/customers.html | 客户管理 |
| AI配置 | /admin-new/pages/ai-config.html | AI服务商配置 |
| VIP配置 | /admin-new/pages/vip-config.html | VIP套餐配置 |
| 报告管理 | /admin-new/pages/reports.html | 评价报告查看 |

### 6.2 微信小程序

**技术栈:** 微信小程序原生开发

**页面结构:**

```
miniprogram/
├── app.js              # 全局应用逻辑
├── app.json            # 全局配置
├── app.wxss            # 全局样式
├── api/
│   └── api.js          # API封装
└── pages/
    ├── index/          # 首页/登录
    │   ├── index.js
    │   ├── index.wxml
    │   ├── index.wxss
    │   └── index.json
    ├── form/           # 评估表单
    │   ├── form.js
    │   ├── form.wxml
    │   ├── form.wxss
    │   └── form.json
    ├── report/          # 报告查看
    │   ├── report.js
    │   ├── report.wxml
    │   ├── report.wxss
    │   └── report.json
    └── profile/        # 个人中心
        ├── profile.js
        ├── profile.wxml
        ├── profile.wxss
        └── profile.json
```

**API端点 (小程序端):**

```javascript
// 基础配置
const baseUrl = 'http://localhost:8000/api/v1';

// 认证
POST /auth/login     // 登录
POST /auth/register  // 注册
GET  /auth/me        // 获取用户信息

// 评价
POST /evaluation/evaluate           // 执行评估
GET  /evaluation/vip-status         // VIP状态
GET  /evaluation/user/{id}/history  // 评估历史

// 报告
GET  /reports?limit=&offset=         // 报告列表
GET  /reports/{id}                   // 报告详情
```

---

## 7. 安全设计

### 7.1 认证机制

- **JWT Token**: HS256算法，7天有效期
- **密码存储**: bcrypt单向哈希
- **Token传递**: Authorization Header Bearer Token

### 7.2 权限控制

| 角色 | 权限范围 |
|------|----------|
| client | 评估操作、查看个人报告、修改个人信息 |
| admin | 全功能访问、用户管理、系统配置 |

### 7.3 API安全

- CORS配置: 开发环境允许所有来源
- 请求超时: 连接10s，读取30s，写入30s
- 连接池: 池大小10，最大溢出20

---

## 8. 部署架构

### 8.1 环境要求

- **Python**: 3.10+
- **MySQL**: 8.0+ (Docker容器: my-mysql)
- **Node.js**: 16+ (可选，用于前端构建)
- **微信开发者工具**: 最新版本 (小程序开发)

### 8.2 环境变量

```bash
# 数据库配置
DATABASE_URL=mysql+pymysql://root:root@localhost:3306/shuwei_data_manager?charset=utf8mb4
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# JWT密钥
SECRET_KEY=your-secret-key-change-in-production

# AI服务 (可选)
OPENAI_API_KEY=sk-xxx
ZHIPU_API_KEY=xxx
```

### 8.3 启动方式

```bash
# 1. 确保MySQL容器运行
docker start my-mysql

# 2. 初始化数据库 (首次)
python scripts/full_init_db.py

# 3. 创建管理员账号
python scripts/create_admin.py

# 4. 启动FastAPI服务
python main.py
# 或
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## 9. 版本规划

### 9.1 V1.0 MVP (当前版本)

- [x] 用户注册/登录/JWT认证
- [x] 八维评价规则引擎
- [x] 评估计算与报告生成
- [x] 知识库管理
- [x] 渠道推荐体系
- [x] VIP会员管理
- [x] Web管理后台
- [x] 微信小程序客户端
- [x] PDF报告导出
- [x] **AI智能报告增强 (基于LLM)**
- [x] **向量数据库集成 (ChromaDB)**

### 9.2 V2.0 规划

- [ ] 数据产品挂牌支持
- [ ] 数据交易所对接
- [ ] 数据资产质押融资
- [ ] 高级数据分析看板
- [ ] API开放平台

---

## 10. 附录

### 10.1 技能库 (.trae/skills)

系统已配置以下AI技能:

**开发辅助类:**
- 日志分析、环境检查、依赖管理
- 服务监控、性能监控、安全检查
- 数据库备份、数据验证、系统报告
- 测试运行、代码审查、项目初始化
- 自动化部署、数据迁移

**小程序开发类:**
- miniprogram-api、miniprogram-component
- miniprogram-form、miniprogram-state
- miniprogram-release

**设计类:**
- ui-ux-pro-max (UI/UX设计)
- ppt-generator (PPT生成)

**协作类:**
- brainstorming、code-review、git-worktrees
- test-driven-development、systematic-debugging

### 10.2 法规参考

- 《中华人民共和国数据安全法》(2021)
- 《中华人民共和国个人信息保护法》(2021)
- 《企业数据资源相关会计处理暂行规定》(2023)
- 《数据资产评估指导意见》
- 《数据要素流通典型应用场景》

---

*本文档最后更新于 2026-03-25*
