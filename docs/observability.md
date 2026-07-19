# Prometheus and Grafana Observability

This proof of concept includes an observability layer so the DevSecOps workflow covers build, security, deployment readiness, and runtime visibility.

## What was added

- A `/metrics` endpoint in the Flask backend using `prometheus-client`.
- Prometheus scraping the backend service every 15 seconds.
- Grafana provisioned with Prometheus as a data source.
- A starter Grafana dashboard for request count, request rate, p95 latency, and HTTP status codes.
- GitHub Actions smoke tests that verify the metrics endpoint, Prometheus, and Grafana start correctly.
- Kubernetes Prometheus scrape annotations on the backend Deployment.

## Local run

```bash
docker compose up -d --build
```

Open:

- Frontend: `http://localhost:8080`
- Backend health: `http://localhost:5000/health`
- Backend metrics: `http://localhost:5000/metrics`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3001`

Grafana local demo credentials:

```text
Username: admin
Password: admin
```

For a real environment, replace the demo password with a secret stored in AWS Secrets Manager or your CI/CD secret store.

## Why this matters in DevSecOps

Prometheus and Grafana show that the project does not only shift security left; it also supports runtime visibility after deployment. Metrics help teams detect performance problems, failed requests, and abnormal behavior early.

## Interview explanation

> I added Prometheus and Grafana to the project so the pipeline includes observability validation. The backend exposes a `/metrics` endpoint, Prometheus scrapes those metrics, and Grafana displays request count, request rate, latency, and status codes. In the pipeline, I added a smoke test to confirm the metrics endpoint, Prometheus, and Grafana are reachable. This shows that I think beyond deployment by including monitoring and operational readiness.
