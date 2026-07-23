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

## RBAC Design Summary

This project applies RBAC at both the repository and Kubernetes layers. In GitHub, access controls support protected branches, required reviews, CODEOWNERS, and restricted workflow permissions. In Kubernetes, a dedicated ServiceAccount and RoleBinding limit workload permissions inside the cluster.

The goal is to enforce least privilege across the source control, CI/CD, and runtime layers.
