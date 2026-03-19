"""
系统全面检查脚本 - 数维数据管家系统
"""
import os
import sys
import json
from pathlib import Path

# 添加项目根目录到路径
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

print("=" * 80)
print("数维数据管家系统 - 全面检查报告".center(80))
print("=" * 80)

# 1. 项目结构检查
print("\n[1] 项目结构检查")
print("-" * 80)
required_dirs = ['api', 'models', 'services', 'schemas', 'config', 'frontend', 'scripts', 'tests']
required_files = ['main.py', 'requirements.txt']

all_dirs_exist = True
all_files_exist = True

for dir_name in required_dirs:
    dir_path = root_dir / dir_name
    exists = dir_path.exists() and dir_path.is_dir()
    status = "[OK]" if exists else "[MISSING]"
    print(f"  {status} 目录: {dir_name}")
    if not exists:
        all_dirs_exist = False

for file_name in required_files:
    file_path = root_dir / file_name
    exists = file_path.exists() and file_path.is_file()
    status = "[OK]" if exists else "[MISSING]"
    print(f"  {status} 文件: {file_name}")
    if not exists:
        all_files_exist = False

print(f"\n结构检查: {'全部通过' if all_dirs_exist and all_files_exist else '存在问题'}")

# 2. 代码导入检查
print("\n[2] 代码模块导入检查")
print("-" * 80)

import_results = {}

# 检查API模块
api_modules = ['auth', 'rules', 'evaluation', 'knowledge', 'reports', 'users', 'channel', 'config', 'customers', 'ai_config', 'ai_rules']
for module in api_modules:
    try:
        exec(f"from api.{module} import router")
        import_results[f'api.{module}'] = "OK"
        print(f"  [OK] api.{module}")
    except Exception as e:
        import_results[f'api.{module}'] = f"ERROR: {str(e)[:50]}"
        print(f"  [FAIL] api.{module} - {str(e)[:50]}")

# 检查模型模块
model_modules = ['user', 'rule_config', 'evaluation_result', 'knowledge_doc', 'channel', 'ai_config', 'knowledge_category', 'system_config']
for module in model_modules:
    try:
        exec(f"from models.{module} import *")
        import_results[f'models.{module}'] = "OK"
        print(f"  [OK] models.{module}")
    except Exception as e:
        import_results[f'models.{module}'] = f"ERROR: {str(e)[:50]}"
        print(f"  [FAIL] models.{module} - {str(e)[:50]}")

# 检查服务模块
service_modules = ['evaluation', 'rule_calculator', 'report_generator', 'policy_retriever', 'vip_service']
for module in service_modules:
    try:
        exec(f"from services.{module} import *")
        import_results[f'services.{module}'] = "OK"
        print(f"  [OK] services.{module}")
    except Exception as e:
        import_results[f'services.{module}'] = f"ERROR: {str(e)[:50]}"
        print(f"  [FAIL] services.{module} - {str(e)[:50]}")

# 检查Schema
try:
    from schemas import *
    import_results['schemas'] = "OK"
    print(f"  [OK] schemas")
except Exception as e:
    import_results['schemas'] = f"ERROR: {str(e)[:50]}"
    print(f"  [FAIL] schemas - {str(e)[:50]}")

# 3. 检查API路由
print("\n[3] API路由注册检查")
print("-" * 80)
try:
    from main import app
    routes = []
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            for method in route.methods:
                if method != 'HEAD':
                    routes.append(f"{method} {route.path}")
    
    print(f"  发现 {len(routes)} 个API端点")
    
    # 分类统计
    api_categories = {}
    for route in routes:
        if '/api/v1/' in route:
            parts = route.split('/')
            if len(parts) > 3:
                category = parts[3]
                api_categories[category] = api_categories.get(category, 0) + 1
    
    print("\n  API分类统计:")
    for category, count in sorted(api_categories.items()):
        print(f"    /{category}: {count} 个端点")
    
    print(f"\n  路由注册: [OK] 共 {len(routes)} 个端点")
    
except Exception as e:
    print(f"  [FAIL] 路由检查失败 - {str(e)}")

# 4. 检查模型定义
print("\n[4] 数据模型检查")
print("-" * 80)
try:
    from models.rule_config import RuleConfig, DIMENSIONS
    print(f"  [OK] RuleConfig 模型")
    print(f"  [OK] 定义了 {len(DIMENSIONS)} 个维度")
    for code, info in DIMENSIONS.items():
        print(f"    - {code}: {info['name']} (权重: {info['weight']}%)")
    
    from models.evaluation_result import EvaluationResult
    print(f"  [OK] EvaluationResult 模型")
    
    from models.knowledge_doc import KnowledgeDoc
    print(f"  [OK] KnowledgeDoc 模型")
    
    from models.user import User
    print(f"  [OK] User 模型")
    
    print(f"\n  数据模型: [OK]")
    
except Exception as e:
    print(f"  [FAIL] 数据模型检查失败 - {str(e)}")

# 5. 前端文件检查
print("\n[5] 前端文件检查")
print("-" * 80)
frontend_files = [
    'index.html', 'report.html', 'login.html', 'register.html', 'home.html',
    'history.html', 'admin.html', 'rules.html', 'knowledge.html',
    'users.html', 'config.html', 'customers.html', 'reports.html', 'ai_config.html'
]

for file in frontend_files:
    file_path = root_dir / 'frontend' / file
    exists = file_path.exists() and file_path.is_file()
    status = "[OK]" if exists else "[MISSING]"
    print(f"  {status} frontend/{file}")

# 6. 数据文件检查
print("\n[6] 数据文件检查")
print("-" * 80)
data_dir = root_dir / 'data'
if data_dir.exists():
    json_files = list(data_dir.glob('*.json'))
    print(f"  发现 {len(json_files)} 个JSON数据文件:")
    for file in json_files:
        print(f"    - data/{file.name}")
        
        # 尝试解析JSON
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"      [OK] JSON格式正确")
                if 'rules' in data:
                    print(f"      包含 {len(data['rules'])} 条规则")
        except Exception as e:
            print(f"      [ERROR] JSON解析失败: {str(e)[:50]}")
else:
    print(f"  [WARN] data/ 目录不存在")

# 7. 配置文件检查
print("\n[7] 配置文件检查")
print("-" * 80)

# 数据库配置
try:
    from config.database import DATABASE_URL, get_db
    print(f"  [OK] 数据库配置")
    print(f"    Database URL: {DATABASE_URL[:50]}...")
    
    # 检查是否能创建会话
    # try:
    #     db = next(get_db())
    #     db.close()
    #     print(f"    数据库连接: [OK]")
    # except Exception as e:
    #     print(f"    数据库连接: [WARN] {str(e)[:50]}")
except Exception as e:
    print(f"  [FAIL] 数据库配置失败 - {str(e)[:50]}")

# 8. 服务功能检查
print("\n[8] 服务功能检查")
print("-" * 80)

try:
    from services.rule_calculator import RuleCalculator
    calculator = RuleCalculator()
    
    # 测试简单计算
    test_expr = "1 == 1"
    result = calculator.calculate_single_rule(test_expr, {})
    print(f"  [OK] RuleCalculator 基本功能")
    print(f"    测试表达式 '{test_expr}' 结果: {result}")
    
except Exception as e:
    print(f"  [FAIL] RuleCalculator 检查失败 - {str(e)[:50]}")

try:
    from services.policy_retriever import PolicyRetriever
    retriever = PolicyRetriever()
    print(f"  [OK] PolicyRetriever 模块")
    
    # 检查建议库
    result = retriever.retrieve("D1_COMPLIANCE")
    suggestions = result.get('suggestions', {})
    total_suggestions = sum(len(v) for v in suggestions.values())
    print(f"    策略建议库包含 {total_suggestions} 条建议")
    
except Exception as e:
    print(f"  [FAIL] PolicyRetriever 检查失败 - {str(e)[:50]}")

try:
    from services.report_generator import ReportGenerator
    generator = ReportGenerator()
    print(f"  [OK] ReportGenerator 模块")
    
except Exception as e:
    print(f"  [FAIL] ReportGenerator 检查失败 - {str(e)[:50]}")

# 9. 依赖包检查
print("\n[9] 依赖包检查")
print("-" * 80)
requirements = [
    'fastapi', 'uvicorn', 'sqlalchemy', 'pymysql', 'pydantic',
    'simpleeval', 'passlib', 'jwt'
]

for pkg in requirements:
    try:
        __import__(pkg)
        print(f"  [OK] {pkg}")
    except ImportError:
        print(f"  [MISSING] {pkg}")

# 10. 问题汇总
print("\n" + "=" * 80)
print("检查结果汇总".center(80))
print("=" * 80)

failures = [k for k, v in import_results.items() if v != "OK"]
if failures:
    print(f"\n[WARNING] 发现 {len(failures)} 个导入问题:")
    for fail in failures:
        print(f"  - {fail}: {import_results[fail]}")
else:
    print("\n[SUCCESS] 所有模块导入成功!")

print(f"\n建议:")
print(f"  1. 确保数据库MySQL服务运行正常")
print(f"  2. 运行 python scripts/init_db.py 初始化数据库")
print(f"  3. 运行 python main.py 启动服务")
print(f"  4. 访问 http://localhost:8000/api-docs-cn 查看API文档")

print("\n" + "=" * 80)
print("检查完成!".center(80))
print("=" * 80)
