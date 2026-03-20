# Animation Effects for PPT

PPT 动画效果参考指南。

## 重要说明

`python-pptx` 库**不支持**直接添加动画效果。动画需要在 WPS 或 PowerPoint 中手动添加。

## 推荐的动画添加流程

### 方法1：在 WPS 中手动添加

1. 使用 python-pptx 生成基础 PPT
2. 在 WPS 中打开文件
3. 选择"动画"选项卡
4. 为每个元素添加动画效果

### 方法2：使用 VBA 宏（高级）

如果需要批量添加动画，可以使用 VBA：

```vba
Sub AddFadeAnimation()
    Dim sld As Slide
    Dim shp As Shape
    
    For Each sld In ActivePresentation.Slides
        For Each shp In sld.Shapes
            shp.AnimationSettings.EntryAnimation = ppEffectFade
            shp.AnimationSettings.AdvanceMode = ppAdvanceOnTime
            shp.AnimationSettings.AdvanceTime = 1
        Next shp
    Next sld
End Sub
```

## 常用动画效果类型

### 入场动画

| 效果名称 | WPS 名称 | 适用场景 |
|----------|----------|----------|
| Fade | 淡入 | 标题、文字 |
| Fly In | 飞入 | 列表项 |
| Zoom | 缩放 | 图片、图标 |
| Wipe | 擦除 | 进度条 |
| Float Up | 上浮 | 数据卡片 |

### 强调动画

| 效果名称 | WPS 名称 | 适用场景 |
|----------|----------|----------|
| Pulse | 脉冲 | 重点内容 |
| Color Pulse | 颜色脉冲 | 高亮文字 |
| Teeter | 摇摆 | 警示信息 |
| Spin | 旋转 | 加载图标 |

### 退出动画

| 效果名称 | WPS 名称 | 适用场景 |
|----------|----------|----------|
| Fade | 淡出 | 切换内容 |
| Fly Out | 飞出 | 隐藏元素 |
| Zoom | 缩放 | 关闭弹窗 |

## 动画时间设置建议

```python
ANIMATION_TIMING = {
    'fast': 0.5,      # 快速动画
    'normal': 1.0,    # 正常速度
    'slow': 2.0,      # 慢速动画
    'title': 0.8,     # 标题动画
    'bullet': 0.3,    # 列表项动画
    'chart': 1.5,     # 图表动画
}
```

## 动画触发方式

| 触发方式 | 说明 | 使用场景 |
|----------|------|----------|
| 单击时 | 点击鼠标触发 | 演讲控制 |
| 与上一动画同时 | 同步播放 | 组合动画 |
| 上一动画之后 | 自动播放 | 自动演示 |

## 幻灯片切换效果

### 在 WPS 中设置

1. 选择"切换"选项卡
2. 选择切换效果
3. 设置持续时间
4. 选择换片方式

### 推荐切换效果

| 效果 | 适用场景 |
|------|----------|
| 推进 | 商务演示 |
| 淡出 | 简约风格 |
| 翻转 | 创意展示 |
| 立方体 | 科技主题 |
| 翻页 | 书籍风格 |

## 使用 HTML 实现动画（替代方案）

如果需要复杂动画，可以生成 HTML 格式的演示文稿：

```html
<!DOCTYPE html>
<html>
<head>
<style>
.slide {
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.6s ease-out;
}

.slide.active {
    opacity: 1;
    transform: translateY(0);
}

.animate-fade-up {
    animation: fadeUp 0.6s ease-out forwards;
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-scale {
    animation: scaleIn 0.5s ease-out forwards;
}

@keyframes scaleIn {
    from {
        opacity: 0;
        transform: scale(0.9);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

.stagger > * {
    opacity: 0;
    animation: fadeUp 0.5s ease-out forwards;
}

.stagger > *:nth-child(1) { animation-delay: 0.1s; }
.stagger > *:nth-child(2) { animation-delay: 0.2s; }
.stagger > *:nth-child(3) { animation-delay: 0.3s; }
.stagger > *:nth-child(4) { animation-delay: 0.4s; }
</style>
</head>
<body>
<div class="slide active">
    <h1 class="animate-fade-up">标题</h1>
    <ul class="stagger">
        <li>第一项</li>
        <li>第二项</li>
        <li>第三项</li>
    </ul>
</div>
</body>
</html>
```

## 动画最佳实践

### 1. 保持简洁

- 每页动画不超过 3 种
- 避免过度使用特效
- 动画服务于内容

### 2. 时间控制

```python
RECOMMENDED_TIMING = {
    'title_slide': {
        'title': 0.8,
        'subtitle': 0.5,
        'delay': 0.3
    },
    'content_slide': {
        'title': 0.5,
        'bullets': 0.3,  # 每项
        'delay': 0.2     # 项间延迟
    },
    'data_slide': {
        'title': 0.5,
        'chart': 1.5,
        'insights': 0.4
    }
}
```

### 3. 动画顺序

```
标题 → 副标题 → 内容 → 图片 → 图表 → 总结
```

### 4. 避免的动画

- 旋转文字
- 弹跳效果
- 过于花哨的过渡
- 声音效果（除非必要）

## 在 WPS 中批量添加动画的技巧

### 使用动画刷

1. 为第一个元素设置动画
2. 选中该元素
3. 点击"动画刷"
4. 点击其他元素应用相同动画

### 使用动画窗格

1. 打开"动画窗格"
2. 拖拽调整动画顺序
3. 设置开始时间和持续时间
4. 预览效果

## 示例：动画设计文档

在生成 PPT 时，可以创建一个动画说明文档：

```python
def create_animation_guide(slides_data):
    guide = []
    for i, slide in enumerate(slides_data, 1):
        guide.append(f"第 {i} 页: {slide['title']}")
        guide.append("  动画设置:")
        
        if slide.get('type') == 'title':
            guide.append("    - 标题: 淡入, 0.8秒")
            guide.append("    - 副标题: 淡入, 0.5秒, 延迟0.3秒")
        else:
            guide.append("    - 标题: 飞入(自左), 0.5秒")
            guide.append("    - 内容: 逐项淡入, 每项0.3秒")
        
        guide.append("")
    
    return "\n".join(guide)

# 使用示例
slides = [
    {'type': 'title', 'title': '项目汇报'},
    {'title': '项目概述', 'content': ['背景', '目标', '团队']},
    {'title': '主要成果', 'content': ['成果1', '成果2', '成果3']}
]

print(create_animation_guide(slides))
```

输出：

```
第 1 页: 项目汇报
  动画设置:
    - 标题: 淡入, 0.8秒
    - 副标题: 淡入, 0.5秒, 延迟0.3秒

第 2 页: 项目概述
  动画设置:
    - 标题: 飞入(自左), 0.5秒
    - 内容: 逐项淡入, 每项0.3秒

第 3 页: 主要成果
  动画设置:
    - 标题: 飞入(自左), 0.5秒
    - 内容: 逐项淡入, 每项0.3秒
```
