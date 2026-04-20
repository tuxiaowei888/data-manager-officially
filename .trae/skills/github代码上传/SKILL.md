---
name: "github代码上传"
description: "帮助用户将代码上传到 GitHub 仓库。当用户需要推送代码到 GitHub、初始化 Git 仓库、配置远程仓库或解决上传问题时调用。"
---

# GitHub 代码上传助手

## 功能说明

本 Skill 协助用户将项目代码上传到 GitHub 仓库，包括：
- 初始化 Git 仓库
- 配置 GitHub 远程仓库
- 推送代码到 GitHub
- 解决上传过程中的常见问题
- 支持 SSH 和 HTTPS 两种方式

## 使用前提

1. 已安装 Git
2. 已注册 GitHub 账号 (https://github.com)
3. 已在 GitHub 创建仓库（可选，可后续创建）

## Gitee vs GitHub 对比

| 特性 | Gitee | GitHub |
|------|-------|--------|
| 访问速度 | 国内快 | 国外快，国内需加速器 |
| 私有仓库 | 免费 | 免费 |
| 协作功能 | 适合国内团队 | 适合国际团队 |
| CI/CD | 支持 | GitHub Actions 更强大 |
| 推荐场景 | 国内部署、国内访问 | 开源项目、国际协作 |

## 使用步骤

### 第一步：检查 Git 状态

```bash
# 检查当前目录是否是 Git 仓库
git status

# 如果不是，初始化仓库
git init
```

### 第二步：配置 Git 用户信息（首次使用）

```bash
# 配置用户名和邮箱（使用 GitHub 账号信息）
git config user.name "你的GitHub用户名"
git config user.email "你的GitHub邮箱"

# 查看配置
git config --list
```

### 第三步：添加文件到暂存区

```bash
# 添加所有文件（自动排除 .gitignore 中的内容）
git add .

# 或者添加指定文件
git add 文件名
```

### 第四步：提交代码

```bash
# 提交并添加说明
git commit -m "提交说明"

# 示例
git commit -m "Initial commit: 数维数据管家系统"
git commit -m "feat: 添加用户登录功能"
git commit -m "fix: 修复数据库连接问题"
```

### 第五步：配置 GitHub 远程仓库

#### 方式 A：HTTPS（简单，每次需输入密码）

```bash
# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://github.com/你的用户名/仓库名.git

# 验证远程仓库
git remote -v
```

#### 方式 B：SSH（推荐，免密码）

```bash
# 添加远程仓库（使用 SSH 地址）
git remote add origin git@github.com:你的用户名/仓库名.git

# 验证远程仓库
git remote -v
```

**SSH 配置方法见下方"SSH 密钥配置"章节**

### 第六步：推送到 GitHub

```bash
# 首次推送（建立关联）
git push -u origin main

# 或者使用 master 分支（旧仓库）
git push -u origin master

# 后续推送（简化命令）
git push
```

**注意**：GitHub 新仓库默认使用 `main` 分支，旧仓库可能使用 `master`

## 同时推送到 Gitee 和 GitHub（双平台）

如果你想同时维护两个平台：

```bash
# 1. 添加 Gitee 远程仓库（命名为 gitee）
git remote add gitee https://gitee.com/用户名/仓库名.git

# 2. 添加 GitHub 远程仓库（命名为 github）
git remote add github https://github.com/用户名/仓库名.git

# 3. 推送到 Gitee
git push gitee main

# 4. 推送到 GitHub
git push github main

# 或者一次性推送到所有远程
git push --all
```

## 常用命令速查

| 命令 | 说明 |
|------|------|
| `git status` | 查看当前状态 |
| `git add .` | 添加所有更改 |
| `git commit -m "说明"` | 提交更改 |
| `git push` | 推送到远程 |
| `git pull` | 拉取远程更新 |
| `git log` | 查看提交历史 |
| `git remote -v` | 查看远程仓库 |
| `git remote add 名称 地址` | 添加远程仓库 |

## 常见问题解决

### 问题 1：提示 "fatal: not a git repository"

**原因**：当前目录不是 Git 仓库

**解决**：
```bash
git init
```

### 问题 2：提示 "fatal: remote origin already exists"

**原因**：远程仓库已存在

**解决**：
```bash
# 删除现有远程仓库
git remote remove origin

# 重新添加
git remote add origin https://github.com/你的用户名/仓库名.git
```

### 问题 3：提示 "failed to push some refs"

**原因**：远程仓库有本地没有的更新

**解决**：
```bash
# 先拉取远程更新
git pull origin main

# 然后再推送
git push
```

### 问题 4：提示 "Permission denied" 或 "403 Forbidden"

**原因**：没有权限或需要登录

**解决**：
1. 检查仓库地址是否正确
2. 确认是仓库所有者或协作者
3. 使用 HTTPS 时需要输入 GitHub 账号密码或 Token
4. **推荐**：使用 SSH 密钥（见下方配置）

### 问题 5：GitHub 访问慢或超时

**原因**：国内访问 GitHub 网络不稳定

**解决**：
1. 使用网络加速器/代理
2. 修改 hosts 文件
3. 使用 Gitee 作为备用（国内访问快）

### 问题 6：提示 "Support for password authentication was removed"

**原因**：GitHub 已不支持密码验证，需要使用 Token

**解决**：
1. 生成 Personal Access Token：
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - 点击 "Generate new token"
   - 选择权限（至少勾选 `repo`）
   - 生成后复制 Token

2. 使用 Token 代替密码：
   - 用户名：你的 GitHub 用户名
   - 密码：粘贴刚才生成的 Token

## SSH 密钥配置（强烈推荐）

使用 SSH 可以避免每次输入密码，且更安全：

```bash
# 1. 生成 SSH 密钥（使用你的 GitHub 邮箱）
ssh-keygen -t ed25519 -C "你的邮箱@example.com"

# 2. 按回车使用默认路径，可设置密码（也可留空）

# 3. 复制公钥内容
cat ~/.ssh/id_ed25519.pub
# Windows 上也可以用：clip < ~/.ssh/id_ed25519.pub

# 4. 在 GitHub 添加 SSH 公钥：
#    GitHub → Settings → SSH and GPG keys → New SSH key
#    粘贴公钥内容，保存

# 5. 测试连接
ssh -T git@github.com
# 看到 "Hi 用户名! You've successfully authenticated" 表示成功

# 6. 使用 SSH 地址推送
git remote add origin git@github.com:用户名/仓库名.git
```

## 创建 GitHub 仓库步骤

1. 打开 https://github.com
2. 登录你的账号
3. 点击右上角 **"+"** → **"New repository"**
4. 填写信息：
   - **Repository name**：仓库名称（如 `data-manager-officially`）
   - **Description**：仓库描述（可选）
   - **Public/Private**：选择公开或私有
   - **Initialize this repository with**：
     - ☑️ Add a README file（推荐）
     - 选择 .gitignore 模板（Python 项目选 Python）
     - 选择 License（可选）
5. 点击 **"Create repository"**
6. 复制仓库地址（HTTPS 或 SSH）

## 提交规范建议

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat:` | 新功能 | `feat: 添加用户登录` |
| `fix:` | 修复问题 | `fix: 修复数据库连接` |
| `docs:` | 文档更新 | `docs: 更新 README` |
| `style:` | 代码格式 | `style: 格式化代码` |
| `refactor:` | 重构 | `refactor: 优化查询逻辑` |
| `test:` | 测试相关 | `test: 添加单元测试` |
| `chore:` | 构建/工具 | `chore: 更新依赖` |

## 完整示例流程

```bash
# 1. 进入项目目录
cd d:\数维创擎\代码库\数维数据管家系统

# 2. 初始化 Git（如果还没初始化）
git init

# 3. 配置用户信息
git config user.name "你的GitHub用户名"
git config user.email "你的邮箱@example.com"

# 4. 添加文件
git add .

# 5. 提交
git commit -m "Initial commit: 数维数据管家系统"

# 6. 添加 GitHub 远程仓库（SSH 方式推荐）
git remote add origin git@github.com:你的用户名/data-manager-officially.git

# 7. 推送
git push -u origin main
```

## Gitee 和 GitHub 同时维护示例

```bash
# 场景：代码已在 Gitee，想同时推送到 GitHub

# 1. 查看现有远程仓库
git remote -v
# 应该显示：origin https://gitee.com/xxx/xxx.git

# 2. 重命名 Gitee 远程为 gitee
git remote rename origin gitee

# 3. 添加 GitHub 远程
git remote add github git@github.com:你的用户名/data-manager-officially.git

# 4. 推送到两个平台
git push gitee main
git push github main

# 5. 以后更新时，推送命令
git push gitee main
git push github main
```

## 选择建议

| 场景 | 推荐平台 | 原因 |
|------|---------|------|
| 国内部署、国内用户访问 | Gitee | 访问速度快 |
| 开源项目、国际协作 | GitHub | 生态更完善 |
| 需要 CI/CD 自动化 | GitHub | GitHub Actions 强大 |
| 代码备份、双保险 | Gitee + GitHub | 双平台同时维护 |
| 学习开源、参与社区 | GitHub | 开源项目多 |

## 提示

- GitHub 国内访问可能较慢，建议配置代理或使用加速器
- 私有仓库在 GitHub 和 Gitee 都是免费的
- 建议配置 SSH 密钥，避免每次输入密码
- 重要项目建议同时备份到 Gitee 和 GitHub
