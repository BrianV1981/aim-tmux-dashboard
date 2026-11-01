# aim-tmux-dashboard — Engineering Handoff

> **Updated:** 2026-10-31T23:53:00-04:00
> **Updated by:** Antigravity (`bd07ebad-31e9-4748-9585-b9a3cef74bc2` / Gemini 4 Argon High)
> **Priority Mission:** STANDBY — `v1.0.0` General Availability Shipped (`93a7065`, `14/14` unit tests passing; only future `v2.0` `tmux -C` ticket `#51` open).
> **Operator:** Brian Vasquez (`@BrianV1981` / `brianv1981@gmail.com`)

---

## 0. COMPLETED WORK (DO NOT REVISIT)
| Session | Work | Status |
|---------|------|--------|
| `v0.0.1` (`18c8db6`) | Initial Bash multiplexer prototype (`bin/aim-dash`) and `aim_tmux` skill migration (`docs/HANDOFF_GAMEPLAN.md`) | ✅ RESOLVED |
| `v0.1.0` (`61c4bf5`) | Ported `aim-dash` to Python Textual TUI (`bin/dashboard.py`), tree hierarchy (`#10`), `--popup` mode (`#11`), AI badges (`#12`), Token Grabber `--grab` (`#14`), release hygiene (`#17`), killed cron scope creep (`#18`) | ✅ RESOLVED |
| `v0.2.0` (`c02095e`–`8cad9a8`) | UI facelift (`#19`), layout wrapper hotfix (`#21`), dynamic layout switcher & `[` `]` resizing (`#23`), Command Palette nested provider (`#27`), slide-out `TmuxKeysScreen` (`dd14aa8`), `tmux-resurrect` save/restore integration (`#34`–`#36`) | ✅ RESOLVED |
| `893bacaf` (`ae59adf`–`4a1c928`) | Cold-boot `aim_restore_tmp` dummy-session fix before `restore.sh` (`#37`), Command Palette `Agent: Fast Resume (-c)` (`#38`), `~/.tmux.conf` `@resurrect-processes` `-c` command translations, workspace cleanup (`#39`), open-source path sanitization (`753cf35`), and `README.md` overhaul (`#40`–`#42`) | ✅ RESOLVED |
| `45f735d8` (`287be88`, `7a12a0a`) | Bootstrapped persistent `memory-wiki/` (`#43`) and fixed `@resurrect-processes` inline strategy quoting/tilde syntax (`"~agy->agy -c"`) (`#44`) | ✅ RESOLVED |
| `02feb6e8` (`#45`) | Pruned all 25 stale remote branches on `origin` while keeping `memory-wiki/` tracked on `master` (`#45`) | ✅ RESOLVED |
| `bd07ebad` (`3ff2115`, `f3c2f61`) | Documented cold-boot microservice/MCP/tunnel auto-resurrection (`#46`), closed legacy issues (`#21`–`#36`), synchronized docs across both `aim-tmux-dashboard` (`#50`) and `aim-cron-dashboard` (`#14`), and executed cold-vault dehydration (`1.30 GB` reclaimed) for `aim-cron-dashboard#15` | ✅ RESOLVED |
| `v1.0.0` (`140178a`–`93a7065`) | **Shipped `v1.0.0` GA:** Empty-Save Guardrail (`ConfirmSaveModal`, `#47`), Command Palette & `o` hotkey Spotlight Git Project Launcher (`ProjectLauncherProvider`, `#48`), multi-window `[A.I.]` parent badge bubbling & shell-safe/idle-pane-reusing `Agent: Fast Resume (-c)` (`#49`), `14/14` automated unit test suite wired into GitHub Actions CI, and `v1.0.0` GitHub Release tag | ✅ RESOLVED |

*(Keep clean and consolidated. Point to `memory-wiki/` and GitHub issues for deep history — do not re-audit.)*

---

## 1. PROJECT IDENTITY
`aim-tmux-dashboard` (`aim-dash`) is a Python Textual TUI for orchestrating `tmux` workspaces, viewing live ANSI pane previews, launching local Git repositories (`o` / `Ctrl+P`), extracting tokens from scrollback (`t` / `--grab`), persisting workspace state safely via `tmux-resurrect` (with Empty-Save Guardrail), and fast-resuming local AI coding agents (`agy`, `grok`, `codex`, `opencode`) and background services (`~python3`, `~node`, `~cloudflared`).
- **Repository Root:** `~/aim-tmux-dashboard`
- **Remote Origin:** `https://github.com/BrianV1981/aim-tmux-dashboard.git` (default branch: `master`, release: [`v1.0.0`](https://github.com/BrianV1981/aim-tmux-dashboard/releases/tag/v1.0.0))
- **Global Symlink:** `~/.local/bin/aim-dash` (or `/usr/local/bin/aim-dash`) -> `~/aim-tmux-dashboard/bin/aim-dash`

### Your Knowledge Base
- `~/aim-tmux-dashboard/memory-wiki/index.md` — Master catalog for the persistent project wiki.
- `~/aim-tmux-dashboard/memory-wiki/pages/architecture.md` — Component map of `bin/dashboard.py`, `TmuxManager`, `ProjectLauncherProvider`, `ConfirmSaveModal`, and layout providers.
- `~/aim-tmux-dashboard/memory-wiki/pages/session_persistence_and_resurrect.md` — `tmux-resurrect` integration, Empty-Save Guardrail (`#47`), `aim_restore_tmp` cold-boot fix (`#37`), and microservice/tunnel auto-resurrection (`#46`).
- `~/aim-tmux-dashboard/memory-wiki/pages/ai_agent_integration.md` — `[A.I.]` badge bubbling (`#49`), shell-safe `Agent: Fast Resume (-c)` (`#38`, `#49`), and `~/.tmux.conf` `@resurrect-processes` `-c` command translation rules (`#44`).
- `~/aim-tmux-dashboard/memory-wiki/pages/roadmap_and_concepts.md` — Synthesized `v1.0.0` GA capabilities and `v2.0` backlog (`#51`).

---

## 2. YOUR MISSION: STANDBY / FUTURE `v2.0` ENGINE TRACK (`#51`)
`v1.0.0` General Availability is live on `master` with `14/14` unit tests passing and `0` open `v1.0` issues. Stand by for the Operator's explicit directive before modifying code.

### Execution Queue (in order)
#### 1️⃣ Issue `#51` — `v2.0` Async `tmux -C` Control Mode Backend *(On Explicit Operator Directive Only)*
**Problem:** `TmuxManager` currently spawns synchronous `subprocess.run` processes (`tmux list-panes -a -F`, `tmux capture-pane`) on every hierarchy refresh and 1.0s live preview poll.
**Fix:** When the Operator initiates the `v2.0` milestone, migrate `TmuxManager` to an `asyncio` stream attached to persistent `tmux -C` Control Mode for zero-polling event-driven state updates (`%sessions-changed`, `%window-add`, `%output`).
**Key files:** `~/aim-tmux-dashboard/bin/dashboard.py`, `~/aim-tmux-dashboard/tests/test_dashboard.py`, `~/aim-tmux-dashboard/docs/ROADMAP_v2.md`

---

## 3. DETAILED ANALYSIS / BREAKDOWN
- **`TmuxManager` (`bin/dashboard.py`):** Encapsulates all `tmux` interactions: `get_hierarchy()` (`@@@`-delimited single-call query), `session_has_ai_agent()`, `capture_pane()` (ANSI preview), `capture_pane_scrollback()` (`-10000` lines), `get_saved_resurrect_session_count()` + `should_warn_before_save()` (`#47`), `discover_git_repos()` + `ensure_project_session()` (`#48`), and `fast_resume_agent()` (`#49`). When implementing `#51`, preserve synchronous helpers (or wrap behind an adapter) so `--grab` one-shot mode and `unittest` mocks stay fast and deterministic.
- **Session Tree & AI Visibility (`TmuxDashboard.refresh_sessions()`):** Flattens 1-window/1-pane sessions into single leaf nodes (`◆ <session> [<cmd>]`) while expanding multi-window/multi-pane hierarchies and bubbling `[bold cyan][A.I.][/bold cyan]` badges up to parent `◆ <session>` nodes (`#49`).
- **Command Palette Providers & Safety Modals:**
  - `ProjectLauncherProvider` (`o` hotkey or `Ctrl+P` -> `Project: Open Git Repo...`, `#48`): Depth-2 local Git scan skipping `.bak`/`venv`/`node_modules`, sorting `[ACTIVE]` sessions ahead of `[OFFLINE]` repos.
  - `ConfirmSaveModal` (`#47`): Blocks accidental cold-boot overwrites when `active_count <= 1` or `active_count <= saved_count // 2` across `~/.local/share/tmux/resurrect/last` and `~/.tmux/resurrect/last`.
  - `fast_resume_agent()` (`#38`, `#49`): Reuses idle shells (`bash`/`zsh`/`sh`/`fish`) via `send-keys` or wraps new windows in `bash -ic '<agent> -c; exec bash'` so exiting an agent never kills the window.
  - `TokenGrabberModal` (`t` / `--grab`), `LayoutCommandProvider` (4 layouts + `[` `]` split sizing in `~/.aim_dashboard.json`), and `TmuxKeysScreen` (`Keys (TMUX)`).
- **Automated Test Suite (`tests/test_dashboard.py`):** `14/14` unit tests across `TestEmptySaveGuardrail`, `TestGitProjectDiscovery`, `TestMultiWindowAIBadgeAndFastResume`, and `TestCodebaseAndDocumentationParity` (enforcing zero hardcoded host paths and zero broken relative markdown links), executed automatically via `.github/workflows/test.yml`.

---

## 4. IMPLEMENTATION STRATEGY
1. **Strict GitOps Lifecycle:** Every code or non-wiki documentation change MUST follow:
   - `./aim bug "<Title>" --context "..." --failure "..." --intent "..."`
   - `./aim fix <id>` (spawns `~/aim-tmux-dashboard/workspace/issue-<id>` on branch `fix/issue-<id>`)
   - Write/run `unittest` tests first in `tests/test_dashboard.py` inside `workspace/issue-<id>`
   - Verify `git branch --show-current` is `fix/issue-<id>` (never `master`/`main`)
   - Surgical `git add <files>` (use `git add -f memory-wiki/` when updating `memory-wiki/` since `memory-wiki/` is listed in `.gitignore`)
   - `./aim push "Prefix: <msg> (Closes #<id>)"`
   - Prompt Operator via `ask_question` before running `echo "yes" | ./aim promote`
   - Delete temporary remote branches (`git push origin --delete fix/issue-<id> archive-fix/...`) after promotion so `origin` stays clean.
2. **TDD Verification:** Run `./venv/bin/python3 -m py_compile bin/dashboard.py && ./venv/bin/python3 -m unittest discover -s tests -v` before every push (never test destructively against the live `tmux` server).

---

## 5. THE CRITICAL TRAPS & WARNINGS
> **⚠️ EPISTEMIC / OPERATIONAL WARNINGS**
1. **NEVER KILL THE TMUX SERVER:** You are strictly forbidden from running `tmux kill-server` under any circumstances (`AGENTS.md` §8.3).
2. **Default Branch is `master` (Not `main`):** Remote `origin` uses `master` as its default branch (`git pull --rebase --autostash origin master` / `git push origin master`).
3. **YOLO Restraint (Inquiries vs. Directives):** When the Operator asks a question, requests status, or shares an observation, answer and **STOP** (`AGENTS.md` §2).
4. **`.gitignore` Local Exclusions & `memory-wiki/`:** `memory-wiki/` is listed in `.gitignore` (requiring `git add -f memory-wiki/`), and `.gitignore` carries local unstaged exclusions for `joshua_os/` and `aim` — never run `git add .` or `git commit -a`, and always keep `--autostash` when rebasing.
5. **Worktree `VERSION` / `CHANGELOG.md` Side Effect:** Running `./aim push` inside `workspace/issue-<id>` can bump `VERSION` and `CHANGELOG.md` in the root checkout; check `git status` in root and reset unintended root modifications before `./aim promote`.
6. **Open-Source Sanitization:** Never commit hardcoded host paths or private domains in any tracked file (`TestCodebaseAndDocumentationParity` enforces this automatically).

---

## 6. KEY PATHS
- **Application & Entrypoints:** `~/aim-tmux-dashboard/bin/dashboard.py`, `~/aim-tmux-dashboard/bin/aim-dash`
- **Automated Tests & CI (`14/14` passing):** `~/aim-tmux-dashboard/tests/test_dashboard.py`, `~/aim-tmux-dashboard/.github/workflows/test.yml`
- **Public Documentation & Release Metadata:** `~/aim-tmux-dashboard/README.md`, `~/aim-tmux-dashboard/CHANGELOG.md`, `~/aim-tmux-dashboard/VERSION`
- **Roadmaps & Design Concepts:** `~/aim-tmux-dashboard/docs/ROADMAP_v2.md`, `~/aim-tmux-dashboard/docs/UNIVERSAL_LAUNCHER_CONCEPT.md`, `~/aim-tmux-dashboard/docs/HANDOFF_GAMEPLAN.md`
- **Persistent Memory Wiki:** `~/aim-tmux-dashboard/memory-wiki/index.md`, `~/aim-tmux-dashboard/memory-wiki/log.md`, `~/aim-tmux-dashboard/memory-wiki/pages/`
- **Host User Configs:** `~/.tmux.conf`, `~/.aim_dashboard.json`, `~/.local/share/tmux/resurrect/last`

---

## 7. THE FULL PICTURE / WHAT COMES AFTER
- **`v1.0.0` General Availability (Complete):** Full TUI workspace manager, `tmux-resurrect` cold-boot orchestration + Empty-Save Guardrail (`#47`), Spotlight Git Project Launcher (`#48`), multi-window AI badge bubbling + shell-safe Fast Resume (`#49`), and CI-backed unit tests.
- **`v2.0` Async Control Mode (`#51`):** Event-driven `tmux -C` streaming engine eliminating polling subprocess overhead.
- **Sibling Ecosystem Separation:** Cron scheduling lives exclusively in the standalone `~/aim-cron-dashboard` (`BrianV1981/aim-cron-dashboard`) repository per `#18` — never re-introduce cron management into `aim-tmux-dashboard`.
- **Intentionally Deferred / Rejected Ideas:** Real-time token/cost scraping in tree rows (latency risk), per-row `git status` subprocess badges (latency risk), and 5-minute background autosaves (redundant with `tmux-resurrect` + Empty-Save Guardrail).

---

## 8. OPERATOR PREFERENCES
- **Elevated Operator Role:** Handle all mechanics, syntax, and implementation details autonomously; only ask the Operator for high-level product, UX, or architectural trade-off decisions.
- **Non-Negotiable TDD:** Write and run `unittest` verification for every change; prove behavior empirically rather than guessing.
- **Strict Scope & Push Discipline:** Never push code changes directly to `master` (only `memory-wiki/` and `HANDOFF.md` carry the living-memory direct-push exemption). Always prune temporary `fix/issue-*` and `archive-fix/*` branches after promotion.
- **Communication Style:** Concise, direct, zero fluff, visible lists capped to 5 items, clickable `file://` links, and a plain conversational `🔊 <spoken summary>` block at the end of every response.

---

## 9. IMMEDIATE NEXT STEPS
1. Read `~/aim-tmux-dashboard/HANDOFF.md` and `~/aim-tmux-dashboard/memory-wiki/index.md`.
2. Run `./venv/bin/python -m unittest discover -s tests -v && git status -sb && gh issue list --state open` to confirm `v1.0.0` baseline (`14/14` tests passing, only `#51` open).
3. Await the Operator's explicit directive before opening a ticket or worktree.
