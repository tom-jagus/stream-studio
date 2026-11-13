import contextlib
import io
import json
import unittest
from unittest.mock import MagicMock, patch

from stream_studio import cli


class StatusTests(unittest.TestCase):
    def run_status(self, service=0, topic="Example", keys=None, chat=None,
                   preview="open", topic_error=None):
        keys = keys if keys is not None else {"state": "presenting", "reason": "Allowed"}
        chat = chat if chat is not None else {"state": "connected", "reason": "Receiving chat",
                                              "expiry": 5, "skipped": 2}
        response = MagicMock()
        response.__enter__.return_value = io.BytesIO(json.dumps({"topic": "Example"}).encode())
        opener = MagicMock()
        opener.open.return_value = response
        output = io.StringIO()
        with patch("stream_studio.cli.systemctl", return_value=service), \
             patch("stream_studio.cli.read_topic", side_effect=topic_error, return_value=topic), \
             patch("stream_studio.cli.urllib.request.build_opener", return_value=opener), \
             patch("stream_studio.keys_control.request", side_effect=keys if isinstance(keys, Exception) else None,
                   return_value=keys), \
             patch("stream_studio.chat_control.request", side_effect=chat if isinstance(chat, Exception) else None,
                   return_value=chat), \
             patch("stream_studio.preview.command", side_effect=preview if isinstance(preview, Exception) else None,
                   return_value=preview), \
             contextlib.redirect_stdout(output):
            result = cli.status()
        return result, output.getvalue()

    def test_combines_all_statuses(self):
        result, text = self.run_status()
        self.assertEqual(result, 0)
        for expected in ("Saved topic: Example", "Topic endpoint is responding.",
                         "Keys: presenting (Allowed)", "Chat: connected (Receiving chat)",
                         "expiry: 5", "skipped: 2", "Preview: open"):
            self.assertIn(expected, text)

    def test_inactive_service_still_reports_preview(self):
        result, text = self.run_status(service=3, keys=OSError("offline"),
                                       chat=OSError("offline"), preview="closed")
        self.assertEqual(result, 1)
        self.assertIn("Service is not active", text)
        self.assertIn("Keys: unavailable", text)
        self.assertIn("Chat: unavailable", text)
        self.assertIn("Preview: closed", text)

    def test_one_failure_does_not_hide_other_statuses(self):
        result, text = self.run_status(keys=ValueError("bad response"))
        self.assertEqual(result, 1)
        self.assertIn("Keys: unavailable", text)
        self.assertIn("Chat: connected", text)
        self.assertIn("Preview: open", text)

    def test_unavailable_preview_does_not_hide_service_modules(self):
        result, text = self.run_status(preview=OSError("Hyprland unavailable"))
        self.assertEqual(result, 1)
        self.assertIn("Keys: presenting", text)
        self.assertIn("Chat: connected", text)
        self.assertIn("Preview: unavailable", text)

    def test_corrupt_topic_does_not_hide_modules(self):
        result, text = self.run_status(topic_error=ValueError("bad state"))
        self.assertEqual(result, 1)
        self.assertIn("Saved topic: unavailable", text)
        self.assertIn("Keys: presenting", text)
        self.assertIn("Chat: connected", text)
        self.assertIn("Preview: open", text)


if __name__ == "__main__":
    unittest.main()
