# 🖥️ aim-tmux-dashboard

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
☕ **Support the project:** [Buy Me a Coffee](https://buymeacoffee.com/brianv1981)

<!-- AIM_ECOSYSTEM_START -->
### 🧬 The A.I.M. Ecosystem

For the up-to-date map of the A.I.M. Ecosystem, please visit the **[aim-ecosystem](https://github.com/BrianV1981/aim-ecosystem)** repository or the flagship OS, **[aim-joshua](https://github.com/BrianV1981/aim-joshua)**.
<!-- AIM_ECOSYSTEM_END -->

---

## 📖 Overview

A modern, terminal-based dashboard for managing tmux workspaces. Built with Python Textual, it features a command palette, live previews, robust session persistence (via tmux-resurrect), and seamless zero-friction resumption for AI coding agents.

## ✨ Features

* **Live Workspace Previews:** Navigate your tmux sessions, windows, and panes via an interactive tree and view real-time scrollback/context before attaching.
* **Command Palette:** Quickly execute structural commands, swap layouts, and manage session states via a fuzzy-finding popup palette.
* **AI Agent Fast Resume:** Tightly integrated with the A.I.M. ecosystem. Instantly resume isolated local agents (using the `-c` flag) directly from the dashboard without navigating global menus.
* **Workspace Resurrection:** Natively triggers `tmux-resurrect` to snapshot and securely restore massive development ecosystems.

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

## ⚙️ Tmux Resurrect & AI Agent Integration

To utilize the automated Workspace Save/Restore capabilities, you must have the [tmux-resurrect](https://github.com/tmux-plugins/tmux-resurrect) plugin installed.

If you want your AI agents to automatically resume their local contextual conversations upon a workspace restore, you must explicitly map them to use the `--continue` (`-c`) flag in your `~/.tmux.conf` configuration. 

Update your config to include the native command-translation syntax (`->`):

```tmux
# ~/.tmux.conf
# Save terminal scrollback and history
set -g @resurrect-capture-pane-contents 'on'

# Tell resurrect to automatically inject the -c (continue) flag when restoring agents
set -g @resurrect-processes '"~agy"->"~agy -c" "~grok"->"~grok -c" "~codex"->"~codex -c" "~opencode"->"~opencode -c" ~node ~python3'
```

## ⌨️ Usage & Keybindings

| Keybinding | Action |
| :--- | :--- |
| `Enter` | Attach to the selected Session/Window/Pane |
| `Ctrl+P` | Open the Command Palette |
| `/` | Filter / Search active sessions |
| `r` | Refresh session tree |
| `q` | Quit dashboard |