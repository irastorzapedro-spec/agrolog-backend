import os
from fastapi import FastAPI
from urllib.parse import urlparse

app = FastAPI(title="AgroLog API", version="0.2.3")

DATABASE_URL = os.getenv("DATABASE_URL", "")

@app.get("/health")
def health():
    try:
        parsed = urlparse(DATABASE_URL) if DATABASE_URL else None
        safe = {
            "has_database_url": bool(DATABASE_URL),
            "db_host": parsed.hostname if parsed else None,
            "db_port": parsed.port if parsed else None,
            "db_user": parsed.username if parsed else None,
            "db_name": (parsed.path or "").lstrip("/") if parsed else None,
        }
        return {"status": "diagnostic", "config": safe}
    except Exception as e:
        # Nunca 500: devolvemos el error como texto
        return {"status": "diagnostic_error", "detail": str(e)}

@app.get("/debug/db")
def debug_db():
    return {"DATABASE_URL_raw": DATABASE_URL}
