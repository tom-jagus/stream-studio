import threading
import unittest
from unittest.mock import Mock, patch

from stream_studio.keys_desktop import Desktop, TRANSITIONS


class DesktopTests(unittest.TestCase):
    def setUp(self):
        self.desktop = Desktop.__new__(Desktop)
        self.desktop._lock = threading.Lock()
        self.desktop._connected = True
        self.desktop._revision = 0
        self.desktop._keyboard_revision = 0
        self.desktop._reason = None
        self.desktop._updated = 10
        self.desktop._mapping = ("us", "", "omarchy:shift_caps_compose", 0)
        self.replies = {
            "monitors": [
                {"focused": False, "activeWorkspace": {"id": 9}, "specialWorkspace": {"id": 0}},
                {"focused": True, "activeWorkspace": {"id": 2}, "specialWorkspace": {"id": 0}},
            ],
            "locked": {"locked": False},
            "layers": {"DP-1": {"levels": {"3": []}}},
            "devices": {"keyboards": [{"name": "dh747-w-corne", "layout": "us",
                "variant": "", "options": "omarchy:shift_caps_compose", "active_layout_index": 0}]},
        }
        self.desktop._query = lambda command: self.replies[command]

    def observe(self, shell="false"):
        with patch("stream_studio.keys_desktop.subprocess.run",
                   return_value=Mock(returncode=0, stdout=shell)):
            return self.desktop._observe()[0]

    def test_active_window_events_do_not_suspend_but_safety_events_do(self):
        self.assertNotIn(b"activewindow", TRANSITIONS)
        self.assertNotIn(b"activewindowv2", TRANSITIONS)
        for event in (b"workspace", b"workspacev2", b"focusedmon",
                      b"activespecial", b"openlayer", b"closelayer",
                      b"activelayout", b"configreloaded"):
            self.assertIn(event, TRANSITIONS)

    def test_focus_change_does_not_invalidate_keyboard_mapping(self):
        self.desktop._invalidate()
        self.assertEqual(self.desktop.keyboard_revision(), 0)
        self.assertEqual(self.desktop._revision, 1)

    def test_mapping_change_and_ipc_loss_require_keyboard_recovery(self):
        self.desktop._invalidate(mapping_changed=True)
        self.assertEqual(self.desktop.keyboard_revision(), 1)
        self.desktop._invalidate(False)
        self.assertEqual(self.desktop.keyboard_revision(), 2)

    def test_focus_not_visibility_controls_gate(self):
        self.assertIsNone(self.observe())
        for monitor in self.replies["monitors"]:
            monitor["focused"] = not monitor["focused"]
        self.assertEqual(self.observe(), "Workspace not permitted")

    def test_both_lock_sources_suspend(self):
        self.assertEqual(self.observe("true"), "Screen locked")
        self.replies["locked"]["locked"] = True
        self.assertEqual(self.observe(), "Screen locked")

    def test_polkit_layer_suspends(self):
        self.replies["layers"]["DP-1"]["levels"]["3"].append({"namespace": "omarchy-polkit"})
        self.assertEqual(self.observe(), "Authentication prompt active")

    def test_invalid_shell_response_is_uncertain(self):
        with self.assertRaises(ValueError):
            self.observe("not a state")

    def test_stale_and_disconnected_state_is_rejected(self):
        with patch("stream_studio.keys_desktop.time.monotonic", return_value=10.1):
            self.assertIsNone(self.desktop.snapshot()[0])
            self.desktop._invalidate(False)
            self.assertIsNotNone(self.desktop.snapshot()[0])
        with patch("stream_studio.keys_desktop.time.monotonic", return_value=12):
            self.assertIsNotNone(self.desktop.snapshot()[0])


if __name__ == "__main__":
    unittest.main()
