# Kubernetes Security Manifests

This folder demonstrates core Kubernetes security controls:

- Dedicated namespace
- Non-root containers
- Read-only root filesystem
- Dropped Linux capabilities
- Disabled service account token automounting
- RBAC with least privilege
- NetworkPolicy default deny and explicit allow
- Resource requests and limits
- Health probes

Deploy locally with kind/minikube after building images:

```bash
kubectl apply -f k8s/namespace.yml
kubectl apply -f k8s/serviceaccount-rbac.yml
kubectl apply -f k8s/backend-deployment.yml
kubectl apply -f k8s/frontend-deployment.yml
kubectl apply -f k8s/networkpolicy.yml
```
