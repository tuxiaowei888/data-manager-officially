"""
创建管理员账号脚本
运行方式: python scripts/create_admin.py
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from config.database import SessionLocal, engine, Base
from models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_admin(username: str = "admin", password: str = "admin123", email: str = "admin@shuwei.com"):
    """创建管理员账号"""
    db: Session = SessionLocal()
    
    try:
        # 检查是否已存在
        existing = db.query(User).filter(User.username == username).first()
        if existing:
            print(f"用户名 '{username}' 已存在")
            if existing.user_type != 'admin':
                existing.user_type = 'admin'
                db.commit()
                print(f"已将用户 '{username}' 升级为管理员")
            return existing
        
        # 创建管理员
        admin = User(
            username=username,
            password_hash=pwd_context.hash(password),
            email=email,
            user_type='admin',
            is_active=True
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        print("=" * 50)
        print("管理员账号创建成功！")
        print("=" * 50)
        print(f"用户名: {username}")
        print(f"密码: {password}")
        print(f"邮箱: {email}")
        print("=" * 50)
        print("请登录后访问规则库和知识库管理页面")
        
        return admin
        
    except Exception as e:
        print(f"创建失败: {e}")
        db.rollback()
        return None
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='创建管理员账号')
    parser.add_argument('--username', default='admin', help='用户名')
    parser.add_argument('--password', default='admin123', help='密码')
    parser.add_argument('--email', default='admin@shuwei.com', help='邮箱')
    
    args = parser.parse_args()
    
    create_admin(args.username, args.password, args.email)
