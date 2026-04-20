"""
评价服务模块 - 数维数据管家系统
核心流程：规则库评分 → 知识库碰撞 → AI整体出报告
"""
from typing import Dict, List, Any, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from models.rule_config import RuleConfig, DIMENSIONS
from models.evaluation_result import EvaluationResult
from services.rule_calculator import RuleCalculator
from services.report_generator import ReportGenerator
from services.knowledge_base_engine import KnowledgeBaseEngine


class EvaluationService:
    """
    评价服务 - 核心评估引擎

    核心三段式流程：
    1. 规则库评分    → 31条规则计算，输出8维度得分
    2. 知识库碰撞    → 向量检索+静态库，输出政策建议
    3. AI整体出报告 → 三要素融合，输出7章诊断报告
    """

    def __init__(self, db: Session):
        self.db = db
        self.calculator = RuleCalculator()
        self.report_generator = ReportGenerator()
        self.knowledge_engine = KnowledgeBaseEngine()
    
    def evaluate(self, form_data: Dict[str, Any], user_id: int = None) -> Dict[str, Any]:
        """
        执行完整评估流程
        
        Args:
            form_data: 客户填写的表单数据
            user_id: 用户ID（可选）
            
        Returns:
            完整的评估报告
        """
        
        # Step 1: 准备评估数据
        eval_data = self._prepare_eval_data(form_data)
        
        # Step 2: 规则库计算
        rule_results = self._calculate_with_rules(eval_data)
        
        # Step 3: 知识库检索
        knowledge_results = self._retrieve_knowledge(rule_results, form_data)
        
        # Step 4: 调用AI API
        ai_analysis = self._call_ai_api(rule_results, knowledge_results, form_data)
        
        # Step 5: 输出报告
        report = self._generate_report(
            form_data=form_data,
            rule_results=rule_results,
            knowledge_results=knowledge_results,
            ai_analysis=ai_analysis,
            user_id=user_id
        )
        
        return report
    
    def _prepare_eval_data(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """Step 1: 准备评估数据，转换表单字段为规则可用的变量"""
        data = {}
        
        # 合规与安全相关
        data['user_auth'] = form_data.get('user_auth', '')
        data['sensitive_data'] = form_data.get('sensitive_data', '')
        data['data_encrypt'] = form_data.get('data_encrypt', '')
        data['data_policy'] = form_data.get('data_policy', '')
        data['compliance_history'] = form_data.get('compliance_history', '')
        
        security_cert = form_data.get('security_cert', [])
        data['security_cert'] = security_cert if isinstance(security_cert, list) else [security_cert]
        
        data_source = form_data.get('data_source', [])
        data['data_source'] = data_source if isinstance(data_source, list) else [data_source]
        
        # 数据质量相关
        data['update_frequency'] = form_data.get('update_frequency', '')
        try:
            data['completeness'] = float(form_data.get('completeness', 50))
        except (ValueError, TypeError):
            data['completeness'] = 50.0
        
        data_format = form_data.get('data_format', [])
        data['data_format'] = data_format if isinstance(data_format, list) else [data_format]
        
        data_type = form_data.get('data_type', [])
        data['data_type'] = data_type if isinstance(data_type, list) else [data_type]
        
        # 权属确认相关
        rights_cert = form_data.get('rights_cert', [])
        data['rights_cert'] = rights_cert if isinstance(rights_cert, list) else [rights_cert]
        data['originality'] = form_data.get('originality', '')
        
        # 价值评估相关
        scenarios = form_data.get('application_scenario', [])
        data['application_scenario'] = scenarios if isinstance(scenarios, list) else [scenarios]
        
        purposes = form_data.get('asset_purpose', [])
        data['asset_purpose'] = purposes if isinstance(purposes, list) else [purposes]
        
        data_product = form_data.get('data_product', [])
        data['data_product'] = data_product if isinstance(data_product, list) else [data_product]
        
        data['data_volume_records'] = form_data.get('data_volume_records', '')
        data['commercial_plan'] = form_data.get('commercial_plan', '')
        
        # 成本计量相关
        data['cost_accounting'] = form_data.get('cost_accounting', '')
        try:
            data['cost_input'] = float(form_data.get('cost_input', 0))
        except (ValueError, TypeError):
            data['cost_input'] = 0.0
        
        # 管理体系相关
        data['has_data_dept'] = form_data.get('has_data_dept', '')
        
        # 发展潜力相关
        try:
            data['ip_patent'] = int(form_data.get('ip_patent', 0))
        except (ValueError, TypeError):
            data['ip_patent'] = 0
        try:
            data['ip_copyright'] = int(form_data.get('ip_copyright', 0))
        except (ValueError, TypeError):
            data['ip_copyright'] = 0
        
        return data
    
    def _calculate_with_rules(self, eval_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 2: 规则库计算
        从数据库读取规则，计算各维度得分
        """
        rules = self._get_active_rules()
        
        if not rules:
            return {
                'dimensions': [],
                'rule_details': [],
                'total_score': 0,
                'risk_level': 'P2'
            }
        
        rule_details = []
        dimension_data = {}
        
        for rule in rules:
            score = self.calculator.calculate_single_rule(rule.logic_expression, eval_data)
            score_100 = score * 100
            
            rule_details.append({
                'rule_id': rule.id,
                'rule_name': rule.rule_name,
                'dimension_code': rule.dimension_code,
                'score': round(score_100, 1),
                'weight': rule.weight,
                'risk_threshold': rule.risk_threshold
            })
            
            dim_code = rule.dimension_code
            if dim_code not in dimension_data:
                dimension_data[dim_code] = {'scores': [], 'weights': []}
            dimension_data[dim_code]['scores'].append(score_100)
            dimension_data[dim_code]['weights'].append(rule.weight)
        
        dimensions = []
        for dim_code, data in dimension_data.items():
            if data['weights']:
                weighted_sum = sum(s * w for s, w in zip(data['scores'], data['weights']))
                total_weight = sum(data['weights'])
                dim_score = weighted_sum / total_weight if total_weight > 0 else 0
            else:
                dim_score = 0
            
            dim_info = DIMENSIONS.get(dim_code, {'name': dim_code, 'weight': 20})
            dimensions.append({
                'code': dim_code,
                'name': dim_info['name'],
                'score': round(dim_score, 1),
                'weight': dim_info['weight'],
                'level': self._get_level_text(dim_score)
            })
        
        total_weight = sum(d['weight'] for d in dimensions)
        if total_weight > 0:
            total_score = sum(d['score'] * d['weight'] / total_weight for d in dimensions)
        else:
            total_score = sum(d['score'] for d in dimensions) / len(dimensions) if dimensions else 0
        total_score = round(total_score, 1)
        
        risk_level = self._determine_risk_level(total_score, rule_details)
        
        return {
            'dimensions': dimensions,
            'rule_details': rule_details,
            'total_score': total_score,
            'risk_level': risk_level
        }
    
    def _retrieve_knowledge(self, rule_results: Dict[str, Any], form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 3: 知识库碰撞（使用知识库碰撞引擎）

        根据评估结果和表单数据，与知识库进行碰撞，
        产出政策依据和改进建议。

        V2.0: 使用统一的 KnowledgeBaseEngine
        - 第一层：ChromaDB 向量语义检索
        - 第二层：PolicyRetriever 静态文案库
        """
        dimension_scores = {
            dim['code']: dim['score']
            for dim in rule_results.get('dimensions', [])
        }

        collision_result = self.knowledge_engine.collide(dimension_scores)

        knowledge_results = {
            'suggestions': collision_result.get('suggestions', {}),
            'policies': [],
            'best_practices': [],
            'collision_mode': collision_result.get('collision_mode'),
            'metadata': collision_result.get('metadata', {})
        }

        for policy in collision_result.get('policies', []):
            content = policy.get('content', '')
            if content:
                knowledge_results['policies'].append(content)

        return knowledge_results
    
    def _call_ai_api(self, rule_results: Dict[str, Any], knowledge_results: Dict[str, Any], 
                     form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Step 4: 调用AI API
        基于规则计算结果和知识库内容，调用AI生成分析报告
        """
        from services.ai_service import AIService
        
        ai_analysis = {
            'enabled': False,
            'model': None,
            'provider': None,
            'analysis': None,
            'recommendations': None,
            'full_report': None
        }
        
        # 生成问题列表
        ai_analysis['p0_issues'] = self._generate_p0_issues(form_data)
        ai_analysis['p1_issues'] = self._generate_p1_issues(form_data)
        ai_analysis['p2_issues'] = self._generate_p2_issues(form_data)
        
        # 调用AI服务生成报告（融合三要素：用户数据 + 规则评分 + 知识库政策）
        try:
            ai_service = AIService(self.db)
            
            # 准备AI输入数据
            eval_data = {
                'org_name': form_data.get('org_name', '待填写企业'),
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'total_score': rule_results.get('total_score', 0),
                'maturity_level': self._get_maturity_level(rule_results.get('total_score', 0)),
                'risk_level': rule_results.get('risk_level', 'P2'),
                'dimensions': rule_results.get('dimensions', []),
                'p0_issues': ai_analysis['p0_issues'],
                'p1_issues': ai_analysis['p1_issues'],
                'p2_issues': ai_analysis['p2_issues']
            }
            
            # 调用AI服务，传入知识库检索结果
            ai_result = ai_service.generate_report(eval_data, knowledge_results)
            
            if ai_result.get('success'):
                ai_analysis['enabled'] = True
                ai_analysis['model'] = ai_result.get('model')
                ai_analysis['provider'] = ai_result.get('provider')
                ai_analysis['full_report'] = ai_result.get('content')
            else:
                ai_analysis['error'] = ai_result.get('error')
                
        except Exception as e:
            ai_analysis['error'] = str(e)
        
        return ai_analysis
    
    def _generate_report(self, form_data: Dict[str, Any], rule_results: Dict[str, Any],
                         knowledge_results: Dict[str, Any], ai_analysis: Dict[str, Any],
                         user_id: int = None) -> Dict[str, Any]:
        """
        Step 5: 输出报告
        整合所有数据，生成完整评估报告
        """
        report_id = f"DA-AI-{datetime.now().strftime('%Y%m%d')}-EVAL-{str(hash(str(form_data)) % 1000).zfill(3)}"
        
        dimensions = []
        for dim in rule_results.get('dimensions', []):
            dim_code = dim['code']
            dim_info = {
                **dim,
                'logic': self._get_dimension_logic(dim['name'], dim['score']),
                'suggestions': knowledge_results.get('suggestions', {}).get(dim_code, [])
            }
            dimensions.append(dim_info)
        
        report = {
            'report_id': report_id,
            'org_name': form_data.get('org_name', '待填写企业'),
            'total_score': rule_results.get('total_score', 0),
            'maturity_level': self._get_maturity_level(rule_results.get('total_score', 0)),
            'risk_level': rule_results.get('risk_level', 'P2'),
            'dimensions': dimensions,
            'rule_results': rule_results.get('rule_details', []),
            'p0_issues': ai_analysis.get('p0_issues', []),
            'p1_issues': ai_analysis.get('p1_issues', []),
            'p2_issues': ai_analysis.get('p2_issues', []),
            'ai_analysis': ai_analysis,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'form_data': form_data
        }
        
        # 如果AI生成了完整报告，使用AI报告
        if ai_analysis.get('enabled') and ai_analysis.get('full_report'):
            report['ai_report'] = ai_analysis['full_report']
            report['ai_model'] = ai_analysis.get('model')
            report['ai_provider'] = ai_analysis.get('provider')
        
        # 使用 ReportGenerator 生成格式化报告内容（作为备用）
        report['pdf_content'] = self.report_generator.generate_pdf_content({
            'report_id': report['report_id'],
            'generated_at': report['generated_at'],
            'engine_version': 'v1_ai_enhanced' if ai_analysis.get('enabled') else 'v1_rule_based',
            'summary': {
                'total_score': report['total_score'],
                'risk_level': report['risk_level'],
                'risk_level_text': self._get_risk_level_text(report['risk_level'])
            },
            'dimension_analysis': [
                {
                    'dimension_code': d['code'],
                    'dimension_name': d['name'],
                    'score': d['score'],
                    'suggestions': d.get('suggestions', [])
                }
                for d in dimensions
            ],
            'risk_details': [
                {
                    'dimension_name': d['name'],
                    'score': d['score'],
                    'risk_level': '高风险' if d['score'] < 60 else '中风险'
                }
                for d in dimensions if d['score'] < 70
            ],
            'suggestions': self._generate_overall_suggestions(report['risk_level'], report['total_score'])
        })
        
        if user_id:
            db_id = self._save_result(user_id, report)
            report['id'] = db_id
            report['report_id'] = f"DA-{db_id}"
        
        return report
    
    def _get_risk_level_text(self, risk_level: str) -> str:
        """获取风险等级文本描述"""
        risk_map = {
            'P0': '高风险 - 需要立即采取改进措施',
            'P1': '中风险 - 建议制定改进计划',
            'P2': '低风险 - 保持现有管理水平'
        }
        return risk_map.get(risk_level, '未知风险等级')
    
    def _generate_overall_suggestions(self, risk_level: str, total_score: float) -> List[str]:
        """生成总体改进建议"""
        suggestions = []
        
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
        
        suggestions.extend([
            '建议定期开展数据资产评估，持续跟踪改进效果',
            '可建立数据资产管理委员会，统筹推进各项工作'
        ])
        
        return suggestions
    
    def _get_active_rules(self) -> List[RuleConfig]:
        """获取所有活跃的规则"""
        return self.db.query(RuleConfig).filter(
            RuleConfig.is_active == True,
            RuleConfig.is_deleted == False
        ).order_by(RuleConfig.dimension_code, RuleConfig.id).all()
    
    def _determine_risk_level(self, total_score: float, rule_results: List[Dict]) -> str:
        """判定风险等级"""
        if total_score < 60:
            return 'P0'
        elif total_score < 75:
            return 'P1'
        else:
            return 'P2'
    
    def _get_maturity_level(self, score: float) -> str:
        """获取成熟度等级"""
        if score >= 90:
            return 'A级 (卓越)'
        elif score >= 75:
            return 'B级 (良好)'
        elif score >= 60:
            return 'C级 (合格)'
        else:
            return 'D级 (原始态)'
    
    def _get_level_text(self, score: float) -> str:
        """获取等级文本"""
        if score < 60:
            return '高风险'
        elif score < 75:
            return '待提升'
        else:
            return '良好'
    
    def _get_dimension_logic(self, name: str, score: float) -> str:
        """获取维度逻辑描述"""
        logics = {
            '合规与安全': {
                'high': '底线稳固：已通过安全认证；敏感数据已完成脱敏；拥有完整的用户隐私协议。',
                'medium': '存在合规短板：部分安全措施不到位，建议加强数据加密和授权管理。',
                'low': '触发一票否决预警：检测到敏感数据明文存储；授权链条不完整。'
            },
            '数据质量': {
                'high': '质量系数高：数据完整性高，实时性强，一致性校验通过。',
                'medium': '质量系数中等：存在部分数据质量问题，建议完善数据治理流程。',
                'low': '质量系数低：完整性缺失率较高；一致性校验存在问题。'
            },
            '权属确认': {
                'high': '双证齐全：已获得数据资产登记证书和数据知识产权登记证书。',
                'medium': '有授权无凭证：虽持有授权文件，但缺失法定登记证书。',
                'low': '双轨未启动：无《数据资产登记证书》；无《数据知识产权登记证书》。'
            },
            '价值评估': {
                'high': '场景爆发力强：命中多个高价值应用场景，变现路径清晰。',
                'medium': '场景匹配度中等：存在一定应用价值，建议拓展更多场景。',
                'low': '场景匹配度低：应用场景有限，建议挖掘数据潜在价值。'
            },
            '成本计量': {
                'high': '成本核算清晰：有独立项目核算，成本分摊逻辑明确。',
                'medium': '成本归集一般：有部分分摊，建议完善成本核算体系。',
                'low': '成本归集难：缺乏独立的项目核算代码；成本分摊逻辑不清。'
            }
        }
        
        if score >= 75:
            return logics.get(name, {}).get('high', '表现良好')
        elif score >= 60:
            return logics.get(name, {}).get('medium', '有待提升')
        else:
            return logics.get(name, {}).get('low', '需要改进')
    
    def _generate_p0_issues(self, form_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成P0级问题（阻断性问题）"""
        issues = []
        
        if form_data.get('sensitive_data') == '明文存储':
            issues.append({
                'title': '合规红线触发',
                'problem': '检测到敏感个人信息明文存储',
                'basis': '违反《个人信息保护法》第28条',
                'consequence': '禁止交易、禁止入表、面临行政处罚风险'
            })
        
        if form_data.get('user_auth') == '无明确协议':
            issues.append({
                'title': '用户授权缺失',
                'problem': '用户授权协议缺失或不明确',
                'basis': '违反《个人信息保护法》第13条',
                'consequence': '数据处理缺乏合法依据，面临法律风险'
            })
        
        rights_cert = form_data.get('rights_cert', [])
        if isinstance(rights_cert, str):
            rights_cert = [rights_cert]
        if not rights_cert or '无' in rights_cert:
            issues.append({
                'title': '权属凭证真空',
                'problem': '无任何官方登记证书',
                'basis': '不满足财政部《暂行规定》',
                'consequence': '审计师无法确认资产归属，银行拒绝质押'
            })
        
        return issues
    
    def _generate_p1_issues(self, form_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成P1级问题（减值性问题）"""
        issues = []
        
        try:
            completeness = int(form_data.get('completeness', 50))
        except (ValueError, TypeError):
            completeness = 50
        
        if completeness < 70:
            issues.append({
                'title': '数据质量缺陷',
                'problem': f'关键字段缺失率{100-completeness}%，导致数据可用性降低',
                'basis': '质量系数将从1.0降至0.6',
                'consequence': '直接导致最终估值打折（预计折价30%-40%）'
            })
        
        cost_accounting = form_data.get('cost_accounting', '')
        if cost_accounting in ['完全混合', '有部分分摊']:
            issues.append({
                'title': '成本归集缺失',
                'problem': '未建立数据资源专项成本核算科目',
                'basis': '违反成本可计量性要求',
                'consequence': '入表时难以准确计量初始成本，增加审计难度'
            })
        
        return issues
    
    def _generate_p2_issues(self, form_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成P2级问题（优化性问题）"""
        issues = []
        
        data_product = form_data.get('data_product', [])
        if isinstance(data_product, str):
            data_product = [data_product]
        if len(data_product) <= 1:
            issues.append({
                'title': '产品形态单一',
                'problem': '目前仅为原始数据集，未封装为API或模型服务',
                'suggestion': '建议开发数据产品，提升溢价能力'
            })
        
        return issues
    
    def _save_result(self, user_id: int, report_data: Dict[str, Any]) -> int:
        """保存评估结果到数据库"""
        evaluation_result = EvaluationResult(
            user_id=user_id,
            org_name=report_data.get('org_name', '未命名企业'),
            total_score=report_data['total_score'],
            risk_level=report_data['risk_level'],
            detail_json={
                'dimensions': report_data['dimensions'],
                'rule_results': report_data.get('rule_results', []),
                'p0_issues': report_data['p0_issues'],
                'p1_issues': report_data['p1_issues'],
                'p2_issues': report_data['p2_issues'],
                'form_data': report_data.get('form_data', {})
            },
            engine_version='v1_rule_based',
            ai_analysis_log=report_data.get('ai_analysis')
        )
        
        self.db.add(evaluation_result)
        self.db.commit()
        self.db.refresh(evaluation_result)
        
        return evaluation_result.id
    
    def get_result(self, result_id: int) -> Dict[str, Any]:
        """获取评价结果"""
        result = self.db.query(EvaluationResult).filter(
            EvaluationResult.id == result_id
        ).first()
        
        if not result:
            raise ValueError(f"评价结果不存在：{result_id}")
        
        return {
            'id': result.id,
            'user_id': result.user_id,
            'org_name': result.org_name,
            'total_score': result.total_score,
            'risk_level': result.risk_level,
            'detail_json': result.detail_json,
            'engine_version': result.engine_version,
            'ai_analysis_log': result.ai_analysis_log,
            'created_at': result.created_at.strftime('%Y-%m-%d %H:%M') if result.created_at else '-'
        }
    
    def get_user_results(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """获取用户的评价历史"""
        results = self.db.query(EvaluationResult).filter(
            EvaluationResult.user_id == user_id
        ).order_by(
            EvaluationResult.created_at.desc()
        ).limit(limit).all()
        
        return [
            {
                'id': r.id,
                'user_id': r.user_id,
                'org_name': r.org_name or r.detail_json.get('form_data', {}).get('org_name', '未命名企业'),
                'total_score': r.total_score,
                'risk_level': r.risk_level,
                'engine_version': r.engine_version,
                'created_at': r.created_at.strftime('%Y-%m-%d %H:%M') if r.created_at else '-'
            }
            for r in results
        ]

    def get_all_results(self, limit: int = 100) -> List[Dict[str, Any]]:
        """获取所有评价历史（管理端用）"""
        results = self.db.query(EvaluationResult).order_by(
            EvaluationResult.created_at.desc()
        ).limit(limit).all()

        return [
            {
                'id': r.id,
                'user_id': r.user_id,
                'org_name': r.org_name or r.detail_json.get('form_data', {}).get('org_name', '未命名企业'),
                'total_score': r.total_score,
                'risk_level': r.risk_level,
                'engine_version': r.engine_version,
                'status': 'completed' if r.total_score else 'failed',
                'created_at': r.created_at.strftime('%Y-%m-%d %H:%M') if r.created_at else '-'
            }
            for r in results
        ]

    def delete_result(self, result_id: int) -> bool:
        """删除评价结果"""
        result = self.db.query(EvaluationResult).filter(
            EvaluationResult.id == result_id
        ).first()
        
        if not result:
            raise ValueError(f"评价结果不存在：{result_id}")
        
        self.db.delete(result)
        self.db.commit()
        
        return True
