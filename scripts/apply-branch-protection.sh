#!/usr/bin/env bash
set -euo pipefail

# Requires GitHub CLI authentication and admin rights on the repository.
# Usage: ./scripts/apply-branch-protection.sh OWNER REPO main

OWNER=${1:?Owner or organization required}
REPO=${2:?Repository name required}
BRANCH=${3:-main}

REQ_CHECKS='["Security Gates and Build"]'

gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  "/repos/${OWNER}/${REPO}/branches/${BRANCH}/protection" \
  -f required_status_checks.strict=true \
  -f required_status_checks.contexts="${REQ_CHECKS}" \
  -f enforce_admins=true \
  -f required_pull_request_reviews.dismiss_stale_reviews=true \
  -f required_pull_request_reviews.require_code_owner_reviews=true \
  -F required_pull_request_reviews.required_approving_review_count=1 \
  -f restrictions=null \
  -f allow_force_pushes=false \
  -f allow_deletions=false

echo "Branch protection requested for ${OWNER}/${REPO}:${BRANCH}."
