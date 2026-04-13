#!/bin/bash
# Black Ops Framework Runner

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if virtual environment exists
if [ -d "$SCRIPT_DIR/venv" ]; then
    source "$SCRIPT_DIR/venv/bin/activate"
else
    echo "Virtual environment not found. Run install.sh first."
    exit 1
fi

# Run framework
cd "$SCRIPT_DIR"
python3 black_ops.py "$@"
