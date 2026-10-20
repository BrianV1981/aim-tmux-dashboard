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

## 3. Scrollback Preview "Flash" on Restore
### Symptom
After restoring a workspace, `aim-dash` displays the saved scrollback in the preview pane. However, attaching to an AI session briefly flashes the old scrollback before clearing the screen into a brand-new, contextless AI session.

### Root Cause & Fix
`tmux-resurrect` first replays the captured pane scrollback file onto the terminal buffer, then re-executes the saved process command. If the saved command is raw `agy` (without `-c`), the newly spawned binary overwrites the terminal buffer with a fresh session picker. Mapping `@resurrect-processes` in `~/.tmux.conf` to append `-c` resolves this; see [AI Agent Integration & Fast Resume](ai_agent_integration.md).

## 4. WSL & Windows Terminal Startup Race Condition
- `tmux-resurrect` is completely passive and only runs when manually triggered; it does not hook `.bashrc` or WSL init (unless `tmux-continuum` is installed, which is not used here).
- Unexpected empty `aim-dash` tabs and WSL errors after a Windows/WSL crash are caused by **Windows Terminal's "Open windows from a previous session"** startup setting attempting to re-launch shells before the WSL Linux subsystem and `tmux` daemon finish initializing.
- **Recommended Mitigation:** Set Windows Terminal -> Startup -> *When Terminal starts* to **"Open a new tab"** and launch `aim-dash` manually after boot.

## Related Pages
- [Core TUI Architecture](architecture.md)
- [AI Agent Integration & Fast Resume](ai_agent_integration.md)
- [Project Wiki Index](../index.md)
