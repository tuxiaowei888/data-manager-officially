"""
脚本数据库连接工具 - 数维数据管家系统
为独立脚本提供安全的数据库连接，避免硬编码凭据
"""
import os
import pymysql
from typing import Optional, Dict, Any


def get_db_config_from_env() -> Dict[str, Any]:
    """
    从环境变量获取数据库配置
    
    返回:
        dict: 包含 host, port, user, password, database 的字典
    """
    # 优先使用 DATABASE_URL
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    if DATABASE_URL:
        # 解析 DATABASE_URL (格式: mysql+pymysql://user:password@host:port/database?charset=utf8mb4)
        if not DATABASE_URL.startswith("mysql+pymysql://"):
            raise ValueError(f"不支持的DATABASE_URL格式: {DATABASE_URL}")
        
        # 移除 mysql+pymysql:// 前缀
        url_part = DATABASE_URL.replace("mysql+pymysql://", "")
        
        # 分割用户信息和主机信息
        if "@" not in url_part:
            raise ValueError(f"无效的DATABASE_URL格式，缺少@符号: {DATABASE_URL}")
        
        user_pass, host_db = url_part.split("@", 1)
        
        # 分割用户名和密码
        if ":" not in user_pass:
            raise ValueError(f"无效的DATABASE_URL格式，缺少用户名密码分隔符: {DATABASE_URL}")
        
        user, password = user_pass.split(":", 1)
        
        # 分割主机和数据库
        if "/" not in host_db:
            raise ValueError(f"无效的DATABASE_URL格式，缺少数据库名分隔符: {DATABASE_URL}")
        
        host_port, database_with_params = host_db.split("/", 1)
        
        # 移除查询参数
        database = database_with_params.split("?")[0]
        
        # 解析主机和端口
        if ":" in host_port:
            host, port_str = host_port.split(":", 1)
            try:
                port = int(port_str)
            except ValueError:
                raise ValueError(f"无效的端口号: {port_str}")
        else:
            host = host_port
            port = 3306
            
        return {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database
        }
    else:
        # 使用单独的数据库环境变量
        host = os.getenv("DATABASE_HOST", "localhost")
        port_str = os.getenv("DATABASE_PORT", "3306")
        user = os.getenv("DATABASE_USER", "root")
        password = os.getenv("DATABASE_PASSWORD", "root")
        database = os.getenv("DATABASE_NAME", "shuwei_data_manager")
        
        try:
            port = int(port_str)
        except ValueError:
            raise ValueError(f"无效的端口号: {port_str}")
        
        return {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database
        }


def get_pymysql_connection():
    """
    获取pymysql数据库连接
    
    返回:
        pymysql.Connection: 数据库连接对象
    """
    config = get_db_config_from_env()
    
    # 检查是否是开发环境，如果是则记录警告
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    if DEBUG and config["password"] == "root":
        import warnings
        warnings.warn(
            "使用默认数据库密码 'root'。生产环境必须设置安全的数据库密码！",
            UserWarning
        )
    
    print(f"连接数据库: {config['host']}:{config['port']}/{config['database']}")
    
    return pymysql.connect(
        host=config["host"],
        port=config["port"],
        user=config["user"],
        password=config["password"],
        database=config["database"],
        charset='utf8mb4'
    )


def get_sqlalchemy_session():
    """
    获取SQLAlchemy会话（用于更复杂的脚本）
    
    返回:
        sqlalchemy.orm.Session: SQLAlchemy会话对象
    """
    try:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        # 使用主应用的数据库配置
        from config.database import engine
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return SessionLocal()
    except ImportError:
        raise ImportError("SQLAlchemy未安装，请安装: pip install sqlalchemy")
    except Exception as e:
        raise RuntimeError(f"创建SQLAlchemy会话失败: {e}")