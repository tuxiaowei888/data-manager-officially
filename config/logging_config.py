"""
日志配置模块 - 数维数据管家系统
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

# 日志目录
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 日志格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(log_level: str = None):
    """
    配置日志系统
    
    Args:
        log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # 从环境变量获取日志级别
    if log_level is None:
        log_level = os.getenv("LOG_LEVEL", "INFO")
    
    # 转换为日志级别常量
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # 配置根日志记录器
    logging.basicConfig(
        level=level,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        handlers=[
            # 控制台输出
            logging.StreamHandler(),
            # 应用日志文件 (最大10MB，保留5个备份)
            RotatingFileHandler(
                os.path.join(LOG_DIR, "app.log"),
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding="utf-8"
            ),
        ]
    )
    
    # 错误日志单独记录
    error_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, "error.log"),
        maxBytes=10*1024*1024,
        backupCount=5,
        encoding="utf-8"
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    
    # 获取根日志记录器并添加错误处理器
    root_logger = logging.getLogger()
    root_logger.addHandler(error_handler)
    
    # 设置第三方库的日志级别
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    获取日志记录器
    
    Args:
        name: 日志记录器名称（通常使用 __name__）
        
    Returns:
        Logger 实例
    """
    return logging.getLogger(name)
