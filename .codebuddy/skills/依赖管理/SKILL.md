---
name: 依赖管理
description: 管理Python依赖，更新、清理依赖包。当用户要求更新依赖、检查依赖或清理环境时调用。
---

# 依赖管理

该技能用于管理Python依赖，包括安装、更新、清理等操作。

## 常用命令

### 1. 查看依赖
```bash
# 查看所有已安装的包
pip list

# 查看requirements.txt中的包
pip list | Select-String -Pattern (Get-Content requirements.txt)

# 检查特定包是否安装
pip list | Select-String -Pattern "fastapi"

# 查看包详细信息
pip show fastapi
```

### 2. 安装依赖
```bash
# 从requirements.txt安装
pip install -r requirements.txt

# 安装特定包
pip install fastapi

# 安装指定版本
pip install fastapi==0.135.1

# 安装多个包
pip install fastapi uvicorn sqlalchemy
```

### 3. 更新依赖
```bash
# 查看可更新的包
pip list --outdated

# 更新单个包
pip install --upgrade fastapi

# 更新所有包（谨慎）
pip install --upgrade -r requirements.txt

# 批量更新过时的包
pip freeze | Select-String -Pattern "==" | ForEach-Object {
    $pkg = $_ -replace "==.*", ""
    pip install --upgrade $pkg
}
```

### 4. 卸载依赖
```bash
# 卸载单个包
pip uninstall fastapi

# 卸载多个包
pip uninstall fastapi uvicorn

# 卸载所有不在requirements.txt的包
pip freeze > current_requirements.txt
diff requirements.txt current_requirements.txt
```

### 5. 导出依赖
```bash
# 导出当前依赖
pip freeze > requirements_backup.txt

# 导出开发依赖
pip freeze --dev > dev_requirements.txt

# 生成简洁的requirements.txt
pip freeze | Where-Object { $_ -notmatch "^-e" } > requirements_new.txt
```

## 依赖检查

### 检查依赖完整性
```bash
# 对比requirements.txt和实际安装
$required = Get-Content requirements.txt
$installed = pip list | ForEach-Object { $_ -replace "\s+==.*", "" }
Compare-Object $required $installed
```

### 检查版本兼容性
```bash
# 查看fastapi及其依赖
pip show fastapi

# 检查依赖冲突
pip check
```

### 生成依赖报告
```bash
# 统计依赖数量
$count = (pip list | Measure-Object).Count
Write-Host "已安装包数量: $count"

# 按包大小统计
pip list | Format-Table
```

## 虚拟环境

### 创建虚拟环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境（Windows）
.\venv\Scripts\activate

# 激活虚拟环境（Linux/Mac）
# source venv/bin/activate
```

### 在虚拟环境中操作
```bash
# 激活后安装依赖
.\venv\Scripts\activate
pip install -r requirements.txt

# 导出虚拟环境依赖
pip freeze > venv_requirements.txt

# 退出虚拟环境
deactivate
```

## 常见问题

### 问题：安装失败
```bash
# 清理缓存后重试
pip cache purge
pip install fastapi

# 使用国内镜像
pip install fastapi -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题：版本冲突
```bash
# 查看冲突详情
pip install fastapi==0.135.1 --force-reinstall

# 创建新虚拟环境
python -m venv new_venv
.\new_venv\Scripts\activate
pip install -r requirements.txt
```

### 问题：权限错误
```bash
# 使用用户目录安装
pip install --user fastapi

# 或使用虚拟环境
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## 依赖管理最佳实践

1. **使用虚拟环境** - 每个项目使用独立的虚拟环境
2. **锁定版本** - 使用 `pip freeze` 锁定依赖版本
3. **定期更新** - 定期更新依赖但要测试兼容性
4. **检查安全** - 定期使用 `pip check` 检查安全问题

## 输出报告

```
## 依赖管理报告
时间: 2024-03-18 15:30

### 依赖统计
- 总包数: 85
- 核心依赖: 12
- 开发依赖: 5

### 需要更新的包
| 包名 | 当前版本 | 最新版本 |
|------|---------|---------|
| fastapi | 0.135.1 | 0.136.0 |
| uvicorn | 0.42.0 | 0.42.1 |

### 安全问题
- 无安全问题发现

### 建议
1. 建议更新 fastapi 到最新版本
2. 定期检查依赖安全性
3. 保持虚拟环境清洁
```