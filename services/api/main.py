import os
import httpx
from fastapi import FastAPI

app = FastAPI()

XRPL_SERVICE_URL = os.getenv("XRPL_SERVICE_URL", "http://localhost:3001")

@app.get("/health")
def health():
    return {"ok": True, "service": "api"}

@app.get("/xrpl/health")
async def xrpl_health():
    async with httpx.AsyncClient(timeout=5.0) as client:
        r = await client.get(f"{XRPL_SERVICE_URL}/health")
        r.raise_for_status()
        return {"ok": True, "xrpl_service": r.json()}
