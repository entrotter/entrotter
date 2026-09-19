#!/usr/bin/env bash
set -euo pipefail
WORKSPACE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
for repo in engine sdk-python cli scenarios entrotter.github.io; do
  if [[ ! -d "$WORKSPACE/$repo" ]]; then
    git clone "https://github.com/entrotter/$repo.git" "$WORKSPACE/$repo"
  fi
done
python3 -m venv "$WORKSPACE/.venv"
# Install sibling source packages explicitly; never resolve unpublished Entrotter names from PyPI.
"$WORKSPACE/.venv/bin/python" -m pip install --no-deps -e "$WORKSPACE/engine" -e "$WORKSPACE/sdk-python" -e "$WORKSPACE/cli"
printf '\nActivate with: source "%s/.venv/bin/activate"\n' "$WORKSPACE"
printf 'Then run: entrotter doctor\n'
