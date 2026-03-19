import sys
sys.path.insert(0, '.')

from config.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE evaluation_results ADD COLUMN detail_json JSON"))
        print("添加 detail_json 成功")
    except Exception as e:
        print(f"detail_json: {e}")
    
    try:
        conn.execute(text("ALTER TABLE evaluation_results ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"))
        print("添加 created_at 成功")
    except Exception as e:
        print(f"created_at: {e}")
    
    conn.commit()
print("完成！")
