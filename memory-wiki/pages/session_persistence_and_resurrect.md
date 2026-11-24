# Session Persistence & Resurrection

`aim-tmux-dashboard` does not implement a custom state-serialization engine in Python. Instead, it acts as a remote control for **[tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect)** (`~/.tmux/plugins/tmux-resurrect/scripts/save.sh` and `restore.sh`).

## 1. Third-Party Dependency Boundary & Empty-Save Guardrail (Issues #40–#41, #47)
- The Command Palette actions **Workspace: Save Tmux State** and **Workspace: Restore Tmux State** require `tmux-resurrect` to be installed in `~/.tmux/plugins/tmux-resurrect/`.
- If the scripts are missing, `TmuxDashboard` surfaces an error toast: `"tmux-resurrect not found in ~/.tmux/plugins/"`.
- **Empty-Save Guardrail (`Issue #47`):** Before invoking `save.sh`, `TmuxDashboard.action_save_tmux_state()` compares the active session count against the distinct session count in `~/.local/share/tmux/resurrect/last` (or `~/.tmux/resurrect/last`). If `active_count <= 1` or `active_count <= saved_count // 2`, it presents `ConfirmSaveModal` to prevent accidentally overwriting a rich multi-session snapshot after a reboot.

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

## 6. Headless WSL2 Keepalive & Crash-Recovery Blueprint (`Issue #52`, Planned)
> **Status:** Architectural blueprint documented for remote uptime; implementation is tracked in GitHub **Issue #52** (`enhancement`) and intentionally not wired yet.

### Why Leaving `aim-dash` Open Is Not Actually Required
1. **Zero Runtime Dependency:** `aim-connect` (`~/aim-connect/startup.sh`) launches `aim-connect-workspace` (`uvicorn` on `:8000`, optional `aim-mcp` on `:8001`, and `cloudflared`) directly inside `tmux`. Currently `aim-dash` is only acting as (a) a manual trigger for `restore.sh` after reboot, and (b) an open Windows Terminal handle keeping WSL2 awake.
2. **Why WSL2 Shuts Down Without a Terminal:** Even with `systemd=true` in `/etc/wsl.conf`, WSL2's default `vmIdleTimeout` (`60000` ms) suspends/terminates the Linux VM shortly after the last Windows-side client window closes—killing background `tmux` servers, AI agents, and `aim-connect`.

### Keeping WSL2 + `tmux` Alive With Zero Open Terminal Windows
To keep `tmux`, `aim-connect`, and optionally a detached `aim-dash` session running continuously across reboots or terminal closes:
1. **Global `.wslconfig` Idle Timeout (`Windows`):**
   - In `C:\Users\<YourUsername>\.wslconfig` under `[wsl2]`, add:
     ```ini
     [wsl2]
     vmIdleTimeout=-1
     ```
   - Apply once with `wsl --shutdown` in PowerShell. Note that depending on Windows/WSL build behavior, closing the last interactive `wsl.exe` client can still release the distro instance unless a Windows-side process holds a client handle.
2. **Hidden Windows Task Scheduler Keepalive (`Windows`):**
   - Create a Task Scheduler job triggered **At log on** (or **At startup**, configured hidden / non-interactive) that holds a headless `wsl.exe` client handle open in the background with zero visible Windows Terminal tabs:
     ```cmd
     wsl.exe -d Ubuntu --exec sleep infinity
     ```
   - Pair with Windows Power settings (`Never` sleep when plugged in) so remote hardware stays reachable over `cloudflared`.
3. **Linux `systemd` Cold-Boot Auto-Restore (`Issue #52` Target):**
   - With `systemd=true` in `/etc/wsl.conf`, a boot unit/script can check `tmux has-session`: if no server is active, run the `aim_restore_tmp` + `~/.tmux/plugins/tmux-resurrect/scripts/restore.sh` bootstrap, then idempotently invoke `~/aim-connect/startup.sh` so `:8000`, `:8001`, and `cloudflared` auto-start after an unattended reboot or crash.
   - If `aim-dash` itself is desired pre-loaded for instant attach, it can live inside a detached `tmux` session (`tmux new-session -d -s aim-dash "aim-dash"`) or remain on-demand via `F9` / `F10` popup bindings—never requiring a dedicated Windows Terminal window to stay open.

## Related Pages
- [Core TUI Architecture](architecture.md)
- [AI Agent Integration & Fast Resume](ai_agent_integration.md)
- [Project Wiki Index](../index.md)
