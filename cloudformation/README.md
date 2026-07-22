# CloudFormation Templates

`secure-app-foundation.yml` provisions a secure AWS foundation for this DevSecOps PoC.

Security controls demonstrated:

- S3 server-side encryption
- S3 public access block
- S3 HTTPS-only bucket policy
- S3 versioning
- ECR image scanning on push
- ECR immutable tags
- ECR lifecycle policy
- GitHub Actions OIDC role instead of long-lived AWS keys
- Least-privilege IAM policy for CI/CD
- CloudWatch log retention

