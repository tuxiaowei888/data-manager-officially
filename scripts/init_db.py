"""
数据库初始化脚本 - 数维数据管家系统
功能：
1. 创建所有数据库表
2. 检查 rule_configs 表是否为空
3. 若为空，读取 JSON 文件并插入 18 条预设规则
"""
import json
import os
import sys

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import engine, Base, SessionLocal
from models.rule_config import RuleConfig
from models.evaluation_result import EvaluationResult
from models.knowledge_doc import KnowledgeDoc


def create_tables():
    """创建所有数据库表"""
    print("正在创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("✓ 数据库表创建完成")


def init_seed_rules():
    """初始化种子规则数据"""
    print("\n正在检查规则数据...")
    
    db = SessionLocal()
    try:
        # 检查 rule_configs 表是否为空
        existing_count = db.query(RuleConfig).count()
        
        if existing_count > 0:
            print(f"✓ 规则表已有 {existing_count} 条数据，跳过初始化")
            return
        
        # 读取 JSON 文件
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
        
        # 插入规则
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
                ai_prompt_context=rule_data.get("ai_prompt_context")
            )
            rule_objects.append(rule)
        
        db.add_all(rule_objects)
        db.commit()
        
        print(f"✓ 成功插入 {len(rule_objects)} 条预设规则")
        print("\n规则分布:")
        
        # 统计各维度规则数量
        dimension_count = {}
        for rule in rule_objects:
            dim = rule.dimension_code
            dimension_count[dim] = dimension_count.get(dim, 0) + 1
        
        for dim, count in sorted(dimension_count.items()):
            print(f"  - {dim}: {count} 条")
        
    except Exception as e:
        db.rollback()
        print(f"✗ 初始化失败：{str(e)}")
        raise
    finally:
        db.close()


def main():
    """主函数"""
    print("=" * 60)
    print("数维数据管家系统 - 数据库初始化脚本")
    print("=" * 60)
    
    try:
        # 创建表
        create_tables()
        
        # 初始化种子规则
        init_seed_rules()
        
        print("\n" + "=" * 60)
        print("✓ 数据库初始化完成")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"✗ 初始化失败：{str(e)}")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
