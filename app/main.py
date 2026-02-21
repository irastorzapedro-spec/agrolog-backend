import os
from urllib.parse import urlparse
from fastapi import FastAPI
import psycopg

app = FastAPI(title="AgroLog API", version="0.2.2")

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
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
        return {"status": "ok", "database": "connected", "config": safe}
    except Exception as e:
        return {"status": "error", "detail": str(e), "config": safe}
