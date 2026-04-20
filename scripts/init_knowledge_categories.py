"""
初始化知识库目录分类
根据数据要素领域知识体系设计
"""
import json
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal
from models.knowledge_category import KnowledgeCategory


def init_categories():
    """初始化知识库目录分类"""
    db = SessionLocal()
    
    try:
        # 检查是否已有分类
        existing_count = db.query(KnowledgeCategory).count()
        if existing_count > 0:
            print(f"数据库中已有 {existing_count} 个分类")
            response = input("是否清空现有分类并重新初始化？(yes/no): ")
            if response.lower() != 'yes':
                print("已取消初始化")
                return
            
            # 清空现有分类
            db.query(KnowledgeCategory).delete()
            db.commit()
            print("已清空现有分类")
        
        # 读取分类配置
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'data', 'knowledge_categories_seed.json'
        )
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        categories = config.get('categories', [])
        
        # 创建分类
        total_created = 0
        for parent_cat in categories:
            # 创建父分类
            parent = KnowledgeCategory(
                name=parent_cat['name'],
                description=parent_cat.get('description', ''),
                icon=parent_cat.get('icon', 'bi bi-folder'),
                sort_order=parent_cat.get('sort_order', 0),
                parent_id=None,
                is_active=True
            )
            db.add(parent)
            db.flush()  # 获取父分类ID
            
            print(f"✓ 创建主分类: {parent.name}")
            total_created += 1
            
            # 创建子分类
            children = parent_cat.get('children', [])
            for child_cat in children:
                child = KnowledgeCategory(
                    name=child_cat['name'],
                    description=child_cat.get('description', ''),
                    icon=child_cat.get('icon', 'bi bi-file-text'),
                    sort_order=child_cat.get('sort_order', 0),
                    parent_id=parent.id,
                    is_active=True
                )
                db.add(child)
                total_created += 1
                print(f"  └─ 创建子分类: {child.name}")
        
        db.commit()
        print(f"\n✅ 成功创建 {total_created} 个分类")
        
        # 显示分类统计
        main_cats = db.query(KnowledgeCategory).filter(KnowledgeCategory.parent_id.is_(None)).count()
        sub_cats = db.query(KnowledgeCategory).filter(KnowledgeCategory.parent_id.isnot(None)).count()
        print(f"\n统计:")
        print(f"  - 主分类: {main_cats} 个")
        print(f"  - 子分类: {sub_cats} 个")
        print(f"  - 总计: {main_cats + sub_cats} 个")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 初始化失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("知识库目录分类初始化工具")
    print("=" * 60)
    print()
    
    init_categories()
    
    print()
    print("=" * 60)
    print("初始化完成!")
    print("=" * 60)
