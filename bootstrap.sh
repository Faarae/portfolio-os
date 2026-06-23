#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Task runner script for Unix-like systems (Linux/macOS)
# Checks virtualenv and delegates to Makefile

VENV_DIR=".venv"
VENV_BIN="$VENV_DIR/bin"

if [ -d "$VENV_BIN" ]; then
    export PATH="$PWD/$VENV_BIN:$PATH"
fi

ACTION=${1:-"run"}
shift || true
ARGS="$@"

case "$ACTION" in
    install)
        make install
        ;;
    format)
        make format
        ;;
    lint)
        make lint
        ;;
    test)
        make test
        ;;
    run)
        make run ARGS="$ARGS"
        ;;
    *)
        echo "Usage: ./bootstrap.sh {install|format|lint|test|run} [arguments]"
        exit 1
        ;;
esac
