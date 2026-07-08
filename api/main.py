import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 1. STRICT CORS POLICY: Only allow your assigned origin. No wildcards.
ALLOWED_ORIGIN = "https://dash-84w9rm.example.com"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. CUSTOM MIDDLEWARE: Inject X-Request-ID and X-Process-Time
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start_time = time.time()
    request_id = str(uuid.uuid4())
    
    # Process the request
    response = await call_next(request)
    
    # Calculate duration
    process_time = time.time() - start_time
    
    # Add required headers
    response.headers["X-Request-ID"] = request_id
    # Ensure it's a non-negative decimal as a string
    response.headers["X-Process-Time"] = f"{max(0.0, process_time):.6f}"
    
    return response

# 3. STATS ENDPOINT
@app.get("/stats")
@app.get("/api/stats")  # Catch Vercel pathing just in case
def get_stats(values: str):
    # Parse comma-separated string into a list of integers
    int_values = [int(v.strip()) for v in values.split(",") if v.strip()]
    
    if not int_values:
        return {"error": "No values provided"}
        
    count = len(int_values)
    total_sum = sum(int_values)
    min_val = min(int_values)
    max_val = max(int_values)
    mean_val = total_sum / count

    return {
        "email": "24f2002227@ds.study.iitm.ac.in",  # <-- CHANGE THIS TO YOUR EXAM EMAIL
        "count": count,
        "sum": total_sum,
        "min": min_val,
        "max": max_val,
        "mean": mean_val
    }
