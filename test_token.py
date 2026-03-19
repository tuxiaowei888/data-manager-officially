import requests

# 使用create_access_token直接创建token
from config.database import SessionLocal
from models.user import User
from api.auth import create_access_token

db = SessionLocal()
try:
    user = db.query(User).filter(User.username == 'tuxiaowei520').first()
    if user:
        # sub应该是username
        token = create_access_token({'sub': user.username})
        print(f"用户: {user.username}, VIP: {user.is_vip}")
        print(f"Token: {token[:50]}...")
        
        # 调用下载API
        download_url = "http://localhost:8000/api/v1/evaluation/2/download"
        headers = {"Authorization": f"Bearer {token}"}
        
        print(f"\n调用API: {download_url}")
        download_resp = requests.get(download_url, headers=headers, timeout=30)
        print(f"状态码: {download_resp.status_code}")
        
        if download_resp.status_code == 200:
            print(f"✅ PDF下载成功！文件大小: {len(download_resp.content)} bytes")
        else:
            print(f"❌ 下载失败: {download_resp.text}")
    else:
        print("用户不存在")
finally:
    db.close()
