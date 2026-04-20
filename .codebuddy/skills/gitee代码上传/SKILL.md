---
name: gitee代码上传
description: 帮助用户将代码上传到 Gitee 仓库。当用户需要推送代码到 Gitee、初始化 Git 仓库、配置远程仓库或解决上传问题时调用。
---

# Gitee 代码上传助手

## 功能说明

本 Skill 协助用户将项目代码上传到 Gitee 仓库，包括：
- 初始化 Git 仓库
- 配置 Gitee 远程仓库
- 推送代码到 Gitee
- 解决上传过程中的常见问题

## 使用前提

1. 已安装 Git
2. 已注册 Gitee 账号
3. 已在 Gitee 创建仓库（可选，可后续创建）

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
# 配置用户名和邮箱（使用 Gitee 账号信息）
git config user.name "涂晓伟的GITEE"
git config user.email "tuxiaowei520@163.com"

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

### 第五步：配置 Gitee 远程仓库

#### 情况 A：已有 Gitee 仓库

```bash
# 添加远程仓库（替换为你的仓库地址）
git remote add origin https://gitee.com/你的用户名/仓库名.git

# 验证远程仓库
git remote -v
```

#### 情况 B：没有 Gitee 仓库

1. 登录 Gitee (https://gitee.com)
2. 点击右上角 "+" → "新建仓库"
3. 填写仓库信息：
   - 仓库名称：建议与项目名一致
   - 仓库介绍：简要描述项目
   - 是否开源：根据需求选择
4. 创建后复制仓库地址

### 第六步：推送到 Gitee

```bash
# 首次推送（建立关联）
git push -u origin master

# 或者使用 main 分支（新项目推荐）
git push -u origin main

# 后续推送（简化命令）
git push
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
git remote add origin https://gitee.com/你的用户名/仓库名.git
```

### 问题 3：提示 "failed to push some refs"

**原因**：远程仓库有本地没有的更新

**解决**：
```bash
# 先拉取远程更新
git pull origin master

# 然后再推送
git push
```

### 问题 4：提示 "Permission denied"

**原因**：没有权限或需要登录

**解决**：
1. 检查仓库地址是否正确
2. 确认是仓库所有者或协作者
3. 使用 HTTPS 地址时需要输入 Gitee 账号密码
4. 或使用 SSH 密钥（推荐）

### 问题 5：Windows 下中文显示乱码

**解决**：
```bash
# 设置 Git 使用 UTF-8
git config --global core.quotepath false
git config --global gui.encoding utf-8
git config --global i18n.commit.encoding utf-8
git config --global i18n.logoutputencoding utf-8
```

## SSH 密钥配置（推荐）

使用 SSH 可以避免每次输入密码：

```bash
# 1. 生成 SSH 密钥
ssh-keygen -t ed25519 -C "你的邮箱"

# 2. 复制公钥内容
cat ~/.ssh/id_ed25519.pub

# 3. 在 Gitee 设置中添加 SSH 公钥
#    路径：Gitee → 设置 → SSH 公钥 → 添加

# 4. 测试连接
ssh -T git@gitee.com

# 5. 使用 SSH 地址推送
git remote add origin git@gitee.com:用户名/仓库名.git
```

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

# 2. 初始化 Git
git init

# 3. 配置用户信息
git config user.name "张三"
git config user.email "zhangsan@example.com"

# 4. 添加文件
git add .

# 5. 提交
git commit -m "Initial commit: 数维数据管家系统"

# 6. 添加远程仓库
git remote add origin https://gitee.com/zhangsan/shuwei-data-manager.git

# 7. 推送
git push -u origin master
```