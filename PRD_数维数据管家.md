产品需求文档 (PRD) - 数维数据管家系统

表格

| 版本号 | 状态 | 描述 |
| --- | --- | --- |
| V1.0 | 开发中 (MVP) | 核心闭环：内置规则库 + 人工配置 + 动态计算引擎 + 基础报告。 |
| V2.0 | 规划中 (预留) | 智能增强：AI 规则自动生成 + RAG 政策动态关联 + 行业模型市场。 |

1. 项目概述

构建一个 SaaS 化数据资产评价系统，命名为 "数维数据管家系统"。

V1.0 目标：通过预置的专家规则库，让用户完成数据填报后，系统自动计算得分、判定风险并生成标准报告。验证业务流程。

V2.0 目标：引入 LLM 能力，实现上传政策文档自动更新规则库，以及报告内容的智能解读。

🤖 给 Trae 的核心指令：

- 项目名称：所有代码注释、数据库表注释、前端标题均使用 "数维数据管家系统"。
- 只开发 V1.0 功能逻辑。
- 必须执行 V2.0 的架构预留（包括数据库字段、空接口定义、前端占位 UI）。
- 严禁在 V1.0 阶段编写复杂的 AI 解析或 RAG 检索逻辑，仅做桩代码（Stub）或返回固定提示。
- 初始化数据：必须包含脚本，将预设的 18 条专家规则写入数据库。

2. 功能需求详解

2.1 模块一：规则管理引擎 (Rule Engine)

2.1.1 规则数据结构 (Database Schema)

表名: rule_configs

用途: 存储所有评价指标的逻辑、权重和阈值。

表格

| 字段名 | 类型 | V1.0 默认值/行为 | V2.0 预留要求 (必须实现) | 说明 |
| --- | --- | --- | --- | --- |
| id | Integer | PK | - | 主键 |
| dimension_code | String | - | - | 维度代码 (如 D1_COMPLIANCE) |
| rule_name | String | - | - | 规则名称 |
| logic_expression | Text | - | - | 计算逻辑字符串 (Python 表达式，供 simpleeval 使用) |
| weight | Float | - | - | 权重 (0.0 - 1.0) |
| risk_threshold | Float | - | - | 风险触发阈值 |
| is_active | Boolean | True | - | 是否启用 |
| source_type | String | 'manual' | Enum: ['manual', 'ai_generated', 'imported'] | 关键预留: 标记规则来源。V1.0 全为 'manual'。 |
| version | Integer | 1 | Auto-increment on update | 关键预留: 记录规则版本，用于 V2.0 版本对比。 |
| ai_prompt_context | Text | NULL | Store original policy text | 关键预留: V2.0 存储生成该规则所用的原始政策片段，V1.0 留空。 |

2.1.2 功能逻辑

表格

| 功能点 | V1.0 实现逻辑 (Must Have) | V2.0 规划逻辑 (TODO - 仅预留) | Trae 执行指令 |
| --- | --- | --- | --- |
| 规则初始化 | 运行脚本 seed_rules.py，将预设的 18 条 JSON 规则写入 DB。 | - | 必须生成 scripts/seed_rules.py 并在启动时检查执行。 |
| 人工配置 | 提供 CRUD 接口，允许管理员修改公式、权重。保存即生效。 | 增加"版本历史"查看，支持回滚到旧版本。 | 后端实现标准的 RESTful API (POST/PUT/DELETE /rules)。 |
| AI 生成规则 | 不实现具体逻辑。 | 用户上传 PDF -> LLM 解析 -> 生成 JSON 规则 -> 待审核。 | 必须定义 API: POST /api/v1/rules/ai-generate。<br>行为: 接收文件参数，直接返回 { "status": "coming_soon", "message": "V2.0 功能" }。<br>前端: 按钮置灰或显示 "Beta" 标签。 |
| 规则执行 | 读取 logic_expression，使用 simpleeval 库安全执行计算。 | 支持自然语言条件，由 AI 实时转译为表达式。 | 封装 RuleCalculator 类，确保输入输出接口稳定，方便 V2.0 替换内部实现。 |

2.2 模块二：评价计算服务 (Evaluation Service)

2.2.1 计算流程

1. 用户提交表单数据 (JSON)。
2. 系统加载所有 is_active=True 的规则。
3. 遍历规则，代入用户数据执行 logic_expression。
4. 加权求和得到总分。
5. 根据 risk_threshold 判定风险等级 (P0/P1/P2)。

2.2.2 结果数据结构 (Database Schema)

表名: evaluation_results

表格

| 字段名 | 类型 | V1.0 默认值/行为 | V2.0 预留要求 (必须实现) | 说明 |
| --- | --- | --- | --- | --- |
| id | Integer | PK | - | 主键 |
| user_id | Integer | FK | - | 用户 ID |
| total_score | Float | - | - | 总分 |
| risk_level | String | - | - | 最高风险等级 (P0/P1/P2) |
| detail_json | JSON | - | - | 各维度得分详情 |
| engine_version | String | 'v1_static' | Dynamic (e.g., 'v2_ai_rag') | 关键预留: 记录计算时使用的引擎版本。 |
| ai_analysis_log | JSON | NULL | Store AI reasoning steps | 关键预留: V2.0 存储 AI 推导过程，V1.0 留空。 |

🤖 给 Trae 的执行指令:

- 在 services/evaluation.py 中，创建一个 EvaluationService 类。
- 方法 calculate(data, rules) 必须完全基于 V1.0 逻辑实现。
- 禁止在此处调用任何 LLM API。
- 在类定义上方添加注释：# TODO V2.0: Integrate dynamic threshold adjustment based on industry benchmarks.

2.3 模块三：知识库与报告 (Knowledge & Reporting)

2.3.1 知识库结构

表名: knowledge_docs

用途: 存储政策文档及其元数据。

表格

| 字段名 | 类型 | V1.0 默认值/行为 | V2.0 预留要求 (必须实现) | 说明 |
| --- | --- | --- | --- | --- |
| id | Integer | PK | - | 主键 |
| title | String | - | - | 文档标题 |
| content_text | Text | - | - | 解析后的纯文本 |
| embedding_status | Boolean | False | True if vectorized | 关键预留: 标记是否已进行向量化处理。V1.0 恒为 False。 |
| vector_ids | JSON | NULL | Store Chroma IDs | 关键预留: 存储对应的向量库 ID 列表。 |

2.3.2 报告生成逻辑

表格

| 功能点 | V1.0 实现逻辑 (Must Have) | V2.0 规划逻辑 (TODO - 仅预留) | Trae 执行指令 |
| --- | --- | --- | --- |
| 报告内容 | 基于固定模板填充分数和风险。改进建议使用预设的静态文案库（Key-Value 匹配）。 | 基于 RAG 检索具体政策条款，动态生成针对性的改进建议。 | 创建 PolicyRetriever 类。<br>V1.0 实现：retrieve(keyword) 返回硬编码的字典数据。<br>注释标记：# TODO V2.0: Replace with Chroma semantic search. |
| PDF 导出 | 使用 reportlab 或 WeasyPrint 生成静态 PDF。 | 增加"AI 解读"章节，包含对话式摘要。 | 保持 PDF 生成接口一致，V2.0 仅增加渲染区块。 |
| AI 助手浮窗 | 不显示。 | 在报告页右下角增加 Chat 浮窗，支持针对报告提问。 | 前端报告页面预留 <div id="ai-chat-widget"></div> 容器，V1.0 设置 display: none 或隐藏。 |

2.4 模块四：用户端 (小程序/Web)

V1.0 界面:

- 首页：开始评估按钮（标题：数维数据管家系统）。
- 表单页：5 步向导，支持本地草稿保存。
- 结果页：雷达图、总分、风险列表、静态改进建议。
- 管理后台：规则列表（增删改查）、文档上传（仅存文本）。

V2.0 预留:

- 管理后台规则列表页：增加"AI 生成"按钮（置灰，Tooltip: "V2.0 即将上线"）。
- 结果页：预留"询问 AI 助手"入口（隐藏）。

3. 技术栈与开发约束

- 后端: Python 3.9+, FastAPI, SQLAlchemy, Pydantic.
- 计算引擎: simpleeval (用于安全执行字符串表达式).
- 数据库: MySQL 8.0+ (必须严格遵循上述 Schema 设计).
- 向量库: ChromaDB (V1.0 仅安装并初始化 Collection，不写入向量数据, 不进行检索).
- AI/LLM: V1.0 严禁 调用任何 LLM API (节省成本，减少复杂度)。所有 AI 相关接口必须返回 Mock 数据或 "Coming Soon" 状态。

4. 数据初始化要求 (Seed Data)

必须在项目根目录创建 data/seed_rules_v1.json 文件，并编写 scripts/init_db.py 脚本。

脚本逻辑：

1. 检查 rule_configs 表是否为空。
2. 若为空，读取 JSON 文件，插入以下 18 条预设规则 (示例数据结构)：
   - D1 合规性: 数据来源合法性, 隐私脱敏, 授权链条.
   - D2 质量: 完整性, 准确性, 及时性.
   - D3 价值: 场景覆盖, 收益预估, 成本节约.
   - D4 管理: 制度健全, 人员配置, 审计记录.
   - D5 流通: 标准化, 接口可用, 交易历史.
   - D6 潜力: 稀缺性, 可衍生, 政策契合.

所有插入数据的 source_type 字段必须设为 'manual'。

5. 验收标准 (Acceptance Criteria)

- 数据库检查: rule_configs 表包含 source_type, version, ai_prompt_context 字段。
- 功能检查:
  - 用户可以提交表单并立即获得评分报告。
  - 管理员可以在后台修改规则权重，下次计算即时生效。
  - 点击"AI 生成规则"按钮，弹出"功能开发中"提示，不报错。
- 代码检查:
  - 搜索代码库，不存在 V1.0 阶段调用 LLM API 的代码。
  - 存在 # TODO V2.0 相关的注释标记。
  - seed_rules.py 脚本运行成功，数据库中有初始数据。
- 品牌检查: 系统标题、Logo 文字（如有）、数据库注释中均体现 "数维数据管家系统"。