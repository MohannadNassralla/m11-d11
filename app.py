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

from fastapi import FastAPI
from pydantic import BaseModel

# TODO: import Counter, Gauge, Histogram, make_asgi_app from prometheus_client.

# TODO: import uuid, json, logging, time, contextvars as you need them.


# TODO: declare requests_total Counter (labels: path, status) at module scope.
# TODO: declare request_latency_seconds Histogram at module scope.
#       Labels: ["path"]. Use this explicit bucket sequence
#       (do NOT use prometheus_client.Histogram's DEFAULT_BUCKETS --
#       the published Drill guide pins these exact values):
#         buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
# TODO: declare inflight_requests Gauge (no labels) at module scope.


# TODO: declare a module-level ContextVar named request_id_var (default "").


# TODO: implement RequestIdMiddleware.
#   - On entry: generate uuid4().hex and store it in request_id_var.
#   - On response: set the X-Request-ID header.


# TODO: implement StructuredLoggingMiddleware.
#   - Time the request.
#   - Emit one JSON line at INFO level via the logging module with keys:
#     ts, level, request_id, path, status, latency_ms.
#   - Do NOT use print(...).


# TODO: implement MetricsMiddleware.
#   - On entry: increment inflight_requests.
#   - Time the handler.
#   - On exit (try/finally): decrement inflight_requests, increment
#     requests_total.labels(path=..., status=...).inc(),
#     call request_latency_seconds.labels(path=...).observe(elapsed).


class EchoRequest(BaseModel):
    message: str


app = FastAPI(title="M11 Drill — Toy FastAPI Service")


# TODO: wire the three middlewares onto `app` in the correct order.
#       Last add_middleware is outermost (request-id outer, metrics inner).


# TODO: mount /metrics on `app` using make_asgi_app().


# ---------------------------------------------------------------------------
# Endpoints (do not modify — these are what the autograder hits with traffic).
# ---------------------------------------------------------------------------


@app.post("/echo")
def echo(req: EchoRequest):
    return {"echo": req.message}


@app.get("/sum")
def sum_endpoint(a: int = 0, b: int = 0):
    return {"sum": a + b}
