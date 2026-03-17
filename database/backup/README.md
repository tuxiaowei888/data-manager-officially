# 数维数据管家系统 - 数据库备份与恢复指南

## 📁 文件说明

| 文件名 | 说明 |
|--------|------|
| `shuwei_data_manager_backup.sql` | 数据库完整备份（结构+数据） |
| `备份数据库.bat` | 一键备份脚本 |
| `恢复数据库.bat` | 一键恢复脚本 |

## 🔄 在其他机器上恢复数据库

### 前置条件
1. 已安装 Docker Desktop
2. 已启动 MySQL 容器（运行 `启动服务.bat`）

### 恢复步骤

#### 方法一：使用恢复脚本（推荐）
1. 将整个 `database/backup` 文件夹复制到新机器
2. 确保备份文件名为 `shuwei_data_manager_backup.sql`
3. 双击运行 `恢复数据库.bat`
4. 等待恢复完成

#### 方法二：手动恢复
```bash
# 1. 复制备份文件到容器
docker cp shuwei_data_manager_backup.sql shuwei-mysql:/tmp/restore.sql

# 2. 执行恢复
docker exec shuwei-mysql sh -c "mysql -u root -proot < /tmp/restore.sql"
```

## 💾 定期备份

建议在以下情况执行备份：
- 完成重要功能开发后
- 每日开发结束前
- 重大数据变更前

### 执行备份
双击运行 `备份数据库.bat`，会生成带时间戳的备份文件。

## ⚠️ 注意事项

1. **恢复会覆盖现有数据**：恢复操作会删除现有数据库并重新创建
2. **容器必须运行**：备份和恢复前确保 MySQL 容器正在运行
3. **编码问题**：备份文件使用 UTF-8 编码，支持中文

## 📊 当前数据库结构

### 数据表清单
| 表名 | 说明 |
|------|------|
| `users` | 用户表 |
| `channels` | 渠道表 |
| `channel_user_relations` | 渠道用户关联表 |
| `evaluation_results` | 评估结果表 |
| `knowledge_docs` | 知识库文档表 |
| `rule_items` | 规则项表 |
| `survey_forms` | 调研表单表 |
| `survey_responses` | 调研响应表 |

### 数据库连接信息
```
主机: localhost
端口: 3306
数据库名: shuwei_data_manager
用户名: root
密码: root
字符集: utf8mb4
```

---
*最后更新: 2026-03-13*
