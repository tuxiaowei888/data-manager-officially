-- ============================================================
-- 数维数据管家系统 - 数据库扩展
-- 版本：V1.5 - 用户系统与推荐码
-- 创建时间：2026-03-13
-- ============================================================

USE shuwei_data_manager;

-- ============================================================
-- 1. 创建渠道表（推荐码管理）
-- ============================================================
CREATE TABLE IF NOT EXISTS channels (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '渠道 ID',
    channel_name VARCHAR(100) NOT NULL COMMENT '渠道名称',
    channel_code VARCHAR(20) UNIQUE NOT NULL COMMENT '推荐码（唯一）',
    contact_person VARCHAR(50) COMMENT '联系人',
    contact_phone VARCHAR(20) COMMENT '联系电话',
    referred_users_count INT DEFAULT 0 COMMENT '推荐用户总数',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    remark TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='渠道表';

-- ============================================================
-- 2. 创建用户表
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户 ID',
    username VARCHAR(50) UNIQUE NOT NULL COMMENT '用户名',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    email VARCHAR(100) COMMENT '邮箱',
    phone VARCHAR(20) COMMENT '手机号',
    referrer_code VARCHAR(20) COMMENT '推荐码（注册时填写）',
    channel_id INT COMMENT '绑定渠道 ID',
    user_type ENUM('client', 'admin', 'channel') DEFAULT 'client' COMMENT '用户类型',
    is_vip BOOLEAN DEFAULT FALSE COMMENT '是否 VIP',
    vip_expire_date DATE COMMENT 'VIP 到期日期',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    last_login_at TIMESTAMP NULL COMMENT '最后登录时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- ============================================================
-- 3. 创建渠道用户关联表
-- ============================================================
CREATE TABLE IF NOT EXISTS channel_user_relations (
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '关联 ID',
    channel_id INT NOT NULL COMMENT '渠道 ID',
    user_id INT NOT NULL COMMENT '用户 ID',
    relation_type ENUM('direct', 'indirect') DEFAULT 'direct' COMMENT '推荐关系类型',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '绑定时间',
    FOREIGN KEY (channel_id) REFERENCES channels(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uk_channel_user (channel_id, user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='渠道用户关联表';

-- ============================================================
-- 4. 扩展 evaluation_results 表
-- ============================================================
ALTER TABLE evaluation_results 
ADD COLUMN user_id INT COMMENT '用户 ID' AFTER id,
ADD COLUMN report_pdf_url VARCHAR(500) COMMENT 'PDF 报告下载地址' AFTER report_data,
ADD COLUMN report_word_url VARCHAR(500) COMMENT 'Word 报告下载地址' AFTER report_pdf_url,
ADD COLUMN is_deleted BOOLEAN DEFAULT FALSE COMMENT '是否删除' AFTER generated_at;

-- 设置默认值
UPDATE evaluation_results SET user_id = 1 WHERE user_id IS NULL;
UPDATE evaluation_results SET is_deleted = FALSE WHERE is_deleted IS NULL;

-- ============================================================
-- 5. 插入测试数据
-- ============================================================

-- 插入测试渠道
INSERT INTO channels (channel_name, channel_code, contact_person, contact_phone, remark) VALUES
('官方直营', 'OFFICIAL', '系统管理员', '13800000000', '官方渠道'),
('合作伙伴 A', 'PARTNER_A', '张三', '13800000001', '首批合作伙伴'),
('合作伙伴 B', 'PARTNER_B', '李四', '13800000002', '战略合作伙伴');

-- 插入测试用户（密码都是 123456）
-- 注意：这里的密码哈希是 bcrypt 生成的示例
INSERT INTO users (username, password_hash, email, phone, referrer_code, channel_id, user_type, is_vip) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu', 'admin@shuwei.com', '13800000000', NULL, NULL, 'admin', FALSE),
('test_user', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu', 'test@test.com', '13800000001', 'OFFICIAL', 1, 'client', FALSE),
('vip_user', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzS3MebAJu', 'vip@test.com', '13800000002', 'PARTNER_A', 2, 'client', TRUE);

-- 设置 VIP 到期日期
UPDATE users SET vip_expire_date = DATE_ADD(NOW(), INTERVAL 1 YEAR) WHERE username = 'vip_user';

-- 插入渠道用户关联
INSERT INTO channel_user_relations (channel_id, user_id, relation_type) VALUES
(1, 2, 'direct'),
(2, 3, 'direct');

-- 更新渠道推荐用户数
UPDATE channels SET referred_users_count = (
    SELECT COUNT(*) FROM channel_user_relations WHERE channel_id = channels.id
);

-- ============================================================
-- 6. 验证结果
-- ============================================================
SELECT '✅ 数据库扩展完成！' as status;
SELECT CONCAT('渠道数量：', COUNT(*)) as info FROM channels;
SELECT CONCAT('用户数量：', COUNT(*)) as info FROM users;
SELECT CONCAT('关联记录：', COUNT(*)) as info FROM channel_user_relations;
