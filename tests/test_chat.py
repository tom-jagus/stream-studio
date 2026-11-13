import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from stream_studio.chat import Chat, MAX_MESSAGES, video_id


def timestamp(seconds):
    return datetime.fromtimestamp(seconds, timezone.utc).isoformat()


class VideoIdTests(unittest.TestCase):
    def test_supported_ids_and_urls(self):
        for value in ("abcdefghijk", "https://youtu.be/abcdefghijk",
                      "https://www.youtube.com/watch?v=abcdefghijk",
                      "https://youtube.com/live/abcdefghijk"):
            self.assertEqual(video_id(value), "abcdefghijk")

    def test_rejects_other_hosts_and_invalid_ids(self):
        for value in ("https://youtube.com.example.org/watch?v=abcdefghijk",
                      "https://youtube.com/watch?v=bad", "bad"):
            with self.assertRaises(ValueError):
                video_id(value)


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.now = 10000
        self.chat = Chat(clock=lambda: self.now)
        self.generation = self.chat.start()

    def add(self, identifier, posted=None):
        self.chat.add(self.generation, identifier, "viewer", "hello", posted)

    def test_bounded_and_deduplicated(self):
        for index in range(MAX_MESSAGES + 10):
            self.add(str(index))
        self.add(str(MAX_MESSAGES + 9))
        self.assertEqual(len(self.chat.snapshot()["messages"]), MAX_MESSAGES)

    def test_stop_clears_and_rejects_stale_generation(self):
        self.add("first")
        self.chat.stop()
        self.add("late")
        self.assertEqual(self.chat.snapshot()["messages"], [])
        self.chat.start()
        self.add("stale")
        self.assertEqual(self.chat.snapshot()["messages"], [])

    def test_invalid_times_are_allowed_when_expiry_off(self):
        self.add("missing")
        self.add("invalid", "bad")
        self.assertEqual(len(self.chat.snapshot()["messages"]), 2)

    def test_expiry_and_clock_skew(self):
        self.chat.set_expiry(5)
        self.add("recent", timestamp(self.now - 299))
        self.add("old", timestamp(self.now - 300))
        self.add("future", timestamp(self.now + 60))
        self.add("too-far", timestamp(self.now + 61))
        self.add("invalid", "bad")
        self.assertEqual(len(self.chat.snapshot()["messages"]), 2)
        self.assertEqual(self.chat.status()["skipped"], 2)
        self.now += 2
        self.assertEqual(len(self.chat.snapshot()["messages"]), 1)

    def test_enabling_expiry_removes_invalid_existing_messages(self):
        self.add("missing")
        self.chat.set_expiry(1)
        self.assertEqual(self.chat.snapshot()["messages"], [])
        self.assertEqual(self.chat.status()["skipped"], 1)

    def test_invalid_expiry_does_not_change_setting(self):
        self.chat.set_expiry(5)
        for value in (0, -1, True, "5"):
            with self.assertRaises(ValueError):
                self.chat.set_expiry(value)
        self.assertEqual(self.chat.status()["expiry"], 5)


class ChatProtoTests(unittest.TestCase):
    def test_wire_message_round_trip(self):
        try:
            from stream_studio.chat_proto import messages
            Request, Response = messages()
        except ImportError:
            self.skipTest("protobuf chat dependency not installed")
        request = Request(live_chat_id="chat", part=["snippet", "authorDetails"], page_token="next")
        self.assertEqual(Request.FromString(request.SerializeToString()).page_token, "next")
        response = Response(next_page_token="token")
        item = response.items.add(id="id")
        item.snippet.display_message = "hello"
        item.author_details.display_name = "viewer"
        decoded = Response.FromString(response.SerializeToString())
        self.assertEqual(decoded.items[0].snippet.display_message, "hello")
        self.assertEqual(decoded.next_page_token, "token")


class ChatServiceTests(unittest.TestCase):
    def test_expiry_persists_and_invalid_does_not_replace_it(self):
        from stream_studio.chat_service import ChatService
        with tempfile.TemporaryDirectory() as directory, patch.dict("os.environ", {"XDG_CONFIG_HOME": directory}):
            service = ChatService()
            service.command("expiry", "5")
            with self.assertRaises(ValueError):
                service.command("expiry", "0")
            self.assertEqual(ChatService().chat.status()["expiry"], 5)
            service.command("expiry", "off")
            self.assertIsNone(ChatService().chat.status()["expiry"])
            self.assertEqual((Path(directory) / "stream-studio/chat.json").stat().st_mode & 0o777, 0o600)

    def test_private_control_round_trip(self):
        from stream_studio.chat_control import Control, request
        from stream_studio.chat_service import ChatService
        with tempfile.TemporaryDirectory() as directory, patch.dict("os.environ", {"XDG_RUNTIME_DIR": directory, "XDG_CONFIG_HOME": directory}):
            service = ChatService()
            control = Control(service)
            try:
                self.assertEqual(request("status")["state"], "stopped")
                self.assertEqual(request("expiry", "5")["expiry"], 5)
                self.assertEqual(request("stop")["state"], "stopped")
            finally:
                control.close()
                service.close()


if __name__ == "__main__":
    unittest.main()
