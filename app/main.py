import os
from fastapi import FastAPI
import psycopg

app = FastAPI(title="AgroLog API", version="0.2.0")

DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/health")
def health():
    try:
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
