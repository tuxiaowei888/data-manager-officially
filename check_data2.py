from config.database import SessionLocal
from models.evaluation_result import EvaluationResult

db = SessionLocal()
try:
    report = db.query(EvaluationResult).first()
    if report:
        print('Report ID:', report.id)
        print('Org name:', report.org_name)
        print('Total score:', report.total_score)
        print('Risk level:', report.risk_level)
        detail = report.detail_json or {}
        print('\nDetail keys:', list(detail.keys()))
        for key in detail.keys():
            print(f'\n--- {key} ---')
            print(repr(detail[key])[:200])
finally:
    db.close()
