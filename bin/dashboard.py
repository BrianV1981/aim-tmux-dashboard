#!/usr/bin/env python3
import subprocess
import os
import sys
import re
import time
from textual.app import App, ComposeResult
from textual import on
from textual.widgets.option_list import Option
from textual.widgets import Header, OptionList, Footer, Tree, Label, Static, Input, Button
from textual.containers import Horizontal, Vertical, Container
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.command import Provider, Hit
from rich.text import Text

class TmuxManager:
    """Wrapper for tmux commands."""
    
    @staticmethod
    def get_hierarchy():
        """Returns a nested dict representing sessions -> windows -> panes."""
        try:
            result = subprocess.run(
                ["tmux", "list-panes", "-a", "-F", "#{session_name}@@@#{session_attached}@@@#{window_id}@@@#{window_name}@@@#{window_active}@@@#{pane_id}@@@#{pane_current_command}@@@#{pane_active}"],
                capture_output=True, text=True, check=True
            )
            sessions = {}
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                parts = line.split('@@@')
                if len(parts) == 8:
                    s_name, s_attached, w_id, w_name, w_active, p_id, p_cmd, p_active = parts
                    
                    if s_name not in sessions:
                        sessions[s_name] = {"attached": int(s_attached) > 0, "windows": {}}
                    
                    if w_id not in sessions[s_name]["windows"]:
                        sessions[s_name]["windows"][w_id] = {"name": w_name, "active": int(w_active) > 0, "panes": []}
                        
                    sessions[s_name]["windows"][w_id]["panes"].append({
                        "id": p_id,
                        "cmd": p_cmd,
                        "active": int(p_active) > 0
                    })
            return sessions
        except subprocess.CalledProcessError:
            return {}

    @staticmethod
    def new_session(name: str):
        subprocess.run(["tmux", "new-session", "-d", "-s", name])

    @staticmethod
    def kill_session(name: str):
        subprocess.run(["tmux", "kill-session", "-t", name])

    @staticmethod
    def rename_session(old_name: str, new_name: str):
        subprocess.run(["tmux", "rename-session", "-t", old_name, new_name])

    @staticmethod
    def capture_pane_scrollback(name: str) -> str:
        """Capture the entire scrollback history without colors."""
        try:
            result = subprocess.run(
                ["tmux", "capture-pane", "-S", "-10000", "-p", "-t", name],
                capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return ""

    @staticmethod
    def capture_pane(name: str) -> str:
        """Capture the visible contents of the target session/window/pane."""
        try:
            # -e includes escape sequences (colors), -p prints to stdout
            result = subprocess.run(
                ["tmux", "capture-pane", "-e", "-p", "-t", name],
                capture_output=True, text=True, check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return "Unable to capture pane (target might be dead or empty)."



class TokenGrabberModal(ModalScreen[str]):
    """Modal dialog to fuzzy search and extract tokens."""

    def __init__(self, target_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_name = target_name
        self.tokens = []

    CSS = """
    TokenGrabberModal {
        align: center middle;
        background: $background 50%;
    }
    #token-dialog {
        width: 80;
        height: 80%;
        padding: 1 2;
        background: $surface;
        border: round $accent;
        box-sizing: border-box;
    }
    #token-list {
        height: 1fr;
        margin-top: 1;
    }
    """

    BINDINGS = [("escape", "cancel", "Cancel")]

    def compose(self) -> ComposeResult:
        from textual.containers import Vertical
        from textual.widgets import Label, Input, OptionList
        with Vertical(id="token-dialog"):
            yield Label(f"Extracted Tokens for '{self.target_name}'", classes="bold")
            yield Input(id="token-search", placeholder="Search tokens...")
            yield OptionList(id="token-list")

    def on_mount(self) -> None:
        raw_text = TmuxManager.capture_pane_scrollback(self.target_name)
        
        urls = re.findall(r'https?://[^\s\'"<>]+', raw_text)
        ips = re.findall(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', raw_text)
        hashes = re.findall(r'\b[0-9a-fA-F]{7,40}\b', raw_text)
        
        clean_urls = []
        for url in urls:
            if "token=" in url.lower() or "key=" in url.lower() or "secret=" in url.lower():
                clean_urls.append(url.split("=")[0] + "=[REDACTED]")
            else:
                clean_urls.append(url)
                
        all_tokens = list(dict.fromkeys(clean_urls + ips + hashes))
        self.tokens = all_tokens
        
        self.populate_list(self.tokens)
        self.query_one("#token-search").focus()

    def populate_list(self, tokens: list[str]) -> None:
        from textual.widgets.option_list import Option
        token_list = self.query_one("#token-list")
        token_list.clear_options()
        for t in tokens:
            token_list.add_option(Option(t))

    @on(Input.Changed, "#token-search")
    def on_search(self, event: Input.Changed) -> None:
        query = event.value.lower()
        filtered = [t for t in self.tokens if query in t.lower()]
        self.populate_list(filtered)

    @on(Input.Submitted, "#token-search")
    def on_submit(self) -> None:
        self.query_one("#token-list").focus()

    @on(OptionList.OptionSelected, "#token-list")
    def on_token_selected(self, event) -> None:
        self.dismiss(str(event.option.prompt))

    def action_cancel(self) -> None:
        self.dismiss("")

class ConfirmKillModal(ModalScreen[bool]):
    """Modal dialog to confirm session deletion."""

    def __init__(self, session_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session_name = session_name

    CSS = """
    ConfirmKillModal {
        align: center middle;
        background: $background 50%;
    }
    #confirm-dialog {
        width: 40;
        height: auto;
        padding: 1 2;
        background: $surface;
        border: round $error;
    }
    .buttons {
        width: 100%;
        layout: horizontal;
        align: center middle;
        margin-top: 1;
    }
    Button {
        margin: 0 1;
    }
    """

    BINDINGS = [("escape", "cancel", "Cancel")]

    def compose(self) -> ComposeResult:
        with Vertical(id="confirm-dialog"):
            yield Label(f"Are you sure you want to kill session\n'{self.session_name}'?")
            with Horizontal(classes="buttons"):
                yield Button("Yes (Kill)", variant="error", id="btn-yes")
                yield Button("Cancel", variant="primary", id="btn-no")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-yes":
            self.dismiss(True)
        else:
            self.dismiss(False)

    def action_cancel(self) -> None:
        self.dismiss(False)


class NewSessionModal(ModalScreen[str]):
    """Modal dialog to get a new session name."""

    CSS = """
    NewSessionModal {
        align: center middle;
        background: $background 50%;
    }
    #dialog {
        width: 40;
        height: auto;
        padding: 1 2;
        background: $surface;
        border: round $primary;
    }
    """

    BINDINGS = [("escape", "cancel", "Cancel")]

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label("Enter new session name:")
            yield Input(placeholder="session-name", id="name-input")

    def on_mount(self) -> None:
        self.query_one(Input).focus()

    @on(Input.Submitted)
    def on_input_submitted(self, event: Input.Submitted) -> None:
        name = event.value.strip()
        if name:
            self.dismiss(name)
        else:
            self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)


class RenameSessionModal(ModalScreen[str]):
    """Modal dialog to rename a session."""

    def __init__(self, current_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_name = current_name

    CSS = """
    RenameSessionModal {
        align: center middle;
        background: $background 50%;
    }
    #rename-dialog {
        width: 40;
        height: auto;
        padding: 1 2;
        background: $surface;
        border: round $primary;
    }
    """

    BINDINGS = [("escape", "cancel", "Cancel")]

    def compose(self) -> ComposeResult:
        with Vertical(id="rename-dialog"):
            yield Label(f"Rename session '{self.current_name}':")
            yield Input(value=self.current_name, id="rename-input")

    def on_mount(self) -> None:
        inp = self.query_one(Input)
        inp.focus()
        inp.cursor_position = len(self.current_name)

    @on(Input.Submitted)
    def on_input_submitted(self, event: Input.Submitted) -> None:
        name = event.value.strip()
        if name and name != self.current_name:
            self.dismiss(name)
        else:
            self.dismiss(None)

    def action_cancel(self) -> None:
        self.dismiss(None)








class TmuxKeysScreen(ModalScreen):
    """Side panel displaying Tmux keys cheat sheet."""
    
    CSS = """
    TmuxKeysScreen {
        align: right top;
        background: transparent;
    }
    #tmux-keys-panel {
        width: 45;
        height: 100%;
        background: $surface;
        border-left: vkey $primary;
        padding: 1 2;
        overflow-y: auto;
    }
    .tk-category {
        text-style: bold;
        color: $accent;
        margin-top: 1;
        margin-bottom: 1;
    }
    .tk-row {
        layout: horizontal;
        width: 100%;
    }
    .tk-desc {
        width: 1fr;
    }
    .tk-key {
        width: 15;
        color: $secondary;
        text-align: right;
    }
    """

    BINDINGS = [("escape", "dismiss", "Close")]

    def compose(self) -> ComposeResult:
        with Vertical(id="tmux-keys-panel"):
            yield Label("Tmux Cheat Sheet", classes="bold")
            
            categories = {
                "Panes": [
                    ("Split vertically", "prefix + %"),
                    ("Split horizontally", 'prefix + "'),
                    ("Navigate", "prefix + arrows"),
                    ("Close pane", "prefix + x"),
                    ("Zoom pane", "prefix + z"),
                    ("Swap pane up", "prefix + {"),
                    ("Swap pane down", "prefix + }"),
                ],
                "Windows": [
                    ("New window", "prefix + c"),
                    ("Next window", "prefix + n"),
                    ("Prev window", "prefix + p"),
                    ("Rename window", "prefix + ,"),
                    ("Kill window", "prefix + &"),
                    ("List windows", "prefix + w"),
                ],
                "Sessions": [
                    ("New session", "tmux new -s name"),
                    ("Detach", "prefix + d"),
                    ("List sessions", "prefix + s"),
                    ("Rename session", "prefix + $"),
                ]
            }
            
            for cat, keys in categories.items():
                yield Label(cat, classes="tk-category")
                for desc, key in keys:
                    with Horizontal(classes="tk-row"):
                        yield Label(desc, classes="tk-desc")
                        yield Label(key, classes="tk-key")

    def action_dismiss(self) -> None:
        self.dismiss()

class LayoutCommandProvider(Provider):
    async def discover(self) -> Hit:
        matcher = self.matcher("")
        async for hit in self.search(""):
            yield hit

    async def search(self, query: str) -> Hit:
        matcher = self.matcher(query)
        app = self.app
        layouts = [
            ("Side-by-Side (List Left)", "horizontal", False),
            ("Side-by-Side (List Right)", "horizontal", True),
            ("Stacked (List Top)", "vertical", False),
            ("Stacked (List Bottom)", "vertical", True),
        ]
        for layout_name, orientation, swapped in layouts:
            action = lambda o=orientation, s=swapped: app.action_set_layout(o, s)
            if not query:
                yield Hit(1.0, layout_name, action, help=f"Switch to {layout_name}")
                continue
            score = matcher.match(layout_name)
            if score > 0:
                yield Hit(score, matcher.highlight(layout_name), action, help=f"Switch to {layout_name}")

class TmuxDashboard(App):
    COMMANDS = App.COMMANDS
    """A Textual TUI to manage tmux sessions."""

    def get_system_commands(self, screen):
        yield from super().get_system_commands(screen)
        yield ("UI Layouts...", "Switch structural window layouts", self.action_search_layouts, True)
        yield ("Keys (TMUX)", "Show tmux cheat sheet panel", self.action_show_tmux_keys, False)

    def action_search_layouts(self) -> None:
        from textual.command import CommandPalette
        self.push_screen(CommandPalette(providers=[LayoutCommandProvider], placeholder="Search Layouts..."))

    def action_show_tmux_keys(self) -> None:
        self.push_screen(TmuxKeysScreen())

    def __init__(self, popup_mode=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.popup_mode = popup_mode

    CSS = """
    Screen {
        background: $background;
        padding: 1 2;
    }
    #app-container {
        layout: horizontal;
        height: 100%;
        width: 100%;
    }
    #left-panel {
        width: 35%;
        border: round $primary-muted;
        height: 100%;
        background: $surface;
        padding: 0 1;
    }
    #left-panel:focus-within {
        border: round $accent;
    }
    #main-panel {
        width: 1fr;
        height: 1fr;
        border: round $secondary-muted;
        background: $surface;
        padding: 1 2;
        overflow-y: scroll;
    }
    #main-panel:focus-within {
        border: round $accent;
    }
    #preview-area {
        width: 100%;
        height: auto;
    }
    Tree {
        height: 1fr;
        padding-top: 1;
    }
    Input {
        border: tall $primary-muted;
        margin-bottom: 1;
    }
    Input:focus {
        border: tall $accent;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("n", "new_session", "New Session"),
        Binding("k", "kill_session", "Kill Selected"),
        Binding("e", "rename_session", "Rename"),
        Binding("a", "attach_session", "Attach (or Enter)"),
        Binding("r", "refresh", "Refresh"),
        Binding("/", "focus_search", "Search"),
        Binding("l", "toggle_live", "Toggle Live Preview"),
        Binding("t", "grab_tokens", "Token Grabber"),
        Binding("[", "shrink_pane", "Shrink Pane"),
        Binding("]", "expand_pane", "Expand Pane"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Container(id="app-container"):
            with Vertical(id="left-panel"):
                yield Input(id="search-input", placeholder="Filter sessions (/)")
                yield Tree("Tmux Sessions", id="session-tree")
            with Vertical(id="main-panel"):
                yield Static("Select a session, window, or pane on the left to preview.", id="preview-area")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "A.I.M. Sovereign Orchestrator"
        self.sub_title = "Tmux Session Manager (Tree View)"
        self.live_preview_timer = None
        self.pane_split_percent = 35
        self.current_layout = "horizontal"
        tree = self.query_one("#session-tree", Tree)
        tree.root.expand()
        self.refresh_sessions()
        tree.focus()  # Bypass search input, focus tree by default

    def format_cmd(self, cmd: str) -> str:
        """Add a high-visibility badge to known AI agent processes."""
        agents = ["agy", "aider", "claude", "grok", "gpt", "agent", "opencode", "gemini", "codex", "antigravity"]
        if any(agent in cmd.lower() for agent in agents):
            return f"[bold cyan][A.I.][/bold cyan] {cmd}"
        return cmd

    def refresh_sessions(self) -> None:
        """Fetch hierarchy from tmux and populate the tree."""
        tree = self.query_one("#session-tree", Tree)
        search_query = self.query_one("#search-input", Input).value.lower()
        
        # Save currently focused node name to attempt to restore focus
        focused_name = None
        if tree.cursor_node and tree.cursor_node.data:
            focused_name = tree.cursor_node.data.get('name')
        
        tree.clear()
        
        sessions = TmuxManager.get_hierarchy()
        node_to_focus = None
        
        for s_name, s_data in sessions.items():
            if search_query and search_query not in s_name.lower():
                continue
                
            s_status = " (Attached)" if s_data["attached"] else ""
            
            # Check for simple 1:1:1 session to dynamically flatten the tree
            windows = list(s_data["windows"].values())
            if len(windows) == 1 and len(windows[0]["panes"]) == 1:
                pane_cmd = self.format_cmd(windows[0]["panes"][0]["cmd"])
                session_node = tree.root.add(f"◆ {s_name} [{pane_cmd}]{s_status}", data={"type": "session", "name": s_name})
                if s_name == focused_name:
                    node_to_focus = session_node
            else:
                session_node = tree.root.add(f"◆ {s_name}{s_status}", data={"type": "session", "name": s_name}, expand=True)
                if s_name == focused_name:
                    node_to_focus = session_node
                
                for w_id, w_data in s_data["windows"].items():
                    w_status = " *" if w_data["active"] else ""
                    
                    if len(w_data["panes"]) == 1:
                        pane_cmd = self.format_cmd(w_data["panes"][0]["cmd"])
                        window_node = session_node.add(f"□ {w_data['name']} [{pane_cmd}]{w_status}", data={"type": "window", "name": w_id})
                        if w_id == focused_name:
                            node_to_focus = window_node
                    else:
                        window_node = session_node.add(f"□ {w_data['name']}{w_status}", data={"type": "window", "name": w_id}, expand=False)
                        if w_id == focused_name:
                            node_to_focus = window_node
                        
                        for p_data in w_data["panes"]:
                            p_status = " *" if p_data["active"] else ""
                            pane_cmd = self.format_cmd(p_data['cmd'])
                            pane_node = window_node.add(f"❯ {pane_cmd}{p_status}", data={"type": "pane", "name": p_data["id"]})
                            if p_data["id"] == focused_name:
                                node_to_focus = pane_node
                        
        if node_to_focus:
            tree.move_cursor(node_to_focus)
        else:
            tree.move_cursor(tree.root)

    @on(Input.Changed, "#search-input")
    def on_search_changed(self, event: Input.Changed) -> None:
        """Dynamically filter the session tree as the user types."""
        self.refresh_sessions()

    @on(Input.Submitted, "#search-input")
    def on_search_submitted(self, event: Input.Submitted) -> None:
        """Return focus to the tree when user hits enter in search."""
        self.query_one("#session-tree").focus()


    def update_pane_sizes(self) -> None:
        container = self.query_one("#app-container")
        left_panel = self.query_one("#left-panel")
        if getattr(self, "current_layout", "horizontal") == "horizontal":
            left_panel.styles.width = f"{self.pane_split_percent}%"
            left_panel.styles.height = "100%"
        else:
            left_panel.styles.height = f"{self.pane_split_percent}%"
            left_panel.styles.width = "100%"

    def action_shrink_pane(self) -> None:
        self.pane_split_percent = max(10, self.pane_split_percent - 5)
        self.update_pane_sizes()

    def action_expand_pane(self) -> None:
        self.pane_split_percent = min(90, self.pane_split_percent + 5)
        self.update_pane_sizes()

    def action_set_layout(self, layout_type: str, swap: bool) -> None:
        container = self.query_one("#app-container")
        left = self.query_one("#left-panel")
        main = self.query_one("#main-panel")
        
        container.styles.layout = layout_type
        self.current_layout = layout_type
        if swap:
            container.move_child(left, after=main)
        else:
            container.move_child(left, before=main)
        self.update_pane_sizes()

    def action_focus_search(self) -> None:
        """Focus the search input when / is pressed."""
        self.query_one("#search-input").focus()

    def action_refresh(self) -> None:
        """Manually refresh the tree."""
        self.refresh_sessions()
        self.notify("Roster refreshed.", title="A.I.M.")

    def action_toggle_live(self) -> None:
        """Toggle the 1-second polling loop for the preview pane."""
        if self.live_preview_timer is not None:
            self.live_preview_timer.stop()
            self.live_preview_timer = None
            self.notify("Live polling disabled.", title="A.I.M.")
        else:
            self.live_preview_timer = self.set_interval(1.0, self.update_preview)
            self.notify("Live polling enabled (1s interval).", title="A.I.M.")

    def action_new_session(self) -> None:
        """Prompt for a new session name and create it."""
        def check_name(name: str | None) -> None:
            if name:
                TmuxManager.new_session(name)
                self.refresh_sessions()
        self.push_screen(NewSessionModal(), check_name)

    def action_rename_session(self) -> None:
        """Rename the currently selected session."""
        tree = self.query_one("#session-tree", Tree)
        node = tree.cursor_node
        if node and node.data and node.data.get('type') == 'session':
            old_name = node.data['name']
            def check_rename(new_name: str | None) -> None:
                if new_name:
                    TmuxManager.rename_session(old_name, new_name)
                    self.refresh_sessions()
            self.push_screen(RenameSessionModal(old_name), check_rename)
        else:
            self.notify("You can only rename Sessions right now.", title="A.I.M.", severity="warning")

    def action_kill_session(self) -> None:
        """Prompt for confirmation, then kill the currently selected session."""
        tree = self.query_one("#session-tree", Tree)
        node = tree.cursor_node
        if node and node.data and node.data.get('type') == 'session':
            name = node.data['name']
            def check_kill(confirmed: bool) -> None:
                if confirmed:
                    TmuxManager.kill_session(name)
                    self.refresh_sessions()
            self.push_screen(ConfirmKillModal(name), check_kill)
        else:
            self.notify("You can only kill Sessions right now.", title="A.I.M.", severity="warning")


    def action_grab_tokens(self) -> None:
        """Extract tokens from scrollback and show fuzzy search popup."""
        tree = self.query_one("#session-tree")
        node = tree.cursor_node
        if node and node.data:
            target_name = node.data['name']
            
            def check_token(token: str) -> None:
                if token:
                    self.app.copy_to_clipboard(token)
                    self.notify(f"Copied to clipboard: {token}", title="A.I.M.")
            
            self.push_screen(TokenGrabberModal(target_name), check_token)

    @on(Tree.NodeHighlighted, "#session-tree")
    def on_node_highlighted(self, event: Tree.NodeHighlighted) -> None:
        """Instantly update the preview when the user highlights a node."""
        self.update_preview()

    def update_preview(self) -> None:
        """Fetch and render the pane contents for the currently highlighted node."""
        tree = self.query_one("#session-tree", Tree)
        preview_area = self.query_one("#preview-area", Static)

        if tree.cursor_node is not None and tree.cursor_node.data is not None:
            target_name = tree.cursor_node.data['name']
            
            raw_ansi_text = TmuxManager.capture_pane(target_name)
            rich_text = Text.from_ansi(raw_ansi_text)
            preview_area.update(rich_text)
        else:
            preview_area.update("Select a session, window, or pane to preview.")

    @on(Tree.NodeSelected, "#session-tree")
    def on_node_selected(self, event: Tree.NodeSelected) -> None:
        """Attach to target when Enter is pressed on it."""
        node = event.node
        if node and node.data:
            target_name = node.data['name']
            if self.popup_mode:
                subprocess.run(["tmux", "switch-client", "-t", target_name])
                self.exit()
            else:
                with self.suspend():
                    if "TMUX" in os.environ:
                        subprocess.run(["tmux", "switch-client", "-t", target_name])
                    else:
                        subprocess.run(["tmux", "attach", "-t", target_name])

    def action_attach_session(self) -> None:
        """Suspend the TUI and attach to the selected tmux target."""
        tree = self.query_one("#session-tree", Tree)
        node = tree.cursor_node
        if node and node.data:
            target_name = node.data['name']
            if self.popup_mode:
                subprocess.run(["tmux", "switch-client", "-t", target_name])
                self.exit()
            else:
                with self.suspend():
                    if "TMUX" in os.environ:
                        subprocess.run(["tmux", "switch-client", "-t", target_name])
                    else:
                        subprocess.run(["tmux", "attach", "-t", target_name])

class GrabApp(App):
    """A minimal app that launches the TokenGrabberModal directly."""
    
    def __init__(self, target_pane: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_pane = target_pane
        
    def on_mount(self) -> None:
        def check_token(token: str) -> None:
            if token:
                self.copy_to_clipboard(token)
                subprocess.run(["tmux", "display-message", f"Copied to clipboard: {token}"])
            self.exit()
            
        self.push_screen(TokenGrabberModal(self.target_pane), check_token)

if __name__ == "__main__":
    if "--grab" in sys.argv:
        # Fallback: get current pane if not provided
        target = subprocess.run(["tmux", "display-message", "-p", "#{pane_id}"], capture_output=True, text=True).stdout.strip()
        app = GrabApp(target)
        app.run()
    else:
        popup_mode = "--popup" in sys.argv
        app = TmuxDashboard(popup_mode=popup_mode)
        app.run()
