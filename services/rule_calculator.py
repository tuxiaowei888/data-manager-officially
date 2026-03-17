"""
规则计算器模块 - 数维数据管家系统
使用 simpleeval 安全执行规则表达式
"""
from simpleeval import simple_eval, EvalWithCompoundTypes
from typing import Dict, List, Any


class RuleCalculator:
    """规则计算器 - 安全执行规则表达式"""
    
    RISK_LEVELS = {
        'P0': '高风险',
        'P1': '中风险',
        'P2': '低风险'
    }
    
    def __init__(self):
        self.functions = {
            'min': min,
            'max': max,
            'sum': sum,
            'abs': abs,
            'round': round,
            'len': len,
            'str': str,
            'int': int,
            'float': float,
            'any': any,
            'all': all,
        }
        
        self.names = {
            'True': True,
            'False': False,
            'None': None,
        }
    
    def calculate_single_rule(self, expression: str, data: Dict[str, Any]) -> float:
        """
        计算单个规则的得分
        
        Args:
            expression: 规则表达式（Python 表达式字符串）
            data: 用户填报的数据
            
        Returns:
            计算结果（0-1 之间的浮点数）
        """
        try:
            names = {**self.names, **data}
            
            result = simple_eval(
                expression,
                functions=self.functions,
                names=names
            )
            
            if isinstance(result, (int, float)):
                normalized = result / 100.0 if result > 1 else result
                return max(0.0, min(1.0, float(normalized)))
            elif isinstance(result, bool):
                return 1.0 if result else 0.0
            else:
                return 0.0
                
        except Exception as e:
            print(f"规则计算失败：{expression}, 错误：{str(e)}")
            try:
                evaluator = EvalWithCompoundTypes(functions=self.functions, names=names)
                result = evaluator.eval(expression)
                if isinstance(result, (int, float)):
                    normalized = result / 100.0 if result > 1 else result
                    return max(0.0, min(1.0, float(normalized)))
            except Exception as e2:
                print(f"二次尝试失败：{str(e2)}")
            return 0.0
    
    def calculate_total_score(self, rule_results: List[Dict[str, float]]) -> float:
        """计算加权总分"""
        if not rule_results:
            return 0.0
        
        total_weight = sum(item['weight'] for item in rule_results)
        
        if total_weight == 0:
            return 0.0
        
        weighted_sum = sum(item['score'] * item['weight'] for item in rule_results)
        total_score = (weighted_sum / total_weight) * 100
        
        return round(total_score, 2)
    
    def determine_risk_level(self, total_score: float, rules: List[Dict]) -> str:
        """判定风险等级"""
        if not rules:
            return 'P2'
        
        score_normalized = total_score / 100.0
        
        min_threshold = min(rule.get('risk_threshold', 0.6) for rule in rules)
        avg_threshold = sum(rule.get('risk_threshold', 0.6) for rule in rules) / len(rules)
        
        if score_normalized < min_threshold * 0.6:
            return 'P0'
        elif score_normalized < avg_threshold:
            return 'P1'
        else:
            return 'P2'
    
    def calculate(self, data: Dict[str, Any], rules: List[Any]) -> Dict[str, Any]:
        """完整计算流程"""
        rule_results = []
        dimension_scores = {}
        
        for rule in rules:
            if not rule.is_active:
                continue
            
            score = self.calculate_single_rule(rule.logic_expression, data)
            
            rule_results.append({
                'rule_id': rule.id,
                'dimension_code': rule.dimension_code,
                'rule_name': rule.rule_name,
                'score': score,
                'weight': rule.weight,
                'risk_threshold': rule.risk_threshold
            })
            
            dim = rule.dimension_code
            if dim not in dimension_scores:
                dimension_scores[dim] = {
                    'rules': [],
                    'total_score': 0,
                    'total_weight': 0
                }
            dimension_scores[dim]['rules'].append({
                'rule_name': rule.rule_name,
                'score': score,
                'weight': rule.weight
            })
            dimension_scores[dim]['total_score'] += score * rule.weight
            dimension_scores[dim]['total_weight'] += rule.weight
        
        for dim in dimension_scores:
            if dimension_scores[dim]['total_weight'] > 0:
                dimension_scores[dim]['score'] = round(
                    (dimension_scores[dim]['total_score'] / dimension_scores[dim]['total_weight']) * 100,
                    2
                )
            else:
                dimension_scores[dim]['score'] = 0.0
        
        total_score = self.calculate_total_score(rule_results)
        risk_level = self.determine_risk_level(total_score, rule_results)
        
        return {
            'total_score': total_score,
            'risk_level': risk_level,
            'rule_results': rule_results,
            'dimension_scores': dimension_scores
        }
