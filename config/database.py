"""
数据库配置模块 - 数维数据管家系统
"""
import os
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config.logging_config import get_logger

logger = get_logger(__name__)

# 数据库连接配置 - 从环境变量读取，提供默认值用于开发环境
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:root@localhost:3306/shuwei_data_manager?charset=utf8mb4"
)

# 连接池配置
POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "10"))
MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "20"))
POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))
POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "3600"))

# 创建数据库引擎 - 优化连接池配置
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,           # 连接前检查连接是否有效
    echo=False,                   # 不输出SQL语句
    pool_size=POOL_SIZE,          # 连接池大小
    max_overflow=MAX_OVERFLOW,    # 最大溢出连接数
    pool_timeout=POOL_TIMEOUT,    # 获取连接超时时间（秒）
    pool_recycle=POOL_RECYCLE,    # 连接回收时间（秒）
    connect_args={
        "connect_timeout": 10,    # 连接超时时间
        "read_timeout": 30,       # 读取超时时间
        "write_timeout": 30,      # 写入超时时间
    }
)

# 监听连接事件
@event.listens_for(engine, "connect")
def on_connect(dbapi_conn, connection_record):
    """连接建立时的回调"""
    logger.debug("数据库连接已建立")


@event.listens_for(engine, "checkout")
def on_checkout(dbapi_conn, connection_record, connection_proxy):
    """连接从池中取出时的回调"""
    logger.debug("数据库连接已从连接池取出")


@event.listens_for(engine, "checkin")
def on_checkin(dbapi_conn, connection_record):
    """连接归还到池时的回调"""
    logger.debug("数据库连接已归还到连接池")


# 创建会话工厂
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False  # 提交后不过期对象
)

# 创建基类
Base = declarative_base()


def get_db():
    """
    获取数据库会话
    
    Yields:
        Session: 数据库会话对象
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"数据库操作错误: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db():
    """初始化数据库 - 创建所有表"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        raise
