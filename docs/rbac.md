# RBAC Notes

RBAC means Role-Based Access Control. In DevSecOps, RBAC applies to both source control and runtime platforms.

## GitHub RBAC

- Use least privilege.
- Give most contributors read or write access, not admin access.
- Restrict who can modify repository settings, secrets, branch protection, and workflows.
- Use teams instead of one-off user permissions.
- Require reviews before code merges to `main`.

## Kubernetes RBAC

This project uses:

- ServiceAccount: `app-service-account`
- Role: read-only access to ConfigMaps only
- RoleBinding: binds the app service account to the limited role
- Disabled service account token automounting

## Interview answer

> I treat the repository, CI/CD pipeline, and Kubernetes cluster as security boundaries. I use RBAC to enforce least privilege, branch protection to prevent unauthorized changes, CODEOWNERS to require review for sensitive files, and Kubernetes RoleBindings to limit what workloads can access inside the cluster.
