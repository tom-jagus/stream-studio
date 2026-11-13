"use strict";
const display = document.getElementById("chat");
const authorColors = new Map();
const palette = [
  "#f5c2e7", "#cba6f7", "#f38ba8", "#fab387", "#f9e2af",
  "#a6e3a1", "#94e2d5", "#89dceb", "#74c7ec", "#89b4fa", "#b4befe"
];
function updateAuthorColors(messages) {
  const visible = new Set(messages.map(message => message.author));
  for (const name of authorColors.keys()) {
    if (!visible.has(name)) authorColors.delete(name);
  }
  for (const name of visible) {
    if (!authorColors.has(name)) {
      authorColors.set(name, palette[Math.floor(Math.random() * palette.length)]);
    }
  }
}
async function poll() {
  try {
    const response = await fetch("/api/chat", {cache: "no-store", signal: AbortSignal.timeout(3000)});
    if (!response.ok) throw new Error("Unavailable");
    const data = await response.json();
    if (!Array.isArray(data.messages) || data.messages.length > 50 ||
        !data.messages.every(message => message && typeof message.author === "string" && typeof message.text === "string")) {
      throw new Error("Invalid response");
    }
    updateAuthorColors(data.messages);
    const nodes = data.messages.map(message => {
      const row = document.createElement("div");
      row.className = "message";
      const author = document.createElement("span");
      author.className = "author";
      author.style.color = authorColors.get(message.author);
      author.textContent = message.author + ": ";
      const text = document.createElement("span");
      text.textContent = message.text;
      row.append(author, text);
      return row;
    });
    display.replaceChildren(...nodes);
    while (display.firstElementChild && display.scrollHeight > display.clientHeight) {
      display.firstElementChild.remove();
    }
  } catch (_) {
    display.replaceChildren();
  } finally {
    window.setTimeout(poll, 1000);
  }
}
poll();
