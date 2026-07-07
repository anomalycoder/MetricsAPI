from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uuid
import time

app = FastAPI()

ALLOWED_ORIGIN = "https://dash-84w9rm.example.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_headers(request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    response.headers["X-Request-ID"] = str(uuid.uuid4())
    response.headers["X-Process-Time"] = str(time.perf_counter() - start)

    return response


@app.get("/stats")
def stats(values: str):
    nums = [int(x) for x in values.split(",")]

    return {
        "email": "24f2002227@ds.study.iitm.ac.in",
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / len(nums)
    }
