# A.I.M. Tmux Dashboard - v2 Roadmap

This document tracks the feature roadmap for `aim-tmux-dashboard` (`aim-dash`), combining shipped `v0.1.0`–`v0.2.0` (Beta) capabilities with active v2.0 backlog issues.

---

## ✅ Shipped Capabilities (`v0.1.0` – `v0.2.0` Beta)

### Navigation & UX
*   [x] **Tree-Based Hierarchy (`#10`):** Collapsible Textual `Tree` widget (`session -> window -> pane`) with automatic 1:1:1 leaf flattening (`◆ session [cmd]`).
*   [x] **Popup Palette Mode (`#11`):** `--popup` CLI flag for `tmux display-popup` (Tmux 3.2+) floating overlay orchestration.
*   [x] **Dynamic Layout Engine & Resizing (`#19`, `#21`, `#23`):** 4 switchable orientations (`Side-by-Side Left/Right`, `Stacked Top/Bottom`) and `[` / `]` pane resizing persisted in `~/.aim_dashboard.json`.
*   [x] **Command Palette & Cheat Sheet (`#27`):** Nested `LayoutCommandProvider` submenu and slide-out `TmuxKeysScreen` (`Keys (TMUX)`).

### A.I. MLOps & Workspace Persistence
*   [x] **AI Agent Detection (`#12`):** Automatic inspection of `#{pane_current_command}` with high-visibility `[A.I.]` badges for `agy`, `grok`, `codex`, `opencode`, `claude`, `aider`, `gemini`, `gpt`, and `antigravity`.
*   [x] **Agent Fast Resume (`-c`) (`#38`):** Command Palette action to spawn a localized `<agent> -c` window in the selected pane's `#{pane_current_path}`.
*   [x] **Token Grabber (`#14`):** Extrakto-style scrollback scraper (`t` and `--grab`) for URLs (with token/key/secret redaction), IPv4 addresses, and Git commit hashes.
*   [x] **Cold-Boot Workspace & Microservice Resurrection (`#34`–`#37`, `#44`, `#46`):** Non-blocking `tmux-resurrect` save/restore integration with `aim_restore_tmp` dead-daemon bootstrap and `@resurrect-processes` auto-recovery for AI agents (`-c`), Python/FastAPI backends (`~python3`), Node/MCP servers (`~node`), and Cloudflare tunnels (`~cloudflared`).

---

## 🚀 Active Backlog (`v2.0` Track)

### 1. Empty-Save Guardrail (`Issue #47`)
*   [ ] **Low-Session Overwrite Protection:** Check active session count in `TmuxDashboard.action_save_tmux_state()` and prompt with a confirmation modal before overwriting a multi-session `tmux-resurrect` backup when `<= 1` session is running.

### 2. Universal Project Launcher (`Issue #48`)
*   [ ] **Offline Git Repository Discovery ([UNIVERSAL_LAUNCHER_CONCEPT.md](UNIVERSAL_LAUNCHER_CONCEPT.md)):** Asynchronously scan local project directories and merge `[🟢 ACTIVE]` `tmux` sessions with `[📁 OFFLINE]` Git repositories so selecting an offline repo creates and attaches to a session in one keystroke.

### 3. Control Mode (`tmux -C`) & Multi-Window Agent Visibility (`Issue #49`)
*   [ ] **Tmux Control Mode (`tmux -C`) & Async Core:** Replace synchronous `subprocess.run` polling in `TmuxManager` with an `asyncio` stream connected to `tmux -C` for event-driven updates.
*   [ ] **Multi-Window `[A.I.]` Badge Bubbling & Shell Persistence:** Surface `[A.I.]` badges on parent session rows even when 2+ windows exist, and ensure `Agent: Fast Resume (-c)` runs inside a persistent interactive shell or reuses an idle pane.

---

## ⏸️ Deferred / On-Hold Ideas
*   ~~**Token & Cost Tracking:**~~ *(On Hold — Latency Risk)*
*   ~~**Git & Worktree Branch Badges:**~~ *(On Hold — Latency Risk)*
*   ~~**Continuous 5-Minute Background Autosaves:**~~ *(On Hold — Redundant to `tmux-resurrect`)*
*   **Visual Plugin Manager (`tpm`):** *(Deferred to Future v3.0)*
