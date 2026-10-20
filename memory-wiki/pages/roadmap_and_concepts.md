# Roadmap & Universal Project Launcher

Synthesized status of `docs/ROADMAP.md`, `docs/ROADMAP_v2.md`, `docs/UNIVERSAL_LAUNCHER_CONCEPT.md`, and repository hygiene milestones.

## 1. Completed Milestones (v0.1 – v0.2+)
- **Textual TUI & Tree Hierarchy:** Ported from the v0.0.1 Bash script to Python Textual with a collapsible session/window/pane `Tree` and 1:1:1 node flattening.
- **Live Preview & Layout Engine:** ANSI-aware pane preview (`capture-pane -e -p`), 1s live polling toggle (`l`), resizable split panes (`[` / `]`), and 4 structural layouts persisted in `~/.aim_dashboard.json`.
- **Popup Overlay & Token Grabber:** Added `--popup` mode (`F10`) and `--grab` / `t` `TokenGrabberModal` for scraping URLs, IPs, and Git hashes from scrollback.
- **Resurrect & Fast-Resume Reliability (Issues #37–#38):** Automated cold-boot `aim_restore_tmp` server startup before `tmux-resurrect` restore and added `Agent: Fast Resume (-c)` to the Command Palette.
- **Open-Source Readiness (Issues #39–#42):** Removed temporary patch scripts and nested clones, untrack/ignored `.vscode/mcp.json` and local symlinks (`aim-browser`), verified dynamic path resolution across `bin/aim-dash`, `install.sh`, and `bin/dashboard.py`, and overhauled `README.md`.

## 2. Open / Planned Roadmap Items (`docs/ROADMAP_v2.md`)
- **Tmux Control Mode (`tmux -C`) & Async Core (Phase 1):** Replace synchronous `subprocess.run` calls in `TmuxManager` with an `asyncio` stream attached to `tmux -C` for event-driven, zero-latency UI updates (relates to open Issue #36 on UI freezing during heavy operations).
- **Command Palette Submenus & Layout Polish:** Tracked under open Issues #21, #23, and #27.
- **Workspace Save/Restore Guardrails:** Tracked under open Issues #34, #35, and #36 (handling accidental overwrite of good saves with empty/fresh states and UI responsiveness during restore).
- **On-Hold Features:** Real-time Token & Cost Tracking (latency risk), Git/Worktree branch badges (latency risk), and Continuous 5-Minute Background Autosaves (redundant to `tmux-resurrect`).

## 3. Concept: Universal Project Launcher (`docs/UNIVERSAL_LAUNCHER_CONCEPT.md`)
Tracked in Git via Issue #39, this Phase 3/4 design turns `aim-dash` into a Spotlight/`sesh`-style launcher that treats **Active Tmux Sessions** (`[🟢 ACTIVE]`) and **Offline Local Git Repositories** (`[📁 OFFLINE]`) as unified fuzzy-searchable destinations:
- Selecting an `[🟢 ACTIVE]` entry attaches to the existing session.
- Selecting an `[📁 OFFLINE]` entry runs `tmux new-session -d -s <name> -c <repo_path>` and immediately attaches.
- **Candidate Discovery Strategies:** Explicit `~/.config/aim-dash/config.yaml` search paths, `zoxide`/shell-history frecency integration, or an async max-depth-2 `.git` directory scanner.

## Related Pages
- [Core TUI Architecture](architecture.md)
- [Session Persistence & Resurrection](session_persistence_and_resurrect.md)
- [AI Agent Integration & Fast Resume](ai_agent_integration.md)
- [Project Wiki Index](../index.md)
