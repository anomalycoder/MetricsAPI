from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uuid
import time

app = FastAPI()

EMAIL = "24f2002227@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = [
    "https://dash-84w9rm.example.com",
    "https://exam.sanand.workers.dev/tds-2026-05-ga2",
    "https://exam.sanand.workers.dev"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_headers(request, call_next):
    start = time.perf_counter()
    response = await call_next(request)

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"

    return response

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/stats")
def stats(values: str):
    nums = [int(v.strip()) for v in values.split(",") if v.strip()]

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / len(nums),
    }
