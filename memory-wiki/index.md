# Project Wiki Index

Persistent knowledge base for **aim-tmux-dashboard** (`aim-dash`), a Python Textual TUI for orchestrating `tmux` workspaces, session persistence, and local AI coding agents.

## Core Concepts
- [AI Agent Integration & Fast Resume](pages/ai_agent_integration.md) — Process detection badges (`[A.I.]`), Command Palette fast-resume (`-c` / `--continue`), and native `tmux-resurrect` command translations for `agy`, `grok`, `codex`, and `opencode`.
- [Session Persistence & Resurrection](pages/session_persistence_and_resurrect.md) — How `aim-dash` delegates state snapshots to `tmux-resurrect`, the `aim_restore_tmp` dead-daemon bootstrap fix, and WSL/Windows Terminal startup behavior.

## Architecture
- [Core TUI Architecture](pages/architecture.md) — Structural breakdown of `bin/dashboard.py`, `TmuxManager`, Textual screens/modals, layout switching, live preview polling, and Token Grabber (`--grab`).

## Roadmap & Future Designs
- [Roadmap & Universal Project Launcher](pages/roadmap_and_concepts.md) — Evolution from v0.0.1 Bash prototype to v0.1+ Textual TUI, v2 Control Mode (`tmux -C`) plans, and the Spotlight-style Universal Project Launcher concept.

## Operations Log
- [Memory Log](log.md) — Chronological record of wiki bootstrap and session ingestion events.
