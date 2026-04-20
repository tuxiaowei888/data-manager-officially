"""
客户分层信号计算服务 - 数维数据管家系统 V2.0
根据产品设计文档，将客户分为三类：
1. 高价值客户（high_value）：评估次数多，订阅层级高，付费意愿强
2. 培育客户（nurturing）：有一定活跃度，需要引导升级
3. 观察客户（observer）：低活跃度，需要激活
"""
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, or_

from models.user import User
from models.evaluation_result import EvaluationResult
from models.dataset import Dataset
from models.org_profile import OrgProfile


def calculate_customer_signals(user: User, db: Session) -> Dict[str, Any]:
    """
    计算客户分层信号
    
    Args:
        user: 用户对象
        db: 数据库会话
        
    Returns:
        dict: 包含客户分层信号和详细指标
    """
    # 获取用户基本信息
    user_data = {
        'user_id': user.id,
        'subscription_tier': user.subscription_tier or 'free',
        'is_vip': user.is_vip,
        'registration_days': (datetime.now().date() - user.created_at.date()).days if user.created_at else 0,
    }
    
    # 计算核心指标
    metrics = calculate_customer_metrics(user.id, db)
    
    # 计算信号强度
    signals = calculate_signal_strength(metrics, user_data)
    
    # 确定客户分层标签
    tier_label = determine_customer_tier(signals, metrics, user_data)
    
    # 生成推荐建议
    recommendations = generate_recommendations(tier_label, signals, metrics)
    
    return {
        'customer_tier_label': tier_label,
        'customer_tier_signals': signals,
        'metrics': metrics,
        'recommendations': recommendations,
        'calculated_at': datetime.now().isoformat()
    }


def calculate_customer_metrics(user_id: int, db: Session) -> Dict[str, Any]:
    """计算客户核心指标"""
    # 评估次数统计
    eval_stats = db.query(
        func.count(EvaluationResult.id).label('total_evaluations'),
        func.avg(EvaluationResult.total_score).label('avg_score'),
        func.max(EvaluationResult.created_at).label('latest_eval_date')
    ).filter(EvaluationResult.user_id == user_id).first()
    
    # 时间范围统计
    today = datetime.now().date()
    last_30_days = today - timedelta(days=30)
    last_90_days = today - timedelta(days=90)
    
    # 最近30天评估次数
    recent_30_eval = db.query(func.count(EvaluationResult.id)).filter(
        EvaluationResult.user_id == user_id,
        EvaluationResult.created_at >= last_30_days
    ).scalar() or 0
    
    # 最近90天评估次数
    recent_90_eval = db.query(func.count(EvaluationResult.id)).filter(
        EvaluationResult.user_id == user_id,
        EvaluationResult.created_at >= last_90_days
    ).scalar() or 0
    
    # 数据集使用统计
    dataset_count = db.query(func.count(Dataset.id)).filter(
        Dataset.user_id == user_id
    ).scalar() or 0
    
    # 企业档案统计
    org_profile_count = db.query(func.count(OrgProfile.id)).filter(
        OrgProfile.user_id == user_id
    ).scalar() or 0
    
    return {
        'total_evaluations': eval_stats.total_evaluations or 0,
        'avg_score': float(eval_stats.avg_score or 0),
        'latest_eval_date': eval_stats.latest_eval_date,
        'recent_30_eval': recent_30_eval,
        'recent_90_eval': recent_90_eval,
        'days_since_last_eval': calculate_days_since(eval_stats.latest_eval_date),
        'dataset_count': dataset_count,
        'org_profile_count': org_profile_count,
    }


def calculate_signal_strength(metrics: Dict[str, Any], user_data: Dict[str, Any]) -> Dict[str, float]:
    """计算各信号强度（0-100分）"""
    signals = {}
    
    # 1. 活跃度信号（基于近期评估频率）
    if metrics['recent_30_eval'] >= 10:
        activity_score = 90
    elif metrics['recent_30_eval'] >= 5:
        activity_score = 70
    elif metrics['recent_30_eval'] >= 2:
        activity_score = 40
    elif metrics['recent_30_eval'] >= 1:
        activity_score = 20
    else:
        activity_score = 10
    
    signals['activity'] = activity_score
    
    # 2. 价值深度信号（基于评估数量和质量）
    value_score = min(100, metrics['total_evaluations'] * 10)  # 每1次评估加10分
    if metrics['avg_score'] >= 80:
        value_score += 20
    elif metrics['avg_score'] >= 70:
        value_score += 10
    
    signals['value_depth'] = min(100, value_score)
    
    # 3. 产品使用广度信号（基于功能使用）
    breadth_score = 0
    if metrics['dataset_count'] > 0:
        breadth_score += 30
    if metrics['org_profile_count'] > 0:
        breadth_score += 30
    if user_data['subscription_tier'] != 'free':
        breadth_score += 40
    
    signals['product_breadth'] = breadth_score
    
    # 4. 忠诚度信号（基于注册时间和持续使用）
    loyalty_score = 0
    if user_data['registration_days'] > 180:
        loyalty_score += 40
    elif user_data['registration_days'] > 90:
        loyalty_score += 25
    elif user_data['registration_days'] > 30:
        loyalty_score += 10
    
    if metrics['days_since_last_eval'] <= 30:
        loyalty_score += 30
    elif metrics['days_since_last_eval'] <= 90:
        loyalty_score += 15
    
    signals['loyalty'] = min(100, loyalty_score)
    
    # 5. 升级潜力信号
    upgrade_potential = 0
    if user_data['subscription_tier'] == 'free':
        if metrics['recent_30_eval'] >= 3:
            upgrade_potential = 80
        elif metrics['recent_30_eval'] >= 1:
            upgrade_potential = 50
    elif user_data['subscription_tier'] == 'basic':
        if metrics['recent_30_eval'] >= 8:
            upgrade_potential = 70
        elif metrics['recent_30_eval'] >= 5:
            upgrade_potential = 40
    
    signals['upgrade_potential'] = upgrade_potential
    
    return signals


def determine_customer_tier(signals: Dict[str, float], metrics: Dict[str, Any], user_data: Dict[str, Any]) -> str:
    """确定客户分层标签"""
    # 计算综合得分
    weights = {
        'activity': 0.25,
        'value_depth': 0.25,
        'product_breadth': 0.20,
        'loyalty': 0.20,
        'upgrade_potential': 0.10
    }
    
    total_score = sum(signals[signal] * weight for signal, weight in weights.items())
    
    # 判断标准
    if total_score >= 70:
        # 高价值客户：高活跃度、高价值深度、多产品使用
        if signals['activity'] >= 60 and signals['value_depth'] >= 60 and signals['product_breadth'] >= 50:
            return 'high_value'
        else:
            return 'nurturing'
    elif total_score >= 40:
        # 培育客户：中等活跃度，有升级潜力
        return 'nurturing'
    else:
        # 观察客户：低活跃度，需要激活
        return 'observer'


def generate_recommendations(tier_label: str, signals: Dict[str, float], metrics: Dict[str, Any]) -> List[str]:
    """根据客户分层生成推荐建议"""
    recommendations = []
    
    if tier_label == 'high_value':
        recommendations.extend([
            '高价值客户，建议提供专属客户经理服务',
            '推荐介绍企业版功能，提升客户粘性',
            '定期邀请参加用户交流会，收集产品反馈',
            '提供优先技术支持和技术咨询'
        ])
    elif tier_label == 'nurturing':
        recommendations.extend([
            '培育客户，重点关注升级转化机会',
            '发送个性化内容，介绍高级功能价值',
            '定期跟进使用情况，提供使用指导',
            '考虑提供试用期延长或优惠券'
        ])
    else:  # observer
        recommendations.extend([
            '观察客户，需要激活和引导使用',
            '发送入门指南和使用教程',
            '提供免费评估次数，激发使用兴趣',
            '定期发送产品更新和新功能介绍'
        ])
    
    # 根据具体信号提供针对性建议
    if signals['activity'] < 30:
        recommendations.append('客户活跃度较低，建议通过邮件或短信触达激活')
    
    if signals['value_depth'] < 40:
        recommendations.append('评估深度不足，建议引导尝试更多评估维度')
    
    if signals['product_breadth'] < 30:
        recommendations.append('产品功能使用有限，建议介绍数据集和企业档案功能')
    
    if signals['upgrade_potential'] > 60:
        recommendations.append('升级潜力较高，建议安排销售跟进')
    
    return recommendations[:6]  # 最多返回6条建议


def calculate_days_since(last_date: Optional[datetime]) -> int:
    """计算距离上次评估的天数"""
    if not last_date:
        return 999  # 从未评估过
    
    if isinstance(last_date, datetime):
        last_date = last_date.date()
    
    return (datetime.now().date() - last_date).days


def batch_update_customer_tiers(db: Session, limit: int = 100) -> Dict[str, Any]:
    """
    批量更新客户分层（定时任务使用）
    
    Args:
        db: 数据库会话
        limit: 每次处理的用户数量
        
    Returns:
        dict: 处理统计信息
    """
    # 获取需要处理的用户（最近30天活跃或未分层）
    subquery = db.query(EvaluationResult.user_id).filter(
        EvaluationResult.created_at >= datetime.now() - timedelta(days=30)
    ).distinct().subquery()
    
    users = db.query(User).filter(
        or_(
            User.id.in_(db.query(subquery.c.user_id)),
            User.customer_tier_label.is_(None),
            User.last_signal_update.is_(None),
            User.last_signal_update < datetime.now() - timedelta(days=7)
        )
    ).limit(limit).all()
    
    stats = {
        'total_processed': 0,
        'high_value': 0,
        'nurturing': 0,
        'observer': 0,
        'errors': 0
    }
    
    try:
        for user in users:
            try:
                # 计算分层信号
                result = calculate_customer_signals(user, db)
                
                # 更新用户分层信息
                user.customer_tier_label = result['customer_tier_label']
                user.customer_tier_signals = result['customer_tier_signals']
                user.last_signal_update = datetime.now()
                
                # 统计
                stats[result['customer_tier_label']] += 1
                stats['total_processed'] += 1
                
            except Exception as e:
                logger = get_logger(__name__)
                logger.error(f"更新用户 {user.id} 分层时出错：{e}")
                stats['errors'] += 1
                # 单个用户失败不影响其他用户，继续处理
        
        # 所有用户处理成功后统一提交
        db.commit()
        
    except Exception as e:
        # 发生严重错误时回滚
        logger = get_logger(__name__)
        logger.error(f"批量更新客户分层时发生严重错误：{e}")
        db.rollback()
        raise
    finally:
        db.close()
    
    return stats


def get_customer_segmentation_stats(db: Session) -> Dict[str, Any]:
    """获取客户分层统计信息"""
    total = db.query(User).filter(User.user_type == 'client').count()
    
    high_value = db.query(User).filter(
        User.user_type == 'client',
        User.customer_tier_label == 'high_value'
    ).count()
    
    nurturing = db.query(User).filter(
        User.user_type == 'client',
        User.customer_tier_label == 'nurturing'
    ).count()
    
    observer = db.query(User).filter(
        User.user_type == 'client',
        User.customer_tier_label == 'observer'
    ).count()
    
    unclassified = total - high_value - nurturing - observer
    
    return {
        'total_customers': total,
        'high_value_count': high_value,
        'nurturing_count': nurturing,
        'observer_count': observer,
        'unclassified_count': max(0, unclassified),
        'high_value_percentage': round(high_value / total * 100, 2) if total > 0 else 0,
        'nurturing_percentage': round(nurturing / total * 100, 2) if total > 0 else 0,
        'observer_percentage': round(observer / total * 100, 2) if total > 0 else 0,
    }