# Observability with Prometheus and Grafana

This project includes an observability layer so the DevSecOps pipeline covers security validation, deployment readiness, and runtime visibility after release.

Observability is included to show that secure delivery does not stop at the CI/CD gate. After an application is deployed, teams still need visibility into service health, latency, request patterns, and abnormal behavior.

## Metrics Endpoint

The Flask backend exposes a `/metrics` endpoint using the `prometheus-client` library. This endpoint provides application metrics that can be scraped by Prometheus.

Kubernetes scrape annotations are included on the backend deployment so Prometheus can discover and scrape the service automatically:

```yaml
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/path: "/metrics"
  prometheus.io/port: "5000"
```

## Prometheus

Prometheus is used to collect runtime metrics from the backend service. It scrapes the `/metrics` endpoint on a regular interval and stores time-series data for operational visibility.

This allows the project to track signals such as request volume, error behavior, service health, and latency trends after deployment.

## Grafana

Grafana is provisioned with Prometheus as a data source. The dashboard provides a starting point for visualizing application and service metrics, including:

- Request count
- Request rate
- Latency
- HTTP status code breakdown
- Service health indicators

Grafana helps turn raw metrics into dashboards that are easier for engineering and operations teams to review.

## CI/CD Smoke Tests

The GitHub Actions workflow includes smoke tests to verify that the observability stack starts correctly. These checks confirm that the backend metrics endpoint, Prometheus, and Grafana are reachable before the pipeline reports success.

This helps validate not only that the application can run, but also that the monitoring layer is available.

## Why Observability Matters in DevSecOps

DevSecOps is not only about shifting security left. It also includes runtime awareness after deployment.

Prometheus and Grafana help detect:

- Increased error rates after a release
- Latency regressions
- Failed requests
- Service health degradation
- Unusual traffic patterns that may indicate operational or security concerns

Including observability in this project shows that the pipeline supports secure delivery, deployment confidence, and operational readiness.
