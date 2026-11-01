# Changelog

## [v1.0.0] - 2026-10-31
### Added
- **Empty-Save Guardrail (`#47`):** Added `ConfirmSaveModal`, `TmuxManager.get_saved_resurrect_session_count()`, and `TmuxManager.should_warn_before_save()` to warn before overwriting a multi-session `tmux-resurrect` backup when `<= 1` (or `<= 50%` of previously saved) sessions are active.
- **Spotlight Git Project Launcher (`#48`):** Added `ProjectLauncherProvider` (`Project: Open Git Repo...` in `Ctrl+P` and hotkey `o`) and `TmuxManager.discover_git_repos()` to fuzzy-find `[ACTIVE]` and `[OFFLINE]` local Git repositories without cluttering the live session tree, automatically creating a `tmux` session in the repository directory when offline.
- **Multi-Window `[A.I.]` Badge Bubbling & Shell-Safe Fast Resume (`#49`):** Bubbled `[A.I.]` badges up to parent `◆ session` rows whenever any child window runs a known AI agent, and upgraded `Agent: Fast Resume (-c)` to reuse idle shell panes (`bash`/`zsh`/`sh`/`fish`) or wrap new windows in an interactive `bash` fallback so exiting an agent never destroys the window/session.
- **Automated Unit Test Suite & CI:** Added `tests/test_dashboard.py` (`12/12` unit tests) and wired GitHub Actions (`.github/workflows/test.yml`) to execute the full test suite on every push and PR.

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
