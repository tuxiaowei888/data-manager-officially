---
name: 测试报告
description: 生成测试结果报告。当用户要求测试报告、结果分析或测试统计时调用。
---

# 测试报告

该技能用于生成测试结果报告和统计分析。

## 测试类型

| 测试类型 | 说明 | 命令 |
|---------|------|------|
| 单元测试 | 测试单个函数/模块 | `python -m pytest tests/` |
| API测试 | 测试API接口 | `python tests/test_api.py` |
| 集成测试 | 测试完整流程 | `python tests/integration_test.py` |
| 性能测试 | 测试性能指标 | `python tests/performance_test.py` |

## 测试执行

### 1. 运行单元测试
```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试文件
python -m pytest tests/test_api.py -v

# 运行特定测试函数
python -m pytest tests/test_api.py::test_login -v

# 显示详细输出
python -m pytest tests/ -v -s

# 生成覆盖率报告
python -m pytest tests/ --cov=. --cov-report=html
```

### 2. 运行API测试
```bash
# 测试健康检查
curl -X GET http://localhost:8000/health

# 测试登录接口
curl -X POST http://localhost:8000/api/v1/auth/login `
  -H "Content-Type: application/x-www-form-urlencoded" `
  -d "username=admin&password=admin123"

# 测试获取规则列表
curl -X GET http://localhost:8000/api/v1/rules `
  -H "Authorization: Bearer <token>"
```

### 3. 运行快速测试
```bash
# 快速冒烟测试
python tests/quick_test.py

# 简单测试
python test_simple.py
```

## 测试报告生成

### 生成HTML报告
```bash
# 安装pytest-html
pip install pytest-html

# 生成HTML报告
python -m pytest tests/ --html=reports/test_report.html --self-contained-html
```

### 生成JUnit XML报告
```bash
# 生成XML报告
python -m pytest tests/ --junitxml=reports/test-results.xml

# 查看XML内容
Get-Content reports/test-results.xml
```

### 手动生成报告
```powershell
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

$report = @"

============================================================
                       测试报告
============================================================
测试时间: $timestamp

一、测试概要
------------------------------------------------------------
测试总数: 50
通过数:   48
失败数:   2
跳过数:   0
成功率:   96%

二、测试详情
------------------------------------------------------------

三、失败测试
------------------------------------------------------------

四、建议
------------------------------------------------------------

============================================================
"@

Write-Host $report
```

## 测试报告模板

```
============================================================
                       测试报告
============================================================
测试时间: 2024-03-18 15:30
测试环境: 开发环境

一、测试概要
------------------------------------------------------------
| 指标 | 值 |
|------|-----|
| 总测试数 | 50 |
| 通过 | 48 |
| 失败 | 2 |
| 跳过 | 0 |
| 成功率 | 96% |
| 总耗时 | 12.5秒 |

二、按模块统计
------------------------------------------------------------
| 模块 | 通过 | 失败 | 总数 | 成功率 |
|------|------|------|------|--------|
| 用户认证 | 10 | 0 | 10 | 100% |
| 规则管理 | 15 | 1 | 16 | 93.75% |
| 知识库 | 12 | 1 | 13 | 92.31% |
| 报告生成 | 11 | 0 | 11 | 100% |

三、失败测试详情
------------------------------------------------------------
1. test_update_rule
   - 错误: AssertionError
   - 原因: 权重值超出范围
   - 位置: tests/test_api.py:45

2. test_delete_knowledge
   - 错误: HTTP 404
   - 原因: 知识文档不存在
   - 位置: tests/test_api.py:78

四、API性能测试
------------------------------------------------------------
| 接口 | 响应时间 | 状态 |
|------|---------|------|
| /health | 12ms | 正常 |
| /api/v1/auth/login | 89ms | 正常 |
| /api/v1/rules | 45ms | 正常 |

五、总结
------------------------------------------------------------
测试状态: 基本通过
主要问题:
  1. 1个规则更新测试失败
  2. 1个知识库删除测试失败

建议:
  1. 修复规则权重验证逻辑
  2. 添加知识文档存在性检查
============================================================
```

## 测试统计分析

### 统计测试覆盖率
```bash
# 安装coverage
pip install coverage

# 运行测试并生成覆盖率
coverage run -m pytest tests/
coverage report

# 生成HTML覆盖率报告
coverage html
```

### 统计测试时间
```bash
# 显示最慢的10个测试
python -m pytest tests/ --durations=10

# 显示所有测试的执行时间
python -m pytest tests/ --durations=0
```

### 统计测试结果趋势
```powershell
# 读取历史测试结果
$results = @()
Get-ChildItem -Path "reports" -Filter "test_results_*.json" | ForEach-Object {
    $results += Get-Content $_.FullName | ConvertFrom-Json
}

# 统计趋势
$results | Select-Object date, passRate | Sort-Object date
```

## 保存测试报告

### 保存为JSON
```powershell
# 创建测试结果对象
$testResult = @{
    timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    total = 50
    passed = 48
    failed = 2
    skipped = 0
    passRate = 96
}

# 保存为JSON
$testResult | ConvertTo-Json | Out-File -FilePath "reports/test_results_$(Get-Date -Format 'yyyyMMdd_HHmmss').json" -Encoding UTF8
```

### 保存为HTML
```html
<!-- reports/test_report_template.html -->
<!DOCTYPE html>
<html>
<head>
    <title>测试报告</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .pass { color: green; }
        .fail { color: red; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
    </style>
</head>
<body>
    <h1>测试报告</h1>
    <p>生成时间: {{timestamp}}</p>
    <h2>测试概要</h2>
    <table>
        <tr><th>总测试数</th><td>{{total}}</td></tr>
        <tr><th>通过</th><td class="pass">{{passed}}</td></tr>
        <tr><th>失败</th><td class="fail">{{failed}}</td></tr>
        <tr><th>成功率</th><td>{{passRate}}%</td></tr>
    </table>
</body>
</html>
```

## 测试最佳实践

1. **定期运行测试** - 每次代码提交后自动运行
2. **保持测试独立** - 测试之间不应有依赖
3. **清晰的测试命名** - 测试名称应清晰表达测试内容
4. **及时修复失败** - 失败的测试应及时修复
5. **记录测试历史** - 保存测试报告便于追踪问题