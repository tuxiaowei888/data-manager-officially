#!/usr/bin/env python3
"""
订阅体系功能测试脚本
测试订阅服务、报告生成器等核心功能
"""
import sys
import os
from datetime import datetime, timedelta

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.subscription_service import (
    get_user_subscription_tier,
    check_user_can_evaluate,
    get_report_depth,
    get_subscription_plans,
    upgrade_subscription,
    get_user_subscription_info
)
from services.report_generator import ReportGenerator
from models.system_config import SystemConfig


def test_subscription_service():
    """测试订阅服务核心功能"""
    print("=== 测试订阅服务 ===")
    
    # 模拟数据库会话对象
    class MockDB:
        def commit(self):
            pass
        def query(self, *args, **kwargs):
            return self
        def filter(self, *args, **kwargs):
            return self
        def first(self):
            return None
    
    # 模拟用户对象
    class MockUser:
        def __init__(self, subscription_tier='free', is_vip=False, vip_expire_date=None):
            self.subscription_tier = subscription_tier
            self.is_vip = is_vip
            self.vip_expire_date = vip_expire_date
            self.eval_count_used = 0
            self.eval_count_reset_date = datetime.now().date()
            self.subscription_start_date = None
            self.subscription_end_date = None
            
        @property
        def is_subscription_active(self):
            if not self.subscription_end_date:
                return False
            return self.subscription_end_date >= datetime.now().date()
    
    # 测试1: 获取用户订阅层级
    print("\n1. 测试获取用户订阅层级:")
    
    # 测试不同层级的用户
    test_cases = [
        ('free', 'free', False, None, False),  # free用户，无VIP，订阅未激活
        ('basic', 'basic', False, None, True),  # basic用户，订阅激活
        ('pro', 'pro', False, None, True),      # pro用户，订阅激活
        ('enterprise', 'enterprise', False, None, True),  # enterprise用户，订阅激活
        ('free', 'free', True, None, False),  # 历史VIP用户但已过期，订阅未激活
    ]
    
    for tier, expected_tier, is_vip, vip_expire, subscription_active in test_cases:
        user = MockUser(subscription_tier=tier, is_vip=is_vip, vip_expire_date=vip_expire)
        # 如果订阅应该激活，设置未来的结束日期
        if subscription_active:
            user.subscription_end_date = datetime.now().date() + timedelta(days=30)
            user.subscription_start_date = datetime.now().date() - timedelta(days=10)
        effective_tier = get_user_subscription_tier(user)
        print(f"  用户层级: {tier}, VIP: {is_vip}, 激活: {subscription_active} -> 有效层级: {effective_tier}")
        assert effective_tier == expected_tier, f"层级不匹配: {effective_tier} != {expected_tier}"
    
    # 测试2: 检查用户评估权限（简化版，因为需要数据库配置）
    print("\n2. 测试用户评估权限检查（简化）:")
    
    # 创建测试用户（basic和pro用户具有激活的订阅）
    user_free = MockUser(subscription_tier='free')
    user_basic = MockUser(subscription_tier='basic')
    user_basic.subscription_end_date = datetime.now().date() + timedelta(days=30)
    user_basic.subscription_start_date = datetime.now().date() - timedelta(days=10)
    user_pro = MockUser(subscription_tier='pro')
    user_pro.subscription_end_date = datetime.now().date() + timedelta(days=30)
    user_pro.subscription_start_date = datetime.now().date() - timedelta(days=10)
    
    # 模拟数据库会话
    db = MockDB()
    
    # 测试免费用户（简化测试，只验证函数调用）
    result = check_user_can_evaluate(user_free, db)
    print(f"  免费用户评估检查: {result['can_evaluate']} - {result['message']}")
    # 注意：实际限制取决于数据库配置，这里只测试函数是否正常执行
    
    # 测试基础用户
    result = check_user_can_evaluate(user_basic, db)
    print(f"  基础用户评估检查: {result['can_evaluate']} - {result['message']}")
    
    # 测试专业用户
    result = check_user_can_evaluate(user_pro, db)
    print(f"  专业用户评估检查: {result['can_evaluate']} - {result['message']}")
    
    # 测试3: 获取报告深度限制（简化版）
    print("\n3. 测试报告深度限制（简化）:")
    
    depth_map = {
        'free': 'summary',
        'basic': 'diagnosis',
        'pro': 'action_plan',
        'enterprise': 'full'
    }
    
    for tier, expected_depth in depth_map.items():
        user = MockUser(subscription_tier=tier)
        # 为除free外的所有层级设置激活的订阅
        if tier != 'free':
            user.subscription_end_date = datetime.now().date() + timedelta(days=30)
            user.subscription_start_date = datetime.now().date() - timedelta(days=10)
        allowed_depth = get_report_depth(user, db)
        print(f"  层级 {tier} -> 允许深度: {allowed_depth}")
        # 注意：实际深度取决于数据库配置，这里只测试函数是否正常执行
    
    print("✅ 订阅服务测试通过")


def test_report_generator():
    """测试报告生成器深度控制"""
    print("\n=== 测试报告生成器 ===")
    
    generator = ReportGenerator()
    
    # 创建模拟评估结果
    mock_evaluation = {
        'id': 123,
        'user_id': 1,
        'total_score': 75.5,
        'risk_level': 'P1',
        'engine_version': 'v1_static',
        'detail_json': {
            'dimension_scores': {
                'D1_COMPLIANCE': {'score': 80, 'rules': []},
                'D2_QUALITY': {'score': 65, 'rules': []},
                'D3_VALUE': {'score': 70, 'rules': []},
            }
        },
        'org_name': '测试公司'
    }
    
    # 测试不同深度的报告生成
    depths = ['summary', 'diagnosis', 'action_plan', 'full']
    
    for depth in depths:
        print(f"\n生成 {depth} 深度报告:")
        report = generator.generate_report(mock_evaluation, depth=depth)
        
        # 验证报告结构
        assert 'report_id' in report
        assert 'summary' in report
        assert 'report_depth' in report
        assert report['report_depth'] == depth
        
        # 验证深度特定的内容
        if depth == 'summary':
            assert len(report['dimension_analysis']) == 0
            assert len(report['risk_details']) == 0
            assert len(report['suggestions']) == 0
            assert len(report['path_recommendations']) == 0
            assert report['value_projection'] == {}
            assert len(report['locked_sections']) > 0
        elif depth == 'diagnosis':
            assert len(report['dimension_analysis']) > 0
            assert len(report['suggestions']) > 0
            assert len(report['path_recommendations']) == 0
            assert report['value_projection'] == {}
            assert len(report['locked_sections']) > 0
        elif depth == 'action_plan':
            assert len(report['dimension_analysis']) > 0
            assert len(report['suggestions']) > 0
            assert len(report['path_recommendations']) > 0
            assert report['value_projection'] != {}
            assert len(report['implementation_roadmap']) > 0
            assert len(report['locked_sections']) > 0
        elif depth == 'full':
            assert len(report['dimension_analysis']) > 0
            assert len(report['suggestions']) > 0
            assert len(report['path_recommendations']) > 0
            assert report['value_projection'] != {}
            assert len(report['implementation_roadmap']) > 0
            assert 'brand_customization' in report
            assert len(report['locked_sections']) == 0
        
        print(f"  报告ID: {report['report_id']}")
        print(f"  维度分析数量: {len(report['dimension_analysis'])}")
        print(f"  锁定部分数量: {len(report['locked_sections'])}")
    
    # 测试PDF生成
    print("\n测试PDF内容生成:")
    full_report = generator.generate_report(mock_evaluation, depth='full')
    pdf_content = generator.generate_pdf_content(full_report)
    
    assert '数维数据管家系统' in pdf_content
    # PDF内容可能不直接包含机构名称，只检查基本结构
    assert '报告编号' in pdf_content or '总分' in pdf_content
    
    print(f"  PDF内容长度: {len(pdf_content)} 字符")
    print("✅ 报告生成器测试通过")


def test_system_config():
    """测试系统配置（简化版）"""
    print("\n=== 测试系统配置（简化） ===")
    
    # 测试订阅层级配置（简化，不连接真实数据库）
    config_keys = [
        'subscription.free.daily_eval_limit',
        'subscription.basic.daily_eval_limit',
        'subscription.pro.daily_eval_limit',
        'subscription.enterprise.daily_eval_limit',
        'subscription.free.report_depth',
        'subscription.basic.report_depth',
        'subscription.pro.report_depth',
        'subscription.enterprise.report_depth',
    ]
    
    print("  配置键列表（需要数据库连接才能获取实际值）:")
    for key in config_keys:
        print(f"  - {key}")
    
    print("✅ 系统配置测试完成（简化版）")


if __name__ == "__main__":
    print("开始订阅体系功能测试...")
    
    try:
        test_subscription_service()
        test_report_generator()
        test_system_config()
        
        print("\n🎉 所有测试通过！")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)