# A.I.M. Tmux Dashboard - v2 Roadmap

This document outlines the formalized, prioritized feature roadmap for Version 2.0. These features were sourced from auditing top-tier multiplexer managers (`tuimux`, `tmuxy`, `lunemis/mux`, and `tmux-popup-control`).

---

## Phase 1: Architectural Foundation (The Control Mode Migration)
Before we can build complex features, we must upgrade how the dashboard communicates with the `tmux` daemon. 

*   **Tmux Control Mode (`tmux -C`):** Replace synchronous polling and shelling out (`subprocess.run`) with a persistent `tmux -C` connection. This provides a raw stdout stream where `tmux` natively pushes events (e.g., pane resized, text outputted). This unlocks true, zero-latency, event-driven UI updates without micro-stutters.
*   **Async Core Refactor:** Migrate the `TmuxManager` backend to use native Python `asyncio`. This ensures the UI thread remains 100% fluid, even if the backend is parsing thousands of lines of output from 50 different sessions.

## Phase 2: Navigation & UX Overhaul
With the architecture modernized, we expand how the user navigates their environments.

*   **Tree-Based Hierarchy:** Upgrade the session list to a collapsible Textual `Tree` widget. Users can expand a session to reveal and attach directly to individual windows and panes.
*   **Popup Palette Mode:** Leverage `tmux display-popup` (Tmux 3.2+) so the dashboard can be summoned via a hotkey (e.g., `Prefix + m`) as a transparent, floating overlay on top of active code, rather than taking over the full terminal window.

## Phase 3: A.I. MLOps & Project Awareness
Upgrading the dashboard from a generic manager into a specialized "Sovereign Orchestrator" for AI Agents.

*   **AI Agent Detection:** Automatically inspect pane processes to detect running AI agents (Claude, Aider, Gemini). Flag these sessions in the UI with distinct badges.
*   ~~**Token & Cost Tracking:** Natively parse agent log files to display real-time API token usage and estimated cost burn-rates directly in the dashboard.~~ *(On Hold - Latency Risk)*
*   ~~**Git & Worktree Awareness:** Display the active Git branch next to each session. Visually distinguish isolated Git Worktrees from main branches to track which agent is working on which ticket.~~ *(On Hold - Latency Risk)*

## Phase 4: Power Tools & Persistence
Implementing massive workflow multipliers and bulletproofing the environment against data loss.

*   **Token Grabber (Extrakto-style):** A hotkey that parses the active pane's scrollback, extracts all URLs, IP addresses, and Git hashes, and presents them in a fuzzy-search popup for instant clipboard copying.
*   **Continuous Background Autosaves:** A background daemon that silently snapshots all pane contents, layouts, and window topologies on a 5-minute interval. If the server crashes, the user can restore their entire environment exactly as they left it.
*   **Visual Plugin Manager:** A UI replacement for `tpm`. Visually browse, install, and update tmux plugins and themes without manually editing `~/.tmux.conf`.
*   **Command Palette:** A searchable catalog of every tmux command and keybinding with contextual auto-completion.
