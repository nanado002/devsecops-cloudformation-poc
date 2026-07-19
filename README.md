# DevSecOps CloudFormation Proof of Concept

A GitHub-ready proof-of-concept that demonstrates secure software delivery from repository controls through CI/CD, CloudFormation security scanning, container security, Kubernetes RBAC/NetworkPolicy, and application security testing.

This project is designed for a DevSecOps interview where the employer uses **AWS CloudFormation**. It intentionally focuses on CloudFormation instead of Terraform while still showing the same Infrastructure as Code security principles.

## What this project proves

| Area | What is included |
|---|---|
| Repository security | `.gitignore`, native Git pre-commit hook, Gitleaks, branch protection guidance, mandatory reviews, CODEOWNERS, Dependabot |
| Threat modeling | OWASP Threat Dragon model file and summary |
| CloudFormation / IaC security | Secure AWS foundation template (ECR, S3, OIDC, Secrets Manager), `cfn-lint`, Checkov scanning |
| Secrets management | AWS Secrets Manager resource, `.env.example` pattern, `SECRET_KEY` enforced at startup |
| Application security | Security response headers, structured JSON error handlers, input validation on all endpoints |
| Container security | Pinned base images, non-root containers, read-only filesystem, Trivy image scanning |
| Kubernetes security | Namespace, Deployment, Service, RBAC, ServiceAccount, RoleBinding, NetworkPolicy, Ingress + TLS (cert-manager) |
| AppSec testing | SAST with Bandit/Semgrep, SCA with pip-audit/Dependabot, DAST with OWASP ZAP baseline |
| CI/CD | GitHub Actions pipeline: security gates → DAST → EKS deploy on merge to main |
| Observability | Prometheus metrics endpoint (pinned v2.53.0), Grafana dashboard (pinned v11.1.0), CI smoke tests |
| Test suite | 25+ tests covering happy paths, input validation, security headers, metrics accuracy, error handlers |

## Architecture

```text
Developer
  -> Git pre-commit hook + Gitleaks
  -> GitHub Pull Request
  -> Branch Protection + Mandatory Review + CODEOWNERS
  -> GitHub Actions DevSecOps Pipeline
       - Secret scan
       - SAST
       - SCA
       - CloudFormation lint/security scan
       - Docker build
       - Trivy image scan
       - Kubernetes manifest scan
       - Optional DAST with OWASP ZAP
       - Observability smoke test for /metrics, Prometheus, and Grafana
  -> AWS CloudFormation deploys secure foundation
  -> Container image can be pushed to ECR
  -> Kubernetes manifests can deploy to EKS or local Kubernetes
```

## Repository structure

```text
.
├── app/
│   ├── backend/              # Python Flask API
│   └── frontend/             # Static frontend served by nginx
├── cloudformation/           # AWS CloudFormation templates
├── k8s/                      # Kubernetes manifests, RBAC, NetworkPolicy
├── monitoring/               # Prometheus and Grafana local observability config
├── .github/workflows/        # CI/CD pipelines
├── .githooks/                # Native Git pre-commit hook
├── .threatdragon/            # Threat Dragon threat model
├── scripts/                  # Helper scripts
├── docs/                     # Interview notes and security documentation
├── tests/                    # Basic tests
├── .gitleaks.toml            # Secret scanning rules
├── .gitignore
└── Makefile
```

## Quick start

### 1. Install local Git hooks

```bash
chmod +x scripts/install-git-hooks.sh
./scripts/install-git-hooks.sh
```

### 2. Configure environment variables

```bash
make env           # creates .env from .env.example
# Then edit .env and set SECRET_KEY and GF_ADMIN_PASSWORD to real values.
```

### 3. Run the app locally

```bash
make observability-local
```

Open:

- Frontend: http://localhost:8080
- Backend health endpoint: http://localhost:5000/health
- Backend metrics endpoint: http://localhost:5000/metrics
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (credentials from `.env`)

### 3. Run security checks locally

```bash
make security-local
```

### 4. Run CloudFormation validation

```bash
make cfn-validate
```

### 5. Run Kubernetes validation

```bash
make k8s-validate
```

## AWS CloudFormation deployment

The CloudFormation template creates a secure foundation for a DevSecOps pipeline:

- ECR repositories for frontend and backend images
- Encrypted S3 artifact bucket
- CloudWatch log group
- GitHub Actions OIDC role for short-lived AWS credentials
- Least-privilege IAM policy for CI/CD

Deploy with:

```bash
aws cloudformation deploy \
  --stack-name devsecops-poc-foundation \
  --template-file cloudformation/secure-app-foundation.yml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    ProjectName=devsecops-poc \
    GitHubOrg=YOUR_GITHUB_USERNAME_OR_ORG \
    GitHubRepo=YOUR_REPO_NAME \
    GitHubBranch=main
```

## GitHub repository settings to enable

After pushing the project to GitHub, configure the repository:

1. Require pull request before merging.
2. Require at least one approval.
3. Require CODEOWNERS review.
4. Require status checks to pass.
5. Block force pushes.
6. Restrict who can push to `main`.
7. Enable Dependabot alerts and security updates.
8. Store AWS deployment values as GitHub Actions variables/secrets if deploying to AWS.

See `docs/branch-protection.md` and `scripts/apply-branch-protection.sh`.

## Observability with Prometheus and Grafana

This project includes Prometheus and Grafana to prove runtime visibility. The backend exposes `/metrics`, Prometheus scrapes the backend, and Grafana is provisioned with a starter dashboard. The CI pipeline also verifies that the metrics endpoint, Prometheus, an