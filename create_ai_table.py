import sys
sys.path.insert(0, '.')

from config.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    try:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS ai_configs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                config_name VARCHAR(100) NOT NULL COMMENT '配置名称',
                provider VARCHAR(50) NOT NULL COMMENT 'AI提供商',
                api_key VARCHAR(255) COMMENT 'API密钥',
                api_base_url VARCHAR(255) COMMENT 'API基础URL',
                model_name VARCHAR(100) NOT NULL COMMENT '模型名称',
                temperature VARCHAR(10) DEFAULT '0.7' COMMENT '温度参数',
                max_tokens INT DEFAULT 4096 COMMENT '最大token数',
                system_prompt TEXT COMMENT '系统提示词',
                report_prompt_template TEXT COMMENT '报告生成提示词模板',
                is_active TINYINT DEFAULT 1 COMMENT '是否启用',
                is_default TINYINT DEFAULT 0 COMMENT '是否默认配置',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
        """))
        conn.commit()
        print("✅ ai_configs 表创建成功")
    except Exception as e:
        print(f"创建表失败: {e}")
