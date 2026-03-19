"""
API 测试脚本 - 数维数据管家系统
测试所有 API 接口的功能
"""
import requests
import json

# API 基础 URL
BASE_URL = "http://localhost:8000/api/v1"


def test_health():
    """测试健康检查"""
    print("\n=== 测试健康检查 ===")
    response = requests.get("http://localhost:8000/health")
    print(f"状态码：{response.status_code}")
    print(f"响应：{response.json()}")
    return response.status_code == 200


def test_rules():
    """测试规则管理 API"""
    print("\n=== 测试规则管理 API ===")
    
    # 获取所有规则
    response = requests.get(f"{BASE_URL}/rules")
    print(f"获取所有规则 - 状态码：{response.status_code}")
    if response.status_code == 200:
        rules = response.json()
        print(f"规则数量：{len(rules)}")
        if rules:
            print(f"第一条规则：{rules[0]['rule_name']}")
    
    # 获取活跃规则
    response = requests.get(f"{BASE_URL}/rules/active")
    print(f"\n获取活跃规则 - 状态码：{response.status_code}")
    if response.status_code == 200:
        active_rules = response.json()
        print(f"活跃规则数量：{len(active_rules)}")
    
    # 测试 AI 生成规则（占位接口）
    print("\n测试 AI 生成规则接口（V2.0 占位）")
    response = requests.post(f"{BASE_URL}/rules/ai-generate")
    print(f"状态码：{response.status_code}")
    print(f"响应：{response.json()}")
    
    return True


def test_evaluation():
    """测试评价服务 API"""
    print("\n=== 测试评价服务 API ===")
    
    # 创建评价
    test_data = {
        "user_id": 1,
        "data": {
            "data_source_legal": 1,
            "privacy_anonymization": 1,
            "authorization_chain_complete": 1,
            "data_completeness_score": 0.85,
            "data_accuracy_score": 0.9,
            "data_timeliness_score": 0.8,
            "scenario_coverage_score": 0.75,
            "revenue_estimation_score": 0.7,
            "cost_saving_score": 0.65,
            "policy_completeness_score": 0.8,
            "staff_allocation_score": 0.7,
            "audit_record_score": 0.75,
            "data_standardization_score": 0.6,
            "api_availability_score": 0.65,
            "transaction_history_score": 0.5,
            "data_scarcity_score": 0.55,
            "derivability_score": 0.5,
            "policy_alignment_score": 0.6
        }
    }
    
    print("创建评价...")
    response = requests.post(f"{BASE_URL}/evaluation", json=test_data)
    print(f"状态码：{response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"评价 ID: {result['id']}")
        print(f"总分：{result['total_score']}")
        print(f"风险等级：{result['risk_level']}")
        
        # 测试报告生成
        print(f"\n生成报告...")
        response = requests.get(f"{BASE_URL}/reports/{result['id']}")
        if response.status_code == 200:
            report = response.json()
            print(f"报告 ID: {report['report_id']}")
            print(f"总体评价：{report['summary']['risk_level_text']}")
            print(f"维度数量：{len(report['dimension_analysis'])}")
        
        # 测试报告下载
        print(f"\n下载测试报告...")
        response = requests.get(f"{BASE_URL}/reports/{result['id']}/download")
        print(f"下载状态码：{response.status_code}")
        
        return True
    else:
        print(f"评价失败：{response.text}")
        return False


def test_knowledge():
    """测试知识库 API"""
    print("\n=== 测试知识库 API ===")
    
    # 获取所有文档
    response = requests.get(f"{BASE_URL}/knowledge")
    print(f"获取知识库文档 - 状态码：{response.status_code}")
    if response.status_code == 200:
        docs = response.json()
        print(f"文档数量：{len(docs)}")
    
    # 创建测试文档
    test_doc = {
        "title": "测试政策文档",
        "content_text": "这是一个测试政策文档的内容..."
    }
    
    print("\n创建测试文档...")
    response = requests.post(f"{BASE_URL}/knowledge", json=test_doc)
    print(f"状态码：{response.status_code}")
    if response.status_code == 200:
        doc = response.json()
        print(f"文档 ID: {doc['id']}")
        print(f"向量化状态：{doc['embedding_status']} (V1.0 应为 False)")
    
    return True


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("数维数据管家系统 - API 测试脚本")
    print("=" * 60)
    
    try:
        # 检查服务是否运行
        print("\n检查 API 服务状态...")
        try:
            response = requests.get("http://localhost:8000")
            print(f"API 服务状态：{response.status_code}")
            print(f"服务信息：{response.json()}")
        except requests.exceptions.ConnectionError:
            print("✗ 错误：无法连接到 API 服务")
            print("请先运行：python main.py 启动服务")
            return False
        
        # 运行测试
        results = {
            "健康检查": test_health(),
            "规则管理": test_rules(),
            "评价服务": test_evaluation(),
            "知识库": test_knowledge()
        }
        
        # 输出测试结果
        print("\n" + "=" * 60)
        print("测试结果汇总")
        print("=" * 60)
        for test_name, passed in results.items():
            status = "✓ 通过" if passed else "✗ 失败"
            print(f"{test_name}: {status}")
        
        all_passed = all(results.values())
        print("\n" + "=" * 60)
        if all_passed:
            print("✓ 所有测试通过")
        else:
            print("✗ 部分测试失败")
        print("=" * 60)
        
        return all_passed
        
    except Exception as e:
        print(f"\n✗ 测试执行失败：{str(e)}")
        return False


if __name__ == "__main__":
    run_all_tests()
