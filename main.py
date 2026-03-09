# main.py
from fastapi import FastAPI
from app.db.database import create_tables
from app.core.config import settings

app = FastAPI(
    title="Azure Resource Monitor Agent",
    description="Identifies and reports underutilised Azure resources",
    version="0.1.0"
)

@app.on_event("startup")
def startup():
    create_tables()
    print(f"DB tables created. Monitoring {len(settings.subscription_ids)} subscription(s).")

@app.get("/health")
def health():
    return {"status": "ok", "subscriptions": settings.subscription_ids}