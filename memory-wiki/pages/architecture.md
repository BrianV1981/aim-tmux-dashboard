# Core TUI Architecture

`aim-tmux-dashboard` (`aim-dash`) is a terminal user interface built on Python **Textual** and **Rich**.

> **Historical Note (Resolving Stale Docs):** Early handoff notes (`docs/HANDOFF_GAMEPLAN.md`) described `bin/aim-dash` as a pure Bash multiplexer script. Since v0.1.0, `bin/aim-dash` is a lightweight shell wrapper that activates the local Python `venv` and launches `bin/dashboard.py`.

## Component Map

### 1. Entrypoints (`bin/aim-dash` & `bin/dashboard.py`)
- **Standard Mode (`aim-dash`):** Launches `TmuxDashboard(popup_mode=False)`. When attaching outside `tmux`, it suspends the Textual app (`with self.suspend():`) and runs `tmux attach -t <target>`. When inside `tmux`, it executes `tmux switch-client -t <target>` and exits.
- **Popup Mode (`aim-dash --popup`):** Designed for `tmux display-popup` (bound to `F10` or `Prefix + m`). Attaching switches the active client and closes the popup overlay.
- **Token Grabber Mode (`aim-dash --grab`):** Launches `GrabApp`, bypassing the main dashboard to immediately open `TokenGrabberModal` against the active pane (`#{pane_id}`).

### 2. Backend Wrapper (`TmuxManager`)
`TmuxManager` encapsulates synchronous `subprocess` calls to the `tmux` binary:
- `get_hierarchy()`: Runs a single `tmux list-panes -a -F` query delimited by `@@@` capturing `session_name`, `session_attached`, `window_id`, `window_name`, `window_active`, `pane_id`, `pane_current_command`, `pane_active`, and `pane_current_path`.
- `capture_pane(name)`: Runs `tmux capture-pane -e -p -t <name>` (preserving ANSI escape sequences) and converts output via `rich.text.Text.from_ansi` for the live preview panel.
- `capture_pane_scrollback(name)`: Captures up to `-10000` lines of plain-text scrollback for regex token extraction.
- Session lifecycle helpers: `new_session`, `kill_session`, and `rename_session`.

### 3. Session Tree & Dynamic Flattening
- `TmuxDashboard.refresh_sessions()` populates `#session-tree`.
- **1:1:1 Flattening:** If a session has exactly 1 window and 1 pane, it renders as a single leaf node (`◆ <session> [<cmd>]`) to reduce visual nesting. Multi-window or multi-pane sessions expand into `□ <window>` and `❯ <pane>` child nodes.
- **Live Polling (`l`):** Toggles a 1.0-second interval timer (`self.set_interval(1.0, self.update_preview)`) to refresh the preview pane continuously.

### 4. Modals & Providers
- `TokenGrabberModal` (`t`): Extracts URLs (redacting `token=`, `key=`, `secret=` query values), IPv4 addresses, and 7–40 char hex hashes from scrollback, with live search filtering and clipboard copy.
- `NewSessionModal` (`n`), `RenameSessionModal` (`e`), `ConfirmKillModal` (`k`): Modal dialogs for session CRUD operations.
- `TmuxKeysScreen`: Slide-out right-hand cheat sheet panel triggered from the Command Palette (`Keys (TMUX)`).
- `LayoutCommandProvider`: Command Palette provider (`UI Layouts...`) supporting 4 orientations (`Side-by-Side Left/Right`, `Stacked Top/Bottom`) persisted alongside `pane_split_percent` (`[` / `]`) in `~/.aim_dashboard.json`.

## Related Pages
- [Session Persistence & Resurrection](session_persistence_and_resurrect.md)
- [AI Agent Integration & Fast Resume](ai_agent_integration.md)
- [Roadmap & Universal Project Launcher](roadmap_and_concepts.md)
- [Project Wiki Index](../index.md)
