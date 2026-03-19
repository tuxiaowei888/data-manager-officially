import sys
import traceback
from config.database import SessionLocal
from models.user import User
from models.evaluation_result import EvaluationResult
from services.evaluation import EvaluationService
from services.pdf_service import generate_report_pdf
from datetime import datetime

db = SessionLocal()
try:
    user = db.query(User).filter(User.username == 'tuxiaowei520').first()
    print(f"User: {user.username}, VIP: {user.is_vip}")
    
    service = EvaluationService(db)
    result = service.get_result(2)
    print(f"Report: {result.get('org_name')}")
    
    detail_json = result.get('detail_json') or {}
    report_data = {
        'id': 2,
        'org_name': result.get('org_name') or 'test',
        'total_score': result.get('total_score') or 80,
        'risk_level': result.get('risk_level') or 'P2',
        'maturity_level': detail_json.get('maturity_level', ''),
        'dimensions': detail_json.get('dimensions', []) or [],
        'p0_issues': detail_json.get('p0_issues', []) or [],
        'p1_issues': detail_json.get('p1_issues', []) or [],
        'generated_at': str(result.get('created_at')) if result.get('created_at') else ''
    }
    
    print(f"Data: {report_data}")
    
    pdf_file = generate_report_pdf(report_data)
    print(f"PDF generated: {len(pdf_file.getvalue())} bytes")
    print("SUCCESS")
    
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
    traceback.print_exc()
finally:
    db.close()
