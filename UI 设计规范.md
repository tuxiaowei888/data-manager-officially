# 数维数据管家系统 - UI/UX 设计规范

## 🎨 设计理念

**"理性科技 + 权威信赖"** - 专家级顾问质感

### 核心设计关键词
- **专业 (Professional)** - 数据严谨性、法律权威性
- **通透 (Translucent)** - 数据流动性和透明度
- **智慧 (Intelligent)** - AI 智能感的微动效和光影
- **克制 (Restrained)** - 色彩和元素不滥用，重点突出数据和结论

---

## 🌈 色彩体系 (Color Palette)

### 主色调 - 深空蓝
```css
--primary-color: #1B3A57;        /* 深空蓝 - 主品牌色 */
--primary-dark: #0F4C81;         /* 经典蓝 - 备选主色 */
--primary-light: #2E5A7C;        /* 浅蓝 - 辅助色 */
```

**应用场景**：
- 导航栏、主按钮
- 标题文字
- 品牌标识

**心理暗示**：稳重、信任、权威

### 辅助科技色 - 青色光
```css
--tech-accent: #00D2FF;          /* 青色光 - 科技高亮 */
--tech-secondary: #4ECDC4;       /* 青绿 - 辅助科技色 */
```

**应用场景**：
- 渐变背景
- AI 加载动画
- 高亮图标
- 数据可视化

**心理暗示**：科技、未来、流动

### 数据增值色 - 翡翠绿
```css
--success-color: #2ECC71;        /* 翡翠绿 - 高分/通过 */
--success-light: #58D68D;        /* 浅绿 - 成功态 */
```

**应用场景**：
- 高分段展示
- 估值上升
- 合规通过
- 成功状态

**心理暗示**：安全、增长、通行

### 风险警示色
```css
--danger-color: #FF6B6B;         /* 珊瑚红 - P0 风险 */
--warning-color: #FF9F43;        /* 橙色 - P1 风险 */
--danger-light: #FFB3B3;         /* 浅红 - 警告态 */
```

**应用场景**：
- P0 阻断风险
- 低分项
- 合规风险
- 错误状态

**心理暗示**：警惕、注意、停止

### 中性色
```css
/* 背景色 */
--bg-primary: #F5F7FA;           /* 浅灰蓝 - 主背景 */
--bg-card: #FFFFFF;              /* 纯白 - 卡片背景 */
--bg-dark: #0B1120;              /* 午夜蓝黑 - 深色模式 */

/* 文字色 */
--text-primary: #1B3A57;         /* 深蓝 - 主标题 */
--text-secondary: #5A6C7D;       /* 灰蓝 - 正文 */
--text-disabled: #99A8B8;        /* 浅灰 - 禁用态 */

/* 边框色 */
--border-light: #E8EDF2;         /* 浅灰蓝 - 边框 */
--border-focus: #1B3A57;         /* 深蓝 - 聚焦态 */
```

---

## 🎨 渐变运用

### 品牌渐变
```css
/* 深蓝 -> 青绿 (数据转化为资产) */
--gradient-brand: linear-gradient(135deg, #1B3A57 0%, #00D2FF 100%);

/* 深空蓝渐变 */
--gradient-deep: linear-gradient(180deg, #0B1120 0%, #1B3A57 100%);

/* 科技光晕 */
--gradient-tech: linear-gradient(135deg, #00D2FF 0%, #4ECDC4 100%);
```

**应用场景**：
- AI 分析加载页背景
- 雷达图填充
- 报告封面
- 重要按钮

---

## 🔤 字体与排版 (Typography)

### 字体家族
```css
/* 中文字体 - 系统默认无衬线 */
--font-family-zh: -apple-system, BlinkMacSystemFont, "PingFang SC", 
                   "HarmonyOS Sans", "Microsoft YaHei", sans-serif;

/* 数字字体 - 等宽数字（财务报表质感） */
--font-family-num: "Roboto Mono", "DIN Alternate", "SF Mono", monospace;
```

### 字号规范
```css
/* L1 标题 - 页面大标题 */
--font-l1: 24px;
--font-l1-line: 32px;
--font-l1-weight: 600;

/* L2 标题 - 模块标题 */
--font-l2: 18px;
--font-l2-line: 26px;
--font-l2-weight: 600;

/* L3 标题 - 小结论 */
--font-l3: 16px;
--font-l3-line: 24px;
--font-l3-weight: 600;

/* 正文 */
--font-body: 14px;
--font-body-line: 24px;
--font-body-weight: 400;

/* 辅助文字 */
--font-meta: 12px;
--font-meta-line: 20px;
--font-meta-weight: 400;
```

### 排版规范
```css
/* 标题 */
h1 {
  font-size: var(--font-l1);
  line-height: var(--font-l1-line);
  font-weight: var(--font-l1-weight);
  letter-spacing: -0.5px;  /* 微缩字间距，体现力量感 */
}

h2 {
  font-size: var(--font-l2);
  line-height: var(--font-l2-line);
  font-weight: var(--font-l2-weight);
}

h3 {
  font-size: var(--font-l3);
  line-height: var(--font-l3-line);
  font-weight: var(--font-l3-weight);
}

/* 正文 */
p {
  font-size: var(--font-body);
  line-height: var(--font-body-line);
  font-weight: var(--font-body-weight);
}

/* 数字（关键！） */
.score, .amount, .percentage {
  font-family: var(--font-family-num);
  font-feature-settings: "tnum";  /* 等宽数字 */
  font-variant-numeric: tabular-nums;
}
```

---

## 🧩 组件与视觉元素

### A. 卡片式设计 (Card UI)

```css
.card {
  background: var(--bg-card);
  border-radius: 12px;  /* 圆角 8px-12px */
  padding: 24px;
  
  /* 极淡的弥散阴影 - 悬浮感 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  
  /* Web 端管理后台 - 极细边框 */
  border: 1px solid var(--border-light);
}

.card-hover {
  transition: all 0.3s ease;
}

.card-hover:hover {
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}
```

### B. 数据可视化 (Data Viz)

#### 雷达图
```css
/* 品牌色渐变填充，半透明 */
.radar-chart {
  fill: rgba(27, 58, 87, 0.2);
  stroke: var(--primary-color);
  stroke-width: 2;
}

.radar-chart-gradient {
  fill: url(#radarGradient);  /* 深蓝 -> 青绿渐变 */
}
```

#### 仪表盘
```css
/* 半圆仪表盘 - 总分展示 */
.gauge-chart {
  /* 指针带微动效 */
  animation: gauge-pointer 1s ease-out;
}

@keyframes gauge-pointer {
  from { transform: rotate(-90deg); }
  to { transform: rotate(var(--score-deg)); }
}
```

#### 进度条
```css
/* 分段式进度条 - 每完成一步点亮节点 */
.progress-segmented {
  display: flex;
  justify-content: space-between;
}

.progress-node {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--border-light);
  transition: all 0.3s ease;
}

.progress-node.completed {
  background: var(--success-color);
  box-shadow: 0 0 8px rgba(46, 204, 113, 0.4);
}
```

### C. AI 专属元素

#### 呼吸灯效
```css
/* AI 分析中 - 缓慢呼吸的光圈 */
.ai-breathing {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: radial-gradient(circle, 
    rgba(0, 210, 255, 0.3) 0%, 
    transparent 70%);
  animation: ai-breathe 2s ease-in-out infinite;
}

@keyframes ai-breathe {
  0%, 100% { transform: scale(0.95); opacity: 0.6; }
  50% { transform: scale(1.05); opacity: 1; }
}
```

#### 魔法棒图标
```css
/* AI 生成建议 - ✨图标 */
.ai-suggestion::before {
  content: "✨";
  margin-right: 8px;
  font-size: 16px;
}
```

#### 引用标注
```css
/* 知识库引用 - 特殊背景块 + 侧边竖线 */
.citation-block {
  background: rgba(0, 210, 255, 0.05);
  border-left: 4px solid var(--tech-accent);
  padding: 16px 20px;
  margin: 16px 0;
  position: relative;
}

.citation-source {
  display: inline-block;
  margin-top: 8px;
  font-size: var(--font-meta);
  color: var(--text-secondary);
}

.citation-source::before {
  content: "[来源：";
}

.citation-source::after {
  content: "]";
}
```

### D. 风险可视化

#### P0 阻断
```css
/* 红色背景 Alert 组件 - 闪烁边框 */
.p0-alert {
  background: rgba(255, 107, 107, 0.1);
  border: 2px solid var(--danger-color);
  border-radius: 8px;
  padding: 16px 20px;
  animation: p0-flash 2s ease-in-out infinite;
}

@keyframes p0-flash {
  0%, 100% { border-color: var(--danger-color); }
  50% { border-color: var(--danger-light); }
}
```

#### 等级徽章
```css
/* 金属质感徽章 - 金牌/银牌/铜牌/铁牌 */
.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  font-size: var(--font-body);
  
  /* 金属渐变 */
  background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);  /* 金牌 */
  color: #fff;
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
  box-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
}

.badge-silver {
  background: linear-gradient(135deg, #C0C0C0 0%, #808080 100%);  /* 银牌 */
}

.badge-bronze {
  background: linear-gradient(135deg, #CD7F32 0%, #8B4513 100%);  /* 铜牌 */
}

.badge-iron {
  background: linear-gradient(135deg, #4A4A4A 0%, #2C2C2C 100%);  /* 铁牌 */
}
```

---

## 📱 双端差异化策略

### 微信小程序 (C 端 - 轻量、便捷)

#### 布局
```css
/* 单列流式布局 */
.page {
  padding: 16px;
  background: var(--bg-primary);
}

.card {
  margin-bottom: 16px;
  border-radius: 12px;
}
```

#### 交互
- 多用选择器 (Picker)、开关 (Switch)、滑块 (Slider)
- 少用键盘输入，降低手机操作成本
- 报告页支持长按保存图片（生成海报）
- 海报设计精美，适合朋友圈传播（带二维码和推荐码）

#### 风格
- 更偏向"工具化"
- 清爽明亮
- 减少深色背景（费电且在小屏上显得压抑）

### Web 端 (C 端/B 端 - 沉浸、大屏)

#### C 端报告页
```css
/* 宽屏沉浸式布局 */
.report-page {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 24px;
  
  /* 左侧导航锚点，右侧内容滚动 */
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 32px;
}

/* 支持深色模式切换 */
.report-page.dark {
  background: var(--bg-dark);
  color: #fff;
}
```

#### B 端管理台
```css
/* 经典左右结构 */
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 240px;
  background: var(--bg-dark);
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
}

.main-content {
  margin-left: 240px;
  flex: 1;
  background: var(--bg-primary);
  padding: 24px;
}
```

#### 交互
- 支持复杂的图表交互（Hover 显示详情、缩放、下钻）
- 规则库/知识库管理支持拖拽上传、富文本编辑、分屏预览

#### 风格
- 更偏向"驾驶舱 (Dashboard)"感
- 体现掌控力
- 信息密度高

---

## 🎬 动效与微交互 (Motion Design)

### 页面转场
```css
/* Fade-in + Slide-up - 向上浮入 */
.page-enter {
  opacity: 0;
  transform: translateY(20px);
}

.page-enter-active {
  opacity: 1;
  transform: translateY(0);
  transition: all 0.3s ease;
}
```

### 数字滚动
```css
/* 报告加载时 - 分数从 0 滚动到最终值 */
@keyframes number-roll {
  from { transform: translateY(100%); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.score-animate {
  display: inline-block;
  animation: number-roll 1s ease-out;
}
```

### 骨架屏 (Skeleton)
```css
/* 数据加载前 - 灰色骨架屏 */
.skeleton {
  background: linear-gradient(
    90deg,
    var(--border-light) 25%,
    var(--bg-card) 50%,
    var(--border-light) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
}

@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### 按钮反馈
```css
/* 按钮点击 - 微弱缩放 */
.btn {
  transition: all 0.2s ease;
}

.btn:active {
  transform: scale(0.98);
}

/* 成功提交 - 绿色对勾动画 */
.btn-success::after {
  content: "✓";
  display: inline-block;
  animation: check-appear 0.3s ease-out;
}

@keyframes check-appear {
  from { transform: scale(0); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
```

---

## 🖼️ 画面参考意向 (Mood Board)

### 设计描述
> "参考 **阿里云/腾讯云的控制台风格**（专业、蓝白灰），
> 结合 **麦肯锡/波士顿咨询的报告风格**（极简、排版考究、图表清晰），
> 再融入一点 **科幻电影中的数据终端界面**（微光、粒子、深色背景下的霓虹点缀，仅用于报告封面和加载页）。"

### 推荐参考案例
1. **Ant Design Pro** - 后台管理系统的标杆（适合 B 端）
2. **Flurry / Google Analytics** - 数据可视化的清晰度
3. **Stripe Dashboard** - 现代 SaaS 的精致感
4. **国内数据交易所官网** - 上海数交所、北京国际大数据交易所（配色和严肃感）

---

## 📋 实施检查清单

### 基础组件
- [ ] 按钮（主按钮、次按钮、文字按钮）
- [ ] 输入框（文本框、下拉框、选择器）
- [ ] 卡片（普通卡片、可折叠卡片、数据卡片）
- [ ] 表格（普通表格、可排序表格、分页表格）
- [ ] 弹窗（确认框、提示框、表单弹窗）

### 数据组件
- [ ] 雷达图（五维度）
- [ ] 仪表盘（总分）
- [ ] 进度条（分段式）
- [ ] 数字展示（滚动动画）
- [ ] 等级徽章（A/B/C/D）

### 反馈组件
- [ ] Alert（P0/P1/P2风险）
- [ ] Toast（成功/失败/加载）
- [ ] 骨架屏（列表骨架、卡片骨架）
- [ ] 加载动画（AI 呼吸灯、旋转加载）

### 导航组件
- [ ] 顶部导航（Web）
- [ ] 侧边菜单（管理后台）
- [ ] 底部 Tab（小程序）
- [ ] 面包屑（管理后台）

---

## 🎨 设计资源

### 色板文件
- Sketch Color Palette
- Figma Color Styles
- Adobe Swatch Exchange

### 字体文件
- Roboto Mono (数字字体)
- DIN Alternate (备选数字字体)

### 图标库
- 使用系统图标（SF Symbols / Material Icons）
- 自定义 AI 专属图标（魔法棒、呼吸灯）

### 动效资源
- Lottie 动画文件（AI 加载、成功反馈）
- CSS 动画代码片段

---

**这是完整的 UI/UX 设计规范文档！**

**下一步**：
1. ✅ 根据此规范更新现有前端页面
2. ✅ 创建小程序端 UI
3. ✅ 统一管理后台 UI

**请确认这个设计规范是否符合您的预期？** 🎨
