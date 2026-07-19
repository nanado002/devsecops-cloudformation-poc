# Kubernetes Observability Option

For an EKS or local Kubernetes demo, use the Prometheus and Grafana community Helm chart instead of hand-writing all monitoring manifests.

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
kubectl create namespace monitoring
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set grafana.service.type=ClusterIP
```

The backend Deployment already includes Prometheus scrape annotations:

```yaml
prometheus.io/scrape: "true"
prometheus.io/path: "/metrics"
prometheus.io/port: "5000"
```

For a local view of Grafana:

```bash
kubectl -n monitoring port-forward svc/monitoring-grafana 3001:80
```

Then open `http://localhost:3001`.

Interview point: this shows that the DevSecOps pipeline does not stop at deployment. It also validates observability, making the app measurable after release.
