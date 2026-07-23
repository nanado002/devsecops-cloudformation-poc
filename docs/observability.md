# Observability with Prometheus and Grafana

This project includes an observability layer so the DevSecOps pipeline covers security validation, deployment readiness, and runtime visibility after release.

## What is included

### Metrics endpoint

The Flask backend exposes a `/metrics` endpoint using the `prometheus-client` library. Pod annotations in the Kubernetes deployment manifest tell Prometheus which pods to scrape automatically:

```yaml
annotations:
  prometheus.io/scrape: true
  prometheus.io/path: /metrics
  prometheus.io/port: '5000'
```

### Prometheus

Prometheus is deployed alongside the application and scrapes the backend `/metrics` endpoint on a regular interval. No manual configuration is required — the scrape annotations are read automatically.

### Grafana

Grafana is provisioned with Prometheus as a data source and includes a starter dashboard tracking:

- Request count
- Request rate
- Request latency (p50, p95, p99)
- HTTP status code breakdown

### GitHub Actions smoke tests

The CI pipeline includes smoke tests that verify the observability stack starts correctly after deployment. These tests confirm that the `/metrics` endpoint, Prometheus, and Grafana are all reachable before the pipeline reports a successful run.

## Why observability matters in DevSecOps

DevSecOps does not stop at the deployment gate. Prometheus and Grafana provide runtime visibility after every release, enabling teams to detect:

- Elevated error rates from a newly deployed service
- Latency regressions introduced by a dependency update
- Abnormal traffic patterns that may indicate a security incident
- Service health degradation before it becomes an outage

Including observability in this pipeline demonstrates that security and reliability controls extend through the full software delivery lifecycle — from code commit to production runtime.
