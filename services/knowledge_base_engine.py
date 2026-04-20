"""
知识库碰撞引擎 - 数维数据管家系统
核心设计：规则库评分 → 知识库碰撞 → AI整体出报告

这个模块是知识库系统的统一入口，将两层检索架构（向量库+静态库）
封装为一个完整的"碰撞引擎"，供评估服务调用。
"""
from typing import Dict, List, Any, Optional
from config.logging_config import get_logger

logger = get_logger(__name__)


class KnowledgeBaseEngine:
    """
    知识库碰撞引擎

    核心设计理念：规则库评分 → 知识库碰撞 → AI整体出报告

    知识库碰撞 = 两层检索架构
    ├── 第一层：ChromaDB 向量语义检索  ← 管理员上传的政策文档
    └── 第二层：PolicyRetriever 静态库 ← 内置18组改进建议

    碰撞输入：8维度得分
    碰撞输出：{维度: [政策依据, 改进建议]}
    """

    def __init__(self):
        """初始化知识库碰撞引擎"""
        self._vector_store = None
        self._policy_retriever = None
        self._init_components()

    def _init_components(self):
        """初始化组件（延迟加载）"""
        from services.vector_store import VectorStore
        from services.policy_retriever import PolicyRetriever

        self._vector_store = VectorStore()
        self._policy_retriever = PolicyRetriever()
        logger.info("[知识库引擎] 初始化完成")

    @property
    def vector_store(self):
        """向量存储组件（ChromaDB）"""
        return self._vector_store

    @property
    def policy_retriever(self):
        """静态策略库组件"""
        return self._policy_retriever

    def is_vector_available(self) -> bool:
        """检查向量检索是否可用"""
        return self._vector_store.is_available()

    def collide(self, dimension_scores: Dict[str, float]) -> Dict[str, Any]:
        """
        知识库碰撞 - 核心方法

        将规则评分结果与知识库进行碰撞，产出政策依据和改进建议。

        Args:
            dimension_scores: 维度得分字典，格式 {维度代码: 得分}
                例如: {'C': 75.5, 'Q': 82.0, 'O': 60.0, ...}

        Returns:
            碰撞结果字典，包含:
            - policies: 检索到的政策文档列表
            - suggestions: {维度代码: [建议列表]}
            - collision_mode: 碰撞模式 ('vector' / 'static' / 'hybrid')
            - metadata: 碰撞元数据（检索时间、命中数等）
        """
        collision_results = {
            'policies': [],
            'suggestions': {},
            'collision_mode': None,
            'metadata': {
                'total_dimensions': len(dimension_scores),
                'vector_retrieval_used': False,
                'static_library_used': False,
                'total_policies_found': 0
            }
        }

        for dim_code, score in dimension_scores.items():
            query = self._build_query(dim_code, score)

            # 第一层：向量语义检索
            if self._vector_store.is_available():
                try:
                    vector_results = self._vector_store.search(query, top_k=3)
                    if vector_results:
                        collision_results['policies'].extend(vector_results)
                        collision_results['metadata']['vector_retrieval_used'] = True
                        logger.debug(f"[知识库引擎] 维度 {dim_code} 向量检索命中 {len(vector_results)} 条")
                except Exception as e:
                    logger.warning(f"[知识库引擎] 向量检索失败: {e}")

            # 第二层：静态库补充（总是执行，确保有建议返回）
            try:
                suggestions = self._policy_retriever.get_suggestions_by_score(dim_code, score)
                collision_results['suggestions'][dim_code] = suggestions
                collision_results['metadata']['static_library_used'] = True
            except Exception as e:
                logger.warning(f"[知识库引擎] 静态库检索失败: {e}")
                collision_results['suggestions'][dim_code] = []

        # 确定碰撞模式
        if collision_results['metadata']['vector_retrieval_used']:
            collision_results['collision_mode'] = 'hybrid' if collision_results['metadata']['static_library_used'] else 'vector'
        else:
            collision_results['collision_mode'] = 'static'

        collision_results['metadata']['total_policies_found'] = len(collision_results['policies'])

        logger.info(
            f"[知识库引擎] 碰撞完成，模式={collision_results['collision_mode']}，"
            f"政策文档={len(collision_results['policies'])}，维度建议={len(collision_results['suggestions'])}"
        )

        return collision_results

    def collide_for_report(
        self,
        dimension_scores: Dict[str, float],
        maturity_level: str,
        risk_level: str
    ) -> Dict[str, Any]:
        """
        为报告生成进行知识库碰撞

        这是 collide() 的报告专用版本，额外处理报告格式要求。

        Args:
            dimension_scores: 维度得分
            maturity_level: 成熟度等级
            risk_level: 风险等级

        Returns:
            报告专用的碰撞结果，包含:
            - dimension_advice: {维度: 改进建议列表}
            - risk_mitigation: 风险缓解建议
            - policy_references: 政策引用列表
            - knowledge_coverage: 知识库覆盖率
        """
        collision = self.collide(dimension_scores)

        report_result = {
            'dimension_advice': collision['suggestions'],
            'risk_mitigation': self._get_risk_mitigation_suggestions(risk_level),
            'policy_references': self._extract_policy_references(collision['policies']),
            'knowledge_coverage': {
                'dimensions_with_vectors': sum(1 for p in collision['policies']),
                'total_dimensions': len(dimension_scores),
                'coverage_rate': len(collision['policies']) / max(len(dimension_scores), 1)
            },
            'collision_mode': collision['collision_mode'],
            'raw_policies': collision['policies'][:10]
        }

        return report_result

    def search_policies(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        主动搜索政策文档

        供管理后台或知识库管理页面使用。

        Args:
            query: 搜索查询
            top_k: 返回结果数量

        Returns:
            匹配的政策文档列表
        """
        if self._vector_store.is_available():
            return self._vector_store.search(query, top_k=top_k)
        return []

    def add_policy_document(
        self,
        doc_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        添加政策文档到向量库

        Args:
            doc_id: 文档ID
            content: 文档内容
            metadata: 元数据

        Returns:
            是否成功
        """
        if not self._vector_store.is_available():
            logger.warning("[知识库引擎] 向量库不可用，无法添加文档")
            return False

        return self._vector_store.add_document(doc_id, content, metadata)

    def delete_policy_document(self, doc_id: str) -> bool:
        """
        从向量库删除政策文档

        Args:
            doc_id: 文档ID

        Returns:
            是否成功
        """
        if not self._vector_store.is_available():
            return False

        return self._vector_store.delete_document(doc_id)

    def get_statistics(self) -> Dict[str, Any]:
        """
        获取知识库统计信息

        Returns:
            统计信息字典
        """
        stats = {
            'vector_store_available': self._vector_store.is_available(),
            'document_count': 0,
            'collection_name': None
        }

        if self._vector_store.is_available():
            stats['document_count'] = self._vector_store.get_document_count()
            stats['collection_name'] = self._vector_store.collection_name

        return stats

    def _build_query(self, dim_code: str, score: float) -> str:
        """
        构建检索查询

        根据维度代码和得分，生成有意义的检索 query。

        Args:
            dim_code: 维度代码
            score: 得分

        Returns:
            检索查询字符串
        """
        dim_names = {
            'C': '合规与安全',
            'Q': '数据质量',
            'O': '权属确认',
            'V': '价值评估',
            'M': '管理体系',
            'L': '流通能力',
            'P': '发展潜力',
            'S': '成本计量'
        }

        dim_name = dim_names.get(dim_code, dim_code)
        score_level = self._get_score_level(score)

        return f"{dim_name}，{score_level}，数据资产化，合规管理，改进建议"

    def _get_score_level(self, score: float) -> str:
        """
        根据得分获取等级描述

        Args:
            score: 得分

        Returns:
            等级描述字符串
        """
        if score >= 80:
            return "高分优秀"
        elif score >= 60:
            return "中等合格"
        else:
            return "低分风险"

    def _get_risk_mitigation_suggestions(self, risk_level: str) -> List[str]:
        """
        获取风险缓解建议

        Args:
            risk_level: 风险等级 (P0/P1/P2)

        Returns:
            建议列表
        """
        suggestions = {
            'P0': [
                '【紧急】建议立即成立专项改进小组，制定详细的整改计划',
                '【紧急】优先解决高风险维度的问题，防止风险进一步扩大',
                '建议聘请第三方专业机构进行全面诊断和指导'
            ],
            'P1': [
                '建议制定 3-6 个月的改进计划，明确责任人和时间节点',
                '重点关注得分较低的维度，优先投入资源改进',
                '建议建立定期评估机制，跟踪改进效果'
            ],
            'P2': [
                '当前管理水平良好，建议持续保持',
                '可考虑申报相关行业认证，提升竞争力',
                '建议总结经验，形成最佳实践案例'
            ]
        }

        return suggestions.get(risk_level, suggestions['P2'])

    def _extract_policy_references(self, policies: List[Dict[str, Any]]) -> List[str]:
        """
        从检索结果中提取政策引用

        Args:
            policies: 检索到的政策文档列表

        Returns:
            政策引用列表（最多10条）
        """
        references = []

        for policy in policies[:10]:
            content = policy.get('content', '')
            if content:
                references.append(content[:200] + '...' if len(content) > 200 else content)

        return references


knowledge_base_engine = KnowledgeBaseEngine()
