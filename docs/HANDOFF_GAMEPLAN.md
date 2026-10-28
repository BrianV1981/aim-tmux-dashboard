# AIM-Tmux-Dashboard: Historical v0.0.1 Bootstrap Spec (Archived)

> **⚠️ HISTORICAL ARCHIVE NOTE:** This document is the original `v0.0.1` bootstrap specification from when `aim-dash` began as a pure Bash multiplexer script. Since `v0.1.0`, `aim-dash` is a Python **Textual** TUI (`bin/dashboard.py` launched via `bin/aim-dash`). For current architecture and usage documentation, see [README.md](../README.md) and [memory-wiki/index.md](../memory-wiki/index.md).

---

## Overview (v0.0.1)
This repository contains `aim-dash`, the backend TUI sister-app to `aim-connect`. It began as a bash multiplexer dashboard allowing the Operator (and other AIM agents) to dynamically create, attach to, and destroy background `tmux` workspaces.

## Directory Structure
- `bin/aim-dash`: Wrapper script that activates `venv` and launches `bin/dashboard.py`.
- `bin/dashboard.py`: The core Python Textual TUI application.
- `install.sh`: Runs `scripts/setup.sh` and creates a global symlink so the Operator can type `aim-dash` from anywhere.
