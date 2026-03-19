# 数维数据管家系统

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0-blue" alt="version">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue" alt="python">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
</p>

SaaS 化数据资产评价系统，通过预置的专家规则库，让用户完成数据填报后，系统自动计算得分、判定风险并生成标准报告。

## ✨ 核心功能

### 评价维度（6 大维度）

| 维度 | 权重 | 说明 |
|------|------|------|
| D1 合规性 | 25% | 数据来源合法性、隐私保护、授权链条 |
| D2 质量 | 20% | 数据完整性、准确性、及时性 |
| D3 价值 | 20% | 应用场景、收益预期、成本节约 |
| D4 管理 | 15% | 管理制度、人员配置、审计记录 |
| D5 流通 | 10% | 标准化程度、接口可用性、交易记录 |
| D6 潜力 | 10% | 稀缺性、可衍生性、政策契合度 |

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

## 🚀 快速开始

### 环境要求

- Python 3.8+
- MySQL 5.7+
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
```

### 3. 初始化数据库

```bash
python scripts/init_db.py
```

### 4. 启动服务

```bash
# Windows 一键启动
双击运行 启动服务.bat

# 或手动启动
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. 访问系统

| 页面 | 地址 |
|------|------|
| 登录页面 | http://localhost:8000/login.html |
| 首页 | http://localhost:8000/home.html |
| 调研表单 | http://localhost:8000/index.html |
| 评估报告 | http://localhost:8000/report.html |
| 管理后台 | http://localhost:8000/admin.html |
| API 文档 | http://localhost:8000/docs |
| 中文文档 | http://localhost:8000/api_docs_chinese.html |

## 📁 项目结构

```
数维数据管家系统/
├── api/                    # API 路由层
│   ├── auth.py            # 认证授权
│   ├── evaluation.py      # 评价服务
│   ├── rules.py           # 规则管理
│   ├── knowledge.py       # 知识库
│   ├── reports.py         # 报告服务
│   ├── users.py           # 用户管理
│   ├── customers.py       # 客户管理
│   ├── channel.py         # 渠道管理
│   └── config.py          # 系统配置
├── config/                # 配置文件
│   └── database.py        # 数据库配置
├── data/                  # 数据文件
│   └── seed_rules_v1.json # 种子规则
├── database/              # 数据库相关
│   └── backup/            # 备份文件
├── frontend/              # 前端页面
│   ├── login*.html        # 登录页面（多个版本）
│   ├── home.html          # 首页
│   ├── index.html         # 调研表单
│   ├── report.html        # 报告展示
│   ├── admin.html         # 管理后台
│   ├── customers.html     # 客户管理
│   ├── knowledge.html     # 知识库
│   └── ui-*.css/js        # UI 组件
├── miniprogram/           # 微信小程序
│   ├── pages/             # 小程序页面
│   └── app.js/json/wxss   # 小程序配置
├── models/                # 数据库模型
│   ├── user.py
│   ├── evaluation_result.py
│   ├── knowledge_doc.py
│   ├── rule_config.py
│   └── ...
├── schemas/               # Pydantic 模型
├── scripts/               # 工具脚本
│   ├── init_db.py         # 数据库初始化
│   └── create_admin.py    # 创建管理员
├── services/              # 业务服务层
│   ├── evaluation.py      # 评价服务
│   ├── rule_calculator.py # 规则计算器
│   ├── policy_retriever.py# 策略检索器
│   ├── report_generator.py# 报告生成器
│   ├── vector_store.py    # 向量存储
│   └── ai_service.py      # AI 服务
├── tests/                 # 测试文件
├── .trae/skills/          # Trae AI Skills
├── main.py                # 应用入口
├── requirements.txt       # 项目依赖
└── .env.example           # 环境变量示例
```

## 🔌 API 接口

### 认证服务
```
POST /api/v1/auth/login           # 用户登录
POST /api/v1/auth/register        # 用户注册
GET  /api/v1/auth/me              # 获取当前用户
```

### 评价服务
```
POST /api/v1/evaluation/evaluate         # 执行评估
GET  /api/v1/evaluation/{id}             # 获取评估结果
GET  /api/v1/evaluation/user/{user_id}/history  # 历史记录
POST /api/v1/evaluation/{id}/report      # 生成报告
```

### 规则管理
```
GET    /api/v1/rules              # 获取所有规则
GET    /api/v1/rules/active       # 获取活跃规则
POST   /api/v1/rules              # 创建规则
PUT    /api/v1/rules/{id}         # 更新规则
DELETE /api/v1/rules/{id}         # 删除规则
```

### 知识库
```
GET    /api/v1/knowledge          # 获取文档列表
POST   /api/v1/knowledge          # 创建文档
GET    /api/v1/knowledge/search   # 语义搜索
PUT    /api/v1/knowledge/{id}     # 更新文档
DELETE /api/v1/knowledge/{id}     # 删除文档
```

### 用户管理
```
GET    /api/v1/users              # 获取用户列表
GET    /api/v1/users/{id}         # 获取用户详情
PUT    /api/v1/users/{id}         # 更新用户
DELETE /api/v1/users/{id}         # 删除用户
```

## 🛠️ 技术栈

- **后端**: FastAPI + SQLAlchemy + Pydantic
- **数据库**: MySQL + ChromaDB（向量数据库）
- **前端**: HTML5 + CSS3 + JavaScript（原生）
- **小程序**: 微信小程序
- **AI**: Sentence-Transformers（文本向量化）
- **部署**: Docker + Nginx（推荐）

## 📊 数据库备份与恢复

```bash
# 备份数据库
database/backup/备份数据库.bat

# 恢复数据库
database/backup/恢复数据库.bat
```

## 🗺️ 开发路线

- [x] Phase 1: 核心评估功能
- [x] Phase 1.5: 前端表单与报告页面
- [x] Phase 2: 报告持久化与历史查询
- [x] Phase 3: 知识库与规则库管理
- [x] Phase 4: 用户认证与权限管理
- [x] Phase 5: 微信小程序端
- [ ] Phase 6: AI 智能分析增强
- [ ] Phase 7: 云端部署与运维

## 📚 文档索引

| 文档 | 说明 |
|------|------|
| [使用指南.md](使用指南.md) | 系统使用指南 |
| [开发路线图.md](开发路线图.md) | 开发规划与进度 |
| [UI 设计规范.md](UI 设计规范.md) | UI/UX 设计规范 |
| [项目结构说明.md](项目结构说明.md) | 项目结构详解 |
| [项目完整分析报告.md](项目完整分析报告.md) | 项目分析报告 |
| [功能架构图.md](功能架构图.md) | 系统架构说明 |

## ☁️ 部署建议

### 推荐配置（1500元/年预算）

| 组件 | 选择 | 年费 |
|------|------|------|
| 云服务器 | 腾讯云 CVM 2核4G 3M | ~650元 |
| 云数据库 | 腾讯云 CDB MySQL 基础版 1核2G | ~550元 |
| 向量数据库 | Chroma Cloud 免费版 | 0元 |
| 对象存储 | 腾讯云 COS 50GB | ~50元 |
| 域名 | .com/.cn | ~60元 |
| **总计** | | **~1310元** |

### 部署架构

```
┌─────────────────────────────────────────┐
│              腾讯云                      │
│  ┌─────────────┐    ┌─────────────┐    │
│  │  CVM 服务器  │    │  云数据库    │    │
│  │  Nginx      │◄──►│  MySQL      │    │
│  │  FastAPI    │    │  基础版      │    │
│  └─────────────┘    └─────────────┘    │
│         │                               │
│         ▼                               │
│  ┌─────────────┐                        │
│  │ Chroma Cloud│                        │
│  │ 向量数据库   │                        │
│  └─────────────┘                        │
└─────────────────────────────────────────┘
```

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🔗 相关链接

- Gitee 仓库：https://gitee.com/tuxiaowei520/data-manager-officially
- GitHub 仓库：https://github.com/tuxiaowei888/data-manager-officially

## 💬 联系方式

如有问题或建议，欢迎通过以下方式联系：
- 邮箱：tuxiaowei520@163.com
- 邮箱：tuxiaowei888@gmail.com

---

<p align="center">Made with ❤️ by 数维创擎团队</p>
