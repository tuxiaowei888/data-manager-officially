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
        evaluation_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        生成完整报告
        
        Args:
            evaluation_result: 评价结果字典
            
        Returns:
            完整报告字典
        """
        # 提取基本信息
        report_data = {
            'report_id': f"RPT{evaluation_result['id']}",
            'user_id': evaluation_result['user_id'],
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'engine_version': evaluation_result.get('engine_version', 'v1_static'),
            
            # 总体评价
            'summary': {
                'total_score': evaluation_result['total_score'],
                'risk_level': evaluation_result['risk_level'],
                'risk_level_text': self._get_risk_level_text(evaluation_result['risk_level'])
            },
            
            # 维度分析
            'dimension_analysis': [],
            
            # 改进建议
            'suggestions': [],
            
            # 风险详情
            'risk_details': []
        }
        
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
                    'risk_level': '高风险' if dim_data.get('score', 0) < 60 else '中风险'
                })
        
        # 生成总体改进建议
        report_data['suggestions'] = self._generate_overall_suggestions(
            evaluation_result['risk_level'],
            evaluation_result['total_score']
        )
        
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
