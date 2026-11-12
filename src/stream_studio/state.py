"""One shared state file, read by the service and written by the CLI."""

import json
import os
import tempfile
from pathlib import Path

MAX_TOPIC_LENGTH = 2000


def state_path() -> Path:
    return Path.home() / ".local/share/stream-studio/topic.json"


def validate_topic(topic: str) -> str:
    if len(topic) > MAX_TOPIC_LENGTH:
        raise ValueError(f"Topic must be at most {MAX_TOPIC_LENGTH} characters.")
    if any(ord(character) < 32 or ord(character) == 127 for character in topic):
        raise ValueError("Topic must be a single line without control characters.")
    return topic.strip()


def read_topic(path: Path | None = None) -> str:
    path = state_path() if path is None else path
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return ""
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"Cannot read topic state at {path}: {error}") from error
    if not isinstance(value, dict) or not isinstance(value.get("topic"), str):
        raise ValueError(f"Invalid topic state at {path}.")
    return validate_topic(value["topic"])


def write_topic(topic: str, path: Path | None = None) -> str:
    topic = validate_topic(topic)
    path = state_path() if path is None else path
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    # Readers see either the old complete file or the new complete file.
    descriptor, temporary = tempfile.mkstemp(dir=path.parent, prefix=".topic-")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as output:
            json.dump({"topic": topic}, output, ensure_ascii=False)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return topic
