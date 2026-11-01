# Memory Log

Chronological, append-only record of knowledge ingestion into `memory-wiki/`.

## [2026-10-20] ingest | Bootstrap Wiki & Ingest Session Milestones (Issues #37–#42)
- Bootstrapped `memory-wiki/index.md`, `memory-wiki/log.md`, and `memory-wiki/pages/`.
- Created `pages/architecture.md` documenting `bin/dashboard.py`, `TmuxManager`, Textual modals, dynamic tree flattening, layout switching, and `GrabApp` (`--grab`). Resolved stale claims in `docs/HANDOFF_GAMEPLAN.md` that referred to `aim-dash` as a pure Bash script.
- Created `pages/session_persistence_and_resurrect.md` capturing the `tmux-resurrect` third-party dependency boundary, the cold-boot `aim_restore_tmp` dummy-session fix (Issue #37), the scrollback-flash diagnosis when restoring without `-c`, and the Windows Terminal session-restore race condition on WSL boot.
- Created `pages/ai_agent_integration.md` documenting AI binary badge detection, the Command Palette `Agent: Fast Resume (-c)` workflow (Issue #38), and `~/.tmux.conf` `@resurrect-processes` `-c` command translation rules.
- Created `pages/roadmap_and_concepts.md` synthesizing `docs/ROADMAP.md`, `docs/ROADMAP_v2.md`, and `docs/UNIVERSAL_LAUNCHER_CONCEPT.md` (Issue #39), plus open-source sanitization and README milestones (Issues #40–#42).

## [2026-10-20] ingest | Fix `@resurrect-processes` Inline Strategy Quoting & Tilde Bug (Issue #44)
- Updated `README.md`, `pages/ai_agent_integration.md`, and `pages/session_persistence_and_resurrect.md` to replace the broken `"~agy"->"~agy -c"` syntax with `"~agy->agy -c"`.
- Documented the 3 root causes in `tmux-resurrect`'s `process_restore_helpers.sh`: unquoted `>` file redirection during `eval set $(_restore_list)`, invalid tilde `~` on the right-hand execution command, and duplicate command emission when both `~agy` and `~agy.real` are listed.

## [2026-10-25] ingest | Document Full-Stack Service, MCP & Tunnel Auto-Resurrection (Issue #46)
- Empirically verified cold-boot workspace restoration across a full system reboot: `aim-dash` restored all `agy` CLI agent sessions (`-c`) and automatically restarted companion FastAPI backends (`~python3`), MCP SSE servers, and `cloudflared` edge tunnels (`~cloudflared`).
- Updated `README.md`, `pages/session_persistence_and_resurrect.md`, and `pages/ai_agent_integration.md` to document `~node ~python3 ~cloudflared` process resurrection alongside AI agent auto-resume.

## [2026-10-28] ingest | Synchronize All Documentation with Live v0.2.0 Codebase (Issue #50)
- Updated `README.md` with all 12 keyboard shortcuts from `TmuxDashboard.BINDINGS`, all 5 Command Palette actions from `get_system_commands()`, and all 3 CLI execution modes (`aim-dash`, `--popup`, `--grab`).
- Updated `CHANGELOG.md` and `VERSION` to `v0.2.0` covering all shipped milestones through Issue #50.
- Updated `docs/ROADMAP_v2.md`, `docs/HANDOFF_GAMEPLAN.md`, and `pages/roadmap_and_concepts.md` to mark shipped features as completed, reflect the closure of stale issues (#21–#36, #45), and link active v2 backlog tickets (#47, #48, #49).

## [2026-10-31] ingest | Ship v1.0.0 General Availability (Issues #47, #48, #49 & Spin Out #51)
- **Issue #47 (Empty-Save Guardrail):** Added `ConfirmSaveModal`, `TmuxManager.get_saved_resurrect_session_count()`, and `TmuxManager.should_warn_before_save()` to prevent accidental cold-boot overwrites of multi-session `tmux-resurrect` backups.
- **Issue #48 (Command Palette Git Project Launcher):** Added `ProjectLauncherProvider` (`Project: Open Git Repo...` in `Ctrl+P` and hotkey `o`) and `TmuxManager.discover_git_repos()` to launch offline local Git repositories without cluttering `#session-tree`.
- **Issue #49 (Multi-Window AI Visibility & Shell-Safe Fast Resume):** Added `TmuxManager.session_has_ai_agent()` to bubble `[A.I.]` badges up to multi-window parent rows and `TmuxManager.fast_resume_agent()` to reuse idle shells or wrap new windows in `bash -ic '<agent> -c; exec bash'`. Spun out the `v2.0` `tmux -C` engine rewrite to Issue #51.
- Added `tests/test_dashboard.py` (`12/12` unit tests), wired `.github/workflows/test.yml`, and bumped `VERSION` and `CHANGELOG.md` to `v1.0.0`.
