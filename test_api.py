from config.database import SessionLocal
from models.user import User
from models.evaluation_result import EvaluationResult
from api.auth import create_access_token
import requests
import traceback

print("=== 测试PDF下载API")
print("=" * 50)

db = SessionLocal()
try:
    user = db.query(User).filter(User.username == 'tuxiaowei520').first()
    report = db.query(EvaluationResult).first()
    
    if user and report:
        print(f"用户: {user.username}, VIP: {user.is_vip}")
        print(f"报告ID: {report.id}")
        print(f"企业名称: {report.org_name}")
        
        token = create_access_token({'sub': user.username})
        url = f'http://localhost:8000/api/v1/evaluation/{report.id}/download'
        
        print(f"\n调用API: {url}")
        print(f"Token: {token[:60]}...")
        
        resp = requests.get(url, headers={'Authorization': f'Bearer {token}'})
        
        print(f"\n状态码: {resp.status_code}")
        
        if resp.status_code == 200:
            print(f"响应头: {dict(resp.headers)}")
            print(f"PDF大小: {len(resp.content)} bytes")
            print("\n✅ API调用成功！")
        else:
            print(f"响应内容: {resp.text}")
            print(f"\n❌ API调用失败")
    else:
        print("未找到用户或报告")
except Exception as e:
    print(f"\n发生错误: {e}")
    traceback.print_exc()
finally:
    db.close()
