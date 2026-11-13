import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from stream_studio.keys import Keys
from stream_studio.keys_capture import Capture


class CaptureEventTests(unittest.TestCase):
    def setUp(self):
        self.keys = Keys(clock=lambda: 0)
        self.keys.command("on")
        self.keys.observe(None)
        self.capture = Capture.__new__(Capture)
        self.capture.keys = self.keys
        self.capture._down = {"one": set(), "two": set()}
        self.capture._pending_modifiers = {}
        self.capture._state = Mock()
        self.capture._state.key_get_one_sym.return_value = 97
        self.capture._state.key_get_string.return_value = "a"
        self.codes = SimpleNamespace(
            EV_SYN=0, SYN_DROPPED=3, EV_KEY=1,
            KEY_LEFTCTRL=29, KEY_RIGHTCTRL=97, KEY_LEFTALT=56, KEY_RIGHTALT=100,
            KEY_LEFTMETA=125, KEY_RIGHTMETA=126, KEY_LEFTSHIFT=42, KEY_RIGHTSHIFT=54,
            KEY={30: "KEY_A"},
        )
        self.evdev = SimpleNamespace(ecodes=self.codes)
        self.xkb = SimpleNamespace(
            keysym_get_name=lambda _: "a",
            KeyDirection=SimpleNamespace(XKB_KEY_DOWN=1, XKB_KEY_UP=0),
        )

    def event(self, code=30, value=1, path="one", event_type=1):
        self.capture._event(path, SimpleNamespace(type=event_type, code=code, value=value),
                            self.evdev, self.xkb, self.keys.ticket())

    def test_press_repeat_and_release(self):
        self.event()
        self.event(value=2)
        self.event(value=0)
        self.assertEqual(self.keys.snapshot()["keys"], [
            {"text": "a", "parts": ["a"], "count": 1}
        ])
        self.assertEqual(self.capture._state.update_key.call_count, 2)

    def test_released_and_pressed_again_groups_on_third_press(self):
        self.event()
        self.event(value=0)
        self.event()
        self.assertEqual([entry["count"] for entry in self.keys.snapshot()["keys"]],
                         [1, 1])
        self.event(value=0)
        self.event()
        self.assertEqual(self.keys.snapshot()["keys"][0]["count"], 3)

    def test_duplicate_down_does_not_increment_count(self):
        self.event()
        self.event()
        self.assertEqual(self.keys.snapshot()["keys"][0]["count"], 1)

    def test_left_and_right_modifier_labels_are_normalized(self):
        self.capture._state.key_get_string.return_value = ""
        self.xkb.keysym_get_name = lambda _: "Super_L"
        self.event(code=self.codes.KEY_LEFTMETA)
        self.event(code=self.codes.KEY_LEFTMETA, value=0)
        self.xkb.keysym_get_name = lambda _: "Super_R"
        self.event(code=self.codes.KEY_RIGHTMETA)
        self.event(code=self.codes.KEY_RIGHTMETA, value=0)
        self.assertEqual(self.keys.snapshot()["keys"], [
            {"text": "Super", "parts": ["Super"], "count": 1},
            {"text": "Super", "parts": ["Super"], "count": 1},
        ])

    def test_ctrl_combination_does_not_show_standalone_modifier(self):
        self.event(code=self.codes.KEY_LEFTCTRL)
        self.assertEqual(self.keys.snapshot()["keys"], [])
        self.event()
        self.event(value=0)
        self.event(code=self.codes.KEY_LEFTCTRL, value=0)
        self.assertEqual(self.keys.snapshot()["keys"], [
            {"text": "Ctrl+a", "parts": ["Ctrl", "a"], "count": 1}
        ])

    def test_multi_modifier_combination_has_no_standalone_entries(self):
        self.event(code=self.codes.KEY_LEFTCTRL)
        self.event(code=self.codes.KEY_LEFTSHIFT)
        self.event(code=2)
        self.event(code=2, value=0)
        self.event(code=self.codes.KEY_LEFTSHIFT, value=0)
        self.event(code=self.codes.KEY_LEFTCTRL, value=0)
        self.assertEqual(self.keys.snapshot()["keys"], [
            {"text": "Ctrl+Shift+1", "parts": ["Ctrl", "Shift", "1"], "count": 1}
        ])

    def test_unused_modifiers_display_on_release(self):
        for code, label in [(29, "Ctrl"), (56, "Alt"), (125, "Super"), (42, "Shift")]:
            with self.subTest(label=label):
                self.event(code=code)
                self.event(code=code, value=2)
                self.event(code=code, value=0)
                self.assertEqual(self.keys.snapshot()["keys"][-1]["parts"], [label])
        self.assertEqual(len(self.keys.snapshot()["keys"]), 4)

    def test_modifier_pressed_before_suspension_is_not_replayed(self):
        self.event(code=29)
        self.keys.observe("Desktop transition")
        self.keys.observe(None)
        self.event(code=29, value=0)
        self.assertEqual(self.keys.snapshot()["keys"], [])
        self.assertEqual(self.capture._pending_modifiers, {})

    def test_suppressed_modifier_is_not_shown_on_release_after_resume(self):
        self.capture._event("one", SimpleNamespace(type=1, code=29, value=1),
                            self.evdev, self.xkb, None)
        self.event(code=29, value=0)
        self.assertEqual(self.keys.snapshot()["keys"], [])

    def test_cross_device_combination_uses_modifier_without_standalone_entry(self):
        self.event(code=29, path="one")
        self.event(path="two")
        self.event(code=29, value=0, path="one")
        self.assertEqual(self.keys.snapshot()["keys"][0]["parts"], ["Ctrl", "a"])
        self.assertEqual(len(self.keys.snapshot()["keys"]), 1)

    def test_unknown_repeat_is_rejected(self):
        with self.assertRaises(OSError):
            self.event(value=2)
        self.assertEqual(self.keys.snapshot()["keys"], [])

    def test_shared_key_is_not_released_until_both_devices_release(self):
        self.event(path="one")
        self.event(path="two")
        self.event(path="one", value=0)
        self.assertEqual(self.capture._state.update_key.call_count, 1)
        self.event(path="two", value=0)
        self.assertEqual(self.capture._state.update_key.call_count, 2)

    def test_overflow_requests_queue_reset(self):
        with self.assertRaises(OSError):
            self.event(code=self.codes.SYN_DROPPED, event_type=self.codes.EV_SYN)

    def test_suspended_press_updates_state_without_formatting_or_publishing(self):
        self.capture._event("one", SimpleNamespace(type=1, code=29, value=1),
                            self.evdev, self.xkb, None)
        self.assertIn(29, self.capture._down["one"])
        self.capture._state.key_get_string.assert_not_called()
        self.assertEqual(self.keys.snapshot()["keys"], [])
        self.capture._event("one", SimpleNamespace(type=1, code=29, value=0),
                            self.evdev, self.xkb, None)
        self.assertNotIn(29, self.capture._down["one"])

    def test_modified_digit_names_the_base_digit(self):
        self.capture._down["one"].update({29, 42})
        self.capture._state.key_get_string.return_value = "!"
        self.xkb.keysym_get_name = lambda _: "exclam"
        self.event(code=2)
        self.assertEqual(self.keys.snapshot()["keys"][0]["parts"], ["Ctrl", "Shift", "1"])

    def test_ctrl_digit_is_presented(self):
        self.capture._down["one"].add(29)
        self.capture._state.key_get_string.return_value = ""
        self.xkb.keysym_get_name = lambda _: "1"
        self.event(code=2)
        self.assertEqual(self.keys.snapshot()["keys"][0]["parts"], ["Ctrl", "1"])

    def test_focus_transition_retains_modifiers_and_discards_suspended_input(self):
        device = Mock()
        pending = []
        def read():
            events = list(pending)
            pending.clear()
            return iter(events)
        device.read.side_effect = read
        self.capture._devices = {"one": device}
        self.capture._revision = 0
        self.capture._keyboard_revision = 0
        self.capture._desktop = Mock()
        self.capture._desktop.keyboard_revision.return_value = 0
        self.capture._open = Mock()
        self.capture.close_devices = Mock()
        self.capture._down["one"].update({29, 42})
        self.keys.publish("old", self.keys.ticket())
        self.capture._desktop.snapshot.return_value = ("Desktop transition pending", None, 1)
        pending.append(SimpleNamespace(type=1, code=30, value=1))
        with patch("stream_studio.keys_capture.select.select",
                   side_effect=lambda *_: ([device] if pending else [], [], [])):
            self.capture._cycle(self.evdev, self.xkb)
            self.assertEqual(self.keys.snapshot()["keys"], [])
            self.assertEqual(self.capture._down["one"], {29, 42, 30})
            self.capture.close_devices.assert_not_called()
            # A release and another press already queued while suspended must
            # update state but must not be replayed when the gate reopens.
            pending.extend([SimpleNamespace(type=1, code=30, value=0),
                            SimpleNamespace(type=1, code=2, value=1)])
            self.capture._desktop.snapshot.return_value = (None, ("us",), 1)
            self.capture._cycle(self.evdev, self.xkb)
            self.assertEqual(self.keys.status()["state"], "presenting")
            self.assertEqual(self.keys.snapshot()["keys"], [])
            pending.extend([SimpleNamespace(type=1, code=2, value=0),
                            SimpleNamespace(type=1, code=3, value=1)])
            self.capture._cycle(self.evdev, self.xkb)
            self.assertEqual(self.keys.snapshot()["keys"][0]["parts"], ["Ctrl", "Shift", "2"])
            self.capture.close_devices.assert_not_called()

    def test_mapping_change_still_closes_devices(self):
        self.capture._revision = 0
        self.capture._keyboard_revision = 0
        self.capture._devices = {}
        self.capture._desktop = Mock()
        self.capture._desktop.snapshot.return_value = ("Desktop transition pending", None, 1)
        self.capture._desktop.keyboard_revision.return_value = 1
        self.capture.close_devices = Mock()
        self.capture._cycle(self.evdev, self.xkb)
        self.capture.close_devices.assert_called_once_with()
        self.assertEqual(self.keys.status()["state"], "suspended")

    def test_control_characters_are_replaced_by_key_labels(self):
        self.capture._down["one"].add(self.codes.KEY_LEFTCTRL)
        self.capture._state.key_get_string.return_value = "\x01"
        self.event()
        self.assertEqual(self.keys.snapshot()["keys"], [
            {"text": "Ctrl+a", "parts": ["Ctrl", "a"], "count": 1}
        ])


if __name__ == "__main__":
    unittest.main()
