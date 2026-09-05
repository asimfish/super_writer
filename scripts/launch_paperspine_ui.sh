#!/usr/bin/env bash
# Run the compatible intake wizard in the user's current terminal.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [[ ! -t 0 ]]; then
    echo "Interactive stdin is required. Use intake_wizard.py --no-interactive with explicit options." >&2
    exit 2
fi
for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then
        exec "$candidate" "$SCRIPT_DIR/intake_wizard.py" --classic-input \
            --output-dir "${1:-paper_rewriting_output}"
    fi
done
echo "Python 3.10 or later is required." >&2
exit 1
