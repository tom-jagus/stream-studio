import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from stream_studio.keys import Keys, MAX_KEYS, suspension_reason
from stream_studio.keys_control import Control, request


class KeysTests(unittest.TestCase):
    def setUp(self):
        self.now = 0.0
        self.keys = Keys(clock=lambda: self.now)

    def enable(self):
        self.keys.command("on")
        self.keys.observe(None)
        return self.keys.ticket()

    def test_starts_disabled_and_cannot_publish(self):
        self.keys.publish("secret", None)
        self.assertEqual(self.keys.status()["state"], "disabled")
        self.assertEqual(self.keys.snapshot()["keys"], [])

    def test_enabling_without_adapter_stays_suspended(self):
        self.assertEqual(self.keys.command("on")["state"], "suspended")
        self.assertIsNone(self.keys.ticket())

    def test_manual_off_closes_capture_and_revokes_tickets(self):
        close = Mock()
        self.keys.attach(close)
        ticket = self.enable()
        self.keys.publish("a", ticket)
        self.keys.command("off")
        close.assert_called_once_with()
        self.keys.observe(None)
        self.keys.publish("b", ticket)
        self.assertEqual(self.keys.snapshot()["keys"], [])
        self.assertEqual(self.keys.status()["state"], "disabled")
        self.enable()
        self.keys.publish("c", ticket)
        self.assertEqual(self.keys.snapshot()["keys"], [])

    def test_toggle_enables_then_disables_and_closes_capture(self):
        close = Mock()
        self.keys.attach(close)
        self.assertEqual(self.keys.command("toggle")["state"], "suspended")
        self.keys.observe(None)
        ticket = self.keys.ticket()
        self.keys.publish("a", ticket)
        self.assertEqual(self.keys.command("toggle")["state"], "disabled")
        close.assert_called_once_with()
        self.assertEqual(self.keys.snapshot()["keys"], [])
        self.keys.observe(None)
        self.keys.publish("b", ticket)
        self.assertEqual(self.keys.snapshot()["keys"], [])

    def test_toggle_while_suspended_disables_instead_of_enabling(self):
        close = Mock()
        self.keys.attach(close)
        self.enable()
        self.keys.observe("Workspace not permitted")
        self.assertEqual(self.keys.command("toggle")["state"], "disabled")
        close.assert_called_once_with()
        self.keys.observe(None)
        self.assertEqual(self.keys.status()["state"], "disabled")
        self.assertEqual(self.keys.command("toggle")["state"], "suspended")

    def test_suspension_discards_old_events_on_resume(self):
        ticket = self.enable()
        self.keys.publish("a", ticket)
        self.keys.observe("Workspace not permitted")
        self.assertEqual(self.keys.snapshot()["keys"], [])
        self.keys.observe(None)
        self.keys.publish("stale", ticket)
        self.assertEqual(self.keys.snapshot()["keys"], [])
        self.keys.publish("fresh", self.keys.ticket())
        self.assertEqual(self.keys.snapshot()["keys"], [
            {"text": "fresh", "parts": ["fresh"], "count": 1}
        ])

    def test_stale_observation_suspends_without_status_poll(self):
        ticket = self.enable()
        self.keys.publish("a", ticket)
        self.now = 1
        self.keys.observe(None)
        self.keys.publish("stale", ticket)
        self.assertEqual(self.keys.snapshot()["keys"], [])

    def test_stale_observation_clears_immediately_when_queried(self):
        ticket = self.enable()
        self.keys.publish("a", ticket)
        self.now = 1
        self.assertEqual(self.keys.status()["state"], "suspended")
        self.assertEqual(self.keys.snapshot()["keys"], [])

    def test_buffer_is_bounded_and_temporary(self):
        ticket = self.enable()
        for index in range(100):
            self.keys.publish(str(index), ticket)
        self.assertEqual(len(self.keys.snapshot()["keys"]), MAX_KEYS)
        self.now = 5
        self.keys.observe(None)
        self.assertEqual(self.keys.snapshot()["keys"], [])

    def test_only_consecutive_presses_are_grouped(self):
        ticket = self.enable()
        for text in ["j", "j", "j", "w", "j"]:
            self.keys.publish(text, ticket)
        entries = self.keys.snapshot()["keys"]
        self.assertEqual([(entry["text"], entry["count"]) for entry in entries],
                         [("j", 3), ("w", 1), ("j", 1)])

    def test_two_presses_stay_separate_then_third_collapses_them(self):
        ticket = self.enable()
        for text in ["l", "o", "o"]:
            self.keys.publish(text, ticket)
        self.assertEqual([(entry["text"], entry["count"])
                          for entry in self.keys.snapshot()["keys"]],
                         [("l", 1), ("o", 1), ("o", 1)])
        self.keys.publish("o", ticket)
        self.assertEqual([(entry["text"], entry["count"])
                          for entry in self.keys.snapshot()["keys"]],
                         [("l", 1), ("o", 3)])
        self.keys.publish("o", ticket)
        self.assertEqual(self.keys.snapshot()["keys"][-1]["count"], 4)

    def test_third_press_collapses_at_capacity_without_losing_older_entry(self):
        ticket = self.enable()
        for index in range(MAX_KEYS - 2):
            self.keys.publish(str(index), ticket)
        self.keys.publish("o", ticket)
        self.keys.publish("o", ticket)
        self.assertEqual(len(self.keys.snapshot()["keys"]), 11)
        self.keys.publish("o", ticket)
        entries = self.keys.snapshot()["keys"]
        self.assertEqual(len(entries), 10)
        self.assertEqual(entries[0]["text"], "0")
        self.assertEqual(entries[-1]["count"], 3)

    def test_suspension_breaks_two_press_sequence(self):
        ticket = self.enable()
        self.keys.publish("o", ticket)
        self.keys.publish("o", ticket)
        self.keys.observe("Workspace not permitted")
        self.keys.observe(None)
        self.keys.publish("o", self.keys.ticket())
        self.assertEqual([entry["count"] for entry in self.keys.snapshot()["keys"]], [1])

    def test_expired_pair_does_not_join_new_press(self):
        self.enable()
        self.keys.publish("o", self.keys.ticket())
        self.keys.publish("o", self.keys.ticket())
        for tick in range(1, 12):
            self.now = tick * 0.4
            self.keys.observe(None)
        self.keys.publish("o", self.keys.ticket())
        self.assertEqual([entry["count"] for entry in self.keys.snapshot()["keys"]], [1])

    def test_matching_press_refreshes_lifetime(self):
        self.enable()
        self.keys.publish("j", self.keys.ticket())
        for tick in range(1, 8):
            self.now = tick * 0.4
            self.keys.observe(None)
        self.keys.publish("j", self.keys.ticket())
        for tick in range(8, 12):
            self.now = tick * 0.4
            self.keys.observe(None)
        self.assertEqual([entry["count"] for entry in self.keys.snapshot()["keys"]],
                         [1, 1])

    def test_snapshot_does_not_expose_mutable_parts(self):
        self.enable()
        self.keys.publish("+", self.keys.ticket(), parts=["+"])
        self.keys.snapshot()["keys"][0]["parts"].append("changed")
        self.assertEqual(self.keys.snapshot()["keys"][0]["parts"], ["+"])

    def test_oldest_entry_is_removed_at_limit(self):
        ticket = self.enable()
        for index in range(MAX_KEYS + 1):
            self.keys.publish(str(index), ticket)
        self.assertEqual(self.keys.snapshot()["keys"][0]["text"], "1")

    def test_status_has_no_keys(self):
        ticket = self.enable()
        self.keys.publish("private", ticket)
        self.assertEqual(set(self.keys.status()), {"state", "reason"})

    def test_workspace_and_uncertainty_policy(self):
        base = dict(special=False, locked=False, prompt=False, ipc_connected=True)
        for workspace in range(1, 6):
            self.assertIsNone(suspension_reason(workspace, **base))
        for workspace in [0, 6, 7, 8, 9, 10, 11, None]:
            self.assertIsNotNone(suspension_reason(workspace, **base))
        for key, value in [("special", True), ("locked", True), ("locked", None),
                           ("prompt", True), ("prompt", None), ("ipc_connected", False)]:
            self.assertIsNotNone(suspension_reason(1, **{**base, key: value}))


class ControlTests(unittest.TestCase):
    def test_private_control_reports_no_key_history(self):
        with tempfile.TemporaryDirectory() as temporary:
            with patch.dict("os.environ", {"XDG_RUNTIME_DIR": temporary}):
                control = Control(Keys())
                try:
                    path = Path(temporary) / "stream-studio/keys.sock"
                    self.assertEqual(path.stat().st_mode & 0o777, 0o600)
                    self.assertEqual(request("status")["state"], "disabled")
                    self.assertEqual(request("on")["state"], "suspended")
                    self.assertEqual(request("toggle")["state"], "disabled")
                    self.assertEqual(request("toggle")["state"], "suspended")
                    self.assertEqual(request("off")["state"], "disabled")
                    self.assertNotIn("keys", request("status"))
                    with self.assertRaises(OSError):
                        Control(Keys())
                finally:
                    control.close()
                self.assertFalse(path.exists())


if __name__ == "__main__":
    unittest.main()
