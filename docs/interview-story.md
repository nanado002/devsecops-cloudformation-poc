# Interview Story for This Project

## 60-second explanation

I built a CloudFormation-based DevSecOps proof of concept to demonstrate how I would secure a software delivery lifecycle from source code to deployment. The project includes repository security, Gitleaks secret scanning, branch protection guidance, mandatory reviews, CODEOWNERS, Dependabot, SAST, SCA, DAST, CloudFormation security scanning, Docker image scanning, Kubernetes RBAC, and NetworkPolicy.

Because your environment uses CloudFormation, I used CloudFormation to provision the AWS foundation instead of Terraform. The template creates encrypted artifact storage, ECR repositories with image scanning and immutable tags, a CloudWatch log group, and a GitHub Actions OIDC role to avoid long-lived AWS keys.

## STAR example

Situation: I wanted to show that DevSecOps is not just scanning at the end of deployment.

Task: I needed to design a complete PoC that covered repository controls, CI/CD security, IaC, containers, and Kubernetes.

Action: I built a three-tier style app with GitHub Actions security gates, CloudFormation scanning, Gitleaks, Bandit, Semgrep, pip-audit, Trivy, OWASP ZAP, Kubernetes RBAC, and NetworkPolicy.

Result: The project demonstrates how security can be shifted left and enforced continuously before changes reach production.

## Key phrase

> This project shows that I understand DevSecOps as a full lifecycle: secure source control, secure pipelines, secure infrastructure, secure containers, secure Kubernetes, and continuous validation.


## Observability addition

I also implemented Prometheus and Grafana to show operational readiness. The backend exposes Prometheus metrics, Prometheus scrapes the app, and Grafana displays request count, request rate, latency, and HTTP status codes. The CI workflow includes smoke tests to confirm the metrics endpoint, Prometheus, and Grafana are reachable. This helps show that the project covers not only shift-left security, but also runtime visibility after deployment.
