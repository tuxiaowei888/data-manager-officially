"""
报告生成服务 - 数维数据管家系统
基于模板填充数据，生成标准化报告
"""
from typing import Dict, List, Any
from datetime import datetime

from services.policy_retriever import PolicyRetriever


class ReportGenerator:
    """
    报告生成器 - V1.0 实现
    
    功能：
    1. 基于固定模板填充评价结果
    2. 生成改进建议
    3. 支持 PDF 导出
    
    # TODO V2.0: Add AI-powered report interpretation
    """
    
    def __init__(self):
        """初始化报告生成器"""
        self.policy_retriever = PolicyRetriever()
    
    def generate_report(
        self,
        evaluation_result: Dict[str, Any],
        depth: str = 'full'
    ) -> Dict[str, Any]:
        """
        生成报告（支持深度控制）
        
        Args:
            evaluation_result: 评价结果字典
            depth: 报告深度 (summary/diagnosis/action_plan/full)
            
        Returns:
            报告字典，包含锁定部分提示
        """
        # 验证深度参数
        valid_depths = ['summary', 'diagnosis', 'action_plan', 'full']
        if depth not in valid_depths:
            depth = 'full'  # 默认使用完整报告
        
        # 提取基本信息
        report_data = {
            'report_id': f"RPT{evaluation_result['id']}",
            'user_id': evaluation_result['user_id'],
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'engine_version': evaluation_result.get('engine_version', 'v1_static'),
            'report_depth': depth,
            
            # 总体评价（所有深度都包含）
            'summary': {
                'total_score': evaluation_result['total_score'],
                'risk_level': evaluation_result['risk_level'],
                'risk_level_text': self._get_risk_level_text(evaluation_result['risk_level'])
            },
            
            # 维度分析（diagnosis及以上深度包含）
            'dimension_analysis': [],
            
            # 风险详情（diagnosis及以上深度包含）
            'risk_details': [],
            
            # 总体改进建议（diagnosis及以上深度包含）
            'suggestions': [],
            
            # 路径推荐（action_plan及以上深度包含）
            'path_recommendations': [],
            
            # 价值预测（action_plan及以上深度包含）
            'value_projection': {},
            
            # 实施路线图（action_plan及以上深度包含）
            'implementation_roadmap': [],
            
            # 多数据集概览（full深度包含）
            'multi_dataset_overview': {},
            
            # 品牌定制内容（full深度包含）
            'brand_customization': {},
            
            # 锁定部分提示
            'locked_sections': []
        }
        
        # 生成摘要部分（所有深度）
        report_data['summary'] = {
            'total_score': evaluation_result['total_score'],
            'risk_level': evaluation_result['risk_level'],
            'risk_level_text': self._get_risk_level_text(evaluation_result['risk_level']),
            'overall_assessment': self._generate_overall_assessment(evaluation_result)
        }
        
        # 如果深度为diagnosis/action_plan/full，生成维度分析和风险详情
        if depth in ['diagnosis', 'action_plan', 'full']:
            # 生成维度分析
            detail_json = evaluation_result.get('detail_json', {})
            dimension_scores = detail_json.get('dimension_scores', {})
            
            for dim_code, dim_data in dimension_scores.items():
                dim_analysis = {
                    'dimension_code': dim_code,
                    'dimension_name': self._get_dimension_name(dim_code),
                    'score': dim_data.get('score', 0),
                    'rules': dim_data.get('rules', []),
                    'suggestions': self.policy_retriever.get_suggestions_by_score(
                        dim_code,
                        dim_data.get('score', 0)
                    )
                }
                report_data['dimension_analysis'].append(dim_analysis)
                
                # 收集低分项的风险详情
                if dim_data.get('score', 0) < 70:
                    report_data['risk_details'].append({
                        'dimension_code': dim_code,
                        'dimension_name': dim_analysis['dimension_name'],
                        'score': dim_data.get('score', 0),
                        'risk_level': '高风险' if dim_data.get('score', 0) < 60 else '中风险',
                        'priority': '高' if dim_data.get('score', 0) < 60 else '中'
                    })
            
            # 生成总体改进建议
            report_data['suggestions'] = self._generate_overall_suggestions(
                evaluation_result['risk_level'],
                evaluation_result['total_score']
            )
        
        # 如果深度为action_plan/full，生成行动方案
        if depth in ['action_plan', 'full']:
            # 生成路径推荐
            report_data['path_recommendations'] = self._generate_path_recommendations(evaluation_result)
            
            # 生成价值预测
            report_data['value_projection'] = self._generate_value_projection(evaluation_result)
            
            # 生成实施路线图
            report_data['implementation_roadmap'] = self._generate_implementation_roadmap(evaluation_result)
        
        # 如果深度为full，生成企业版专属内容
        if depth == 'full':
            # 生成多数据集概览（如果有相关数据）
            if 'related_datasets' in evaluation_result:
                report_data['multi_dataset_overview'] = self._generate_multi_dataset_overview(evaluation_result)
            
            # 生成品牌定制内容
            report_data['brand_customization'] = self._generate_brand_customization(evaluation_result)
        
        # 生成锁定部分提示
        report_data['locked_sections'] = self._get_locked_sections(depth)
        
        return report_data
    
    def _get_risk_level_text(self, risk_level: str) -> str:
        """获取风险等级文本描述"""
        risk_map = {
            'P0': '高风险 - 需要立即采取改进措施',
            'P1': '中风险 - 建议制定改进计划',
            'P2': '低风险 - 保持现有管理水平'
        }
        return risk_map.get(risk_level, '未知风险等级')
    
    def _get_dimension_name(self, dimension_code: str) -> str:
        """获取维度名称"""
        dimension_map = {
            'D1_COMPLIANCE': '合规性',
            'D2_QUALITY': '质量',
            'D3_VALUE': '价值',
            'D4_MANAGEMENT': '管理',
            'D5_CIRCULATION': '流通',
            'D6_POTENTIAL': '潜力'
        }
        return dimension_map.get(dimension_code, dimension_code)
    
    def _generate_overall_suggestions(
        self,
        risk_level: str,
        total_score: float
    ) -> List[str]:
        """
        生成总体改进建议
        
        Args:
            risk_level: 风险等级
            total_score: 总分
            
        Returns:
            建议列表
        """
        suggestions = []
        
        # 根据风险等级生成建议
        if risk_level == 'P0':
            suggestions.extend([
                '【紧急】建议立即成立专项改进小组，制定详细的整改计划',
                '【紧急】优先解决高风险维度的问题，防止风险进一步扩大',
                '建议聘请第三方专业机构进行全面诊断和指导'
            ])
        elif risk_level == 'P1':
            suggestions.extend([
                '建议制定 3-6 个月的改进计划，明确责任人和时间节点',
                '重点关注得分较低的维度，优先投入资源改进',
                '建议建立定期评估机制，跟踪改进效果'
            ])
        else:
            suggestions.extend([
                '当前管理水平良好，建议持续保持',
                '可考虑申报相关行业认证，提升竞争力',
                '建议总结经验，形成最佳实践案例'
            ])
        
        # 添加通用建议
        suggestions.extend([
            '建议定期开展数据资产评估，持续跟踪改进效果',
            '可建立数据资产管理委员会，统筹推进各项工作'
        ])
        
        return suggestions
    
    def generate_pdf_content(self, report_data: Dict[str, Any]) -> str:
        """
        生成 PDF 内容（文本格式）
        
        Args:
            report_data: 报告数据
            
        Returns:
            格式化的文本内容
        """
        lines = []
        
        # 标题
        lines.append("=" * 80)
        lines.append("数维数据管家系统 - 数据资产评估报告")
        lines.append("=" * 80)
        lines.append("")
        
        # 基本信息
        lines.append(f"报告编号：{report_data['report_id']}")
        lines.append(f"生成时间：{report_data['generated_at']}")
        lines.append(f"计算引擎：{report_data['engine_version']}")
        lines.append("")
        
        # 总体评价
        lines.append("-" * 80)
        lines.append("【总体评价】")
        lines.append(f"总分：{report_data['summary']['total_score']}")
        lines.append(f"风险等级：{report_data['summary']['risk_level_text']}")
        lines.append("")
        
        # 维度分析
        lines.append("-" * 80)
        lines.append("【维度分析】")
        for dim in report_data['dimension_analysis']:
            lines.append(f"\n{dim['dimension_name']} ({dim['dimension_code']})")
            lines.append(f"  得分：{dim['score']}")
            lines.append(f"  改进建议:")
            for suggestion in dim['suggestions'][:2]:  # 每个维度最多显示 2 条
                lines.append(f"    - {suggestion}")
        lines.append("")
        
        # 风险详情
        if report_data['risk_details']:
            lines.append("-" * 80)
            lines.append("【风险详情】")
            for risk in report_data['risk_details']:
                lines.append(f"  {risk['dimension_name']}: {risk['risk_level']} (得分：{risk['score']})")
            lines.append("")
        
        # 总体改进建议
        lines.append("-" * 80)
        lines.append("【总体改进建议】")
        for i, suggestion in enumerate(report_data['suggestions'], 1):
            lines.append(f"{i}. {suggestion}")
        lines.append("")
        
        lines.append("=" * 80)
        lines.append("报告结束")
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def _generate_overall_assessment(self, evaluation_result: Dict[str, Any]) -> str:
        """
        生成总体评估文本
        
        Args:
            evaluation_result: 评价结果
            
        Returns:
            总体评估文本
        """
        total_score = evaluation_result['total_score']
        risk_level = evaluation_result['risk_level']
        
        if total_score >= 90:
            return f"您的数据管理水平非常优秀，总分{total_score}分，已达到行业领先水平。建议继续保持并总结经验，形成最佳实践案例。"
        elif total_score >= 80:
            return f"您的数据管理表现良好，总分{total_score}分，处于行业中等偏上水平。建议关注得分较低的维度，进一步提升综合能力。"
        elif total_score >= 70:
            return f"您的数据管理基础扎实，总分{total_score}分，具备良好改进潜力。建议制定系统性的改进计划，重点提升高风险维度。"
        elif total_score >= 60:
            return f"您的数据管理存在一定风险，总分{total_score}分，需要引起重视。建议立即制定整改计划，优先解决高风险问题。"
        else:
            return f"您的数据管理面临较高风险，总分{total_score}分，需要立即采取行动。建议成立专项改进小组，全面诊断并整改。"
    
    def _generate_path_recommendations(self, evaluation_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        生成路径推荐
        
        Args:
            evaluation_result: 评价结果
            
        Returns:
            路径推荐列表，每个推荐包含名称、描述、优先级
        """
        detail_json = evaluation_result.get('detail_json', {})
        dimension_scores = detail_json.get('dimension_scores', {})
        
        recommendations = []
        
        # 分析各维度得分，推荐改进路径
        for dim_code, dim_data in dimension_scores.items():
            score = dim_data.get('score', 0)
            dim_name = self._get_dimension_name(dim_code)
            
            if score < 60:
                recommendations.append({
                    'dimension_code': dim_code,
                    'dimension_name': dim_name,
                    'path_name': f'{dim_name}专项提升计划',
                    'description': f'该维度得分{score}分，属于高风险领域。建议投入专项资源进行系统改进，建立长效管理机制。',
                    'priority': '紧急',
                    'estimated_time': '3-6个月',
                    'key_actions': [
                        '组织专项培训，提升团队能力',
                        '制定详细的操作规程',
                        '建立定期检查和反馈机制'
                    ]
                })
            elif score < 70:
                recommendations.append({
                    'dimension_code': dim_code,
                    'dimension_name': dim_name,
                    'path_name': f'{dim_name}优化改进计划',
                    'description': f'该维度得分{score}分，存在改进空间。建议制定优化方案，逐步提升管理水平。',
                    'priority': '高',
                    'estimated_time': '2-3个月',
                    'key_actions': [
                        '分析现有不足，制定改进措施',
                        '引入行业最佳实践',
                        '建立持续改进机制'
                    ]
                })
        
        # 如果没有具体维度推荐，提供通用建议
        if not recommendations:
            recommendations.append({
                'dimension_code': 'GENERAL',
                'dimension_name': '综合提升',
                'path_name': '数据管理全面优化计划',
                'description': '当前各维度表现均衡，建议从整体视角进行持续优化，进一步提升数据管理水平。',
                'priority': '中',
                'estimated_time': '1-2个月',
                'key_actions': [
                    '定期开展自评，跟踪改进效果',
                    '建立数据管理指标体系',
                    '组织跨部门经验分享'
                ]
            })
        
        return recommendations
    
    def _generate_value_projection(self, evaluation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成价值预测
        
        Args:
            evaluation_result: 评价结果
            
        Returns:
            价值预测字典，包含改进后的潜在价值
        """
        total_score = evaluation_result['total_score']
        risk_level = evaluation_result['risk_level']
        
        # 基于当前得分估算改进潜力
        improvement_potential = 100 - total_score
        
        # 根据得分区间估算价值提升
        if total_score < 60:
            # 高风险，改进价值最大
            efficiency_gain = "30-50%"  # 效率提升
            risk_reduction = "50-70%"   # 风险降低
            roi_estimate = "3-5倍"      # 投资回报率
            time_to_value = "6-12个月"  # 价值实现时间
        elif total_score < 70:
            efficiency_gain = "20-40%"
            risk_reduction = "40-60%"
            roi_estimate = "2-4倍"
            time_to_value = "4-8个月"
        elif total_score < 80:
            efficiency_gain = "10-30%"
            risk_reduction = "30-50%"
            roi_estimate = "1.5-3倍"
            time_to_value = "3-6个月"
        else:
            efficiency_gain = "5-15%"
            risk_reduction = "20-40%"
            roi_estimate = "1-2倍"
            time_to_value = "2-4个月"
        
        return {
            'improvement_potential': f"{improvement_potential:.1f}分",
            'efficiency_gain': efficiency_gain,
            'risk_reduction': risk_reduction,
            'roi_estimate': roi_estimate,
            'time_to_value': time_to_value,
            'key_benefits': [
                '提升数据质量，减少错误和返工',
                '降低合规风险，避免潜在罚款',
                '提高数据价值，支持业务决策',
                '优化资源配置，提升运营效率'
            ]
        }
    
    def _generate_implementation_roadmap(self, evaluation_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        生成实施路线图
        
        Args:
            evaluation_result: 评价结果
            
        Returns:
            路线图阶段列表
        """
        total_score = evaluation_result['total_score']
        
        # 根据得分确定实施阶段
        if total_score < 60:
            # 高风险，需要紧急整改
            phases = [
                {
                    'phase': '第一阶段：紧急整改 (1-2个月)',
                    'focus': '解决高风险问题',
                    'key_activities': [
                        '成立专项改进小组',
                        '制定紧急整改方案',
                        '实施高风险问题修复'
                    ],
                    'deliverables': ['高风险问题清单', '整改方案', '初步改进报告']
                },
                {
                    'phase': '第二阶段：系统改进 (3-6个月)',
                    'focus': '建立系统化管理体系',
                    'key_activities': [
                        '制定数据管理政策',
                        '建立标准化流程',
                        '开展全员培训'
                    ],
                    'deliverables': ['数据管理手册', '标准化流程文档', '培训材料']
                },
                {
                    'phase': '第三阶段：持续优化 (6-12个月)',
                    'focus': '持续改进和优化',
                    'key_activities': [
                        '建立持续改进机制',
                        '引入先进工具和方法',
                        '申报行业认证'
                    ],
                    'deliverables': ['持续改进计划', '认证证书', '最佳实践案例']
                }
            ]
        elif total_score < 70:
            phases = [
                {
                    'phase': '第一阶段：重点改进 (2-3个月)',
                    'focus': '提升关键维度能力',
                    'key_activities': [
                        '分析关键短板',
                        '制定改进计划',
                        '实施重点改进措施'
                    ],
                    'deliverables': ['改进计划', '关键指标跟踪表', '改进进展报告']
                },
                {
                    'phase': '第二阶段：全面优化 (4-6个月)',
                    'focus': '全面提升数据管理水平',
                    'key_activities': [
                        '优化现有流程',
                        '引入最佳实践',
                        '建立指标体系'
                    ],
                    'deliverables': ['优化方案', '指标体系', '阶段性评估报告']
                },
                {
                    'phase': '第三阶段：卓越运营 (6-9个月)',
                    'focus': '实现数据管理卓越运营',
                    'key_activities': [
                        '建立持续改进文化',
                        '实施数字化工具',
                        '分享成功经验'
                    ],
                    'deliverables': ['卓越运营框架', '数字化工具平台', '案例分享材料']
                }
            ]
        else:
            phases = [
                {
                    'phase': '第一阶段：优化提升 (1-2个月)',
                    'focus': '持续优化和改进',
                    'key_activities': [
                        '识别优化机会',
                        '制定优化方案',
                        '实施优化措施'
                    ],
                    'deliverables': ['优化机会清单', '优化方案', '优化效果报告']
                },
                {
                    'phase': '第二阶段：创新突破 (3-4个月)',
                    'focus': '引入创新方法和工具',
                    'key_activities': [
                        '研究行业趋势',
                        '引入创新工具',
                        '试点新技术应用'
                    ],
                    'deliverables': ['创新研究报告', '试点方案', '试点评估报告']
                },
                {
                    'phase': '第三阶段：行业引领 (5-6个月)',
                    'focus': '建立行业领先地位',
                    'key_activities': [
                        '总结最佳实践',
                        '参与标准制定',
                        '分享行业经验'
                    ],
                    'deliverables': ['最佳实践手册', '行业标准贡献', '分享会材料']
                }
            ]
        
        return phases
    
    def _generate_multi_dataset_overview(self, evaluation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成多数据集概览
        
        Args:
            evaluation_result: 评价结果
            
        Returns:
            多数据集概览信息
        """
        # 如果评价结果中包含相关数据集信息，则生成概览
        related_datasets = evaluation_result.get('related_datasets', [])
        
        if not related_datasets:
            # 如果没有相关数据集信息，返回基础结构
            return {
                'has_multi_dataset': False,
                'message': '当前为单数据集评估模式。升级到企业版可支持多数据集对比分析和趋势跟踪。'
            }
        
        # 这里可以扩展真实的多数据集分析逻辑
        return {
            'has_multi_dataset': True,
            'dataset_count': len(related_datasets),
            'avg_score': sum(d.get('score', 0) for d in related_datasets) / len(related_datasets) if related_datasets else 0,
            'score_range': {
                'min': min(d.get('score', 0) for d in related_datasets) if related_datasets else 0,
                'max': max(d.get('score', 0) for d in related_datasets) if related_datasets else 0
            },
            'recommendations': [
                '建议统一各数据集的管理标准',
                '建立跨数据集的治理机制',
                '定期进行多数据集对比分析'
            ]
        }
    
    def _generate_brand_customization(self, evaluation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成品牌定制内容
        
        Args:
            evaluation_result: 评价结果
            
        Returns:
            品牌定制内容
        """
        org_name = evaluation_result.get('org_name', '贵机构')
        
        return {
            'brand_name': org_name,
            'customized_greeting': f'尊敬的{org_name}数据管理团队：',
            'customized_conclusion': f'希望本报告能为{org_name}的数据管理工作提供有价值的参考。',
            'contact_info': {
                'support_email': 'support@shuweidata.com',
                'consultation_phone': '400-xxx-xxxx',
                'website': 'https://shuweidata.com'
            },
            'next_steps': [
                f'欢迎{org_name}团队随时联系我们，获取个性化咨询服务',
                '我们将根据您的具体需求，提供定制化的解决方案',
                '期待与您共同推进数据管理能力的提升'
            ]
        }
    
    def _get_locked_sections(self, depth: str) -> List[Dict[str, Any]]:
        """
        获取锁定部分提示
        
        Args:
            depth: 当前报告深度
            
        Returns:
            锁定部分提示列表
        """
        locked_sections = []
        
        if depth == 'summary':
            locked_sections.extend([
                {
                    'section_name': '维度详细分析',
                    'description': '包含各维度的详细得分分析、问题诊断和改进建议',
                    'upgrade_tier': 'basic',
                    'benefit': '了解各维度的具体表现，识别改进重点'
                },
                {
                    'section_name': '行动方案推荐',
                    'description': '包含具体的改进路径、实施路线图和价值预测',
                    'upgrade_tier': 'pro',
                    'benefit': '获得系统性的改进方案，明确实施步骤和预期价值'
                },
                {
                    'section_name': '多数据集分析',
                    'description': '支持多数据集对比分析、趋势跟踪和品牌定制内容',
                    'upgrade_tier': 'enterprise',
                    'benefit': '实现跨数据集的统一管理，获得个性化品牌展示'
                }
            ])
        elif depth == 'diagnosis':
            locked_sections.extend([
                {
                    'section_name': '行动方案推荐',
                    'description': '包含具体的改进路径、实施路线图和价值预测',
                    'upgrade_tier': 'pro',
                    'benefit': '获得系统性的改进方案，明确实施步骤和预期价值'
                },
                {
                    'section_name': '多数据集分析',
                    'description': '支持多数据集对比分析、趋势跟踪和品牌定制内容',
                    'upgrade_tier': 'enterprise',
                    'benefit': '实现跨数据集的统一管理，获得个性化品牌展示'
                }
            ])
        elif depth == 'action_plan':
            locked_sections.extend([
                {
                    'section_name': '多数据集分析',
                    'description': '支持多数据集对比分析、趋势跟踪和品牌定制内容',
                    'upgrade_tier': 'enterprise',
                    'benefit': '实现跨数据集的统一管理，获得个性化品牌展示'
                }
            ])
        # full深度没有锁定部分
        
        return locked_sections
