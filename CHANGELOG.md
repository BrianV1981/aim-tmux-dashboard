# Changelog

## [v0.2.0] - 2026-10-28
### Added
- **Workspace Persistence (`tmux-resurrect`):** Added Command Palette actions `Workspace: Save Tmux State` and `Workspace: Restore Tmux State`, including automatic cold-boot `aim_restore_tmp` server initialization when no `tmux` server is running (`#37`).
- **AI Agent Fast Resume (`-c`):** Added `Agent: Fast Resume (-c)` to the Command Palette to spawn resumed AI agent sessions directly in the active pane's working directory (`#38`).
- **Dynamic Layout Engine & Persistent Config:** Added `LayoutCommandProvider` (`UI Layouts...`) with 4 structural orientations (`Side-by-Side Left/Right`, `Stacked Top/Bottom`) and `[` / `]` split-pane resizing persisted to `~/.aim_dashboard.json` (`#19`, `#23`, `#27`).
- **Tmux Cheat Sheet Panel:** Added slide-out `TmuxKeysScreen` (`Keys (TMUX)`) accessible from the Command Palette.
- **Documentation & Memory Wiki:** Bootstrapped persistent `memory-wiki/` (`#43`), overhauled `README.md` for open-source release (`#39`–`#42`), documented `@resurrect-processes` inline strategy syntax (`#44`), and documented full-stack microservice, MCP server, and `cloudflared` tunnel auto-resurrection (`#46`, `#50`).

### Fixed
- Fixed UI layout wrapper and initial tree focus on mount (`#21`).
- Fixed Command Palette empty-query `ValueError` in nested providers (`#27`).
- Fixed non-popup exit behavior when switching sessions inside `tmux`.
- Fixed `@resurrect-processes` inline command-translation quoting (`"~agy->agy -c"`) to prevent shell redirection and duplicate command emission (`#44`).

## [v0.1.0] - 2026-07-12
### Added
- Textual UI for hierarchical session/window/pane tree (`#10`), live ANSI preview, and search filtering.
- Token Grabber (`--grab` and `t` hotkey) for scraping URLs, IPs, and Git hashes from scrollback (`#14`).
- `F10` popup overlay support (`--popup`, `#11`).
- `[A.I.]` process detection badges for AI CLI vessels (`#12`).
- Complete release hygiene (`requirements.txt`, `scripts/setup.sh`, updated `bin/aim-dash` wrapper, `#17`).

## [v0.0.1] - 2026-07-11
### Added
- Initial bash-based multiplexer menu prototype (`bin/aim-dash`).
