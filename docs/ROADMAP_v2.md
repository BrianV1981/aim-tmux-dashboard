# A.I.M. Tmux Dashboard - Roadmap (`v1.0.0` GA & `v2.0` Track)

This document tracks the feature roadmap for `aim-tmux-dashboard` (`aim-dash`), covering shipped `v1.0.0` General Availability capabilities and future `v2.0` architectural upgrades.

---

## ✅ Shipped Capabilities (`v0.1.0` – `v1.0.0` GA)

### Navigation, Project Discovery & UX
*   [x] **Tree-Based Hierarchy (`#10`, `#49`):** Collapsible Textual `Tree` widget (`session -> window -> pane`) with automatic 1:1:1 leaf flattening (`◆ session [cmd]`) and parent-level `[A.I.]` badge bubbling on multi-window sessions.
*   [x] **Spotlight Git Project Launcher (`#48`):** Command Palette (`Project: Open Git Repo...`) and hotkey `o` fuzzy-finder scanning local Git repositories (`[ACTIVE]` and `[OFFLINE]`) without cluttering the live session tree.
*   [x] **Popup Palette Mode (`#11`):** `--popup` CLI flag for `tmux display-popup` (Tmux 3.2+) floating overlay orchestration.
*   [x] **Dynamic Layout Engine & Resizing (`#19`, `#21`, `#23`):** 4 switchable orientations (`Side-by-Side Left/Right`, `Stacked Top/Bottom`) and `[` / `]` pane resizing persisted in `~/.aim_dashboard.json`.
*   [x] **Command Palette & Cheat Sheet (`#27`):** Nested `LayoutCommandProvider` & `ProjectLauncherProvider` submenus and slide-out `TmuxKeysScreen` (`Keys (TMUX)`).

### A.I. MLOps & Workspace Persistence
*   [x] **AI Agent Detection (`#12`):** Automatic inspection of `#{pane_current_command}` with high-visibility `[A.I.]` badges for `agy`, `grok`, `codex`, `opencode`, `claude`, `aider`, `gemini`, `gpt`, and `antigravity`.
*   [x] **Shell-Safe Agent Fast Resume (`-c`) (`#38`, `#49`):** Reuses idle shell panes (`bash`/`zsh`/`sh`/`fish`) or spawns an interactive shell-wrapped window (`bash -ic '<agent> -c; exec bash'`) in the selected pane's `#{pane_current_path}`.
*   [x] **Token Grabber (`#14`):** Extrakto-style scrollback scraper (`t` and `--grab`) for URLs (with token/key/secret redaction), IPv4 addresses, and Git commit hashes.
*   [x] **Cold-Boot Resurrection & Empty-Save Guardrail (`#34`–`#37`, `#44`, `#46`, `#47`):** Non-blocking `tmux-resurrect` save/restore integration with `aim_restore_tmp` dead-daemon bootstrap, `ConfirmSaveModal` overwrite protection, and `@resurrect-processes` auto-recovery for AI agents (`-c`), Python/FastAPI backends (`~python3`), Node/MCP servers (`~node`), and Cloudflare tunnels (`~cloudflared`).

---

## 🚀 Future Backlog (`v2.0` Track)

### 1. Control Mode (`tmux -C`) & Async Core (`Issue #51`)
*   [ ] **Tmux Control Mode (`tmux -C`):** Replace synchronous `subprocess.run` polling in `TmuxManager` with an `asyncio` stream connected to `tmux -C` for zero-polling event-driven UI updates.

---

## ⏸️ Deferred / On-Hold Ideas
*   ~~**Token & Cost Tracking:**~~ *(On Hold — Latency Risk)*
*   ~~**Git & Worktree Branch Badges:**~~ *(On Hold — Latency Risk)*
*   ~~**Continuous 5-Minute Background Autosaves:**~~ *(On Hold — Redundant to `tmux-resurrect`)*
*   **Visual Plugin Manager (`tpm`):** *(Deferred to Future v3.0)*
