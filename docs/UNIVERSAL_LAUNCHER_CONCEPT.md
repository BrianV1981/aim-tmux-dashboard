# 🚀 Concept: The Universal Project Launcher

## Overview
This document outlines a potential Phase 3/4 feature for the `aim-dash` TUI. 
Rather than limiting the dashboard to only managing *currently active* tmux sessions, this feature transforms the dashboard into a "Universal Project Launcher" (similar to macOS Spotlight, or tools like `sesh` and `tmuxinator`).

By treating **Active Tmux Sessions**, **Git Repositories**, and **Local Directories** as equal "Destinations", we eliminate the cognitive friction of starting work.

---

## 🖥️ The User Experience Flow
1. **The Summoning:** The Operator presses a global hotkey (or runs the command) which opens the `aim-dash` floating popup over their current terminal.
2. **The Search:** A fuzzy-finder input field is focused by default.
3. **The Magic Resolution:** As the Operator types "dash", the list populates with:
    - `[🟢 ACTIVE] aim-tmux-dashboard` (A running tmux session)
    - `[📁 OFFLINE] ~/projects/aim-tmux-dashboard` (A local git repo)
4. **The Execution:** The Operator selects a destination and hits `Enter`:
    - If it's `[🟢 ACTIVE]`, the TUI instantly attaches them to the existing session.
    - If it's `[📁 OFFLINE]`, the TUI silently runs `tmux new-session -d -s "aim-tmux-dashboard" -c "~/projects/aim-tmux-dashboard"`, boots it up, and attaches them to it.

---

## ⚙️ Discovery Strategy (How do we find offline projects?)
To offer offline directories in the fuzzy finder without scanning the entire hard drive (which is too slow), we need a discovery strategy. 

### Option A: The Configuration File (Explicit)
- The user maintains a `~/.config/aim-dash/config.yaml` file listing their root project directories.
- Example: 
  ```yaml
  search_paths:
    - "~/projects"
    - "~/.gemini/antigravity-cli/skills"
  ```
- **Pros:** Fast, predictable, no junk folders.
- **Cons:** Requires manual setup by the user.

### Option B: Zoxide / History Integration (Implicit)
- We read the database from terminal tools the user already has, like `zoxide` (a smarter `cd` command that tracks frecency) or `bash_history`.
- **Pros:** Zero configuration. Learns what directories the user actually works in.
- **Cons:** Requires relying on external binaries.

### Option C: The Hybrid "Max Depth" Scanner
- Hardcode standard developer paths (e.g., `~/`, `~/projects/`, `~/Documents/Github/`) and run a fast asynchronous scan looking for `.git` folders up to a max depth of 2.
- **Pros:** Works out of the box for most standard folder structures.
- **Cons:** Can still pick up unwanted/archived repositories.

---

## 🛠️ Technical Implementation in Textual
1. **Asynchronous Gathering:** When the TUI boots, it fires an `async` worker to scan the discovery paths and build a cache of offline projects. This prevents the UI from freezing on startup.
2. **The Unified Roster:** We merge the output of `tmux ls` with the offline project cache. We use Textual's `ListView` or `DataTable` to display them, using rich color formatting (e.g., Green for active, Gray for offline) to visually separate them.
3. **Smart Attach Logic:** 
   ```python
   def handle_attach(destination):
       if destination.is_active_session:
           subprocess.run(["tmux", "attach", "-t", destination.name])
       else:
           # Boot it up first
           subprocess.run(["tmux", "new-session", "-d", "-s", destination.name, "-c", destination.path])
           subprocess.run(["tmux", "attach", "-t", destination.name])
   ```
