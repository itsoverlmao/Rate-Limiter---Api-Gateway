import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from limiter import RateLimiter, TokenBucket

app = FastAPI()
rate_limiter = RateLimiter(capacity=10, refill_rate=1)  # 10 requests per second



@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host
    bucket: TokenBucket = rate_limiter.get_bucket(client_ip)

    if bucket.consume():
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(rate_limiter.capacity)
        response.headers["X-RateLimit-Remaining"] = str(bucket.get_tokens())
        response.headers["X-RateLimit-Reset"] = str(int(bucket.get_reset_time()))
        return response
    else:
        return JSONResponse(status_code=429, content={"detail": "Too Many Requests"},
                            headers={"Retry-After": str(1),
                                     "X-RateLimit-Limit": str(rate_limiter.capacity),
                                     "X-RateLimit-Remaining": str(bucket.get_tokens()),
                                     "X-RateLimit-Reset": str(int(bucket.get_reset_time()))})
    

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
