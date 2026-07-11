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

*(Note: The dashboard is currently evolving from a basic script into a modern, fully interactive TUI.)*

To launch the dashboard from this repository:
```bash
./bin/aim-dash
```

**Basic Controls:**
- `n`: Create a new Tmux workspace.
- `[0-9]`: Enter the number of an active session to attach to it. (Press `Ctrl+B` then `D` to detach and return).
- `k`: Kill / Delete a specific session.
- `q`: Quit the dashboard.

---

## 🧬 Built on the A.I.M. Exoskeleton
This project utilizes the **A.I.M.** framework, an open-source engineering exoskeleton designed to solve context amnesia and drift in long-running autonomous AI coding sessions. 
Learn more about the core engine at [aim-agy](https://github.com/BrianV1981/aim-agy).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
☕ **Support the project:** [Buy Me a Coffee](https://buymeacoffee.com/brianv1981)