# DevSecOps CloudFormation Proof of Concept

A working demonstration of a secure, automated CI/CD pipeline — from developer commit to production deployment on AWS EKS — built with GitHub Actions, CloudFormation, Docker, and Kubernetes.

![DevSecOps CloudFormation Pipeline](docs/devsecops_pipeline_diagram.png)

---

## Table of Contents

- [Project Overview](#project-overview)
- [Pipeline Diagram](#pipeline-diagram)
- [Pipeline Overview](#pipeline-overview)
- [Security Controls Demonstrated](#security-controls-demonstrated)
- [AWS Architecture](#aws-architecture)
- [Kubernetes Security](#kubernetes-security)
- [Observability with Prometheus and Grafana](#observability-with-prometheus-and-grafana)
- [Local Development](#local-development)
- [Security Scanning Commands](#security-scanning-commands)
- [GitHub Actions Pipeline](#github-actions-pipeline)
- [Interview Talking Points](#interview-talking-points)
- [Important Notes](#important-notes)

---

## Project Overview

This project demonstrates a complete DevSecOps pipeline for a containerised, cloud-native web application. Security is embedded at every stage of the software delivery lifecycle — from the developer workstation through automated CI/CD gates to a hardened Kubernetes deployment on AWS.

The application is a three-tier web service: an nginx frontend, a Python/Flask backend, and an observability stack using Prometheus and Grafana. The infrastructure and pipeline are the focus of this project, not the application itself.

**CloudFormation was chosen deliberately** because it is the infrastructure-as-code tool used in the target environment. This project demonstrates the ability to work with CloudFormation alongside modern DevSecOps tooling.

**GitHub Actions OIDC** is used instead of long-lived AWS access keys. The workflow exchanges a short-lived GitHub token for temporary AWS credentials, meaning no AWS secrets are stored in GitHub.

**Key technologies:** GitHub Actions · AWS EKS · AWS CloudFormation · Amazon ECR · AWS Secrets Manager · Docker · Kubernetes · Prometheus · Grafana · Gitleaks · Trivy · Semgrep · Checkov · OWASP ZAP

---

## Pipeline Diagram

> Place your pipeline diagram image at `docs/devsecops_pipeline_diagram.png` to display it here.

![DevSecOps CloudFormation Pipeline](docs/devsecops_pipeline_diagram.png)

---

## Pipeline Overview

Every push to `main` triggers the following automated security gates in sequence:

```
Developer Workstation
  └── .gitignore                        Prevent secrets from being staged
  └── Pre-commit hook                   Block commits with secrets or lint errors
  └── Gitleaks (local)                  Scan staged files for secrets before commit

GitHub Pull Request / Push
  └── Gitleaks (GitHub Actions)         Full repo and history secret scan
  └── pytest                            Unit tests must pass before scans proceed
  └── Bandit                            Python SAST — static analysis for security bugs
  └── pip-audit                         SCA — Python dependency CVE scanning
  └── Semgrep                           Multi-language SAST with security rulesets
  └── cfn-lint                          CloudFormation template validation
  └── Checkov                           IaC and Kubernetes manifest policy scanning
  └── Docker build (backend + frontend) Build hardened, minimal container images
  └── Trivy                             Container image CVE scan — blocks CRITICAL/HIGH
  └── OWASP ZAP (PR only)              DAST baseline scan against the running application

On Push to main (CD Gate)
  └── GitHub Actions OIDC               Authenticate to AWS — no long-lived keys stored
  └── Amazon ECR                        Push scanned, tagged images to private registry
  └── AWS CloudFormation                Provision and update infrastructure declaratively
  └── AWS Secrets Manager               Inject secrets at runtime — never in code
  └── Amazon EKS                        Deploy with RBAC, NetworkPolicy, and Ingress
  └── Prometheus + Grafana              Observability — metrics scraping and dashboards
```

No stage proceeds if an earlier gate fails. The deploy job never runs on pull requests.

---

## Security Controls Demonstrated

| Tool / Control | Category | Purpose |
|---|---|---|
| `.gitignore` | Secrets hygiene | Prevent `.env` files, keys, and credentials from being staged |
| Pre-commit hook | Shift-left | Block commits containing secrets before they reach the remote |
| Gitleaks (local + CI) | Secret scanning | Detect secrets in staged files and full repository history |
| Branch protection rules | Access control | Require passing CI checks and reviewer approval before merge to `main` |
| CODEOWNERS | Access control | Enforce designated reviewers per file or directory |
| Dependabot | Supply chain | Automated PRs for outdated Actions, Python packages, and Docker base images |
| RBAC (GitHub Actions) | Access control | Minimal workflow permissions — `contents: read`, `id-token: write` only where required |
| Mandatory reviews | Process control | Pull requests require human approval before merge |
| pytest | Testing | Unit tests run first — no security scan proceeds on a broken build |
| Bandit | SAST | Python-specific static analysis for common security vulnerabilities |
| Semgrep | SAST | Multi-language static analysis with OWASP and security-focused rulesets |
| pip-audit | SCA | CVE scanning of Python dependencies against OSV and PyPI advisories |
| cfn-lint | IaC validation | CloudFormation template syntax and AWS best-practice checks |
| Checkov | IaC / policy scan | Policy-as-code checks for CloudFormation, Kubernetes manifests, and Dockerfiles |
| Docker build | Container | Reproducible, minimal images built with non-root users |
| Trivy | Image scanning | CVE scan of built images — pipeline fails on   │ Backend  │  │Prometheus│  │    │
│  │  │  (nginx) │  │ (Flask)  │  │+ Grafana │  │    │
│  │  └──────────┘  └──────────┘  └──────────┘  │    │
│  │    NetworkPolicy · RBAC · Non-root pods     │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

**CloudFormation** provisions the VPC, IAM roles, ECR repositories, S3 bucket, and the GitHub Actions OIDC provider as auditable, version-controlled infrastructure. CloudFormation was chosen because it is the standard IaC tool in the target environment.

**GitHub Actions OIDC** eliminates long-lived AWS credentials. The workflow uses `aws-actions/configure-aws-credentials` to exchange a short-lived GitHub token for temporary AWS credentials scoped to only the permissions needed for deployment.

**AWS Secrets Manager** stores application secrets. The EKS deployment injects them at runtime via Kubernetes Secrets, keeping them out of source code, Docker images, and environment files.

---

## Kubernetes Security

The EKS deployment applies multiple layers of Kubernetes-native security controls:

**RBAC** — A dedicated `ServiceAccount` is bound to a minimal `Role` granting only the permissions the application needs. The default service account token is disabled (`automountServiceAccountToken: false`).

**NetworkPolicy** — A default-deny policy blocks all ingress and egress by default. Explicit allow rules permit only the required traffic paths: frontend → backend, and Prometheus → backend scrape endpoint.

**Pod Security Context** — Every pod runs with:
- `runAsNonRoot: true` with an explicit numeric `runAsUser`
- `readOnlyRootFilesystem: true` — writable paths use `emptyDir` volumes
- `allowPrivilegeEscalation: false`
- All Linux capabilities dropped: `capabilities.drop: ["ALL"]`
- `seccompProfile: RuntimeDefault`

**Ingress** — Traffic enters through a Kubernetes Ingress resource, centralising routing and enabling TLS termination without exposing services directly.

---

## Observability with Prometheus and Grafana

Prometheus and Grafana provide runtime visibility after every deployment — security does not stop at the pipeline gate.

**Prometheus** scrapes application metrics from the backend `/metrics` endpoint, exposed via `prometheus_flask_exporter`. Pod annotations (`prometheus.io/scrape`, `prometheus.io/path`, `prometheus.io/port`) tell Prometheus which pods to scrape automatically without manual configuration.

**Grafana** connects to Prometheus as a data source and provides dashboards for request rate, error rate, and latency. Grafana credentials are injected from environment variables at runtime — never hardcoded.

Metrics are visible immediately after deployment, enabling detection of anomalous behaviour and performance regressions alongside security events.

To access locally:
```bash
docker compose up -d
# Prometheus: http://localhost:9090
# Grafana:    http://localhost:3001  (credentials from .env)
```

---

## Local Development

**Prerequisites:** Docker, Docker Compose, Python 3.12+

```bash
# Clone the repository
git clone https://github.com/nanado002/devsecops-cloudformation-poc.git
cd devsecops-cloudformation-poc

# Set up environment variables
cp .env.example .env
# Edit .env and fill in required values

# Build and start all services
docker compose up --build

# Run backend unit tests
pip install -r app/backend/requirements.txt pytest
pytest tests/ -v

# Tear down all containers and volumes
docker compose down -v
```

| Service | Local URL |
|---|---|
| Frontend (nginx) | http://localhost:8080 |
| Backend (Flask) | http://localhost:5000 |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3001 |

---

## Security Scanning Commands

These reproduce what the CI pipeline runs automatically:

```bash
# Secret scanning — full repository history
gitleaks detect --source . --redact --no-git

# Python SAST
bandit -r app/backend -ll

# Python dependency CVE scan
pip-audit -r app/backend/requirements.txt

# Multi-language SAST
semgrep --config p/python --config p/docker --config p/github-actions .

# CloudFormation lint
cfn-lint cloudformation/*.yml

# IaC and Kubernetes policy scan
checkov -d . --quiet

# Container image CVE scan
docker build -t devsecops-poc-backend:local app/backend
trivy image --severity CRITICAL,HIGH --ignore-unfixed devsecops-poc-backend:local

# DAST baseline scan (requires running application)
docker compose up -d
docker run --network host \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t http://localhost:8080
```

---

## GitHub Actions Pipeline

The workflow (`.github/workflows/ci-devsecops.yml`) runs three parallel-eligible jobs with strict dependency ordering:

**Security Gates and Build** — runs on every push and pull request
Gitleaks secret scan → pytest unit tests → Bandit SAST → pip-audit SCA → Semgrep SAST → cfn-lint → Checkov → Docker build (backend + frontend) → Trivy image scan

**DAST Baseline** — runs on pull requests only
Spins up the full application stack via Docker Compose → waits for all services to pass health checks → runs OWASP ZAP baseline scan → tears down

**Deploy to EKS** — runs on push to `main` only, after Security Gates passes
Authenticates to AWS via GitHub Actions OIDC → pushes images to Amazon ECR → updates kubeconfig → creates Kubernetes Secrets from AWS Secrets Manager values → applies namespace, RBAC, NetworkPolicy, and Deployment manifests → waits for rollout to complete → reports pod status

The deploy job never runs on pull requests. No stage proceeds if an earlier gate fails.

---

## Interview Talking Points

- **Shift-left security:** Pre-commit hooks and local Gitleaks scanning catch issues at the cheapest point — before code ever leaves the developer's machine.

- **No long-lived credentials:** GitHub Actions authenticates to AWS using OIDC (`AssumeRoleWithWebIdentity`). There are no AWS access keys stored anywhere — only an IAM role ARN in a non-secret variable.

- **Defense in depth:** Security is layered across the developer environment, CI pipeline, container build stage, infrastructure provisioning, and Kubernetes runtime — not bolted on at a single point.

- **Policy as code:** Checkov encodes Kubernetes and CloudFormation security policies as version-controlled checks. Compliance is automated, auditable, and enforced on every PR.

- **Immutable infrastructure:** CloudFormation manages all AWS resources declaratively. Infrastructure changes go through the same PR review and CI gate as application code.

- **Least privilege everywhere:** IAM roles, Kubernetes RBAC, pod security contexts, and NetworkPolicies all enforce the principle of least privilege — each component has only the permissions it actually needs.

- **Secrets never touch code:** Secrets flow from AWS Secrets Manager → Kubernetes Secret → container environment variable at runtime. They never appear in source code, Docker images, or CI logs.

- **Observability from day one:** Prometheus and Grafana are deployed alongside the application, not added later. This enables detection of anomalous runtime behaviour immediately after every deployment.

- **Supply chain security:** Dependabot monitors GitHub Actions, Python packages, and Docker base images for CVEs and opens automated pull requests to keep the dependency graph current.

- **DAST in the pipeline:** OWASP ZAP runs a baseline scan against the live application on every pull request, catching runtime vulnerabilities that static analysis cannot detect.

- **CloudFormation alignment:** The project deliberately uses CloudFormation rather than Terraform to match the tooling used in the target environment, demonstrating the ability to apply DevSecOps practices within an existing stack rather than replacing it.

---

## Important Notes

This is a **proof-of-concept and learning project**. It demonstrates DevSecOps tooling, pipeline design, and security engineering patterns in a controlled environment.

Before using any part of this project in production:

- Review and tighten all IAM policies to least-privilege for your specific workload
- Replace the OWASP ZAP baseline scan with a full active scan and remediate findings
- Evaluate all Checkov skip-checks against your organisation's security policy
- Implement secret rotation schedules in AWS Secrets Manager
- Add TLS termination at the Ingress layer
- Enable EKS audit logging and CloudTrail for all API events
- Review the CloudFormation stack against your organisation's compliance standards

This project was built for educational and portfolio purposes. Co