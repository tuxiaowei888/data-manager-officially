# Gitee 代码上传技能

帮助用户将代码上传到 Gitee 仓库。当用户需要推送代码到 Gitee、初始化 Git 仓库、配置远程仓库或解决上传问题时调用。

## 适用场景

- 首次将项目推送到 Gitee
- 添加 Gitee 远程仓库
- 推送代码更新到 Gitee
- 解决 Gitee 推送问题
- 配置 Gitee 仓库认证

## 执行流程

### 1. 检查 Git 仓库状态
```bash
# 检查是否已初始化 Git
git status

# 如果不是 Git 仓库，先初始化
git init
```

### 2. 配置远程仓库
```bash
# 检查现有远程仓库
git remote -v

# 添加或更新 Gitee 远程仓库
git remote add gitee https://gitee.com/用户名/仓库名.git
# 或更新现有远程
git remote set-url gitee https://gitee.com/用户名/仓库名.git
```

### 3. 添加并提交文件
```bash
# 添加所有文件
git add .

# 或选择性添加
git add <文件路径>

# 查看添加状态
git status
```

### 4. 创建提交
```bash
# 创建提交（使用详细的提交信息）
git commit -m "type: 描述

- 详细变更 1
- 详细变更 2

Ref: 相关引用"

# 常用 type:
# feat: 新功能
# fix: 修复 bug
# docs: 文档更新
# style: 代码格式
# refactor: 重构
# test: 测试
# chore: 构建/工具
```

### 5. 推送到 Gitee
```bash
# 推送到 main 分支
git push gitee main

# 或强制推送（谨慎使用）
git push gitee main -f

# 推送所有分支
git push gitee --all

# 推送所有标签
git push gitee --tags
```

### 6. 配置认证（如果需要）
```bash
# 配置凭证存储
git config --global credential.helper store

# 或使用 SSH 密钥
# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 将公钥添加到 Gitee: https://gitee.com/profile/ssh_keys
```

## 常见问题解决

### 问题 1: 认证失败
**症状**: `remote: Invalid username or password`

**解决方案**:
```bash
# 清除保存的凭证
git credential-manager erase

# 重新推送，会提示输入新凭证
git push gitee main
```

### 问题 2: 分支不存在
**症状**: `error: src refspec main does not match any`

**解决方案**:
```bash
# 创建并切换到 main 分支
git checkout -b main

# 重新推送
git push gitee main
```

### 问题 3: 远程仓库已存在
**症状**: `remote gitee already exists`

**解决方案**:
```bash
# 更新远程仓库 URL
git remote set-url gitee https://gitee.com/新地址.git
```

### 问题 4: 推送被拒绝
**症状**: `rejected non-fast-forward`

**解决方案**:
```bash
# 先拉取远程变更
git pull gitee main

# 解决冲突后推送
git push gitee main

# 或强制推送（慎用）
git push gitee main -f
```

## 最佳实践

1. **提交前检查**
   - 确保 `.gitignore` 已配置，排除敏感文件
   - 运行代码检查和测试
   - 查看变更内容：`git diff --cached`

2. **提交信息规范**
   ```
   feat: 新增订阅体系重构
   
   - 新增四档订阅层级
   - 新增数据集和企业档案模型
   - 新增报告深度控制
   
   Ref: V2.0 开发计划
   ```

3. **分支管理**
   - main/master: 主分支，保持稳定
   - develop: 开发分支
   - feature/*: 功能分支
   - fix/*: 修复分支

4. **敏感信息保护**
   ```bash
   # 检查是否有敏感文件
   git ls-files | grep -E '\.(sql|env|key|pem)$'
   
   # 从 Git 历史中删除敏感文件
   git rm --cached <敏感文件>
   ```

## 示例工作流

### 首次推送
```bash
# 1. 初始化仓库
git init

# 2. 添加所有文件
git add .

# 3. 创建提交
git commit -m "init: 项目初始化"

# 4. 添加远程仓库
git remote add gitee https://gitee.com/用户名/仓库名.git

# 5. 推送
git push gitee main
```

### 日常更新
```bash
# 1. 查看变更
git status

# 2. 添加变更
git add .

# 3. 提交
git commit -m "feat: 新增功能描述"

# 4. 推送
git push gitee main
```

## 注意事项

1. **Gitee 限制**:
   - 单文件最大 100MB
   - 仓库总大小限制（免费用户 500MB）
   - 大文件请使用 Git LFS

2. **推送前必查**:
   - [ ] 无敏感信息（密码、密钥等）
   - [ ] .gitignore 已正确配置
   - [ ] 代码通过基本测试
   - [ ] 提交信息清晰准确

3. **性能优化**:
   - 大文件使用 Git LFS
   - 定期清理 Git 对象：`git gc`
   - 使用浅克隆加速：`git clone --depth 1`

## 相关技能

- github 代码上传
- using-git-worktrees
- 代码审查
- verification-before-completion
