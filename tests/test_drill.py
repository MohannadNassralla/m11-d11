"""YOUR self-tests for the toy-service instrumentation.

Per the drill guide, write at least 4 substantive test functions, each with at
least one `assert`. The autograder enforces the structure via AST
(`test_learner_self_test_exists_and_passes`).

Required coverage:
  1. After 3 calls to POST /echo and 2 calls to GET /sum, GET /metrics returns 200.
  2. The /metrics body contains the three metric names.
  3. The /metrics body contains a line for requests_total{path="/echo",status="200"} with value >= 3.
  4. Every non-/metrics response has an X-Request-ID response header that is non-empty.
"""

import re
import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_metrics_endpoint_returns_200_after_traffic():
    """GET /metrics returns 200 after 3 calls to /echo and 2 calls to /sum."""
    # Issue 3 calls to POST /echo
    for i in range(3):
        res = client.post("/echo", json={"message": f"traffic-{i}"})
        assert res.status_code == 200

    # Issue 2 calls to GET /sum
    for i in range(2):
        res = client.get("/sum", params={"a": i, "b": 10})
        assert res.status_code == 200

    # GET /metrics (Starlette routes mounted apps with a trailing slash)
    metrics_res = client.get("/metrics/")
    assert metrics_res.status_code == 200


def test_metrics_body_contains_three_metric_families():
    """The /metrics body contains requests_total, request_latency_seconds, inflight_requests."""
    metrics_res = client.get("/metrics/")
    body = metrics_res.text

    assert "requests_total" in body
    assert "request_latency_seconds" in body
    assert "inflight_requests" in body


def test_echo_counter_has_expected_value():
    """After 3 calls to /echo, requests_total{path="/echo",status="200"} >= 3."""
    # Ensure traffic is present
    for i in range(3):
        client.post("/echo", json={"message": "counter-check"})

    metrics_res = client.get("/metrics/")
    body = metrics_res.text

    # Match the standard Prometheus text exposition format for counters
    # e.g., requests_total_total{path="/echo",status="200"} 3.0
    pattern = r'requests_total_total\{path="/echo",status="200"\}\s+(\d+\.\d+)'
    match = re.search(pattern, body)
    
    assert match is not None, "Metric line matching echo and 200 status not found."
    
    value = float(match.group(1))
    assert value >= 3.0


def test_x_request_id_header_set_on_every_non_metrics_response():
    """Every non-/metrics response carries a non-empty X-Request-ID header."""
    # Check POST /echo
    res_echo = client.post("/echo", json={"message": "header test"})
    assert "X-Request-ID" in res_echo.headers
    assert res_echo.headers["X-Request-ID"] != ""

    # Check GET /sum
    res_sum = client.get("/sum", params={"a": 5, "b": 5})
    assert "X-Request-ID" in res_sum.headers
    assert res_sum.headers["X-Request-ID"] != ""