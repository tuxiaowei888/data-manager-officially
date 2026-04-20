#!/usr/bin/env python3
"""
数维数据管家系统 V2.0 订阅体系数据库迁移脚本
执行顺序：
1. 备份数据库
2. 执行表结构变更
3. 初始化配置
4. 验证迁移结果

注意：在生产环境执行前请先备份数据库！
"""
import sys
import os
from datetime import datetime, timedelta

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text, inspect
from config.database import SessionLocal, engine
from models.system_config import init_system_configs


def backup_database():
    """备份数据库（建议手动执行）"""
    print("⚠️  警告：请先手动备份数据库！")
    print("   推荐命令：mysqldump -u root -p shuwei_data_manager > backup_$(date +%Y%m%d_%H%M%S).sql")
    confirm = input("是否已备份数据库？(y/N): ")
    if confirm.lower() != 'y':
        print("❌ 迁移中止，请先备份数据库")
        sys.exit(1)
    return True


def check_table_exists(table_name):
    """检查表是否存在"""
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()


def execute_sql(sql_statements):
    """执行SQL语句"""
    db = SessionLocal()
    try:
        for sql in sql_statements:
            print(f"执行SQL: {sql[:80]}...")
            db.execute(text(sql))
        db.commit()
        print("✅ SQL执行完成")
        return True
    except Exception as e:
        db.rollback()
        print(f"❌ SQL执行失败: {e}")
        return False
    finally:
        db.close()


def migrate_user_table():
    """迁移User表，添加订阅相关字段"""
    print("\n🔧 迁移User表...")
    
    sql_statements = [
        # 检查字段是否已存在，不存在则添加
        """
        ALTER TABLE users 
        ADD COLUMN IF NOT EXISTS subscription_tier VARCHAR(20) DEFAULT 'free' COMMENT '订阅档位：free/basic/pro/enterprise'
        """,
        """
        ALTER TABLE users 
        ADD COLUMN IF NOT EXISTS subscription_start_date DATE COMMENT '订阅开始日期'
        """,
        """
        ALTER TABLE users 
        ADD COLUMN IF NOT EXISTS eval_count_used INT DEFAULT 0 COMMENT '本年度已使用评估次数'
        """,
        """
        ALTER TABLE users 
        ADD COLUMN IF NOT EXISTS eval_count_reset_date DATE COMMENT '评估次数重置日期'
        """,
        """
        ALTER TABLE users 
        ADD COLUMN IF NOT EXISTS customer_tier_signal INT DEFAULT 0 COMMENT '客户分层信号分'
        """,
        """
        ALTER TABLE users 
        ADD COLUMN IF NOT EXISTS customer_tier_label VARCHAR(20) DEFAULT 'observer' COMMENT '客户分层：high_value/nurturing/observer'
        """,
        """
        ALTER TABLE users 
        ADD COLUMN IF NOT EXISTS last_signal_update DATETIME COMMENT '信号分最后更新时间'
        """
    ]
    
    return execute_sql(sql_statements)


def create_org_profiles_table():
    """创建企业画像表"""
    print("\n🔧 创建org_profiles表...")
    
    if check_table_exists("org_profiles"):
        print("✅ org_profiles表已存在，跳过创建")
        return True
    
    sql_statements = [
        """
        CREATE TABLE org_profiles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            org_name VARCHAR(200),
            industry VARCHAR(100),
            company_size VARCHAR(50),
            data_team_status VARCHAR(50),
            security_certs JSON,
            data_security_measures VARCHAR(100),
            compliance_history VARCHAR(100),
            contact_name VARCHAR(100),
            contact_phone VARCHAR(20),
            contact_email VARCHAR(100),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_user_id (user_id),
            INDEX idx_org_profile_id (id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            CONSTRAINT fk_org_profiles_user FOREIGN KEY (user_id) REFERENCES users(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        COMMENT='企业画像表'
        """
    ]
    
    return execute_sql(sql_statements)


def create_datasets_table():
    """创建数据集表"""
    print("\n🔧 创建datasets表...")
    
    if check_table_exists("datasets"):
        print("✅ datasets表已存在，跳过创建")
        return True
    
    sql_statements = [
        """
        CREATE TABLE datasets (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            org_profile_id INT,
            dataset_name VARCHAR(200) NOT NULL,
            dataset_type VARCHAR(50),
            data_volume_value FLOAT,
            data_volume_unit VARCHAR(20),
            contains_personal_info BOOLEAN DEFAULT FALSE,
            desensitization_status VARCHAR(50),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_user_id (user_id),
            INDEX idx_org_profile_id (org_profile_id),
            INDEX idx_dataset_id (id),
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (org_profile_id) REFERENCES org_profiles(id) ON DELETE SET NULL,
            CONSTRAINT fk_datasets_user FOREIGN KEY (user_id) REFERENCES users(id),
            CONSTRAINT fk_datasets_org_profile FOREIGN KEY (org_profile_id) REFERENCES org_profiles(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        COMMENT='数据集表'
        """
    ]
    
    return execute_sql(sql_statements)


def migrate_evaluation_results_table():
    """迁移evaluation_results表，添加关联字段"""
    print("\n🔧 迁移evaluation_results表...")
    
    # 检查字段是否已存在
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns('evaluation_results')]
    
    sql_statements = []
    
    if 'dataset_id' not in columns:
        sql_statements.append("""
        ALTER TABLE evaluation_results 
        ADD COLUMN dataset_id INT COMMENT '数据集ID'
        """)
    
    if 'org_profile_id' not in columns:
        sql_statements.append("""
        ALTER TABLE evaluation_results 
        ADD COLUMN org_profile_id INT COMMENT '企业画像ID'
        """)
    
    if 'subscription_tier' not in columns:
        sql_statements.append("""
        ALTER TABLE evaluation_results 
        ADD COLUMN subscription_tier VARCHAR(20) DEFAULT 'free' COMMENT '评估时的订阅档位'
        """)
    
    # 添加索引
    if 'dataset_id' not in columns:
        sql_statements.append("CREATE INDEX idx_dataset_id ON evaluation_results(dataset_id)")
    
    if 'org_profile_id' not in columns:
        sql_statements.append("CREATE INDEX idx_org_profile_id ON evaluation_results(org_profile_id)")
    
    # 添加外键约束
    if 'dataset_id' not in columns:
        sql_statements.append("""
        ALTER TABLE evaluation_results 
        ADD CONSTRAINT fk_evaluation_results_dataset 
        FOREIGN KEY (dataset_id) REFERENCES datasets(id) ON DELETE SET NULL
        """)
    
    if 'org_profile_id' not in columns:
        sql_statements.append("""
        ALTER TABLE evaluation_results 
        ADD CONSTRAINT fk_evaluation_results_org_profile 
        FOREIGN KEY (org_profile_id) REFERENCES org_profiles(id) ON DELETE SET NULL
        """)
    
    if not sql_statements:
        print("✅ evaluation_results表已包含所有字段，跳过迁移")
        return True
    
    return execute_sql(sql_statements)


def migrate_existing_vip_users():
    """迁移现有的VIP用户到新的订阅体系"""
    print("\n🔧 迁移现有VIP用户...")
    
    db = SessionLocal()
    try:
        # 获取所有VIP用户（is_vip=True且未过期）
        from models.user import User
        from datetime import date
        
        today = date.today()
        vip_users = db.query(User).filter(
            User.is_vip == True,
            User.vip_expire_date >= today
        ).all()
        
        migrated_count = 0
        for user in vip_users:
            if not user.subscription_tier or user.subscription_tier == 'free':
                # 设置订阅档位为基础版
                user.subscription_tier = 'basic'
                user.subscription_start_date = user.vip_expire_date - timedelta(days=30)  # 假设30天前开始
                migrated_count += 1
        
        db.commit()
        print(f"✅ 成功迁移 {migrated_count} 个VIP用户到基础版订阅")
        return True
        
    except Exception as e:
        db.rollback()
        print(f"❌ VIP用户迁移失败: {e}")
        return False
    finally:
        db.close()


def initialize_system_configs():
    """初始化系统配置"""
    print("\n🔧 初始化系统配置...")
    
    db = SessionLocal()
    try:
        init_system_configs(db)
        print("✅ 系统配置初始化完成")
        return True
    except Exception as e:
        print(f"❌ 系统配置初始化失败: {e}")
        return False
    finally:
        db.close()


def verify_migration():
    """验证迁移结果"""
    print("\n🔍 验证迁移结果...")
    
    db = SessionLocal()
    try:
        # 检查表是否存在
        required_tables = ['org_profiles', 'datasets']
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        missing_tables = [table for table in required_tables if table not in existing_tables]
        if missing_tables:
            print(f"❌ 缺失表: {missing_tables}")
            return False
        
        # 检查User表新字段
        user_columns = [col['name'] for col in inspector.get_columns('users')]
        required_columns = ['subscription_tier', 'eval_count_used', 'customer_tier_label']
        missing_columns = [col for col in required_columns if col not in user_columns]
        if missing_columns:
            print(f"❌ User表缺失字段: {missing_columns}")
            return False
        
        # 检查evaluation_results表新字段
        eval_columns = [col['name'] for col in inspector.get_columns('evaluation_results')]
        required_eval_columns = ['dataset_id', 'org_profile_id', 'subscription_tier']
        missing_eval_columns = [col for col in required_eval_columns if col not in eval_columns]
        if missing_eval_columns:
            print(f"❌ evaluation_results表缺失字段: {missing_eval_columns}")
            return False
        
        print("✅ 所有迁移验证通过")
        return True
        
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False
    finally:
        db.close()


def main():
    """主迁移函数"""
    print("🚀 开始执行数维数据管家系统 V2.0 订阅体系数据库迁移")
    print("=" * 60)
    
    # 1. 备份检查
    if not backup_database():
        return
    
    # 2. 执行迁移步骤
    migration_steps = [
        ("迁移User表", migrate_user_table),
        ("创建企业画像表", create_org_profiles_table),
        ("创建数据集表", create_datasets_table),
        ("迁移评估结果表", migrate_evaluation_results_table),
        ("迁移现有VIP用户", migrate_existing_vip_users),
        ("初始化系统配置", initialize_system_configs),
    ]
    
    success = True
    for step_name, step_func in migration_steps:
        print(f"\n📋 步骤: {step_name}")
        if not step_func():
            success = False
            print(f"❌ {step_name} 失败")
            break
    
    # 3. 验证迁移
    if success:
        if not verify_migration():
            success = False
            print("❌ 迁移验证失败")
    
    # 4. 输出结果
    print("\n" + "=" * 60)
    if success:
        print("🎉 数据库迁移成功完成！")
        print("\n下一步操作：")
        print("1. 重启应用服务")
        print("2. 测试新功能")
        print("3. 监控系统运行状态")
    else:
        print("❌ 数据库迁移失败，请检查错误信息")
        sys.exit(1)


if __name__ == "__main__":
    main()