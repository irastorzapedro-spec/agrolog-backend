from fastapi import FastAPI

app = FastAPI(title="AgroLog API", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/auth/me")
def me():
    # Stub: después lo conectamos con JWT + DB
    return {"user": "demo", "roles": ["OPERATOR_ADMIN"]}
