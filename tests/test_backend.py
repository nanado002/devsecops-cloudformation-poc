"""Backend test suite for the secure DevSecOps PoC."""
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path("/sessions/sleepy-ecstatic-allen/mnt/outputs/devsecops-cloudformation-poc/app/backend")))
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production")
from app import app
import pytest

@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

# Health
def test_health_returns_200(client):
    assert client.get("/health").status_code == 200

def test_health_body(client):
    data = client.get("/health").get_json()
    assert data["status"] == "ok"
    assert data["service"] == "backend"

# Message
def test_message_returns_200(client):
    assert client.get("/api/message").status_code == 200

def test_message_contains_security_controls(client):
    data = client.get("/api/message").get_json()
    assert "security_controls" in data
    assert isinstance(data["security_controls"], list)
    assert len(data["security_controls"]) > 0

def test_message_contains_message_field(client):
    assert "message" in client.get("/api/message").get_json()

# Echo - happy path
def test_echo_returns_200(client):
    assert client.post("/api/echo", json={"hello": "world"}).status_code == 200

def test_echo_reflects_payload(client):
    assert client.post("/api/echo", json={"key": "value"}).get_json()["received"]["key"] == "value"

def test_echo_sanitises_long_values(client):
    resp = client.post("/api/echo", json={"k": "x"*500})
    assert len(resp.get_json()["received"]["k"]) <= 200

def test_echo_sanitises_long_keys(client):
    key = list(client.post("/api/echo", json={"k"*100: "v"}).get_json()["received"].keys())[0]
    assert len(key) <= 50

def test_echo_empty_payload(client):
    resp = client.post("/api/echo", json={})
    assert resp.status_code == 200
    assert resp.get_json()["received"] == {}

# Echo - validation
def test_echo_non_json_returns_400(client):
    assert client.post("/api/echo", data="x", content_type="text/plain").status_code == 400

def test_echo_array_returns_400(client):
    resp = client.post("/api/echo", json=["a","b"])
    assert resp.status_code == 400
    assert "error" in resp.get_json()

def test_echo_too_many_keys_returns_400(client):
    resp = client.post("/api/echo", json={str(i): i for i in range(21)})
    assert resp.status_code == 400

# Metrics
def test_metrics_returns_200(client):
    assert client.get("/metrics").status_code == 200

def test_metrics_has_counter(client):
    client.get("/health")
    assert "secure_app_http_requests_total" in client.get("/metrics").data.decode()

def test_metrics_has_histogram(client):
    client.get("/health")
    assert "secure_app_http_request_duration_seconds" in client.get("/metrics").data.decode()

def test_metrics_counter_increments(client):
    def count():
        for line in client.get("/metrics").data.decode().splitlines():
            if 'secure_app_http_requests_total{' in line and 'health' in line and not line.startswith("#"):
                return float(line.split()[-1])
        return 0.0
    before = count()
    client.get("/health"); client.get("/health")
    assert count() >= before + 2

# Error handlers
def test_404_json(client):
    resp = client.get("/no-such-route")
    assert resp.status_code == 404
    assert "error" in resp.get_json()

def test_405_json(client):
    resp = client.post("/health")
    assert resp.status_code == 405
    assert "error" in resp.get_json()

# Security headers
HEADERS = [
    ("X-Content-Type-Options", "nosniff"),
    ("X-Frame-Options", "DENY"),
    ("X-XSS-Protection", "1; mode=block"),
    ("Referrer-Policy", "strict-origin-when-cross-origin"),
    ("Cache-Control", "no-store"),
]

@pytest.mark.parametrize("h,v", HEADERS)
def test_sec_header_health(client, h, v):
    assert client.get("/health").headers.get(h) == v

@pytest.mark.parametrize("h,v", HEADERS)
def test_sec_header_message(client, h, v):
    assert client.get("/api/message").headers.get(h) == v

@pytest.mark.parametrize("h,v", HEADERS)
def test_sec_header_echo(client, h, v):
    assert client.post("/api/echo", json={"x":"y"}).headers.get(h) == v
