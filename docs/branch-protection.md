# Branch Protection and Mandatory Reviews

Recommended GitHub branch protection settings for `main`:

1. Require a pull request before merging.
2. Require at least one approval.
3. Dismiss stale approvals when new commits are pushed.
4. Require review from CODEOWNERS.
5. Require status checks to pass before merging.
6. Require branches to be up to date before merging.
7. Block force pushes.
8. Block branch deletion.
9. Restrict who can push to `main`.
10. Do not allow bypassing the above settings except for a small admin group.

## Why this matters in DevSecOps

Branch protection prevents unreviewed or unsafe changes from reaching production. Mandatory reviews create separation of duties. CODEOWNERS ensures that sensitive files such as CloudFormation templates, Kubernetes manifests, GitHub Actions workflows, and security configuration files receive review from the right people.
