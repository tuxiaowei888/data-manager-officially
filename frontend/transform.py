# 快速替换脚本
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换所有类名
replacements = {
    'class="section-title"': 'class="section-title-glass"',
    'class="section-desc"': 'class="section-desc-glass"',
    'class="form-question"': 'class="form-question-glass"',
    'class="question-label"': 'class="question-label-glass"',
    'class="required-mark"': 'class="required-mark-glass"',
    'class="form-control" name': 'class="form-control form-control-glass" name',
    'class="form-select" name': 'class="form-select form-control-glass" name',
    'class="form-check-input" type': 'class="form-check-input form-check-input-glass" type',
    'class="form-check-label"': 'class="form-check-label form-check-label-glass"',
    'class="other-input-wrapper"': 'class="other-input-wrapper-glass"',
    'class="other-input-label"': 'class="other-input-label-glass"',
    'class="form-label"': 'class="form-label-glass"',
    'class="btn btn-secondary-custom btn-custom"': 'class="btn btn-secondary-glass btn-custom-glass"',
    'class="btn btn-primary-custom btn-custom"': 'class="btn btn-primary-glass btn-custom-glass"',
    'class="btn btn-success-custom btn-custom"': 'class="btn btn-success-glass btn-custom-glass"',
    'class="loading-overlay"': 'class="loading-overlay-glass"',
    'class="engine-breathing"': 'class="engine-breathing-glass"',
    'class="loading-text"': 'class="loading-text-glass"',
    'class="loading-subtext"': 'class="loading-subtext-glass"',
    'class="nav-vip-badge"': 'class="nav-vip-badge-glass"',
}

for old, new in replacements.items():
    content = content.replace(old, new)

# 写入回文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('类名替换完成！')
