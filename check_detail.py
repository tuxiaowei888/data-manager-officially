from config.database import SessionLocal
from models.evaluation_result import EvaluationResult

db = SessionLocal()
try:
    report = db.query(EvaluationResult).first()
    if report:
        detail = report.detail_json or {}
        print('=== Complete Detail JSON ===')
        import json
        print(json.dumps(detail, indent=2, ensure_ascii=False))
finally:
    db.close()
