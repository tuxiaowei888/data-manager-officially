"""
订阅服务模块 - 数维数据管家系统 V2.0
处理订阅四档体系相关业务逻辑，替代旧的VIP体系
"""
from datetime import date, datetime, timedelta
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models.user import User
from models.evaluation_result import EvaluationResult
from models.system_config import SystemConfig


def get_config_int(db: Session, key: str, default: int) -> int:
    """从数据库获取整数配置"""
    config = db.query(SystemConfig).filter(SystemConfig.config_key == key).first()
    if config and config.config_value:
        try:
            return int(config.config_value)
        except:
            return default
    return default


def get_config_bool(db: Session, key: str, default: bool) -> bool:
    """从数据库获取布尔配置"""
    config = db.query(SystemConfig).filter(SystemConfig.config_key == key).first()
    if config and config.config_value:
        return config.config_value.lower() == "true"
    return default


def get_config_str(db: Session, key: str, default: str) -> str:
    """从数据库获取字符串配置"""
    config = db.query(SystemConfig).filter(SystemConfig.config_key == key).first()
    if config and config.config_value:
        return config.config_value
    return default


def get_user_subscription_tier(user: User) -> str:
    """获取用户的有效订阅档位"""
    # 优先使用新的subscription_tier字段
    if user.subscription_tier and user.subscription_tier != 'free':
        # 检查订阅是否有效
        if user.is_subscription_active:
            return user.subscription_tier
        else:
            return 'free'
    
    # 回退到旧的VIP逻辑（兼容性）
    if user.is_vip and user.vip_expire_date and user.vip_expire_date >= date.today():
        return 'basic'  # 旧VIP用户映射为基础版
    
    return 'free'


def check_user_can_evaluate(user: User, db: Session) -> Dict[str, Any]:
    """
    检查用户是否可以进行评估（基于订阅档位的年度次数限制）
    
    Returns:
        dict: {
            'can_evaluate': bool,
            'remaining': int,
            'tier': str,
            'message': str,
            'is_vip': bool  # 兼容字段
        }
    """
    tier = get_user_subscription_tier(user)
    
    # 企业版：无限制
    if tier == 'enterprise':
        return {
            'can_evaluate': True,
            'remaining': -1,
            'tier': tier,
            'message': '企业版用户无评估次数限制',
            'is_vip': True  # 兼容字段
        }
    
    # 检查年度重置
    today = date.today()
    if not user.eval_count_reset_date or user.eval_count_reset_date < today:
        # 重置年度计数
        user.eval_count_used = 0
        # 设置下一年1月1日为重置日期
        user.eval_count_reset_date = date(today.year + 1, 1, 1)
        db.commit()
    
    # 获取年度限额
    limit_key = f"{tier}_eval_limit"
    annual_limit = get_config_int(db, limit_key, 1 if tier == 'free' else 5)
    
    used = user.eval_count_used or 0
    remaining = annual_limit - used
    
    if remaining > 0:
        return {
            'can_evaluate': True,
            'remaining': remaining,
            'tier': tier,
            'message': f'本年度剩余{remaining}次评估机会（共{annual_limit}次）',
            'is_vip': tier != 'free'  # 兼容字段
        }
    else:
        return {
            'can_evaluate': False,
            'remaining': 0,
            'tier': tier,
            'message': f'本年度评估次数已用完（共{annual_limit}次），升级订阅可获取更多次数',
            'is_vip': tier != 'free'  # 兼容字段
        }


def increment_eval_count(user: User, db: Session):
    """增加用户评估计数（基于订阅体系）"""
    tier = get_user_subscription_tier(user)
    
    # 企业版不计次
    if tier == 'enterprise':
        return
    
    # 检查年度重置
    today = date.today()
    if not user.eval_count_reset_date or user.eval_count_reset_date < today:
        # 重置年度计数
        user.eval_count_used = 0
        user.eval_count_reset_date = date(today.year + 1, 1, 1)
    
    # 增加计数
    user.eval_count_used = (user.eval_count_used or 0) + 1
    db.commit()


def can_export_report(user: User, db: Session) -> bool:
    """检查用户是否可以导出报告"""
    tier = get_user_subscription_tier(user)
    
    if tier == 'free':
        return False
    
    # 检查订阅是否有效
    if not user.is_subscription_active:
        return False
    
    # 检查配置权限
    export_key = f"{tier}_pdf_export"
    return get_config_bool(db, export_key, tier != 'free')


def get_report_retention_days(user: User, db: Session) -> int:
    """获取用户报告保留天数"""
    tier = get_user_subscription_tier(user)
    
    # 检查订阅是否有效
    if not user.is_subscription_active:
        tier = 'free'
    
    retention_key = f"{tier}_report_retention"
    return get_config_int(db, retention_key, 7 if tier == 'free' else 365)


def get_report_depth(user: User, db: Session) -> str:
    """获取用户报告深度"""
    tier = get_user_subscription_tier(user)
    
    # 检查订阅是否有效
    if not user.is_subscription_active:
        tier = 'free'
    
    depth_key = f"{tier}_report_depth"
    return get_config_str(db, depth_key, 'summary' if tier == 'free' else 'diagnosis')


def get_subscription_plans(db: Session) -> Dict[str, Any]:
    """获取订阅方案列表"""
    return {
        'free': {
            'name': '体验版',
            'price': 0,
            'annual_eval_limit': get_config_int(db, 'free_eval_limit', 1),
            'report_depth': get_config_str(db, 'free_report_depth', 'summary'),
            'features': [
                '1次年度评估',
                '体检单级别报告',
                '7天报告保留'
            ]
        },
        'basic': {
            'name': '基础版',
            'price': 4980,  # 年费
            'annual_eval_limit': get_config_int(db, 'basic_eval_limit', 5),
            'report_depth': get_config_str(db, 'basic_report_depth', 'diagnosis'),
            'features': [
                '5次年度评估',
                '诊断报告级别',
                '1年报告保留',
                'PDF报告导出',
                '基础知识库访问'
            ]
        },
        'pro': {
            'name': '专业版',
            'price': 16800,  # 年费
            'annual_eval_limit': get_config_int(db, 'pro_eval_limit', 20),
            'report_depth': get_config_str(db, 'pro_report_depth', 'action_plan'),
            'features': [
                '20次年度评估',
                '行动方案级别报告',
                '2年报告保留',
                '行业对标分析',
                '数据资产估值',
                '完整知识库访问'
            ]
        },
        'enterprise': {
            'name': '企业版',
            'price': 49800,  # 年起
            'annual_eval_limit': -1,  # 不限量
            'report_depth': get_config_str(db, 'enterprise_report_depth', 'full'),
            'features': [
                '不限量评估',
                '全量报告+品牌定制',
                '永久报告保留',
                'API接口访问',
                '多数据集概览',
                '专属客户支持'
            ]
        }
    }


def upgrade_subscription(user: User, new_tier: str, duration_days: int, db: Session) -> Dict[str, Any]:
    """
    升级用户订阅
    
    Args:
        user: 用户对象
        new_tier: 新的订阅档位
        duration_days: 订阅时长（天）
        db: 数据库会话
    
    Returns:
        dict: 升级结果
    """
    valid_tiers = ['free', 'basic', 'pro', 'enterprise']
    if new_tier not in valid_tiers:
        return {
            'success': False,
            'message': f'无效的订阅档位：{new_tier}'
        }
    
    # 计算开始日期
    start_date = date.today()
    
    # 如果从免费版升级，重置评估计数
    if user.subscription_tier == 'free' and new_tier != 'free':
        user.eval_count_used = 0
        user.eval_count_reset_date = date(start_date.year + 1, 1, 1)
    
    # 更新订阅信息
    user.subscription_tier = new_tier
    user.subscription_start_date = start_date
    
    # 设置VIP过期日期（兼容旧逻辑）
    if new_tier != 'free':
        user.is_vip = True
        user.vip_expire_date = start_date + timedelta(days=duration_days)
    else:
        user.is_vip = False
        user.vip_expire_date = None
    
    db.commit()
    
    return {
        'success': True,
        'message': f'成功升级到{new_tier}版订阅',
        'tier': new_tier,
        'start_date': start_date.isoformat(),
        'expire_date': user.vip_expire_date.isoformat() if user.vip_expire_date else None
    }


def cleanup_expired_reports(db: Session):
    """
    清理过期的报告（定时任务调用）
    
    基于订阅体系的报告保留策略：
    - 体验版：7天
    - 基础版：1年
    - 专业版：2年
    - 企业版：永久保留
    """
    today = datetime.utcnow()
    
    # 查询所有用户及其订阅状态
    users = db.query(User).all()
    
    deleted_count = 0
    for user in users:
        tier = get_user_subscription_tier(user)
        
        # 企业版报告永久保留
        if tier == 'enterprise':
            continue
        
        # 获取保留天数
        retention_days = get_report_retention_days(user, db)
        if retention_days <= 0:
            continue  # 永久保留或配置错误
        
        cutoff_date = today - timedelta(days=retention_days)
        
        # 清理过期报告
        expired_reports = db.query(EvaluationResult).filter(
            EvaluationResult.user_id == user.id,
            EvaluationResult.created_at < cutoff_date
        ).all()
        
        for report in expired_reports:
            db.delete(report)
            deleted_count += 1
    
    db.commit()
    
    # 记录清理日志
    from config.logging_config import get_logger
    logger = get_logger(__name__)
    logger.info(f"订阅体系报告清理完成，共删除 {deleted_count} 条记录")
    
    return deleted_count


def get_user_subscription_info(user: User, db: Session) -> Dict[str, Any]:
    """获取用户订阅详细信息"""
    tier = get_user_subscription_tier(user)
    plans = get_subscription_plans(db)
    
    # 获取评估次数信息
    eval_info = check_user_can_evaluate(user, db)
    
    # 获取功能权限
    can_export = can_export_report(user, db)
    report_depth = get_report_depth(user, db)
    retention_days = get_report_retention_days(user, db)
    
    return {
        'tier': tier,
        'tier_name': plans[tier]['name'],
        'is_active': user.is_subscription_active,
        'start_date': user.subscription_start_date.isoformat() if user.subscription_start_date else None,
        'expire_date': user.vip_expire_date.isoformat() if user.vip_expire_date else None,
        'eval_used': user.eval_count_used or 0,
        'eval_limit': eval_info['remaining'] if eval_info['remaining'] >= 0 else '不限量',
        'eval_reset_date': user.eval_count_reset_date.isoformat() if user.eval_count_reset_date else None,
        'can_export': can_export,
        'report_depth': report_depth,
        'retention_days': retention_days,
        'customer_tier': user.customer_tier_label or 'observer',
        'customer_score': user.customer_tier_signal or 0
    }