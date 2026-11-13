"""Passive evdev adapter. Devices are opened only after explicit enablement."""

import select
import threading
from pathlib import Path

from .keys_desktop import Desktop

# Linux evdev modifier key codes, independent of their mapped symbols.
MODIFIERS = {
    29: "Ctrl", 97: "Ctrl", 56: "Alt", 100: "Alt",
    125: "Super", 126: "Super", 42: "Shift", 54: "Shift",
}


class Capture:
    def __init__(self, keys):
        self.keys = keys
        self._io = threading.RLock()
        self._stop = threading.Event()
        self._devices = {}
        self._down = {}
        self._pending_modifiers = {}
        self._state = None
        self._revision = None
        self._keyboard_revision = None
        self._desktop = Desktop()
        keys.attach(self.close_devices)
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def close_devices(self):
        with self._io:
            for device in self._devices.values():
                device.close()
            self._devices.clear()
            self._down.clear()
            self._pending_modifiers.clear()
            self._state = None

    def _paths(self):
        paths = []
        for pattern in ("usb-Thomas_Haukland_Cheapino2_*-event*kbd",
                        "usb-DH747_W-CORNE_*-event*kbd"):
            paths.extend(Path("/dev/input/by-id").glob(pattern))
        return {str(path.resolve()): str(path) for path in paths}.values()

    def _open(self, evdev, xkb):
        paths = set(self._paths())
        if not paths:
            raise OSError("Selected keyboards unavailable")
        if self._devices and paths != set(self._devices):
            self.close_devices()
            raise OSError("Keyboard topology changed")
        if self._devices:
            return
        try:
            for path in sorted(paths):
                device = evdev.InputDevice(path)
                # Validate USB identity and alphabetic capabilities after open.
                if ((device.info.vendor, device.info.product) not in {
                    (0xFEE3, 0x0000), (0x55D4, 0x0461)
                } or evdev.ecodes.KEY_A not in device.capabilities().get(evdev.ecodes.EV_KEY, [])):
                    device.close()
                    raise OSError("Unexpected keyboard interface")
                self._devices[path] = device
                self._down[path] = set()
                if device.active_keys():
                    raise OSError("Release held keys before activation")
            context = xkb.Context()
            context.include_path_append("/etc/xkb")
            keymap = context.keymap_new_from_names(
                rules="evdev", model="pc105", layout="us", variant="",
                options="omarchy:shift_caps_compose",
            )
            self._state = keymap.state_new()
            led_states = {tuple(sorted(device.leds())) for device in self._devices.values()}
            if len(led_states) != 1:
                raise OSError("Keyboard lock states differ")
            leds = next(iter(led_states))
            for led, key in ((evdev.ecodes.LED_CAPSL, evdev.ecodes.KEY_CAPSLOCK),
                             (evdev.ecodes.LED_NUML, evdev.ecodes.KEY_NUMLOCK)):
                if led in leds:
                    self._state.update_key(key + 8, xkb.KeyDirection.XKB_KEY_DOWN)
                    self._state.update_key(key + 8, xkb.KeyDirection.XKB_KEY_UP)
        except BaseException:
            self.close_devices()
            raise

    def _event(self, path, event, evdev, xkb, ticket):
        if event.type == evdev.ecodes.EV_SYN and event.code == evdev.ecodes.SYN_DROPPED:
            # Close/reopen creates a fresh evdev queue; wait for held keys to clear.
            raise OSError("Keyboard input overflow")
        if event.type != evdev.ecodes.EV_KEY:
            return
        code, value = event.code, event.value
        if value not in (0, 1, 2):
            raise OSError("Invalid key event")
        if ticket is None:
            self._pending_modifiers.clear()
        union_before = set().union(*self._down.values())
        if value == 0:
            pending = self._pending_modifiers.pop((path, code), None)
            if pending is not None and pending == ticket:
                label = MODIFIERS[code]
                self.keys.publish(label, pending, parts=[label])
            self._down[path].discard(code)
            union_after = set().union(*self._down.values())
            if code in union_before and code not in union_after:
                self._state.update_key(code + 8, xkb.KeyDirection.XKB_KEY_UP)
            return
        if value == 2:
            if code not in self._down[path]:
                raise OSError("Uncertain repeat state")
            return
        if code in self._down[path]:
            return
        if code in MODIFIERS:
            # A modifier alone is shown on release, unless a non-modifier key
            # uses it first. Keep the original ticket so suspension revokes it.
            if ticket is not None and not (union_before - MODIFIERS.keys()):
                self._pending_modifiers[(path, code)] = ticket
        else:
            self._pending_modifiers.clear()
            # Suspended events update only keyboard state, never display content.
            if ticket is not None:
                self._publish_key(code, union_before, evdev, xkb, ticket)
        self._down[path].add(code)
        if code not in union_before:
            self._state.update_key(code + 8, xkb.KeyDirection.XKB_KEY_DOWN)

    def _publish_key(self, code, union_before, evdev, xkb, ticket):
        symbol = self._state.key_get_one_sym(code + 8)
        name = xkb.keysym_get_name(symbol)
        text = self._state.key_get_string(code + 8)
        modifier_codes = {
            evdev.ecodes.KEY_LEFTCTRL: "Ctrl", evdev.ecodes.KEY_RIGHTCTRL: "Ctrl",
            evdev.ecodes.KEY_LEFTALT: "Alt", evdev.ecodes.KEY_RIGHTALT: "Alt",
            evdev.ecodes.KEY_LEFTMETA: "Super", evdev.ecodes.KEY_RIGHTMETA: "Super",
        }
        prefixes = list(dict.fromkeys(modifier_codes[key] for key in sorted(union_before)
                                      if key in modifier_codes))
        if prefixes or not text or any(ord(character) < 32 for character in text):
            label = name or evdev.ecodes.KEY.get(code, str(code))
            aliases = {"Shift_L": "Shift", "Shift_R": "Shift",
                       "Control_L": "Ctrl", "Control_R": "Ctrl",
                       "Alt_L": "Alt", "Alt_R": "Alt",
                       "Super_L": "Super", "Super_R": "Super"}
            label = aliases.get(label, label)
            # The supported US mapping has digit-row evdev codes 2 through 11.
            # Modified shortcuts name the base digit, not its shifted punctuation.
            if prefixes and 2 <= code <= 11:
                label = "1234567890"[code - 2]
            if evdev.ecodes.KEY_LEFTSHIFT in union_before or evdev.ecodes.KEY_RIGHTSHIFT in union_before:
                prefixes.append("Shift")
            parts = list(dict.fromkeys([*prefixes, label]))
        else:
            parts = ["Space" if text == " " else text]
        self.keys.publish("+".join(parts), ticket, parts=parts)

    def _drain(self, evdev, xkb, ticket):
        if ticket is None:
            self._pending_modifiers.clear()
        ready, _, _ = select.select(list(self._devices.values()), [], [], 0)
        for device in ready:
            path = next(path for path, candidate in self._devices.items()
                        if candidate is device)
            for index, event in enumerate(device.read()):
                if index >= 256:
                    raise OSError("Keyboard input backlog")
                if self._desktop.keyboard_revision() != self._keyboard_revision:
                    raise OSError("Keyboard mapping requires recovery")
                reason, mapping, revision = self._desktop.snapshot()
                if reason is not None or mapping is None or revision != self._revision:
                    self.keys.observe(reason or "Desktop transition")
                    ticket = None
                self._event(path, event, evdev, xkb, ticket)

    def _cycle(self, evdev, xkb):
        if self.keys.status()["state"] == "disabled":
            self.close_devices()
            return
        reason, mapping, revision = self._desktop.snapshot()
        if revision != self._revision:
            self.keys.observe("Desktop transition")
            self._revision = revision
        keyboard_revision = self._desktop.keyboard_revision()
        if keyboard_revision != self._keyboard_revision:
            self.keys.observe("Keyboard mapping requires recovery")
            self.close_devices()
            self._keyboard_revision = keyboard_revision
        if reason is not None or mapping is None:
            self.keys.observe(reason or "Keyboard mapping unavailable")
            # Keep valid readers/state through display-only suspension. Do not
            # open new readers while permission to present is uncertain.
            if self._devices:
                self._drain(evdev, xkb, None)
            return
        self._open(evdev, xkb)
        if self.keys.status()["state"] != "presenting":
            # Discard everything already queued before re-enabling publication.
            self._drain(evdev, xkb, None)
            current_reason, current_mapping, current_revision = self._desktop.snapshot()
            if (current_reason is not None or current_mapping is None
                    or current_revision != revision
                    or self._desktop.keyboard_revision() != keyboard_revision):
                self.keys.observe(current_reason or "Desktop transition")
                return
        self.keys.observe(None)
        self._drain(evdev, xkb, self.keys.ticket())

    def _run(self):
        try:
            import evdev
            from xkbcommon import xkb
        except ImportError:
            while not self._stop.is_set():
                self.keys.observe("Install the stream-studio keys extra and restart service")
                self._stop.wait(0.2)
            return
        try:
            while not self._stop.is_set():
                try:
                    with self._io:
                        self._cycle(evdev, xkb)
                except Exception:
                    # Never print exception payloads that could contain typed data.
                    self.keys.observe("Capture unavailable; check access, devices, and mapping")
                    self.close_devices()
                    self._stop.wait(0.2)
                self._stop.wait(0.02)
        finally:
            self.close_devices()

    def close(self):
        self._stop.set()
        self._thread.join(timeout=3)
        self.close_devices()
        self._desktop.close()
