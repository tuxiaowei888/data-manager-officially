# GitHub 代码上传技能

帮助用户将代码上传到 GitHub 仓库。当用户需要推送代码到 GitHub、初始化 Git 仓库、配置远程仓库或解决上传问题时调用。

## 适用场景

- 首次将项目推送到 GitHub
- 添加 GitHub 远程仓库
- 推送代码更新到 GitHub
- 解决 GitHub 推送问题
- 配置 GitHub 仓库认证

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

# 添加或更新 GitHub 远程仓库
git remote add github https://github.com/用户名/仓库名.git
# 或更新现有远程
git remote set-url github https://github.com/用户名/仓库名.git
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

### 5. 推送到 GitHub
```bash
# 推送到 main 分支
git push github main

# 或强制推送（谨慎使用）
git push github main -f

# 推送所有分支
git push github --all

# 推送所有标签
git push github --tags
```

### 6. 配置认证（如果需要）
```bash
# 配置凭证存储
git config --global credential.helper store

# 或使用 SSH 密钥
# 生成 SSH 密钥
ssh-keygen -t ed25519 -C "your_email@example.com"

# 将公钥添加到 GitHub: https://github.com/settings/keys
```

## 常见问题解决

### 问题 1: 认证失败
**症状**: `remote: Invalid username or password` 或 `Authentication failed`

**解决方案**:
```bash
# 清除保存的凭证
git credential-manager erase

# 重新推送，会提示输入新凭证
git push github main

# 或使用 Personal Access Token (PAT)
# 创建 Token: https://github.com/settings/tokens
# 使用时 Token 作为密码
```

### 问题 2: 分支不存在
**症状**: `error: src refspec main does not match any`

**解决方案**:
```bash
# 创建并切换到 main 分支
git checkout -b main

# 重新推送
git push github main
```

### 问题 3: 远程仓库已存在
**症状**: `remote github already exists`

**解决方案**:
```bash
# 更新远程仓库 URL
git remote set-url github https://github.com/新地址.git
```

### 问题 4: 推送被拒绝
**症状**: `rejected non-fast-forward`

**解决方案**:
```bash
# 先拉取远程变更
git pull github main

# 解决冲突后推送
git push github main

# 或强制推送（慎用）
git push github main -f
```

### 问题 5: Git LFS 大文件
**症状**: `file is larger than the maximum size`

**解决方案**:
```bash
# 安装 Git LFS
git lfs install

# 跟踪大文件类型
git lfs track "*.zip"
git lfs track "*.psd"
git lfs track "*.pdf"

# 提交 .gitattributes
git add .gitattributes
git commit -m "chore: 配置 Git LFS"

# 重新推送
git push github main
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

5. **GitHub 特定优化**
   ```bash
   # 添加 GitHub Actions 工作流
   # .github/workflows/ci.yml
   
   # 添加 ISSUE_TEMPLATE
   # .github/ISSUE_TEMPLATE/bug_report.md
   
   # 添加 PULL_REQUEST_TEMPLATE
   # .github/pull_request_template.md
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
git remote add github https://github.com/用户名/仓库名.git

# 5. 推送
git push github main
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
git push github main
```

### 多仓库同步（Gitee + GitHub）
```bash
# 1. 添加两个远程仓库
git remote add gitee https://gitee.com/用户名/仓库名.git
git remote add github https://github.com/用户名/仓库名.git

# 2. 推送到两个平台
git push gitee main
git push github main

# 3. 或创建别名一次性推送
git remote set-url --add --push origin https://gitee.com/用户名/仓库名.git
git remote set-url --add --push origin https://github.com/用户名/仓库名.git
git push origin main
```

## 注意事项

1. **GitHub 限制**:
   - 单文件最大 100MB（超过需使用 Git LFS）
   - 仓库总大小建议不超过 1GB
   - 每月 Git LFS 带宽限制（免费 1GB）

2. **推送前必查**:
   - [ ] 无敏感信息（密码、密钥、Token 等）
   - [ ] .gitignore 已正确配置
   - [ ] 代码通过基本测试
   - [ ] 提交信息清晰准确
   - [ ] 大文件已使用 Git LFS

3. **性能优化**:
   - 大文件使用 Git LFS
   - 定期清理 Git 对象：`git gc`
   - 使用浅克隆加速：`git clone --depth 1`
   - 配置 Git 缓存：`git config --global http.postBuffer 524288000`

4. **GitHub Actions 集成**:
   ```yaml
   # .github/workflows/ci.yml
   name: CI
   
   on: [push, pull_request]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         - name: Run tests
           run: python -m pytest
   ```

## 相关技能

- gitee 代码上传
- using-git-worktrees
- 代码审查
- verification-before-completion
- requesting-code-review

## GitHub 特有功能

### GitHub Pages 部署
```bash
# 推送到 gh-pages 分支
git checkout -b gh-pages
git push github gh-pages

# 启用 Pages: Settings -> Pages -> Source: gh-pages
```

### GitHub Releases
```bash
# 创建标签
git tag -a v1.0.0 -m "版本 1.0.0"

# 推送标签
git push github v1.0.0

# 或使用 GitHub CLI
gh release create v1.0.0 --title "版本 1.0.0" --notes "更新说明"
```

### GitHub CLI 使用
```bash
# 安装 GitHub CLI
# Windows: wingt install gh

# 认证
gh auth login

# 创建仓库
gh repo create 仓库名 --public --source=. --remote=github

# 创建 Pull Request
gh pr create --title "功能标题" --body "详细描述"

# 查看 Issues
gh issue list
```
