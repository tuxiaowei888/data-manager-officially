"""
AI服务模块 - 数维数据管家系统
负责调用AI API生成报告内容
核心：融合用户数据 + 规则评分 + 知识库政策
"""
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
import httpx
import json

from models.ai_config import AIConfig, AI_PROVIDERS, DEFAULT_REPORT_PROMPT, DEFAULT_SYSTEM_PROMPT
from services.policy_retriever import PolicyRetriever


class AIService:
    """AI服务 - 调用大模型API生成报告"""
    
    def __init__(self, db: Session):
        self.db = db
        self.policy_retriever = PolicyRetriever()
    
    def get_active_config(self) -> Optional[AIConfig]:
        """获取当前启用的AI配置"""
        return self.db.query(AIConfig).filter(
            AIConfig.is_active == True,
            AIConfig.is_default == True
        ).first()
    
    def generate_report(self, eval_data: Dict[str, Any], knowledge_results: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        使用AI生成评估报告
        
        Args:
            eval_data: 评估数据，包含分数、维度、问题等
            knowledge_results: 知识库检索结果
            
        Returns:
            AI生成的报告内容
        """
        config = self.get_active_config()
        
        if not config:
            return {
                'success': False,
                'error': '未配置AI服务，请在AI配置管理中添加并启用配置',
                'content': None
            }
        
        # 构建提示词（融合三要素）
        prompt = self._build_prompt(config, eval_data, knowledge_results)
        
        # 调用AI API
        try:
            result = self._call_api(config, prompt)
            return {
                'success': True,
                'error': None,
                'content': result,
                'model': config.model_name,
                'provider': config.provider
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'content': None
            }
    
    def _build_prompt(self, config: AIConfig, eval_data: Dict[str, Any], knowledge_results: Dict[str, Any] = None) -> str:
        """
        构建发送给AI的提示词
        融合三要素：用户数据 + 规则评分 + 知识库政策
        """
        template = config.report_prompt_template or DEFAULT_REPORT_PROMPT
        
        # 第一要素：企业基础画像
        org_name = eval_data.get('org_name', '待填写企业')
        generated_at = eval_data.get('generated_at', '')
        
        # 第二要素：规则库量化评分
        total_score = eval_data.get('total_score', 0)
        maturity_level = eval_data.get('maturity_level', '未评级')
        
        if total_score < 60:
            risk_level = "高风险（P0级）"
        elif total_score < 75:
            risk_level = "中风险（P1级）"
        else:
            risk_level = "低风险（P2级）"
        
        # 格式化维度得分
        dimension_scores = ""
        for d in eval_data.get('dimensions', []):
            score = d.get('score', 0)
            status = "🔴" if score < 60 else "🟡" if score < 75 else "🟢"
            dimension_scores += f"- {status} **{d.get('name', '')}**：{score}分\n"
            if d.get('suggestions'):
                for s in d['suggestions'][:2]:
                    dimension_scores += f"  - {s}\n"
        
        # 格式化问题
        p0_issues = self._format_issues(eval_data.get('p0_issues', []))
        p1_issues = self._format_issues(eval_data.get('p1_issues', []))
        p2_issues = self._format_issues(eval_data.get('p2_issues', []))
        
        # 第三要素：知识库政策依据
        knowledge_policies = self._build_knowledge_section(knowledge_results, eval_data)
        
        # 填充模板
        prompt = template.format(
            org_name=org_name,
            generated_at=generated_at,
            total_score=total_score,
            maturity_level=maturity_level,
            risk_level=risk_level,
            dimension_scores=dimension_scores,
            p0_issues=p0_issues,
            p1_issues=p1_issues,
            p2_issues=p2_issues,
            knowledge_policies=knowledge_policies
        )
        
        return prompt
    
    def _format_issues(self, issues: list) -> str:
        """格式化问题列表"""
        if not issues:
            return "无"
        
        result = ""
        for i, issue in enumerate(issues, 1):
            title = issue.get('title', '')
            problem = issue.get('problem', '')
            basis = issue.get('basis', '')
            consequence = issue.get('consequence', '')
            
            result += f"\n{i}. **{title}**\n"
            if problem:
                result += f"   - 问题：{problem}\n"
            if basis:
                result += f"   - 依据：{basis}\n"
            if consequence:
                result += f"   - 后果：{consequence}\n"
        
        return result
    
    def _build_knowledge_section(self, knowledge_results: Dict[str, Any], eval_data: Dict[str, Any]) -> str:
        """
        构建知识库政策依据部分
        优先使用向量检索结果，降级到静态政策库
        """
        knowledge_text = "### 相关政策法规依据\n\n"
        
        vector_policies = knowledge_results.get('vector_results', [])
        if vector_policies:
            knowledge_text += "**管理员上传的政策文档（语义检索结果）：**\n"
            for i, r in enumerate(vector_policies, 1):
                content = r.get('content', '')
                if content:
                    relevance = r.get('relevance', 0)
                    knowledge_text += f"{i}. (相关性: {relevance:.2f})\n{content[:500]}\n\n"
        
        if knowledge_results and knowledge_results.get('suggestions'):
            knowledge_text += "\n**维度改进建议：**\n"
            for dim_code, suggestions in knowledge_results['suggestions'].items():
                if suggestions:
                    knowledge_text += f"\n{dim_code}维度：\n"
                    for s in suggestions[:3]:
                        knowledge_text += f"- {s}\n"
        
        if not vector_policies and not knowledge_results.get('suggestions'):
            knowledge_text += self._get_static_policies(eval_data)
        
        return knowledge_text
    
    def _get_static_policies(self, eval_data: Dict[str, Any]) -> str:
        """获取静态政策依据（基于评估数据匹配）"""
        policies = []
        
        # 根据问题匹配政策
        for issue in eval_data.get('p0_issues', []):
            title = issue.get('title', '')
            if '敏感' in title or '隐私' in title:
                policies.append("- 《个人信息保护法》第28条：敏感个人信息应当采取严格的保护措施")
            if '授权' in title or '协议' in title:
                policies.append("- 《个人信息保护法》第13条：处理个人信息应当取得个人同意")
            if '权属' in title or '凭证' in title:
                policies.append("- 《企业数据资源相关会计处理暂行规定》：数据资产入表需确认权属")
        
        # 根据维度匹配政策
        for dim in eval_data.get('dimensions', []):
            dim_name = dim.get('name', '')
            score = dim.get('score', 0)
            
            if '合规' in dim_name and score < 70:
                policies.append("- 《数据安全法》第二十七条：开展数据处理活动应当依法建立数据安全管理制度")
            if '质量' in dim_name and score < 70:
                policies.append("- 《数据管理能力成熟度评估模型》(GB/T 36073-2018)：数据质量管理要求")
            if '价值' in dim_name:
                policies.append("- 《企业数据资源相关会计处理暂行规定》：数据资产价值评估指引")
        
        if not policies:
            policies.append("- 《中共中央 国务院关于构建数据基础制度更好发挥数据要素作用的意见》（数据二十条）")
            policies.append("- 《企业数据资源相关会计处理暂行规定》")
        
        # 去重
        policies = list(dict.fromkeys(policies))
        
        return "\n".join(policies[:5]) + "\n"
    
    def _call_api(self, config: AIConfig, prompt: str) -> str:
        """调用AI API"""
        provider = config.provider
        base_url = config.api_base_url or AI_PROVIDERS.get(provider, {}).get('default_url', '')
        
        api_key = (config.api_key or "").strip()
        if not api_key:
            raise ValueError("API Key 未配置或为空，请先在AI设置中配置有效的API Key")
        
        headers = {
            "Content-Type": "application/json"
        }
        
        system_prompt = config.system_prompt or DEFAULT_SYSTEM_PROMPT
        
        if provider == "openai" or provider == "deepseek":
            headers["Authorization"] = f"Bearer {api_key}"
            url = f"{base_url}/chat/completions"
            payload = {
                "model": config.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": float(config.temperature or 0.7),
                "max_tokens": config.max_tokens
            }
        elif provider == "anthropic":
            headers["x-api-key"] = api_key
            headers["anthropic-version"] = "2023-06-01"
            url = f"{base_url}/messages"
            payload = {
                "model": config.model_name,
                "max_tokens": config.max_tokens,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "system": system_prompt
            }
        elif provider == "zhipu":
            headers["Authorization"] = f"Bearer {api_key}"
            url = f"{base_url}/chat/completions"
            payload = {
                "model": config.model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": float(config.temperature or 0.7),
                "max_tokens": config.max_tokens
            }
        elif provider == "qwen":
            headers["Authorization"] = f"Bearer {api_key}"
            url = f"{base_url}/services/aigc/text-generation/generation"
            payload = {
                "model": config.model_name,
                "input": {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ]
                },
                "parameters": {
                    "temperature": float(config.temperature or 0.7),
                    "max_tokens": config.max_tokens
                }
            }
        else:
            raise ValueError(f"不支持的AI提供商: {provider}")
        
        # 发送请求
        with httpx.Client(timeout=120.0) as client:
            response = client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
        
        # 解析响应
        if provider in ["openai", "deepseek", "zhipu"]:
            return result["choices"][0]["message"]["content"]
        elif provider == "anthropic":
            return result["content"][0]["text"]
        elif provider == "qwen":
            return result["output"]["text"]
        else:
            return str(result)
    
    def test_connection(self, config_id: int) -> Dict[str, Any]:
        """测试AI配置连接"""
        config = self.db.query(AIConfig).filter(AIConfig.id == config_id).first()
        
        if not config:
            return {
                'success': False,
                'error': '配置不存在'
            }
        
        api_key = (config.api_key or "").strip()
        if not api_key:
            return {
                'success': False,
                'error': 'API Key 未配置或为空，请先在AI设置中配置有效的API Key'
            }
        
        try:
            result = self._call_api(config, "你好，请用一句话介绍你自己，并说明你能为企业数据资产评估提供什么帮助。")
            return {
                'success': True,
                'response': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
