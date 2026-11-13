import contextlib
import io
import json
import subprocess
import unittest
from unittest.mock import patch

from stream_studio import cli


class CliampVolumeTests(unittest.TestCase):
    def test_start_and_stop_apply_requested_levels_after_success(self):
        for action, level in (("start", -15), ("stop", 0)):
            with self.subTest(action=action), \
                 patch("sys.argv", ["stream", action]), \
                 patch("stream_studio.cli.systemctl", return_value=0) as systemctl, \
                 patch("stream_studio.cli.set_cliamp_volume") as volume:
                self.assertEqual(cli.main(), 0)
                systemctl.assert_called_once_with(action)
                volume.assert_called_once_with(level)

    def test_service_failure_does_not_change_volume(self):
        for action in ("start", "stop"):
            with self.subTest(action=action), \
                 patch("sys.argv", ["stream", action]), \
                 patch("stream_studio.cli.systemctl", return_value=1), \
                 patch("stream_studio.cli.set_cliamp_volume") as volume:
                self.assertEqual(cli.main(), 1)
                volume.assert_not_called()

    def test_verifies_requested_volume_without_printing_metadata(self):
        response = json.dumps({"ok": True, "volume": -15, "track": "PRIVATE"})
        success = subprocess.CompletedProcess([], 0, stdout="", stderr="")
        state = subprocess.CompletedProcess([], 0, stdout=response, stderr="")
        out = io.StringIO()
        with patch("stream_studio.cli.subprocess.run", side_effect=[success, state]) as run, \
             contextlib.redirect_stdout(out):
            cli.set_cliamp_volume(-15)
        self.assertEqual(run.call_args_list[0].args[0], ["cliamp", "volume", "-15"])
        self.assertEqual(run.call_args_list[1].args[0], ["cliamp", "status", "--json"])
        self.assertIn("-15 dB", out.getvalue())
        self.assertNotIn("PRIVATE", out.getvalue())

    def test_zero_volume_is_confirmed(self):
        success = subprocess.CompletedProcess([], 0, stdout="", stderr="")
        state = subprocess.CompletedProcess([], 0, stdout='{"ok": true, "volume": 0}', stderr="")
        out, err = io.StringIO(), io.StringIO()
        with patch("stream_studio.cli.subprocess.run", side_effect=[success, state]), \
             contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            cli.set_cliamp_volume(0)
        self.assertIn("+0 dB", out.getvalue())
        self.assertEqual(err.getvalue(), "")

    def test_missing_cliamp_warns_without_failing(self):
        err = io.StringIO()
        with patch("stream_studio.cli.subprocess.run", side_effect=FileNotFoundError("cliamp")), \
             contextlib.redirect_stderr(err):
            self.assertIsNone(cli.set_cliamp_volume(0))
        self.assertIn("not confirmed", err.getvalue())

    def test_mismatched_or_invalid_state_warns(self):
        success = subprocess.CompletedProcess([], 0, stdout="", stderr="")
        for payload in ("not json", json.dumps({"ok": True, "volume": -10}),
                        json.dumps({"ok": True})):
            with self.subTest(payload=payload):
                state = subprocess.CompletedProcess([], 0, stdout=payload, stderr="")
                err = io.StringIO()
                with patch("stream_studio.cli.subprocess.run", side_effect=[success, state]), \
                     contextlib.redirect_stderr(err):
                    cli.set_cliamp_volume(-15)
                self.assertIn("not confirmed", err.getvalue())


if __name__ == "__main__":
    unittest.main()
