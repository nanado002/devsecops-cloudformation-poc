# Security Policy

Please do not commit secrets, credentials, private keys, or customer data to this repository.

Security checks include:

- Gitleaks for secret detection
- Bandit and Semgrep for SAST
- pip-audit and Dependabot for SCA
- Trivy for image and filesystem scanning
- Checkov and cfn-lint for IaC scanning
- OWASP ZAP for DAST baseline testing

This is a proof-of-concept project and should be reviewed before production use.
