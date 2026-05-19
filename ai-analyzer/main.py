import time
import json
import redis
import asyncio  # Async handling ke liye
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

app = FastAPI(title="AI Threat Analytics Engine")

# 1. CORS Setup (Isse browser request block nahi hogi)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Redis Connection
try:
    r = redis.Redis(host='redis-queue', port=6379, decode_responses=True)
    print("🎉 AI Analyzer connected to Redis Queue!")
except Exception as e:
    print(f"Redis Connection Failed: {e}")

# 3. MongoDB Connection
try:
    mongo_client = MongoClient('mongodb://mongodb-container:27017/')
    db = mongo_client['security_analytics']
    logs_collection = db['threat_logs']
    print("🗄️ AI Analyzer successfully connected to MongoDB!")
except Exception as e:
    print(f"MongoDB Connection Failed: {e}")

def ai_predict_threat(log_message):
    msg = log_message.lower()
    if "sql injection" in msg or "failed login" in msg or "unauthorized" in msg:
        return {"prediction": "THREAT_DETECTED", "confidence": 0.94, "severity": "HIGH"}
    elif "cpu utilization" in msg or "heavy load" in msg:
        return {"prediction": "ANOMALY_LOG", "confidence": 0.78, "severity": "MEDIUM"}
    else:
        return {"prediction": "SAFE_LOG", "confidence": 0.99, "severity": "LOW"}

# 4. Async Non-Blocking Background Worker
async def process_logs_loop():
    print("🤖 AI Background Brain Processing Started...")
    while True:
        try:
            raw_log = r.rpop('logs-queue')
            if raw_log:
                log_data = json.loads(raw_log)
                message = log_data.get('message', '')
                
                ai_result = ai_predict_threat(message)
                
                final_report = {
                    "timestamp": log_data.get('timestamp'),
                    "original_log": message,
                    "ai_analysis": ai_result
                }
                
                logs_collection.insert_one(final_report)
                print(f"💾 [Saved to MongoDB]: {log_data.get('status')} - {message}")
            
            # FastAPI core operations ko break dene ke liye 1 second pause
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Loop Error: {e}")
            await asyncio.sleep(2)

# Startup event me safe thread register karna
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_logs_loop())

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "AI Threat Engine"}
