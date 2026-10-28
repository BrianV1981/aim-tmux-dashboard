# Roadmap & Universal Project Launcher

Synthesized status of `docs/ROADMAP_v2.md`, `docs/UNIVERSAL_LAUNCHER_CONCEPT.md`, and repository milestones through `v0.2.0` (Beta).

## 1. Completed Milestones (`v0.0.1` – `v0.2.0` Beta)
- **Textual TUI & Tree Hierarchy (`#10`):** Ported from the `v0.0.1` Bash script to Python Textual with a collapsible session/window/pane `Tree` and 1:1:1 node flattening.
- **Live Preview & Layout Engine (`#19`, `#21`, `#23`, `#27`):** ANSI-aware pane preview (`capture-pane -e -p`), 1s live polling toggle (`l`), resizable split panes (`[` / `]`), 4 structural layouts persisted in `~/.aim_dashboard.json`, nested Command Palette providers, and `TmuxKeysScreen` (`Keys (TMUX)`).
- **Popup Overlay & Token Grabber (`#11`, `#14`):** Added `--popup` mode (`F10`) and `--grab` / `t` `TokenGrabberModal` for scraping URLs (with query secret redaction), IPv4 addresses, and Git hashes from scrollback.
- **Resurrect, Fast-Resume & Full-Stack Service Recovery (`#34`–`#38`, `#44`, `#46`):** Automated cold-boot `aim_restore_tmp` server startup before `tmux-resurrect` restore, added `Agent: Fast Resume (-c)` to the Command Palette, fixed `@resurrect-processes` inline strategy quoting (`"~agy->agy -c"`), and verified full-stack auto-recovery of Python/FastAPI backends (`~python3`), Node/MCP SSE servers (`~node`), and Cloudflare tunnels (`~cloudflared`).
- **Open-Source Readiness & Hygiene (`#39`–`#43`, `#45`, `#50`):** Removed temporary patch scripts, sanitized paths, pruned stale remote branches, closed resolved legacy issues (`#21`–`#36`), and synchronized `README.md`, `CHANGELOG.md`, `docs/ROADMAP_v2.md`, and `memory-wiki/` with the live codebase.

## 2. Active Backlog (`v2.0` Track)
- **Issue `#47` — Empty-Save Guardrail:** Add a session-count check and confirmation modal in `TmuxDashboard.action_save_tmux_state()` before overwriting a multi-session `tmux-resurrect` snapshot when `<= 1` session is active.
- **Issue `#48` — Universal Project Launcher (`docs/UNIVERSAL_LAUNCHER_CONCEPT.md`):** Spotlight/`sesh`-style unified launcher that merges **Active Tmux Sessions** (`[🟢 ACTIVE]`) and **Offline Local Git Repositories** (`[📁 OFFLINE]`) so selecting an offline repo runs `tmux new-session -d -s <name> -c <repo_path>` and attaches immediately.
- **Issue `#49` — Tmux Control Mode (`tmux -C`) & Multi-Window AI Visibility (`docs/ROADMAP_v2.md`):**
  1. Replace synchronous `subprocess.run` calls in `TmuxManager` with an `asyncio` stream attached to `tmux -C` for event-driven updates.
  2. Bubble up `[A.I.]` badges to parent session rows even when 2+ windows exist, and ensure `Agent: Fast Resume (-c)` runs inside a persistent interactive shell or reuses an idle pane.
- **On-Hold Features:** Real-time Token & Cost Tracking (latency risk), Git/Worktree branch badges (latency risk), and Continuous 5-Minute Background Autosaves (redundant to `tmux-resurrect`).

## Related Pages
- [Core TUI Architecture](architecture.md)
- [Session Persistence & Resurrection](session_persistence_and_resurrect.md)
- [AI Agent Integration & Fast Resume](ai_agent_integration.md)
- [Project Wiki Index](../index.md)
