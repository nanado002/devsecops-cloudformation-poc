#!/usr/bin/env bash
set -euo pipefail

git config core.hooksPath .githooks
echo "Git hooks installed. Pre-commit hook will run before each commit."
echo "Recommended: install gitleaks locally for secret scanning."
