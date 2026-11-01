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


if __name__ == "__main__":
    unittest.main()
