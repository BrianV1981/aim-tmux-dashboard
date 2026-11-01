import importlib.util
import pathlib
import tempfile
import unittest
from unittest import mock

DASHBOARD_PATH = pathlib.Path(__file__).resolve().parents[1] / "bin" / "dashboard.py"
spec = importlib.util.spec_from_file_location("dashboard", str(DASHBOARD_PATH))
dashboard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dashboard)


class TestEmptySaveGuardrailIssue47(unittest.TestCase):
    def test_get_saved_resurrect_session_count_parses_xdg_and_legacy_last(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = pathlib.Path(tmp)
            xdg_dir = home / ".local" / "share" / "tmux" / "resurrect"
            xdg_dir.mkdir(parents=True)
            snap = xdg_dir / "tmux_resurrect_test.txt"
            snap.write_text(
                "pane\taim-dash\t0\t1\t:*\t0\n"
                "pane\taim-dash\t1\t0\t-\t0\n"
                "pane\taim-joshua\t0\t1\t:*\t0\n"
                "pane\taim-connect\t0\t1\t:*\t0\n"
                "window\taim-dash\t0\t:zsh\n",
                encoding="utf-8",
            )
            (xdg_dir / "last").symlink_to(snap.name)

            with mock.patch.object(dashboard.Path, "home", return_value=home):
                self.assertEqual(dashboard.TmuxManager.get_saved_resurrect_session_count(), 3)

    def test_get_saved_resurrect_session_count_returns_zero_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = pathlib.Path(tmp)
            with mock.patch.object(dashboard.Path, "home", return_value=home):
                self.assertEqual(dashboard.TmuxManager.get_saved_resurrect_session_count(), 0)

    def test_should_warn_before_save_triggers_on_low_or_dropped_sessions(self):
        warn, msg = dashboard.TmuxManager.should_warn_before_save(active_count=1, saved_count=12)
        self.assertTrue(warn)
        self.assertIn("1", msg)
        self.assertIn("12", msg)

        warn0, _ = dashboard.TmuxManager.should_warn_before_save(active_count=0, saved_count=0)
        self.assertTrue(warn0)

        warn_drop, _ = dashboard.TmuxManager.should_warn_before_save(active_count=2, saved_count=10)
        self.assertTrue(warn_drop)

        ok, _ = dashboard.TmuxManager.should_warn_before_save(active_count=10, saved_count=12)
        self.assertFalse(ok)

        ok_fresh, _ = dashboard.TmuxManager.should_warn_before_save(active_count=3, saved_count=0)
        self.assertFalse(ok_fresh)

    def test_action_save_tmux_state_pushes_confirm_modal_when_low_sessions(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = pathlib.Path(tmp)
            save_script = home / ".tmux" / "plugins" / "tmux-resurrect" / "scripts" / "save.sh"
            save_script.parent.mkdir(parents=True)
            save_script.write_text("#!/bin/bash\n", encoding="utf-8")

            app = dashboard.TmuxDashboard()
            pushed = []
            app.push_screen = lambda modal, cb=None: pushed.append((modal, cb))
            app.notify = mock.MagicMock()

            with (
                mock.patch.object(dashboard.Path, "home", return_value=home),
                mock.patch.object(dashboard.TmuxManager, "get_hierarchy", return_value={"only-one": {"attached": True, "windows": {}}}),
                mock.patch.object(dashboard.TmuxManager, "get_saved_resurrect_session_count", return_value=14),
                mock.patch.object(dashboard.subprocess, "Popen") as mock_popen,
            ):
                app.action_save_tmux_state()
                self.assertEqual(len(pushed), 1)
                modal, callback = pushed[0]
                self.assertIsInstance(modal, dashboard.ConfirmSaveModal)
                mock_popen.assert_not_called()

                # Cancel does not invoke save.sh
                callback(False)
                mock_popen.assert_not_called()

                # Confirm invokes save.sh
                callback(True)
                mock_popen.assert_called_once_with(["tmux", "run-shell", str(save_script)])

    def test_action_save_tmux_state_saves_immediately_when_healthy(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = pathlib.Path(tmp)
            save_script = home / ".tmux" / "plugins" / "tmux-resurrect" / "scripts" / "save.sh"
            save_script.parent.mkdir(parents=True)
            save_script.write_text("#!/bin/bash\n", encoding="utf-8")

            app = dashboard.TmuxDashboard()
            app.push_screen = mock.MagicMock()
            app.notify = mock.MagicMock()
            healthy_sessions = {f"sess-{i}": {"attached": False, "windows": {}} for i in range(8)}

            with (
                mock.patch.object(dashboard.Path, "home", return_value=home),
                mock.patch.object(dashboard.TmuxManager, "get_hierarchy", return_value=healthy_sessions),
                mock.patch.object(dashboard.TmuxManager, "get_saved_resurrect_session_count", return_value=10),
                mock.patch.object(dashboard.subprocess, "Popen") as mock_popen,
            ):
                app.action_save_tmux_state()
                app.push_screen.assert_not_called()
                mock_popen.assert_called_once_with(["tmux", "run-shell", str(save_script)])


class TestProjectLauncherIssue48(unittest.TestCase):
    def test_discover_git_repos_finds_depth1_and_depth2_and_skips_noise(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            # Depth 1 valid repo
            (root / "aim-alpha" / ".git").mkdir(parents=True)
            # Depth 2 valid repo (e.g. ~/projects/beta.app)
            (root / "projects" / "beta.app" / ".git").mkdir(parents=True)
            # Noise / backup / hidden / worktree dirs that MUST be ignored
            (root / "aim-alpha.bak" / ".git").mkdir(parents=True)
            (root / "old-backup-v1" / ".git").mkdir(parents=True)
            (root / ".hidden" / "secret-repo" / ".git").mkdir(parents=True)
            (root / "aim-alpha" / "workspace" / "issue-1" / ".git").mkdir(parents=True)
            (root / "archive" / "legacy-repo" / ".git").mkdir(parents=True)
            # Depth 3 should be ignored when max_depth=2
            (root / "a" / "b" / "too-deep" / ".git").mkdir(parents=True)

            repos = dashboard.TmuxManager.discover_git_repos(search_roots=[root], max_depth=2)
            names = [r["name"] for r in repos]
            self.assertEqual(names, ["aim-alpha", "beta.app"])
            beta = next(r for r in repos if r["name"] == "beta.app")
            self.assertEqual(beta["session_name"], "beta-app")

    def test_ensure_project_session_creates_when_offline_and_reuses_when_active(self):
        with (
            mock.patch.object(dashboard.TmuxManager, "get_hierarchy", return_value={"aim-alpha": {"attached": False, "windows": {}}}),
            mock.patch.object(dashboard.subprocess, "run") as mock_run,
        ):
            # Already active -> does not call new-session
            s_name, created = dashboard.TmuxManager.ensure_project_session("aim-alpha", "/tmp/aim-alpha")
            self.assertEqual(s_name, "aim-alpha")
            self.assertFalse(created)
            mock_run.assert_not_called()

            # Offline -> spawns detached session in repo directory
            s_name2, created2 = dashboard.TmuxManager.ensure_project_session("beta.app", "/tmp/beta.app")
            self.assertEqual(s_name2, "beta-app")
            self.assertTrue(created2)
            mock_run.assert_called_once_with(
                ["tmux", "new-session", "-d", "-s", "beta-app", "-c", "/tmp/beta.app"],
                check=True,
            )

    def test_project_launcher_provider_empty_and_fuzzy_queries(self):
        import asyncio

        fake_repos = [
            {"name": "aim-dash", "session_name": "aim-dash", "path": "/tmp/aim-dash"},
            {"name": "tbsoftwash-book", "session_name": "tbsoftwash-book", "path": "/tmp/tbsoftwash-book"},
        ]
        fake_hierarchy = {"aim-dash": {"attached": True, "windows": {}}}

        async def run_search():
            app = dashboard.TmuxDashboard(popup_mode=True)
            screen = mock.MagicMock()
            screen.app = app
            provider = dashboard.ProjectLauncherProvider(screen)
            with (
                mock.patch.object(dashboard.TmuxManager, "discover_git_repos", return_value=fake_repos),
                mock.patch.object(dashboard.TmuxManager, "get_hierarchy", return_value=fake_hierarchy),
            ):
                empty_hits = [h async for h in provider.search("")]
                self.assertEqual(len(empty_hits), 2)
                # Active repo sorts first
                self.assertIn("ACTIVE", str(empty_hits[0].text))
                self.assertIn("OFFLINE", str(empty_hits[1].text))

                filtered_hits = [h async for h in provider.search("softwash")]
                self.assertEqual(len(filtered_hits), 1)
                self.assertIn("tbsoftwash-book", str(filtered_hits[0].text))

        asyncio.run(run_search())


if __name__ == "__main__":
    unittest.main()
