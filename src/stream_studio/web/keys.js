"use strict";

const display = document.getElementById("keys");
const freshnessLimit = 750;
const maxKeys = 11;
const symbols = {
  BackSpace: "⌫", Backspace: "⌫", Space: "␣", space: "␣",
  Shift: "⇧", Shift_L: "⇧", Shift_R: "⇧",
  Return: "↵", KP_Enter: "↵", Tab: "⇥", ISO_Left_Tab: "⇤",
  Left: "←", Right: "→", Up: "↑", Down: "↓",
  Delete: "⌦", Home: "Home", End: "↘", Prior: "Page up", Next: "Page down",
  Escape: "Esc", Caps_Lock: "⇪",
  Ctrl: "Ctrl", Control_L: "Ctrl", Control_R: "Ctrl",
  Alt: "Alt", Alt_L: "Alt", Alt_R: "Alt",
  Super: "Super", Super_L: "Super", Super_R: "Super"
};
let lastSuccess = -Infinity;
let generation = null;
let serial = 0;

function clear() {
  display.replaceChildren();
  generation = null;
}

function legend(part) {
  const element = document.createElement("span");
  element.className = "legend";
  element.textContent = symbols[part] || part;
  return element;
}

function fit() {
  // Never wrap or shrink keycaps. Remove whole oldest entries when needed.
  while (display.firstElementChild && display.scrollWidth > display.clientWidth) {
    display.firstElementChild.remove();
  }
}

function render(entries) {
  display.replaceChildren(...entries.slice(-maxKeys).map(entry => {
    const element = document.createElement("span");
    element.className = "key";
    element.title = entry.text;
    element.setAttribute("aria-label", `${entry.text}, ${entry.count} presses`);
    entry.parts.forEach((part, index) => {
      if (index) {
        const join = document.createElement("span");
        join.className = "join";
        join.textContent = "+";
        element.append(join);
      }
      element.append(legend(part));
    });
    if (entry.count > 1) {
      const count = document.createElement("span");
      count.className = "count";
      count.textContent = `×${entry.count}`;
      element.append(count);
    }
    return element;
  }));
  fit();
}

function validEntry(entry) {
  return entry && typeof entry.text === "string" && entry.text.length <= 64
    && Number.isSafeInteger(entry.count) && entry.count >= 1 && entry.count <= 999999
    && Array.isArray(entry.parts) && entry.parts.length >= 1 && entry.parts.length <= 5
    && entry.parts.every(part => typeof part === "string" && part.length >= 1 && part.length <= 64);
}

async function poll() {
  const requestSerial = ++serial;
  const started = performance.now();
  try {
    const response = await fetch("/api/keys", {
      cache: "no-store", signal: AbortSignal.timeout(500)
    });
    if (!response.ok) throw new Error("Unavailable");
    const payload = await response.json();
    if (requestSerial !== serial || performance.now() - started > 500) return;
    if (typeof payload.generation !== "string" || !Array.isArray(payload.keys)
        || payload.keys.length > maxKeys || !payload.keys.every(validEntry)) {
      throw new Error("Invalid key response");
    }
    lastSuccess = performance.now();
    if (payload.state !== "presenting") {
      clear();
      if (payload.state === "disabled") {
        const message = document.createElement("span");
        message.className = "keys-disabled";
        message.textContent = "Keys display disabled";
        display.append(message);
      }
      return;
    }
    if (generation !== payload.generation) clear();
    generation = payload.generation;
    render(payload.keys);
  } catch (_) {
    clear();
  } finally {
    window.setTimeout(poll, 100);
  }
}

new ResizeObserver(fit).observe(display);
document.fonts.ready.then(fit);
window.setInterval(() => {
  if (performance.now() - lastSuccess > freshnessLimit) clear();
}, 100);
document.addEventListener("visibilitychange", () => {
  ++serial;
  lastSuccess = -Infinity;
  clear();
});
window.addEventListener("pagehide", clear);
poll();
