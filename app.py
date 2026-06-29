"""Toy FastAPI service for the Module 11 Core Skills Drill.

Two endpoints (POST /echo, GET /sum) on an in-memory app. Your job:

  1. Declare three Prometheus metrics at module scope (requests_total,
     request_latency_seconds, inflight_requests).
  2. Implement three ASGI middlewares (RequestId, StructuredLogging, Metrics)
     and add them to the app in the correct order.
  3. Mount /metrics via prometheus_client.make_asgi_app().

The published Drill page is the canonical task list. The autograder verifies
the metrics surface, header behavior, and a JSON log line is emitted.
"""

import contextvars
import json
import logging
import time
import uuid
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from pydantic import BaseModel
from prometheus_client import Counter, Gauge, Histogram, make_asgi_app
from starlette.middleware.base import BaseHTTPMiddleware

# 1. Declare metrics at module scope
requests_total = Counter(
    "requests_total", 
    "Total HTTP requests", 
    ["path", "status"]
)

request_latency_seconds = Histogram(
    "request_latency_seconds",
    "Request latency in seconds",
    ["path"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
)

inflight_requests = Gauge(
    "inflight_requests", 
    "In-flight requests"
)

# 2. Declare context variable for Request ID
request_id_var = contextvars.ContextVar("request_id", default="")

# Set up logging configuration
logger = logging.getLogger("app")
if not logger.handlers:
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    logger.addHandler(handler)

# 3. Middlewares Implementations
class RequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_id = uuid.uuid4().hex
        token = request_id_var.set(req_id)
        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = req_id
            return response
        finally:
            request_id_var.reset(token)

class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        log_payload = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": "INFO",
            "request_id": request_id_var.get(),
            "path": request.url.path,
            "status": response.status_code,
            "latency_ms": elapsed_ms
        }
        logger.info(json.dumps(log_payload))
        return response

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        inflight_requests.inc()
        start_time = time.perf_counter()
        try:
            response = await call_next(request)
            elapsed_seconds = time.perf_counter() - start_time
            
            # Record metrics after successful response processing
            requests_total.labels(path=request.url.path, status=str(response.status_code)).inc()
            request_latency_seconds.labels(path=request.url.path).observe(elapsed_seconds)
            return response
        finally:
            inflight_requests.dec()


class EchoRequest(BaseModel):
    message: str


app = FastAPI(title="M11 Drill — Toy FastAPI Service")

# Wire the three middlewares onto `app` in the correct order.
# Innermost-last execution: Middlewares are triggered outermost to innermost.
# request-id middleware runs first, then structured-logging, then metrics closest to route.
app.add_middleware(MetricsMiddleware)
app.add_middleware(StructuredLoggingMiddleware)
app.add_middleware(RequestIdMiddleware)

# Mount /metrics on `app` using make_asgi_app()
app.mount("/metrics", make_asgi_app())

# ---------------------------------------------------------------------------
# Endpoints (do not modify — these are what the autograder hits with traffic).
# ---------------------------------------------------------------------------

@app.post("/echo")
def echo(req: EchoRequest):
    return {"echo": req.message}

@app.get("/sum")
def sum_endpoint(a: int = 0, b: int = 0):
    return {"sum": a + b}