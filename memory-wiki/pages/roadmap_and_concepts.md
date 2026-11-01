# Roadmap & Universal Project Launcher

Synthesized status of `docs/ROADMAP_v2.md`, `docs/UNIVERSAL_LAUNCHER_CONCEPT.md`, and repository milestones through `v1.0.0` General Availability.

## 1. Completed Milestones (`v0.0.1` – `v1.0.0` GA)
- **Textual TUI & Tree Hierarchy (`#10`, `#49`):** Ported from the `v0.0.1` Bash script to Python Textual with a collapsible session/window/pane `Tree`, 1:1:1 node flattening, and parent-row `[A.I.]` badge bubbling on multi-window sessions.
- **Spotlight Git Project Launcher (`#39`, `#48`):** Implemented `ProjectLauncherProvider` (`Project: Open Git Repo...` in `Ctrl+P` and hotkey `o`) and `TmuxManager.discover_git_repos()` to fuzzy-search `[ACTIVE]` and `[OFFLINE]` local Git repositories without cluttering `#session-tree`, creating and attaching to offline repos in one keystroke.
- **Live Preview & Layout Engine (`#19`, `#21`, `#23`, `#27`):** ANSI-aware pane preview (`capture-pane -e -p`), 1s live polling toggle (`l`), resizable split panes (`[` / `]`), 4 structural layouts persisted in `~/.aim_dashboard.json`, nested Command Palette providers, and `TmuxKeysScreen` (`Keys (TMUX)`).
- **Popup Overlay & Token Grabber (`#11`, `#14`):** Added `--popup` mode (`F10`) and `--grab` / `t` `TokenGrabberModal` for scraping URLs (with query secret redaction), IPv4 addresses, and Git hashes from scrollback.
- **Resurrect, Empty-Save Guardrail & Shell-Safe Fast Resume (`#34`–`#38`, `#44`, `#46`, `#47`, `#49`):** Automated cold-boot `aim_restore_tmp` server startup, added `ConfirmSaveModal` overwrite protection, upgraded `Agent: Fast Resume (-c)` to reuse idle shell panes or wrap new windows in an interactive `bash` fallback, and verified full-stack auto-recovery of AI agents (`-c`), Python/FastAPI backends (`~python3`), Node/MCP SSE servers (`~node`), and Cloudflare tunnels (`~cloudflared`).
- **Automated Test Suite & Release Hygiene (`#40`–`#43`, `#45`, `#50`):** Added `tests/test_dashboard.py` (`12/12` unit tests wired into GitHub Actions CI), sanitized paths, pruned stale remote branches, and synchronized all documentation for `v1.0.0` GA.

## 2. Future Backlog (`v2.0` Track)
- **Issue `#51` — Tmux Control Mode (`tmux -C`) & Async Core (`docs/ROADMAP_v2.md`):** Replace synchronous `subprocess.run` calls in `TmuxManager` with an `asyncio` stream attached to `tmux -C` for zero-polling event-driven updates.
- **On-Hold Features:** Real-time Token & Cost Tracking (latency risk), Git/Worktree branch badges (latency risk), and Continuous 5-Minute Background Autosaves (redundant to `tmux-resurrect`).

## Related Pages
- [Core TUI Architecture](architecture.md)
- [Session Persistence & Resurrection](session_persistence_and_resurrect.md)
- [AI Agent Integration & Fast Resume](ai_agent_integration.md)
- [Project Wiki Index](../index.md)
