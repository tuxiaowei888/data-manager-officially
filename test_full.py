import requests

# 1. 登录获取token
print("=== 步骤1: 登录获取Token ===")
login_url = "http://localhost:8000/api/v1/auth/login"
login_data = {
    "username": "tuxiaowei520",
    "password": "tuxiaowei520"  # 请替换为实际密码
}

try:
    login_resp = requests.post(login_url, data=login_data, timeout=10)
    print(f"登录状态码: {login_resp.status_code}")
    
    if login_resp.status_code == 200:
        token = login_resp.json().get("access_token")
        print(f"Token获取成功: {token[:50]}...")
        
        # 2. 使用token调用下载API
        print("\n=== 步骤2: 调用PDF下载API ===")
        download_url = "http://localhost:8000/api/v1/evaluation/2/download"
        headers = {"Authorization": f"Bearer {token}"}
        
        download_resp = requests.get(download_url, headers=headers, timeout=30)
        print(f"下载状态码: {download_resp.status_code}")
        
        if download_resp.status_code == 200:
            print(f"✅ PDF下载成功！文件大小: {len(download_resp.content)} bytes")
        else:
            print(f"❌ 下载失败: {download_resp.text[:500]}")
    else:
        print(f"❌ 登录失败: {login_resp.text[:500]}")
        
except Exception as e:
    print(f"❌ 发生错误: {e}")
