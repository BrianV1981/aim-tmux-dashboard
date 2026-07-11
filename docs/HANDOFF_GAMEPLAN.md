# AIM-Tmux-Dashboard: Architecture & Handoff

## Overview
This repository contains `aim-dash`, the backend TUI sister-app to `aim-connect`. It is a pure bash multiplexer dashboard that allows the Operator (and other AIM agents) to dynamically create, attach to, and destroy background `tmux` workspaces.

## Directory Structure
- `bin/aim-dash`: The core TUI bash script.
- `install.sh`: Creates a global symlink so the Operator can type `aim-dash` from anywhere.
- `.gemini/skills/aim_tmux/SKILL.md`: The crucial integration file. This teaches other AIM agents how to interact with the dashboard.

## Immediate Directives for the Specialized Agent
1. **Refine the Bash Code:** The prototype in `bin/aim-dash` works beautifully, but can be optimized.
2. **Implement Global Shortcuts:** Ensure the `install.sh` correctly exposes the tool globally.
3. **Write the SKILL.md:** This is the most important task. You must write the `.gemini/skills/aim_tmux/SKILL.md` file so that when *other* agents wake up, they know this TUI exists and how to spawn background tasks using standard `tmux` protocols.
4. **Documentation:** Draft a clean `README.md` explaining how `aim-dash` operates identically to the web-based `aim-connect`.
