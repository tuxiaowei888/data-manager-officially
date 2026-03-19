import re

# 读取 form.js
with open('d:\\数维创擎\\代码库\\数维数据管家系统\\frontend\\form.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换类名
replacements = [
    ('.step"', '.step-glass"'),
    ('.step-circle"', '.step-circle-glass"'),
    ('.step-label"', '.step-label-glass"'),
    ('.form-question"', '.form-question-glass"'),
    ('.question-label"', '.question-label-glass"'),
    ('.other-input-wrapper"', '.other-input-wrapper-glass"'),
    ('.loading-overlay"', '.loading-overlay-glass"'),
    ('.nav-vip-badge"', '.nav-vip-badge-glass"'),
    ('.progress-line"', '.progress-line-glass"'),
    ('.progress-node"', '.progress-node-glass"'),
    ('.progress-segments"', '.progress-segmented-glass"'),
    ('.progress-text"', '.progress-text"'),
    ("querySelectorAll('.step')", "querySelectorAll('.step-glass')"),
    ("querySelector('.step-circle')", "querySelector('.step-circle-glass')"),
    ("querySelector('.step-label')", "querySelector('.step-label-glass')"),
    ("closest('.form-question')", "closest('.form-question-glass')"),
    ("querySelector('.question-label')", "querySelector('.question-label-glass')"),
    ("querySelector('.other-input-wrapper')", "querySelector('.other-input-wrapper-glass')"),
    ("getElementById('progress-line')", "getElementById('progress-line')"),
    ("querySelectorAll('#progress-segments .progress-node')", "querySelectorAll('#progress-segments .progress-node-glass')"),
    ("getElementById('progress-text')", "getElementById('progress-text')"),
    ("getElementById('loadingOverlay')", "getElementById('loadingOverlay')"),
    ("getElementById('navVipBadge')", "getElementById('navVipBadge')"),
]

for old, new in replacements:
    content = content.replace(old, new)

# 保存文件
with open('d:\\数维创擎\\代码库\\数维数据管家系统\\frontend\\form.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('form.js 类名更新完成！')

