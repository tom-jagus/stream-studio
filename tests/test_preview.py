import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from stream_studio import preview


class PreviewTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        patcher = patch("stream_studio.preview.runtime_directory", return_value=Path(self.temporary.name))
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_observed_chromium_class_requires_dedicated_process(self):
        clients = [
            {"address": "0x123", "initialClass": preview.CHROMIUM_APP_CLASS, "pid": 10},
            {"address": "0x456", "initialClass": preview.CHROMIUM_APP_CLASS, "pid": 20},
            {"address": "0x789", "initialClass": "other", "pid": 10},
        ]
        with patch("stream_studio.preview.query", return_value=clients), \
             patch("stream_studio.preview.preview_process", side_effect=lambda pid: pid == 10):
            self.assertEqual(preview.windows(), [clients[0]])

    def test_process_identity_with_rewritten_chromium_command_line(self):
        profile = Path(self.temporary.name) / "preview-browser"
        command = f"/usr/lib/chromium/chromium --user-data-dir={profile} --app={preview.URL}"
        with patch.object(Path, "read_bytes", return_value=command.encode() + b"\0"):
            self.assertTrue(preview.preview_process(123))
        with patch.object(Path, "read_bytes", return_value=b"chromium\0--app=" + preview.URL.encode() + b"\0"):
            self.assertFalse(preview.preview_process(123))

    def test_existing_window_is_positioned_without_launch(self):
        window = {"address": "0x123", "pinned": True}
        with patch("stream_studio.preview.windows", return_value=[window]), \
             patch("stream_studio.preview.geometry", return_value=(2400, 30, 400, 870)), \
             patch("stream_studio.preview.subprocess.Popen") as launch, \
             patch("stream_studio.preview.dispatch") as dispatch:
            self.assertEqual(preview.command("on"), "open")
            launch.assert_not_called()
            self.assertEqual(dispatch.call_count, 3)

    def test_unknown_pin_state_does_not_dispatch(self):
        with patch("stream_studio.preview.windows", return_value=[{"address": "0x123"}]), \
             patch("stream_studio.preview.geometry", return_value=(2400, 30, 400, 870)), \
             patch("stream_studio.preview.dispatch") as dispatch:
            with self.assertRaises(ValueError):
                preview.command("on")
            dispatch.assert_not_called()

    def test_status_and_toggle_close_only_matching_window(self):
        window = {"address": "0x123", "initialClass": preview.APP_CLASS}
        with patch("stream_studio.preview.windows", return_value=[window]), \
             patch("stream_studio.preview.dispatch") as dispatch:
            self.assertEqual(preview.command("status"), "open")
            self.assertEqual(preview.command("toggle"), "closed")
            dispatch.assert_called_once_with('hl.dsp.window.close({ window = "address:0x123" })')

    def test_multiple_windows_fail_without_closing_any(self):
        with patch("stream_studio.preview.windows", return_value=[{}, {}]), \
             patch("stream_studio.preview.dispatch") as dispatch:
            with self.assertRaises(ValueError):
                preview.command("off")
            dispatch.assert_not_called()

    def test_geometry_uses_right_reserved_strip(self):
        monitor = {"name": "DP-1", "transform": 0, "scale": 1.6,
                   "width": 2560, "height": 1440, "x": 1200, "y": 0,
                   "reserved": [0, 30, 400, 0]}
        with patch("stream_studio.preview.query", return_value=[monitor]):
            self.assertEqual(preview.geometry(), (2400, 30, 400, 870))

    def test_no_reserved_space_does_not_launch_browser(self):
        with patch("stream_studio.preview.windows", return_value=[]), \
             patch("stream_studio.preview.geometry", side_effect=ValueError("No reservation")), \
             patch("stream_studio.preview.subprocess.Popen") as launch:
            with self.assertRaises(ValueError):
                preview.command("on")
            launch.assert_not_called()

    def test_open_targets_only_new_preview(self):
        window = {"address": "0x123", "class": preview.APP_CLASS, "pinned": False}
        with patch("stream_studio.preview.windows", side_effect=[[], [window]]), \
             patch("stream_studio.preview.geometry", return_value=(2400, 30, 400, 870)), \
             patch("stream_studio.preview.subprocess.Popen", return_value=Mock()) as launch, \
             patch("stream_studio.preview.dispatch") as dispatch:
            self.assertEqual(preview.command("on"), "open")
            self.assertIn("--class=" + preview.APP_CLASS, launch.call_args.args[0])
            self.assertEqual(dispatch.call_count, 4)
            self.assertEqual(dispatch.call_args_list[-1].args[0],
                             'hl.dsp.window.pin({ window = "address:0x123" })')
            for call in dispatch.call_args_list:
                self.assertIn("address:0x123", call.args[0])


if __name__ == "__main__":
    unittest.main()
