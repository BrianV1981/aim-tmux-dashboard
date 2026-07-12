# 🚀 A.I.M. Tmux Dashboard

The **A.I.M. Tmux Dashboard** (`aim-dash`) is a streamlined, interactive Terminal User Interface (TUI) designed to control, orchestrate, and manage multiple isolated tmux sessions. 

Whether you are managing background services or coordinating an army of autonomous AI agents, this dashboard provides a central cockpit to monitor and interact with your workflows.

## 🌟 Why It's Useful

### Standalone Use
Even without the full A.I.M. exoskeleton, `aim-dash` serves as a kickass, lightweight manager for tmux. Instead of memorizing arcane tmux commands or navigating raw terminal output, the dashboard lets you:
- Quickly view all active detached background sessions.
- Spawn new, cleanly-named, isolated workspaces with a single keystroke.
- Attach to running sessions and detach seamlessly.
- Instantly kill rogue or completed sessions.

### In the Larger A.I.M. Ecosystem
In the context of the **A.I.M. (Actual Intelligent Memory)** framework, autonomous agents run detached in the background to prevent terminal paralysis. `aim-dash` becomes your central **Admin Panel**:
- **Visibility:** Monitor exactly what your sovereign Co-Agents are doing without interrupting them.
- **Orchestration:** Spin up separate sandboxes for agents working on different tickets simultaneously.
- **Intervention:** Attach to a session to observe an agent's terminal stream, provide human guidance via TUI chat, or kill a hallucinating agent instantly.

---

## 🛠️ Installation & Usage

To install the dashboard and its Python dependencies locally:
```bash
git clone https://github.com/BrianV1981/aim-tmux-dashboard.git
cd aim-tmux-dashboard
./scripts/setup.sh
```

**Global Server-Wide Installation**
If you want to be able to type `aim-dash` from anywhere on your machine without being in the project directory, run the installer script (requires sudo to create the `/usr/local/bin` symlink):
```bash
sudo ./install.sh
```

To launch the dashboard from this repository:
```bash
./bin/aim-dash
```

**Popup Mode**
You can run the dashboard as a floating popup overlay within tmux using the `--popup` flag. We recommend binding this to a hotkey in your `~/.tmux.conf`:
```tmux
bind-key -n F10 display-popup -E -w 85% -h 85% -d "#{pane_current_path}" "cd /path/to/aim-tmux-dashboard && ./bin/aim-dash --popup"
```

**Token Grabber**
You can instantly grab URLs, IPs, and Git Hashes from the current pane without opening the dashboard by binding the `--grab` flag:
```tmux
bind-key g display-popup -E -w 85% -h 85% -d "#{pane_current_path}" "cd /path/to/aim-tmux-dashboard && venv/bin/python bin/dashboard.py --grab"
```

**Dashboard Controls:**
- `Arrow Keys`: Navigate the session tree.
- `Enter` / `a`: Attach to the selected session, window, or pane.
- `l`: Toggle Live Preview (auto-updates the preview pane every 1 second).
- `n`: Create a new Tmux workspace.
- `e`: Rename the selected session.
- `k`: Kill the selected session.
- `/`: Filter/search sessions.
- `t`: Token Grabber (extracts links/hashes from the highlighted pane).
- `q`: Quit the dashboard.

---

## 🧬 Built on the A.I.M. Exoskeleton
This project utilizes the **A.I.M.** framework, an open-source engineering exoskeleton designed to solve context amnesia and drift in long-running autonomous AI coding sessions. 
Learn more about the core engine at [aim-agy](https://github.com/BrianV1981/aim-agy).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
☕ **Support the project:** [Buy Me a Coffee](https://buymeacoffee.com/brianv1981)