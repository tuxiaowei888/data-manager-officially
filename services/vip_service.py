"""
VIP 服务模块 - 处理VIP相关业务逻辑
"""
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
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


def check_user_can_evaluate(user: User, db: Session) -> dict:
    """
    检查用户是否可以进行评估
    
    Returns:
        dict: {
            'can_evaluate': bool,
            'remaining': int,
            'is_vip': bool,
            'message': str
        }
    """
    if user.is_vip:
        if user.vip_expire_date and user.vip_expire_date < date.today():
            user.is_vip = False
            db.commit()
        else:
            return {
                'can_evaluate': True,
                'remaining': -1,
                'is_vip': True,
                'message': 'VIP用户无限制'
            }
    
    today = date.today()
    
    if user.daily_eval_date != today:
        user.daily_eval_count = 0
        user.daily_eval_date = today
        db.commit()
    
    daily_limit = get_config_int(db, "free_daily_eval_limit", 3)
    remaining = daily_limit - (user.daily_eval_count or 0)
    
    if remaining <= 0:
        return {
            'can_evaluate': False,
            'remaining': 0,
            'is_vip': False,
            'message': f'今日评估次数已用完（{daily_limit}次），VIP用户无限制'
        }
    
    return {
        'can_evaluate': True,
        'remaining': remaining,
        'is_vip': False,
        'message': f'今日剩余{remaining}次评估机会'
    }


def increment_eval_count(user: User, db: Session):
    """增加用户评估计数"""
    today = date.today()
    
    if user.daily_eval_date != today:
        user.daily_eval_count = 1
        user.daily_eval_date = today
    else:
        user.daily_eval_count = (user.daily_eval_count or 0) + 1
    
    db.commit()


def can_export_report(user: User) -> bool:
    """检查用户是否可以导出报告"""
    if user.is_vip:
        if user.vip_expire_date and user.vip_expire_date < date.today():
            return False
        return True
    return False


def get_report_retention_days(user: User, db: Session) -> int:
    """获取用户报告保留天数"""
    if user.is_vip:
        if user.vip_expire_date and user.vip_expire_date < date.today():
            return get_config_int(db, "free_report_retention_days", 7)
        return get_config_int(db, "vip_report_retention_days", 36500)
    return get_config_int(db, "free_report_retention_days", 7)


def cleanup_expired_reports(db: Session):
    """清理过期的报告（定时任务调用）"""
    users = db.query(User).all()
    
    for user in users:
        retention_days = get_report_retention_days(user, db)
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        
        expired_reports = db.query(EvaluationResult).filter(
            EvaluationResult.user_id == user.id,
            EvaluationResult.created_at < cutoff_date
        ).all()
        
        for report in expired_reports:
            db.delete(report)
    
    db.commit()


def set_user_vip(user: User, days: int, db: Session):
    """
    设置用户VIP
    
    Args:
        user: 用户对象
        days: VIP天数
        db: 数据库会话
    """
    user.is_vip = True
    
    if user.vip_expire_date and user.vip_expire_date >= date.today():
        user.vip_expire_date = user.vip_expire_date + timedelta(days=days)
    else:
        user.vip_expire_date = date.today() + timedelta(days=days)
    
    db.commit()


def revoke_user_vip(user: User, db: Session):
    """取消用户VIP"""
    user.is_vip = False
    user.vip_expire_date = None
    db.commit()
