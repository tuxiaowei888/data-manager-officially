"""
完整数据库初始化脚本 - 数维数据管家系统
功能：
1. 创建所有数据库表
2. 初始化系统配置
3. 初始化知识库分类
4. 初始化规则数据
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import engine, Base, SessionLocal
from models.rule_config import RuleConfig
from models.evaluation_result import EvaluationResult
from models.knowledge_doc import KnowledgeDoc
from models.user import User
from models.channel import Channel
from models.ai_config import AIConfig
from models.knowledge_category import KnowledgeCategory
from models.system_config import SystemConfig, init_system_configs, DEFAULT_CONFIGS
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_tables():
    """创建所有数据库表"""
    print("正在创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("✓ 数据库表创建完成")
    
    tables = [
        "users", "channels", "rule_configs", "evaluation_results",
        "knowledge_docs", "ai_configs", "knowledge_categories",
        "system_configs"
    ]
    
    print("\n已创建的表：")
    for table in tables:
        print(f"  - {table}")


def init_knowledge_categories(db):
    """初始化知识库分类"""
    print("\n正在初始化知识库分类...")
    
    from models.knowledge_category import DEFAULT_CATEGORIES
    
    existing_count = db.query(KnowledgeCategory).count()
    if existing_count > 0:
        print(f"✓ 知识库分类表已有 {existing_count} 条数据，跳过初始化")
        return
    
    categories = []
    for cat_data in DEFAULT_CATEGORIES:
        cat = KnowledgeCategory(
            name=cat_data["name"],
            description=cat_data["description"],
            icon=cat_data["icon"],
            sort_order=len(categories) + 1
        )
        categories.append(cat)
    
    db.add_all(categories)
    db.commit()
    print(f"✓ 成功插入 {len(categories)} 条知识库分类")


def init_seed_rules(db):
    """初始化种子规则数据"""
    print("\n正在检查规则数据...")
    
    existing_count = db.query(RuleConfig).count()
    if existing_count > 0:
        print(f"✓ 规则表已有 {existing_count} 条数据，跳过初始化")
        return
    
    json_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "seed_rules_v1.json"
    )
    
    if not os.path.exists(json_path):
        print(f"✗ 错误：种子数据文件不存在：{json_path}")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        seed_data = json.load(f)
    
    rules = seed_data.get("rules", [])
    
    if not rules:
        print("✗ 错误：种子数据文件中没有规则")
        return
    
    rule_objects = []
    for rule_data in rules:
        rule = RuleConfig(
            dimension_code=rule_data["dimension_code"],
            rule_name=rule_data["rule_name"],
            logic_expression=rule_data["logic_expression"],
            weight=rule_data["weight"],
            risk_threshold=rule_data["risk_threshold"],
            is_active=rule_data["is_active"],
            source_type=rule_data["source_type"],
            version=rule_data["version"],
            ai_prompt_context=rule_data.get("ai_prompt_context"),
            rule_description=rule_data.get("rule_description")
        )
        rule_objects.append(rule)
    
    db.add_all(rule_objects)
    db.commit()
    
    print(f"✓ 成功插入 {len(rule_objects)} 条预设规则")
    
    dimension_count = {}
    for rule in rule_objects:
        dim = rule.dimension_code
        dimension_count[dim] = dimension_count.get(dim, 0) + 1
    
    print("\n规则分布:")
    for dim, count in sorted(dimension_count.items()):
        print(f"  - {dim}: {count} 条")


def init_sample_data(db):
    """初始化示例数据"""
    print("\n正在初始化示例数据...")
    
    user_count = db.query(User).count()
    if user_count > 0:
        print(f"✓ 用户表已有 {user_count} 条数据，跳过初始化")
        return
    
    # 简化密码哈希处理，确保密码长度不超过72字节
    admin = User(
        username="admin",
        password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # admin123
        email="admin@shuwei.com",
        phone="13800000000",
        user_type="admin",
        is_vip=True,
        is_active=True
    )
    
    test_user = User(
        username="test_user",
        password_hash="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",  # test123
        email="test@test.com",
        phone="13800000001",
        user_type="client",
        is_vip=False,
        is_active=True
    )
    
    official_channel = Channel(
        channel_name="官方渠道",
        channel_code="OFFICIAL",
        contact_person="系统管理员",
        contact_phone="13800000000",
        is_active=True
    )
    
    from models.ai_config import DEFAULT_SYSTEM_PROMPT, DEFAULT_REPORT_PROMPT
    
    ai_config = AIConfig(
        config_name="数维数据管家AI",
        provider="deepseek",
        api_key="",
        model_name="deepseek-chat",
        temperature=0.7,
        max_tokens=4096,
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        report_prompt_template=DEFAULT_REPORT_PROMPT,
        is_active=True,
        is_default=True
    )
    
    db.add_all([admin, test_user, official_channel, ai_config])
    db.commit()
    print("✓ 示例数据初始化完成")


def main():
    """主函数"""
    print("=" * 60)
    print("数维数据管家系统 - 完整数据库初始化脚本")
    print("=" * 60)
    
    try:
        create_tables()
        
        db = SessionLocal()
        try:
            init_system_configs(db)
            init_knowledge_categories(db)
            init_seed_rules(db)
            init_sample_data(db)
        finally:
            db.close()
        
        print("\n" + "=" * 60)
        print("✓ 数据库初始化完成")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"✗ 初始化失败：{str(e)}")
        import traceback
        traceback.print_exc()
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
