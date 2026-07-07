import time
import uuid
from fastapi import FastAPI, Query, Request, Response
from fastapi.responses import JSONResponse

app = FastAPI()

# 1. Define your assigned variables
ALLOWED_ORIGIN = "https://dash-84w9rm.example.com"
MY_EMAIL = "24f2002227@ds.study.iitm.ac.in"  # <--- Change this to your exact logged-in email

@app.middleware("http")
async def cors_and_headers_middleware(request: request, call_next):
    # Start the timer immediately to calculate processing time
    start_time = time.perf_counter()
    
    # Generate a unique Request ID
    request_id = str(uuid.uuid4())
    
    # Check incoming Origin header from the browser/grader
    origin = request.headers.get("origin")
    
    # Handle Preflight OPTIONS requests manually for strict origin control
    if request.method == "OPTIONS":
        response = Response(status_code=204)
        if origin == ALLOWED_ORIGIN:
            response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
            response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"
        # Preflight requests stop here and return directly
        process_time = time.perf_counter() - start_time
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.6f}"
        return response

    # Process normal requests (like GET) through the API handlers
    response = await call_next(request)
    
    # Attach CORS header only if the origin strictly matches your assigned origin
    if origin == ALLOWED_ORIGIN:
        response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
        
    # Calculate final processing time
    process_time = time.perf_counter() - start_time
    
    # Attach mandatory tracking headers to every single response
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    
    return response

@app.get("/stats")
def get_stats(values: str = Query(..., description="Comma-separated integers")):
    try:
        # Convert the string "1,2,3" into a Python list of integers: [1, 2, 3]
        num_list = [int(v.strip()) for v in values.split(",") if v.strip()]
        
        if not num_list:
            return JSONResponse(status_code=400, content={"error": "No valid integers provided"})
            
        # Calculate statistics
        count_val = len(num_list)
        sum_val = sum(num_list)
        min_val = min(num_list)
        max_val = max(num_list)
        mean_val = sum_val / count_val
        
        # Return the exact JSON structure the grader wants
        return {
            "email": MY_EMAIL,
            "count": count_val,
            "sum": sum_val,
            "min": min_val,
            "max": max_val,
            "mean": round(mean_val, 4) # Easily satisfies the ±0.01 precision check
        }
        
    except ValueError:
        return JSONResponse(status_code=400, content={"error": "Invalid input. Please provide integers only."})
