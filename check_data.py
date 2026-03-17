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
        print('Detail keys:', list(detail.keys()))
        print('Has p0_issues:', 'p0_issues' in detail)
        print('Has p1_issues:', 'p1_issues' in detail)
        if 'p0_issues' in detail:
            print('p0_issues length:', len(detail['p0_issues']))
            if detail['p0_issues']:
                print('First p0_issue:', detail['p0_issues'][0])
finally:
    db.close()
