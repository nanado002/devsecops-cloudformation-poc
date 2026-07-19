# Threat Model Summary

Threat model created for a three-tier DevSecOps application.

## Assets

- Source code
- GitHub Actions workflows
- GitHub secrets and variables
- CloudFormation templates
- Container images
- ECR repositories
- Kubernetes manifests
- Application runtime

## Main threats

| Threat | Control |
|---|---|
| Secret committed to Git | `.gitignore`, pre-commit hook, Gitleaks local scan, Gitleaks CI scan |
| Unauthorized code change | Branch protection, mandatory reviews, CODEOWNERS, GitHub RBAC |
| Vulnerable dependency | Dependabot, pip-audit, SCA in CI |
| Insecure code pattern | Bandit and Semgrep SAST |
| Insecure CloudFormation | cfn-lint and Checkov IaC scan |
| Vulnerable container image | Trivy image scan, non-root Dockerfile |
| Over-permissive Kubernetes workload | RBAC, NetworkPolicy, non-root pods, read-only filesystem |
| Runtime web weakness | OWASP ZAP DAST baseline |
| Long-lived AWS credentials | GitHub Actions OIDC role |

## Why this matters

This threat model shows that DevSecOps is not one tool. It is a layered control system that starts before code is committed and continues through build, infrastructure, deployment, and runtime monitoring.
