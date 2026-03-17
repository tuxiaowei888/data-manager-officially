# 数维数据管家系统

SaaS 化数据资产评价系统，通过预置的专家规则库，让用户完成数据填报后，系统自动计算得分、判定风险并生成标准报告。

**版本**: V1.0 MVP  
**技术栈**: FastAPI + SQLAlchemy + MySQL + Docker

## 快速开始

### 1. 启动服务

```bash
# Windows
双击运行 启动服务.bat

# 或手动启动
docker start shuwei-mysql
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. 访问系统

| 页面 | 地址 |
|------|------|
| 调研表单 | http://localhost:8000/survey |
| 评估报告 | http://localhost:8000/report |
| API 文档 | http://localhost:8000/docs |
| 中文文档 | http://localhost:8000/api-docs-cn |

### 3. 数据库备份与恢复

```bash
# 备份数据库
database/backup/备份数据库.bat

# 恢复数据库
database/backup/恢复数据库.bat
```

## 项目结构

```
数维数据管家系统/
├── api/                 # API 路由层
│   ├── evaluation.py    # 评价服务 API
│   ├── rules.py         # 规则管理 API
│   ├── knowledge.py     # 知识库 API
│   ├── reports.py       # 报告服务 API
│   ├── auth.py          # 认证 API
│   └── channel.py       # 渠道管理 API
├── config/              # 配置文件
│   └── database.py      # 数据库配置
├── data/                # 数据文件
│   └── seed_rules_v1.json  # 种子规则
├── database/            # 数据库相关
│   ├── backup/          # 备份文件
│   └── migrations/      # 迁移脚本
├── frontend/            # 前端页面
│   ├── index.html       # 调研表单页
│   ├── report.html      # 报告展示页
│   └── form.js          # 表单逻辑
├── models/              # 数据库模型
├── schemas/             # Pydantic 模型
├── scripts/             # 工具脚本
│   └── init_db.py       # 数据库初始化
├── services/            # 业务服务层
│   ├── evaluation.py    # 评价服务
│   ├── rule_calculator.py   # 规则计算器
│   ├── policy_retriever.py  # 策略检索器
│   └── report_generator.py  # 报告生成器
├── tests/               # 测试文件
├── main.py              # 应用入口
├── requirements.txt     # 项目依赖
├── 启动服务.bat         # Windows 启动脚本
├── 开发路线图.md        # 开发规划
└── UI 设计规范.md       # UI 规范文档
```

## 核心功能

### 评价维度（5 大维度）

| 维度 | 权重 | 说明 |
|------|------|------|
| 合规与安全 | 30% | 数据来源合法性、隐私保护、授权链条 |
| 治理与质量 | 20% | 数据完整性、准确性、及时性 |
| 确权与权属 | 20% | 权属凭证、独创性评估 |
| 价值与应用 | 20% | 应用场景、资产化目的 |
| 成本与可计量 | 10% | 成本核算、投入计量 |

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

## API 接口

### 评价服务
```
POST /api/v1/evaluation/evaluate    # 执行评估
GET  /api/v1/evaluation/{id}        # 获取结果
GET  /api/v1/evaluation/user/{user_id}/history  # 历史记录
```

### 规则管理
```
GET    /api/v1/rules           # 获取所有规则
GET    /api/v1/rules/active    # 获取活跃规则
POST   /api/v1/rules           # 创建规则
PUT    /api/v1/rules/{id}      # 更新规则
DELETE /api/v1/rules/{id}      # 删除规则
```

### 知识库
```
GET    /api/v1/knowledge       # 获取文档列表
POST   /api/v1/knowledge       # 创建文档
GET    /api/v1/knowledge/search # 搜索文档
```

## 数据库配置

```python
# config/database.py
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/shuwei_data_manager?charset=utf8mb4"
```

## 开发路线

详见 [开发路线图.md](开发路线图.md)

- [x] Phase 1: 核心评估功能
- [x] Phase 1.5: 前端表单与报告页面
- [ ] Phase 2: 报告持久化与历史查询
- [ ] Phase 3: 知识库与规则库管理
- [ ] Phase 4: AI 智能分析
- [ ] Phase 5: 小程序端开发

## 文档索引

| 文档 | 说明 |
|------|------|
| [PRD_数维数据管家.md](PRD_数维数据管家.md) | 产品需求文档 |
| [开发路线图.md](开发路线图.md) | 开发规划与进度 |
| [UI 设计规范.md](UI 设计规范.md) | UI/UX 设计规范 |
| [使用指南.md](使用指南.md) | 系统使用指南 |
| [项目结构说明.md](项目结构说明.md) | 项目结构详解 |

## 技术支持

如有问题，请参考产品需求文档或联系开发团队。
