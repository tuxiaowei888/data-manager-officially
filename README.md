# 数维数据管家系统 V2.0

<p align="center">
  <img src="https://img.shields.io/badge/version-2.0-blue" alt="version">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/badge/completion-75%25-yellow" alt="completion">
</p>

> **版本说明 V2.0** - 本版本包含完整的订阅收费体系、2层评估结构、客户分层系统和微信小程序支持。

---

## 🔥 核心设计理念

**规则库评分 → 知识库碰撞 → AI整体出报告**

```
┌─────────────────────────────────────────────────────────────────────┐
│                    三段式评估流程                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  第一段：规则库评分     →  31条规则计算，输出8维度得分               │
│  ─────────────────                                                   │
│  用户填报31项表单数据，通过SimpleEval引擎求值                        │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  第二段：知识库碰撞     →  向量检索+静态库，输出政策建议               │
│  ─────────────────                                                   │
│  ┌──────────────────────────────────────────────┐                   │
│  │  第一层：ChromaDB 向量语义检索               │                   │
│  │  第二层：PolicyRetriever 静态文案库           │                   │
│  └──────────────────────────────────────────────┘                   │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  第三段：AI整体出报告  →  三要素融合，输出7章诊断报告                 │
│  ─────────────────────                                               │
│  三要素：用户数据(form_data) + 规则评分(rule_results)                │
│          + 知识库政策(knowledge_results)                            │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ✨ 核心功能亮点（V2.0 新增）

### 🆕 订阅收费体系
- **四档订阅层级**：免费版、基础版、专业版、企业版
- **灵活的评估限制**：每日评估次数按层级递增
- **报告深度控制**：Summary、Diagnosis、Action Plan、Full 四种深度
- **数据管理限制**：数据集数量、企业档案数量按层级分配

### 🆕 2层评估结构
- **第一层**：数据集评估 - 单一数据集的综合评价
- **第二层**：企业档案评估 - 跨数据集的全局视角
- **多维度对比**：企业版支持跨数据集对比分析

### 🆕 客户分层系统
- **高价值客户识别**：活跃度高、付费意愿强的核心用户
- **培育客户管理**：有潜力但需要引导的用户群体
- **观察客户激活**：低活跃用户唤醒策略
- **信号强度计算**：5维度信号量化分析

### 🆕 微信小程序
- **完整用户流程**：登录 → 评估 → 报告 → 订阅
- **3 TabBar导航**：首页、评估、我的
- **订阅管理**：套餐展示、支付集成
- **即将来临**：数据集管理、企业档案

---

## ✨ 核心功能

### 用户模块
- **用户登录/注册** - JWT 认证
- **普通用户权限** - 可配置评估次数，知识库查看、报告查看/下载
- **VIP用户权限** - 可配置评估次数翻倍，知识库查看、报告下载、优先队列、历史报告保存

### 订阅配置管理（V2.0 新增）
- 免费版：3次/天，Summary报告，3个数据集
- 基础版：10次/天，Diagnosis报告，10个数据集，3个企业档案
- 专业版：无限制，Action Plan报告，50个数据集，无限企业档案
- 企业版：无限制，Full报告，无限数据集，无限企业档案，品牌定制

### 评价维度（8 大维度，31 条规则）

| 代码 | 维度名称 | 权重 | 规则数 | 说明 |
|------|---------|------|--------|------|
| **C** | 合规与安全 | 20% | 7条 | 数据来源合法性、隐私保护、安全措施 |
| **Q** | 数据质量 | 15% | 4条 | 数据完整性、准确性、标准化程度 |
| **O** | 权属确认 | 15% | 4条 | 数据权属、使用权、收益权、独创性 |
| **V** | 价值评估 | 20% | 4条 | 应用场景、变现能力、数据规模 |
| **M** | 管理体系 | 10% | 3条 | 治理组织、管理制度、质量监控 |
| **L** | 流通能力 | 10% | 3条 | 共享能力、API服务、交易记录 |
| **P** | 发展潜力 | 5% | 3条 | 增长趋势、技术创新、市场拓展 |
| **S** | 成本计量 | 5% | 3条 | 成本核算、存储成本、运维成本 |

**权重总计：100%**

### 详细规则清单

#### C - 合规与安全（7条规则）
| 规则名称 | 评估内容 | 权重 |
|---------|---------|------|
| 数据来源合规性 | 用户授权协议完整性 | 5% |
| 敏感数据处理 | 数据加密存储情况 | 5% |
| 数据安全措施 | 加密策略实施程度 | 4% |
| 隐私政策合规 | 隐私政策制定情况 | 3% |
| 数据跨境传输 | 跨境数据传输合规 | 4% |
| 数据留存管理 | 历史合规记录 | 4% |
| 安全认证情况 | 安全认证持有数量 | 3% |

#### Q - 数据质量（4条规则）
| 规则名称 | 评估内容 | 权重 |
|---------|---------|------|
| 数据质量管理 | 数据更新频率 | 4% |
| 元数据完整性 | 字段完整度百分比 | 4% |
| 数据标准化程度 | 数据格式多样性 | 3% |
| 数据类型多样性 | 数据类型丰富度 | 3% |

#### O - 权属确认（4条规则）
| 规则名称 | 评估内容 | 权重 |
|---------|---------|------|
| 数据权属确认 | 资产登记证书持有 | 5% |
| 使用权界定 | 知识产权登记证书 | 3% |
| 收益权分配 | 政府授权运营书 | 3% |
| 数据独创性评估 | 独创性等级评估 | 3% |

#### V - 价值评估（4条规则）
| 规则名称 | 评估内容 | 权重 |
|---------|---------|------|
| 数据应用场景 | 应用场景数量 | 4% |
| 数据价值评估 | 资产化目的多样性 | 4% |
| 数据变现能力 | 数据产品形态 | 3% |
| 数据规模价值 | 数据记录量级 | 3% |

#### M - 管理体系（3条规则）
| 规则名称 | 评估内容 | 权重 |
|---------|---------|------|
| 数据治理组织 | 专门部门设立情况 | 4% |
| 数据管理制度 | 制度完善程度 | 4% |
| 数据质量监控 | 监控机制健全度 | 3% |

#### L - 流通能力（3条规则）
| 规则名称 | 评估内容 | 权重 |
|---------|---------|------|
| 数据共享能力 | 共享场景丰富度 | 4% |
| API服务能力 | API产品化程度 | 4% |
| 数据交易记录 | 交易历史情况 | 3% |

#### P - 发展潜力（3条规则）
| 规则名称 | 评估内容 | 权重 |
|---------|---------|------|
| 数据增长趋势 | 更新实时性 | 4% |
| 技术创新能力 | 专利著作权数量 | 4% |
| 市场拓展空间 | 应用场景覆盖 | 3% |

#### S - 成本计量（3条规则）
| 规则名称 | 评估内容 | 权重 |
|---------|---------|------|
| 合规成本核算 | 成本归集清晰度 | 3% |
| 存储成本计量 | 投入成本规模 | 4% |
| 运维成本统计 | 独立核算情况 | 3% |

### 成熟度等级

| 等级 | 分数范围 | 状态描述 |
|------|----------|----------|
| A 级 | ≥90 分 | 成熟资产态 |
| B 级 | 75-89 分 | 准资产态 |
| C 级 | 60-74 分 | 治理态 |
| D 级 | <60 分 | 原始数据态 |

### 问题分级

- **P0 阻断性问题**：触发合规红线，禁止交易/入表
- **P1 减值性问题**：影响估值，需要整改
- **P2 优化性问题**：建议改进，提升价值

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- MySQL 5.7+（本地开发：Docker 端口 13306）
- （可选）Docker

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
# 复制示例配置文件
cp .env.example .env

# 编辑 .env 文件，配置数据库连接等信息
# 开发环境使用本地 Docker 数据库：
DATABASE_URL=mysql+pymysql://root:root@localhost:13306/shuwei_data_manager?charset=utf8mb4
SECRET_KEY=your-secret-key-here
```

### 3. 执行数据库迁移（V2.0）

```bash
# V2.0 新增：订阅体系和2层评估结构
python migrate_subscription_v2.py
```

### 4. 初始化数据库（如需要）

```bash
python scripts/init_db.py
```

### 5. 启动服务

```bash
# Windows 一键启动
双击运行 启动服务.bat

# 或手动启动
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 6. 访问系统

| 页面 | 地址 |
|------|------|
| 登录页面 | http://localhost:8000/login.html |
| 注册页面 | http://localhost:8000/register.html |
| 首页 | http://localhost:8000/home.html |
| 调研表单 | http://localhost:8000/index.html |
| 评估报告 | http://localhost:8000/report.html |
| 管理后台 | http://localhost:8000/admin.html |
| API 文档 | http://localhost:8000/docs |
| 中文文档 | http://localhost:8000/api_docs_chinese.html |

### 7. 微信小程序

```bash
# 使用微信开发者工具打开 miniprogram/ 目录
# 配置合法域名（生产环境）
# AppID: your-appid
```

---

## 📁 项目结构（V2.0）

```
数维数据管家系统/
├── api/                          # API 路由层（18个模块）
│   ├── auth.py                  # 认证授权（登录/注册/Token）
│   ├── evaluation.py            # 评价服务（核心评估引擎）
│   ├── rules.py                 # 规则管理（31条规则CRUD）
│   ├── knowledge.py             # 知识库文档管理
│   ├── knowledge_category.py    # 知识库分类管理
│   ├── reports.py               # 报告生成与查询
│   ├── users.py                 # 用户管理
│   ├── customers.py             # 客户管理
│   ├── channel.py               # 渠道与推荐码管理
│   ├── config.py                # 系统配置
│   ├── ai_config.py             # AI服务配置
│   ├── ai_rules.py              # AI规则生成
│   ├── permissions.py           # VIP权限配置
│   ├── subscription.py          # 订阅管理（V2.0新增）
│   ├── datasets.py              # 数据集管理（V2.0新增）
│   └── org_profiles.py         # 企业档案管理（V2.0新增）
│
├── config/                       # 配置文件
│   ├── database.py              # 数据库连接配置
│   ├── logging_config.py        # 日志配置
│   └── script_db.py             # 脚本数据库工具
│
├── models/                       # 数据库模型（12个）
│   ├── user.py                 # 用户模型（支持订阅层级）
│   ├── evaluation_result.py    # 评估结果
│   ├── rule_config.py          # 规则配置
│   ├── knowledge_doc.py        # 知识文档
│   ├── knowledge_category.py    # 知识分类
│   ├── channel.py              # 渠道模型
│   ├── ai_config.py            # AI配置模型
│   ├── ai_prompt_template.py   # Prompt模板
│   ├── system_config.py        # 系统配置（28个订阅配置）
│   ├── dataset.py              # 数据集模型（V2.0新增）
│   └── org_profile.py          # 企业档案模型（V2.0新增）
│
├── services/                     # 业务服务层（13个）
│   ├── evaluation.py           # 评价服务
│   ├── rule_calculator.py      # 规则计算器
│   ├── report_generator.py    # 报告生成器（支持4种深度）
│   ├── knowledge_base_engine.py # 知识库碰撞引擎（统一入口）
│   ├── policy_retriever.py     # 静态策略库
│   ├── vector_store.py        # 向量存储（ChromaDB）
│   ├── ai_service.py          # AI服务集成
│   ├── pdf_service.py         # PDF生成服务
│   ├── vip_service.py         # VIP服务
│   ├── subscription_service.py # 订阅服务（V2.0新增）
│   ├── subscription_decorators.py # 订阅权限装饰器（V2.0新增）
│   └── customer_scoring.py    # 客户分层服务（V2.0新增）
│
├── schemas/                      # Pydantic模型
│   ├── __init__.py            # 统一响应模型
│   ├── auth.py
│   └── channel.py
│
├── scripts/                      # 工具脚本
│   ├── init_db.py             # 数据库初始化
│   ├── full_init_db.py       # 完整初始化
│   ├── create_admin.py       # 创建管理员
│   └── migrate_subscription_v2.py # V2.0迁移脚本
│
├── frontend/                     # 前端页面（31个）
│   ├── login*.html            # 登录页面（多版本）
│   ├── register.html          # 注册页面
│   ├── home.html             # 用户首页
│   ├── index.html            # 调研表单（核心）
│   ├── report.html           # 评估报告展示
│   ├── reports.html          # 报告列表
│   ├── history.html          # 历史记录
│   ├── admin.html            # 管理后台
│   ├── users.html           # 用户管理
│   ├── customers.html        # 客户管理
│   ├── rules.html           # 规则库管理
│   ├── knowledge.html        # 知识库
│   ├── config.html          # 系统配置
│   ├── ai_config.html       # AI配置
│   └── test-*.html          # 测试页面
│
├── miniprogram/                 # 微信小程序（V2.0）
│   ├── app.js               # 入口文件
│   ├── app.json             # 配置文件
│   ├── app.wxss             # 全局样式
│   ├── api/
│   │   └── api.js           # API封装
│   └── pages/
│       ├── index/           # 首页（登录）
│       ├── form/            # 评估表单
│       ├── report/          # 报告详情
│       └── profile/         # 个人中心
│
├── docs/                        # 文档
│   ├── 功能统计与开发计划.md  # 功能统计
│   └── 小程序功能统计.md     # 小程序统计
│
├── .trae/skills/              # Trae AI Skills
│   ├── gitee代码上传/
│   ├── github代码上传/
│   ├── miniprogram-api/
│   ├── miniprogram-component/
│   ├── miniprogram-release/
│   └── ...（其他skills）
│
├── main.py                    # FastAPI主应用入口
├── requirements.txt          # Python依赖
├── .env.example             # 环境变量模板
├── .env                     # 环境变量（本地）
├── .gitignore              # Git忽略配置
└── README.md               # 本文件
```

---

## 📊 项目统计（V2.0）

### 代码规模
```
总代码行数：  ~20,000 行
├── Python:   ~15,000 行
├── HTML:     ~5,000 行
└── 小程序:   ~900 行

文件统计：
├── Python 文件：   64 个
├── HTML 文件：     31 个
├── 小程序文件：    15 个
├── 配置文件：      10 个
└── 总计：        120 个
```

### 功能完成度

| 模块 | 完成度 | 状态 |
|------|--------|------|
| 后端 API | 100% | ✅ 完成 |
| 服务层 | 100% | ✅ 完成 |
| 数据模型 | 100% | ✅ 完成 |
| Web 前端 | 70% | 🟡 开发中 |
| 小程序 | 40% | 🟡 开发中 |
| **总体** | **75%** | 🟡 开发中 |

### 待开发功能

| 优先级 | 功能 | 工作量 |
|--------|------|--------|
| 🔴 P0 | 数据库迁移执行 | 1小时 |
| 🔴 P0 | 订阅管理前端 | 2-3天 |
| 🔴 P0 | 支付系统集成 | 3-5天 |
| 🔴 P0 | 数据集管理前端 | 2-3天 |
| 🔴 P0 | 企业档案前端 | 2-3天 |
| 🟡 P1 | 客户分层展示 | 1-2天 |
| 🟡 P1 | 批量评估功能 | 2天 |
| 🟡 P1 | 数据可视化仪表盘 | 3-4天 |
| 🟡 P1 | 邮件通知系统 | 2天 |
| 🟡 P1 | 定时任务系统 | 1-2天 |

---

## 🔌 API 接口（18个模块，80+接口）

### 🔐 认证服务 `/api/v1/auth`
```
POST   /login                     # 用户登录
POST   /register                  # 用户注册
GET    /me                        # 获取当前用户信息
PUT    /me                        # 更新当前用户信息
POST   /change-password           # 修改密码
```

### 📊 评价服务 `/api/v1/evaluation`
```
POST   /evaluate                  # 执行评估（核心）
GET    /{id}                      # 获取评估结果详情
GET    /user/{user_id}/history   # 获取用户历史记录
POST   /{id}/report               # 生成评估报告
DELETE /{id}                      # 删除评估记录
```

### 📋 规则管理 `/api/v1/rules`
```
GET    /                          # 获取所有规则
GET    /active                    # 获取活跃规则
GET    /dimensions                # 获取维度列表
POST   /                          # 创建规则
PUT    /{id}                      # 更新规则
DELETE /{id}                      # 删除规则
POST   /{id}/toggle               # 启用/禁用规则
POST   /batch-import              # 批量导入规则
```

### 📚 知识库 `/api/v1/knowledge`
```
GET    /                          # 获取文档列表
POST   /                          # 创建文档
GET    /{id}                      # 获取文档详情
PUT    /{id}                      # 更新文档
DELETE /{id}                      # 删除文档
GET    /search                    # 语义搜索
POST   /{id}/vectorize           # 文档向量化
```

### 📁 知识分类 `/api/v1/knowledge-categories`
```
GET    /                          # 获取分类列表
POST   /                          # 创建分类
PUT    /{id}                      # 更新分类
DELETE /{id}                      # 删除分类
```

### 👥 用户管理 `/api/v1/users`
```
GET    /                          # 获取用户列表
GET    /{id}                      # 获取用户详情
PUT    /{id}                      # 更新用户信息
DELETE /{id}                      # 删除用户
PUT    /{id}/role                 # 修改用户角色
POST   /{id}/vip                 # 开通VIP
DELETE /{id}/vip                 # 取消VIP
```

### 💎 订阅管理 `/api/v1/subscription`（V2.0新增）
```
GET    /plans                    # 获取订阅计划列表
GET    /info                      # 获取当前订阅信息
GET    /evaluation-status         # 获取评估状态
POST   /upgrade                   # 升级订阅
GET    /customer-tier              # 获取客户分层信息
GET    /customer-segmentation-stats # 获取分层统计（管理员）
POST   /refresh-customer-tiers    # 刷新客户分层（管理员）
```

### 📊 数据集管理 `/api/v1/datasets`（V2.0新增）
```
GET    /                          # 获取数据集列表
POST   /                          # 创建数据集
GET    /{id}                      # 获取数据集详情
PUT    /{id}                      # 更新数据集
DELETE /{id}                      # 删除数据集
GET    /{id}/evaluations         # 获取数据集评估记录
GET    /stats/summary            # 获取统计摘要
```

### 🏢 企业档案管理 `/api/v1/org-profiles`（V2.0新增）
```
GET    /                          # 获取企业档案列表
POST   /                          # 创建企业档案
GET    /{id}                      # 获取企业档案详情
PUT    /{id}                      # 更新企业档案
DELETE /{id}                      # 删除企业档案
GET    /{id}/evaluations         # 获取评估记录
GET    /{id}/datasets            # 获取关联数据集
GET    /stats/summary            # 获取统计摘要
```

### 🏢 客户管理 `/api/v1/customers`
```
GET    /                          # 获取客户列表
POST   /                          # 创建客户
GET    /{id}                      # 获取客户详情
PUT    /{id}                      # 更新客户信息
DELETE /{id}                      # 删除客户
```

### 🔗 渠道管理 `/api/v1/channels`
```
GET    /                          # 获取渠道列表
POST   /                          # 创建渠道
GET    /{id}                      # 获取渠道详情
PUT    /{id}                      # 更新渠道
DELETE /{id}                      # 删除渠道
POST   /{id}/generate-code       # 生成推荐码
GET    /stats                     # 渠道统计
```

### 📄 报告服务 `/api/v1/reports`
```
GET    /                          # 获取报告列表
GET    /{id}                      # 获取报告详情
POST   /{id}/export/pdf          # 导出PDF
POST   /{id}/export/word        # 导出Word
POST   /{id}/send                # 发送报告
```

### ⚙️ 系统配置 `/api/v1/config`
```
GET    /                          # 获取系统配置
PUT    /                          # 更新系统配置
GET    /version                   # 获取版本信息
```

### 🤖 AI配置 `/api/v1/ai`
```
GET    /                          # 获取AI配置列表
POST   /                          # 创建AI配置
GET    /{id}                      # 获取配置详情
PUT    /{id}                      # 更新配置
DELETE /{id}                      # 删除配置
POST   /{id}/test                 # 测试AI连接
GET    /providers                 # 获取支持的厂商列表
POST   /{config_id}/set-default   # 设为默认配置
```

### 🤖 AI规则 `/api/v1/ai-rules`
```
POST   /generate                  # AI生成规则
POST   /optimize                  # AI优化规则
POST   /explain                   # AI解释规则
```

### 👑 VIP权限配置 `/api/v1/permissions`
```
GET    /                          # 获取所有权限配置
GET    /all                       # 获取所有配置项
GET    /{config_key}              # 获取单个配置
PUT    /{config_key}              # 更新单个配置
PUT    /batch                     # 批量更新配置
POST   /init-defaults             # 初始化默认配置
```

---

## 🛠️ 技术栈

### 核心框架
- **后端框架**: FastAPI 0.104.1（高性能异步Web框架）
- **ORM**: SQLAlchemy 2.0.23（数据库操作）
- **数据验证**: Pydantic 2.5.0（类型校验）
- **认证**: PyJWT 2.8.0 + Passlib（密码哈希）

### 数据库
- **关系数据库**: MySQL 5.7+（业务数据）
- **向量数据库**: ChromaDB 0.4.22（知识库语义检索）
- **连接驱动**: PyMySQL 1.1.0

### AI与数据处理
- **文本向量化**: Sentence-Transformers 2.2.2
- **Token计算**: Tiktoken 0.5.2
- **HTTP客户端**: HTTPX 0.25.2
- **数据计算**: Pandas 2.1.3 + NumPy
- **规则计算**: SimpleEval 0.9.13（安全表达式求值）

### 报告生成
- **PDF生成**: XHTML2PDF 0.2.17 + ReportLab 4.0.7
- **Word文档**: Python-Docx 1.1.0
- **Excel处理**: OpenPyXL 3.1.2
- **PDF解析**: PyPDF2 3.0.1

### 前端
- **Web前端**: HTML5 + CSS3 + JavaScript（原生）
- **UI组件**: Bootstrap 5 + Bootstrap Icons
- **图表**: Chart.js 4.4
- **微信小程序**: 原生框架 + WeUI

### 部署与运维
- **Web服务器**: Nginx（反向代理）
- **进程管理**: Uvicorn 0.24.0（ASGI服务器）
- **云服务**: 腾讯云（推荐配置）
- **容器化**: Docker（可选）

---

## 📊 数据库备份与恢复

```bash
# 备份数据库
docker exec shuwei-mysql mysqldump -u root -p shuwei_data_manager > backup.sql

# 恢复数据库
docker exec -i shuwei-mysql mysql -u root -p shuwei_data_manager < backup.sql
```

---

## 🗺️ 开发路线

### 已完成 ✅

| 阶段 | 功能 | 状态 |
|------|------|------|
| Phase 1 | 核心评估引擎（8维度31规则） | ✅ |
| Phase 2 | 前端表单与报告页面 | ✅ |
| Phase 3 | 报告持久化与历史查询 | ✅ |
| Phase 4 | 知识库与规则库管理 | ✅ |
| Phase 5 | 用户认证与权限管理（JWT） | ✅ |
| Phase 6 | 微信小程序端 | ✅ |
| Phase 7 | AI服务集成（多厂商支持） | ✅ |
| Phase 8 | 新版管理后台 | ✅ |
| Phase 9 | VIP权限配置系统 | ✅ |
| **Phase 10** | **订阅收费体系 V2.0** | ✅ |
| **Phase 11** | **2层评估结构** | ✅ |
| **Phase 12** | **客户分层系统** | ✅ |

### 进行中 🚧

| 阶段 | 功能 | 状态 |
|------|------|------|
| Phase 13 | 订阅管理前端 | 🚧 |
| Phase 14 | 支付系统集成 | 🚧 |
| Phase 15 | 小程序订阅功能 | 🚧 |
| Phase 16 | 云端部署与运维 | 🚧 |

### 待开发 📋

| 阶段 | 功能 | 状态 |
|------|------|------|
| Phase 17 | 数据可视化仪表盘 | 📋 |
| Phase 18 | 邮件通知系统 | 📋 |
| Phase 19 | 定时任务系统 | 📋 |
| Phase 20 | 多语言支持 | 📋 |

---

## ☁️ 部署建议

### 推荐配置（云端数据库版）

| 组件 | 选择 | 年费 |
|------|------|------|
| 云服务器 | 腾讯云 CVM 2核4G 3M | ~650元 |
| **云数据库** | **腾讯云 CDB MySQL 基础版 1核2G** | **~550元** |
| 向量数据库 | Chroma Cloud 免费版 | 0元 |
| 对象存储 | 腾讯云 COS 50GB | ~50元 |
| 域名 | .com/.cn | ~60元 |
| **总计** | | **~1310元** |

> ⚠️ **注意**: 云数据库是生产环境必需的，本地 Docker 数据库仅用于开发测试。

### 部署架构

```
┌─────────────────────────────────────────┐
│              腾讯云                      │
│  ┌─────────────┐    ┌─────────────┐    │
│  │  CVM 服务器  │    │  云数据库    │    │
│  │  Nginx      │◄──►│  MySQL      │    │
│  │  FastAPI    │    │  生产版      │    │
│  └─────────────┘    └─────────────┘    │
│         │                               │
│         ▼                               │
│  ┌─────────────┐                       │
│  │ Chroma Cloud│                       │
│  │ 向量数据库   │                       │
│  └─────────────┘                       │
└─────────────────────────────────────────┘
```

---

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🔗 相关链接

- Gitee 仓库：https://gitee.com/tuxiaowei520/data-manager-officially
- GitHub 仓库：https://github.com/tuxiaowei888/data-manager-officially

---

## 💬 联系方式

如有问题或建议，欢迎通过以下方式联系：
- 邮箱：tuxiaowei520@163.com
- 邮箱：tuxiaowei888@gmail.com

---

## 🙏 致谢

- **Trae AI** - 智能编程助手
- **FastAPI** - 高性能 Web 框架
- **微信小程序** - 跨平台开发框架
- **所有开源贡献者**

---

<p align="center">Made with ❤️ by 数维创擎团队</p>
<p align="center">Powered by Trae AI</p>
