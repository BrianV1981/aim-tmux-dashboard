# 🖥️ aim-tmux-dashboard

## 📖 Overview

A modern, terminal-based dashboard for managing tmux workspaces. Built with Python Textual, it features a command palette, live previews, robust session persistence (via tmux-resurrect), and seamless zero-friction resumption for AI coding agents.

## ✨ Features

* **Live Workspace Previews:** Navigate your tmux sessions, windows, and panes via an interactive tree and view real-time scrollback/context before attaching.
* **Command Palette:** Quickly execute structural commands, swap layouts, and manage session states via a fuzzy-finding popup palette.
* **AI Agent Fast Resume:** Tightly integrated with the A.I.M. ecosystem. Instantly resume isolated local agents (using the `-c` flag) directly from the dashboard without navigating global menus.
* **Cold-Boot Fleet Resurrection:** Natively triggers `tmux-resurrect` (including automatic dead-daemon bootstrap after a full OS reboot) to restore every session, window, pane, and working directory in one action.
* **Microservice, MCP & Tunnel Auto-Start:** Restores not just AI coding agents, but your entire supporting stack—automatically restarting FastAPI/Python backends (`~python3`), Node/MCP SSE servers (`~node`), and Cloudflare edge tunnels (`~cloudflared`) in their respective panes on restore.

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/BrianV1981/aim-tmux-dashboard.git
   cd aim-tmux-dashboard
   ```
2. Run the installation script (sets up the `venv` and symlinks the executable):
   ```bash
   ./install.sh
   ```
3. Launch the dashboard from any terminal:
   ```bash
   aim-dash
   ```

## ⚙️ Workspace Save & Restore (Third-Party Dependency)

To utilize the "Workspace Save" and "Workspace Restore" features in the Command Palette, this dashboard relies on a third-party plugin called **[tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect)**. 

⚠️ **You must install `tmux-resurrect` on your system first.** The dashboard does not reinvent state-saving; instead, it acts as a remote control that seamlessly triggers `tmux-resurrect`'s underlying scripts to save and load your environments.

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

| Keybinding | Action |
| :--- | :--- |
| `Enter` | Attach to the selected Session/Window/Pane |
| `Ctrl+P` | Open the Command Palette |
| `/` | Filter / Search active sessions |
| `r` | Refresh session tree |
| `q` | Quit dashboard |

---

<!-- AIM_ECOSYSTEM_START -->
### 🧬 The A.I.M. Ecosystem

For the up-to-date map of the A.I.M. Ecosystem, please visit the **[aim-ecosystem](https://github.com/BrianV1981/aim-ecosystem)** repository or the flagship OS, **[aim-joshua](https://github.com/BrianV1981/aim-joshua)**.
<!-- AIM_ECOSYSTEM_END -->

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
☕ **Support the project:** [Buy Me a Coffee](https://buymeacoffee.com/brianv1981)