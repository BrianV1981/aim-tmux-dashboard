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
