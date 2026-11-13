import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

from stream_studio.server import Handler, PORT
from stream_studio.state import read_topic, write_topic


class StateTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "data/topic.json"

    def test_missing_state_is_empty(self):
        self.assertEqual(read_topic(self.path), "")

    def test_topic_survives_read_and_can_be_cleared(self):
        write_topic("Building an overlay ✨", self.path)
        self.assertEqual(read_topic(self.path), "Building an overlay ✨")
        write_topic("", self.path)
        self.assertEqual(read_topic(self.path), "")
        self.assertEqual(list(self.path.parent.glob(".topic-*")), [])

    def test_invalid_input_preserves_existing_state(self):
        write_topic("Original", self.path)
        for invalid in ["x" * 2001, "two\nlines", "tab\there", "null\0"]:
            with self.assertRaises(ValueError):
                write_topic(invalid, self.path)
            self.assertEqual(read_topic(self.path), "Original")

    def test_corrupt_state_is_not_silently_cleared(self):
        self.path.parent.mkdir()
        for value in ["not json", "[]", '{"topic":42}']:
            self.path.write_text(value)
            with self.assertRaises(ValueError):
                read_topic(self.path)


class HTTPTests(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
        self.addCleanup(self.close_server)
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def close_server(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()

    def get(self, path, host=None):
        request = urllib.request.Request(
            self.base + path,
            headers={"Host": host or f"127.0.0.1:{PORT}"},
        )
        return self.opener.open(request, timeout=2)

    def test_topic_is_read_only_json(self):
        with patch("stream_studio.server.read_topic", return_value="<script>text</script>"):
            with self.get("/api/topic") as response:
                self.assertEqual(json.load(response), {"topic": "<script>text</script>"})
                self.assertEqual(response.headers["Cache-Control"], "no-store")
                self.assertNotIn("Access-Control-Allow-Origin", response.headers)

    def test_assets_are_available_and_paths_are_allowlisted(self):
        for path in ["/topic", "/topic.js", "/topic.css", "/keys", "/keys.js", "/keys.css"]:
            with self.get(path) as response:
                self.assertTrue(response.read())
        with self.assertRaises(urllib.error.HTTPError) as error:
            self.get("/../../topic.json")
        self.assertEqual(error.exception.code, 404)

    def test_keys_endpoint_is_read_only_and_starts_empty(self):
        from stream_studio.keys import Keys

        self.server.keys = Keys()
        with self.get("/api/keys") as response:
            payload = json.load(response)
        self.assertEqual(payload["state"], "disabled")
        self.assertEqual(payload["keys"], [])
        req = urllib.request.Request(self.base + "/api/keys", data=b"on",
                                     headers={"Host": f"127.0.0.1:{PORT}"})
        with self.assertRaises(urllib.error.HTTPError) as error:
            self.opener.open(req, timeout=2)
        self.assertEqual(error.exception.code, 501)
        self.assertEqual(self.server.keys.status()["state"], "disabled")

    def test_rebinding_host_is_rejected(self):
        with self.assertRaises(urllib.error.HTTPError) as error:
            self.get("/api/topic", host="other.example")
        self.assertEqual(error.exception.code, 403)

    def test_broken_state_reports_unavailable(self):
        with patch("stream_studio.server.read_topic", side_effect=ValueError("bad state")):
            with self.assertRaises(urllib.error.HTTPError) as error:
                self.get("/api/topic")
        self.assertEqual(error.exception.code, 503)


if __name__ == "__main__":
    unittest.main()
