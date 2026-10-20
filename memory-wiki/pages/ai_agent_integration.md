# AI Agent Integration & Fast Resume

`aim-tmux-dashboard` treats local AI CLI vessels (`agy`, `grok`, `codex`, `opencode`, `aider`, `claude`, `gemini`, `antigravity`) as first-class citizens across visual identification, manual resumption, and automated workspace restoration.

## 1. Visual Process Badges
In `TmuxDashboard.format_cmd()`, every pane's `#{pane_current_command}` is inspected against the known agent list:
```python
agents = ["agy", "aider", "claude", "grok", "gpt", "agent", "opencode", "gemini", "codex", "antigravity"]
```
Matching panes are prefixed with a high-visibility `[bold cyan][A.I.][/bold cyan]` badge in the session tree.

## 2. Localized Fast Resume (`-c` / `--continue`)
### How `-c` Works in Antigravity / A.I.M. CLI Vessels
Running `agy -c` (or `--continue`), `grok -c`, `codex -c`, or `opencode -c` inside a project directory instructs the binary to resolve the current working directory against its local session index and immediately resume the single most recent session for that folder—completely bypassing the global TUI session picker.

### Command Palette Integration (`Agent: Fast Resume (-c)`, Issue #38)
1. `TmuxManager.get_hierarchy()` captures `#{pane_current_path}` alongside `#{pane_current_command}` for every pane.
2. When the Operator selects a session, window, or pane in `#session-tree` and triggers **Agent: Fast Resume (-c)** from the Command Palette (`Ctrl+P`), `action_fast_resume_agent()` resolves the active pane's working directory (`target_path`) and command (`target_cmd`).
3. It matches `target_cmd` against the known agent list (defaulting to `agy` if no agent binary is currently active in that pane) and spawns a new window in the target session synced to `target_path`:
   ```bash
   tmux new-window -t <session> -c <target_path> -n "<agent>-resume" "<agent> -c"
   ```

## 3. Automated Restore Translation via `tmux-resurrect`
Because `tmux-resurrect` records the literal command that launched a pane (e.g., `agy`), a standard restore runs `agy` without `-c`, opening a fresh session instead of resuming context.

To force automatic resumption on workspace restore, `~/.tmux.conf` must configure `@resurrect-processes` using `tmux-resurrect`'s `->` command-translation syntax (with the entire `~match->command` rule inside a single pair of double quotes and no leading `~` on the right-hand target command):
```tmux
set -g @resurrect-capture-pane-contents 'on'
set -g @resurrect-processes '"~agy->agy -c" "~grok->grok -c" "~codex->codex -c" "~opencode->opencode -c" ~node ~python3'
```
> **Critical Syntax Rule (Issue #44):**
> - Do **not** quote each side of `->` separately (`"~agy"->"~agy -c"`). When `tmux-resurrect`'s `process_restore_helpers.sh` runs `eval set $(_restore_list)`, an unquoted `>` is parsed by `bash` as stdout file redirection, breaking process matching (`~agy-`) and creating empty files on disk.
> - Do **not** place a tilde (`~`) on the right-hand side of `->` (`~` is only a substring-match prefix for the left-hand side; on the right-hand side `bash` treats `~agy` as home-directory expansion for user `agy`).
> - Do **not** include both `~agy->...` and `~agy.real->...`, as `~agy` substring-matches `agy.real` and causes `_get_inline_strategy` to emit the restore command twice.

## Related Pages
- [Core TUI Architecture](architecture.md)
- [Session Persistence & Resurrection](session_persistence_and_resurrect.md)
- [Project Wiki Index](../index.md)
