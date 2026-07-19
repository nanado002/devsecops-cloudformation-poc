import logging
import os
import time

from flask import Flask, Response, g, jsonify, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = Flask(__name__)

secret_key = os.environ.get("SECRET_KEY")
if not secret_key:
    raise RuntimeError(
        "SECRET_KEY environment variable is not set. "
        "Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
    )
app.config["SECRET_KEY"] = secret_key

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger(__name__)

HTTP_REQUESTS_TOTAL = Counter(
    "secure_app_http_requests_total",
    "Total HTTP requests handled by the secure DevSecOps PoC backend.",
    ["method", "endpoint", "http_status"],
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "secure_app_http_request_duration_seconds",
    "HTTP request latency in seconds for the secure DevSecOps PoC backend.",
    ["method", "endpoint"],
)


@app.before_request
def start_timer():
    g.start_time = time.perf_counter()


@app.after_request
def apply_security_headers(response):
    response.headers.set("X-Content-Type-Options", "nosniff")
    response.headers.set("X-Frame-Options", "DENY")
    response.headers.set("X-XSS-Protection", "1; mode=block")
    response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.set("Cache-Control", "no-store")
    return response


@app.after_request
def record_metrics(response):
    endpoint = request.endpoint or "unknown"
    if endpoint != "metrics":
        elapsed = time.perf_counter() - getattr(g, "start_time", time.perf_counter())
        HTTP_REQUESTS_TOTAL.labels(method=request.method, endpoint=endpoint, http_status=str(response.status_code)).inc()
        HTTP_REQUEST_DURATION_SECONDS.labels(method=request.method, endpoint=endpoint).observe(elapsed)
    return response


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "backend", "env": os.getenv("APP_ENV", "unknown")})


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.get("/api/message")
def message():
    return jsonify({
        "message": "Secure DevSecOps CloudFormation PoC is running.",
        "security_controls": ["SAST", "SCA", "DAST", "Gitleaks", "Trivy", "RBAC", "NetworkPolicy", "Prometheus", "Grafana"],
    })


@app.post("/api/echo")
def echo():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"error": "Request body must be valid JSON."}), 400
    if not isinstance(payload, dict):
        return jsonify({"error": "JSON body must be an object."}), 400
    if len(payload) > 20:
        return jsonify({"error": "Too many keys — maximum 20 allowed."}), 400
    safe_payload = {str(k)[:50]: str(v)[:200] for k, v in payload.items()}
    logger.info("echo called with %d key(s)", len(safe_payload))
    return jsonify({"received": safe_payload})


@app.errorhandler(400)
def bad_request(exc):
    return jsonify({"error": "Bad request.", "detail": str(exc)}), 400


@app.errorhandler(404)
def not_found(exc):
    return jsonify({"error": "Not found."}), 404


@app.errorhandler(405)
def method_not_allowed(exc):
    return jsonify({"error": "Method not allowed."}), 405


@app.errorhandler(500)
def internal_error(exc):
    logger.exception("Unhandled exception: %s", exc)
    return jsonify({"error": "Internal server error."}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
