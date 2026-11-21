# A.I.M. Tmux Dashboard - Roadmap (`v1.0.0` GA)

This document tracks the feature roadmap for `aim-tmux-dashboard` (`aim-dash`), covering shipped `v1.0.0` General Availability capabilities and evaluated architectural proposals that were intentionally rejected or deferred.

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

## ⏸️ Rejected & Deferred Architectural Ideas
*   ~~**Tmux Control Mode (`tmux -C`, `Issue #51`):**~~ *(Closed as YAGNI — Subprocess Backend Retained)* — Live host benchmarks across `16` active sessions and `20` panes measured `tmux list-panes -a` at `2.71 ms` and `tmux capture-pane -e -p` at `2.90 ms` (`< 0.3%` of one CPU core during 1s Live Preview polling). A persistent `tmux -C` stream would force Python to parse and discard an unfiltered `%output` byte firehose across all background AI agent panes, inflate `#{session_attached}` badges via its attached control client, and add cold-boot fragility against `tmux-resurrect` (`#37`) and the Empty-Save Guardrail (`#47`).
*   ~~**In-Memory Search Cache & 1s Tree-Rebuild Polling:**~~ *(Rejected as YAGNI — State & UI Regression Risk)* — Caching `get_hierarchy()` introduces stale-session bugs across `with self.suspend():` attach cycles for a negligible `2.71 ms` savings, while calling `refresh_sessions()` (`tree.clear()`) on the 1s Live Preview timer resets user expand/collapse state and scroll position every second.
*   ~~**Token & Cost Tracking:**~~ *(On Hold — Latency Risk)*
*   ~~**Git & Worktree Branch Badges:**~~ *(On Hold — Latency Risk)*
*   ~~**Continuous 5-Minute Background Autosaves:**~~ *(On Hold — Redundant to `tmux-resurrect`)*
*   **Visual Plugin Manager (`tpm`):** *(Deferred)*
