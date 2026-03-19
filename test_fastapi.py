import uvicorn
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from config.database import SessionLocal, get_db
from models.user import User
from api.evaluation import router as eval_router
from api.auth import get_current_user
from services.vip_service import can_export_report

app = FastAPI()
app.include_router(eval_router)

client = TestClient(app)

def override_get_current_user():
    db = SessionLocal()
    user = db.query(User).filter(User.username == 'tuxiaowei520').first()
    db.close()
    return user

app.dependency_overrides[get_current_user] = override_get_current_user

response = client.get("/api/v1/evaluation/2/download")
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")
