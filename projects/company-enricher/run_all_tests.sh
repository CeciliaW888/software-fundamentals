#!/usr/bin/env bash
# Run every stage's tests. Each stage is a separate snapshot of the service.
set -euo pipefail
cd "$(dirname "$0")/stages"
for stage in */; do
  echo "== ${stage%/}"
  (cd "$stage" && python -m pytest -q)
done
