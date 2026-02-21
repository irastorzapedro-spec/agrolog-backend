import os
from urllib.parse import urlparse

import psycopg
from fastapi import FastAPI

app = FastAPI(title="AgroLog API", version="0.2.4")

DATABASE_URL = os.getenv("DATABASE_URL", "")

@app.get("/health")
def health():
    parsed = urlparse(DATABASE_URL) if DATABASE_URL else None
    safe = {
        "has_database_url": bool(DATABASE_URL),
        "db_host": parsed.hostname if parsed else None,
        "db_port": parsed.port if parsed else None,
        "db_user": parsed.username if parsed else None,
        "db_name": (parsed.path or "").lstrip("/") if parsed else None,
    }

    try:
     with psycopg.connect(DATABASE_URL, prepare_threshold=None) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT 1;")
        cur.fetchone()
        return {"status": "ok", "database": "connected", "config": safe}
    except Exception as e:
        return {"status": "error", "detail": str(e), "config": safe}

@app.get("/debug/db")
def debug_db():
    return {"DATABASE_URL_raw": DATABASE_URL}
