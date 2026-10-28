# 🖥️ aim-tmux-dashboard

## 📖 Overview

A modern, terminal-based dashboard for managing `tmux` workspaces. Built with Python [Textual](https://github.com/Textualize/textual) and [Rich](https://github.com/Textualize/rich), it features an interactive session/window/pane tree, live ANSI pane previews, a fuzzy-searching Command Palette, scrollback token extraction, robust workspace persistence (via `tmux-resurrect`), and zero-friction resumption for local AI coding agents.

## ✨ Features

* **Hierarchical Session Tree & Smart Flattening:** Navigate your `tmux` sessions, windows, and panes in a collapsible tree. Single-window/single-pane sessions automatically flatten into compact 1-line nodes (`◆ session [command]`).
* **Live ANSI Previews:** View real-time color-accurate terminal scrollback (`tmux capture-pane -e -p`) before attaching, with an optional 1-second live polling toggle (`l`).
* **AI Agent Detection & Fast Resume:** Automatically badges running AI CLI harnesses (`agy`, `grok`, `codex`, `opencode`, `claude`, `aider`, `gemini`, `gpt`, `antigravity`) with `[A.I.]` and lets you resume localized agent conversations (`-c`) directly from the Command Palette.
* **Cold-Boot Fleet Resurrection:** Natively triggers `tmux-resurrect` (including automatic dead-daemon bootstrap after a full OS reboot) to restore every session, window, pane, and working directory in one action.
* **Microservice, MCP & Tunnel Auto-Start:** Restores not just AI coding agents, but your entire supporting stack—automatically restarting FastAPI/Python backends (`~python3`), Node/MCP SSE servers (`~node`), and Cloudflare edge tunnels (`~cloudflared`) in their respective panes on restore.
* **Scrollback Token Grabber (`t` / `--grab`):** Fuzzy-search and copy URLs (with automatic secret/token query redaction), IPv4 addresses, and Git commit hashes from the last 10,000 lines of pane scrollback.
* **Customizable UI Layouts:** Switch between 4 structural orientations (`Side-by-Side Left/Right`, `Stacked Top/Bottom`) and dynamically resize split panes (`[` / `]`), automatically persisted in `~/.aim_dashboard.json`.
* **Popup Overlay Mode (`--popup`):** Summon the dashboard or Token Grabber as a floating `tmux display-popup` overlay directly over your active workspace.

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BrianV1981/aim-tmux-dashboard.git
   cd aim-tmux-dashboard
   ```
2. Run the installation script (creates the local `venv`, installs `requirements.txt`, and symlinks `aim-dash` to `/usr/local/bin/aim-dash`):
   ```bash
   ./install.sh
   ```
   *(If you prefer a user-local install without `sudo`, run `./scripts/setup.sh` and symlink `ln -sf "$(pwd)/bin/aim-dash" ~/.local/bin/aim-dash`.)*
3. Launch the dashboard from any terminal:
   ```bash
   aim-dash
   ```

## 💻 CLI Modes & Optional Tmux Popup Hooks

`aim-dash` supports three execution modes:

| Command | Description |
| :--- | :--- |
| `aim-dash` | Standard full-terminal dashboard. Suspends and attaches (`tmux attach`) when outside `tmux`, or switches client (`tmux switch-client`) when inside `tmux`. |
| `aim-dash --popup` | Floating overlay mode designed for `tmux display-popup`. Switches the active client and closes the popup upon selection. |
| `aim-dash --grab` | Standalone **Token Grabber** modal targeting the currently active `tmux` pane (`#{pane_id}`). |

To bind floating popups in your `~/.tmux.conf` (requires `tmux` 3.2+):

```tmux
# Summon A.I.M. Dashboard as a floating popup using F10
bind-key -n F10 display-popup -E -w 85% -h 85% -d "#{pane_current_path}" "aim-dash --popup"

# Summon the Scrollback Token Grabber on the current pane using Prefix + g
bind-key g display-popup -E -w 85% -h 85% -d "#{pane_current_path}" "aim-dash --grab"
```

## ⚙️ Workspace Save & Restore (Third-Party Dependency)

To utilize the **Workspace: Save Tmux State** and **Workspace: Restore Tmux State** commands in the Command Palette (`Ctrl+P`), this dashboard relies on **[tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect)** installed in `~/.tmux/plugins/tmux-resurrect/`.

⚠️ **You must install `tmux-resurrect` on your system first.** The dashboard acts as an orchestration remote control that triggers `tmux-resurrect`'s `save.sh` and `restore.sh` scripts (and automatically bootstraps a detached `tmux` server if invoked from a cold reboot with zero running sessions).

### AI Agent & Background Service Integration (Auto-Resume)

If you want your AI agents to automatically resume their local contextual conversations upon a workspace restore—and want your supporting API servers, MCP daemons, and edge tunnels to restart automatically alongside them—configure `@resurrect-processes` in your `~/.tmux.conf`.

Update your config to include the native command-translation syntax (`->`) for AI harnesses alongside process matchers for your background services:

```tmux
# ~/.tmux.conf
# Save terminal scrollback and history
set -g @resurrect-capture-pane-contents 'on'

# Automatically inject -c (continue) when restoring AI agents, and auto-restart Node, Python, and Cloudflared services
set -g @resurrect-processes '"~agy->agy -c" "~grok->grok -c" "~codex->codex -c" "~opencode->opencode -c" ~node ~python3 ~cloudflared'
```

With this configuration in place, running **Workspace: Restore Tmux State** after a system reboot will:
1. **Reconnect AI Agents (`-c`):** Launch each AI CLI vessel inside its saved project directory and immediately attach to its previous conversation state.
2. **Auto-Start Companion Services (`~python3`, `~node`, `~cloudflared`):** Automatically re-execute FastAPI/Python backends, MCP SSE servers, and `cloudflared` edge tunnels with their original command-line arguments—bringing full-stack development environments back online with zero manual startup steps.

## ⌨️ Usage & Keybindings

### Main Dashboard Shortcuts

| Keybinding | Action |
| :--- | :--- |
| `Enter` / `a` | Attach / switch to the selected Session, Window, or Pane |
| `n` | Create a new `tmux` session |
| `e` | Rename the selected `tmux` session |
| `k` | Kill the selected `tmux` session (with confirmation dialog) |
| `/` | Focus the live search input to filter sessions |
| `l` | Toggle 1-second live preview polling on/off |
| `t` | Open the **Token Grabber** modal on the selected target's scrollback |
| `[` / `]` | Shrink / expand the session tree split pane (`10%`–`90%`, saved to `~/.aim_dashboard.json`) |
| `r` | Manually refresh the session tree |
| `Ctrl+P` | Open the **Command Palette** |
| `q` | Quit dashboard |

### Command Palette (`Ctrl+P`) Actions

| Command | Description |
| :--- | :--- |
| **Agent: Fast Resume (-c)** | Detects the selected pane's working directory and AI binary (`agy`, `grok`, `codex`, `opencode`, etc.) and spawns a resumed (`-c`) agent window in that folder. |
| **UI Layouts...** | Switch between `Side-by-Side (List Left)`, `Side-by-Side (List Right)`, `Stacked (List Top)`, and `Stacked (List Bottom)`. |
| **Keys (TMUX)** | Open a slide-out right-hand `tmux` keybinding cheat sheet (`Escape` to close). |
| **Workspace: Save Tmux State** | Asynchronously snapshots all active sessions, windows, panes, and scrollback via `tmux-resurrect`. |
| **Workspace: Restore Tmux State** | Bootstraps the `tmux` server (if stopped) and restores your saved workspace via `tmux-resurrect`. |

---

<!-- AIM_ECOSYSTEM_START -->
### 🧬 The A.I.M. Ecosystem

For the up-to-date map of the A.I.M. Ecosystem, please visit the **[aim-ecosystem](https://github.com/BrianV1981/aim-ecosystem)** repository or the flagship OS, **[aim-joshua](https://github.com/BrianV1981/aim-joshua)**.
<!-- AIM_ECOSYSTEM_END -->

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
☕ **Support the project:** [Buy Me a Coffee](https://buymeacoffee.com/brianv1981)
