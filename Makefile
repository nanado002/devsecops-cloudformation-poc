.PHONY: help env test test-verbose security-local cfn-validate k8s-validate docker-build observability-local observability-down zap-local

help:
	@echo ""
	@echo "Usage: make <target>"
	@echo ""
	@echo "  env                  Copy .env.example to .env (edit before running compose)"
	@echo "  test                 Run test suite (requires SECRET_KEY env var or .env)"
	@echo "  test-verbose         Run test suite with verbose output"
	@echo "  security-local       Run Gitleaks, Bandit, pip-audit, Trivy, cfn-lint, Checkov locally"
	@echo "  cfn-validate         Lint and security-scan CloudFormation templates"
	@echo "  k8s-validate         Security-scan Kubernetes manifests with Checkov"
	@echo "  docker-build         Build frontend and backend images locally"
	@echo "  observability-local  Start the full stack (app + Prometheus + Grafana) via docker compose"
	@echo "  observability-down   Stop and clean up the local stack"
	@echo "  zap-local            Start stack and print ZAP command"
	@echo ""

# Copy example env file if .env does not already exist.
env:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo ".env created from .env.example — fill in real values before running docker compose."; \
	else \