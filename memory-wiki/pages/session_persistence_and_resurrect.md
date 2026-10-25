# Session Persistence & Resurrection

`aim-tmux-dashboard` does not implement a custom state-serialization engine in Python. Instead, it acts as a remote control for **[tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect)** (`~/.tmux/plugins/tmux-resurrect/scripts/save.sh` and `restore.sh`).

## 1. Third-Party Dependency Boundary (Issues #40–#41)
- The Command Palette actions **Workspace: Save Tmux State** and **Workspace: Restore Tmux State** require `tmux-resurrect` to be installed in `~/.tmux/plugins/tmux-resurrect/`.
- If the scripts are missing, `TmuxDashboard` surfaces an error toast: `"tmux-resurrect not found in ~/.tmux/plugins/"`.

## 2. Cold-Boot Dead Daemon Bug & Fix (Issue #37)
### Symptom
After a system reboot or WSL restart, launching `aim-dash` and triggering **Workspace: Restore Tmux State** silently failed to load any saved sessions unless the user manually created a new session (`n`) first and then ran Restore a second time.

### Root Cause
`action_restore_tmux_state` previously executed:
```python
subprocess.Popen(['tmux', 'run-shell', str(restore_script)])
```
When the `tmux` server daemon is not running (zero active sessions after a reboot), `tmux run-shell` exits immediately with an error because there is no server context to host the shell command. Manually creating a session implicitly started the `tmux` daemon, allowing subsequent restores to succeed.

### Resolution
`TmuxDashboard.action_restore_tmux_state()` in `bin/dashboard.py` now checks `tmux has-session` first:
- If `returncode != 0` (no server/sessions), it spawns a detached bootstrap session (`aim_restore_tmp`), runs `restore.sh` via `tmux run-shell`, waits 5 seconds for session population, and terminates `aim_restore_tmp`:
  ```bash
  tmux new-session -d -s aim_restore_tmp && tmux run-shell '<restore_script>' && sleep 5 && tmux kill-session -t aim_restore_tmp
  ```
- If a session already exists, it invokes `tmux run-shell` directly.

## 3. Scrollback Preview "Flash" / Idle Bash Prompt on Restore (Issue #44)
### Symptom
1. **Fresh Session Flash:** After restoring a workspace, `aim-dash` displays the saved scrollback in the preview pane. However, attaching to an AI session briefly flashes the old scrollback before clearing the screen into a brand-new, contextless AI session (when restored without `-c`).
2. **Idle Bash Below Scrollback ("Ctrl+C" Effect):** The preview in `aim-dash` shows the saved AI conversation, but attaching drops into an idle `bash` prompt inside the project folder with the old conversation text sitting directly above it.

### Root Cause & Fix
`tmux-resurrect` first replays the captured pane scrollback file (`pane_contents.tar.gz`) onto the terminal buffer and `cd`s into the saved directory, then checks `_process_on_the_restore_list` to decide whether to re-execute the process:
- If `@resurrect-processes` uses broken quoting (`"~agy"->"~agy -c"`), `eval set $(_restore_list)` treats the unquoted `>` as shell file redirection, causing `_process_on_the_restore_list` to fail completely so no process is launched below the replayed scrollback.
- Properly quoting the entire inline strategy (`"~agy->agy -c"`) in `~/.tmux.conf` resolves both symptoms; see [AI Agent Integration & Fast Resume](ai_agent_integration.md).

## 4. Full-Stack Microservice & Tunnel Auto-Resurrection (Issue #46)
When `@resurrect-processes` includes substring matchers for runtime daemons (`~node ~python3 ~cloudflared`) alongside AI agent translations, triggering **Workspace: Restore Tmux State** after a cold reboot automatically restarts supporting infrastructure in their saved panes with their original CLI arguments:
1. **Python / FastAPI Backends (`~python3`):** Restores API servers (e.g., Uvicorn/FastAPI health endpoints) automatically in their project panes.
2. **MCP SSE Servers (`~python3` / `~node`):** Restores Model Context Protocol SSE daemons on their configured ports without manual intervention.
3. **Edge Tunnels (`~cloudflared`):** Re-establishes `cloudflared` ingress tunnels automatically on workspace restore.

## 5. WSL & Windows Terminal Startup Race Condition
- `tmux-resurrect` is completely passive and only runs when manually triggered; it does not hook `.bashrc` or WSL init (unless `tmux-continuum` is installed, which is not used here).
- Unexpected empty `aim-dash` tabs and WSL errors after a Windows/WSL crash are caused by **Windows Terminal's "Open windows from a previous session"** startup setting attempting to re-launch shells before the WSL Linux subsystem and `tmux` daemon finish initializing.
- **Recommended Mitigation:** Set Windows Terminal -> Startup -> *When Terminal starts* to **"Open a new tab"** and launch `aim-dash` manually after boot.

## Related Pages
- [Core TUI Architecture](architecture.md)
- [AI Agent Integration & Fast Resume](ai_agent_integration.md)
- [Project Wiki Index](../index.md)
