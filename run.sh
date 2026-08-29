#!/usr/bin/env bash
set -e

# Change to project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PYTHON_BIN="/home/feras/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
PYTEST_BIN="/home/feras/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/pytest"

if [ ! -f "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
    PYTEST_BIN="pytest"
fi

echo "============================================================"
echo "  OLIST E-COMMERCE SALES & BI ANALYTICS PLATFORM"
echo "============================================================"
echo "Working directory: $(pwd)"
echo "Using Python: $PYTHON_BIN"
echo ""

case "$1" in
    test|tests)
        echo "Running automated test suite..."
        PYTHONPATH=. "$PYTEST_BIN" tests/ -v
        ;;
    metrics)
        echo "Displaying latest computed business metrics..."
        cat data/processed/business_metrics.json
        echo ""
        ;;
    *)
        echo "Executing ETL Pipeline & Analytics Star Schema Generation..."
        PYTHONPATH=. "$PYTHON_BIN" src/pipeline.py
        ;;
esac
