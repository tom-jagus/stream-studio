"use strict";
const display = document.getElementById("chat");
async function poll() {
  try {
    const response = await fetch("/api/chat", {cache: "no-store", signal: AbortSignal.timeout(3000)});
    if (!response.ok) throw new Error("Unavailable");
    const data = await response.json();
    if (!Array.isArray(data.messages) || data.messages.length > 50) throw new Error("Invalid response");
    const nodes = data.messages.map(message => {
      if (typeof message.author !== "string" || typeof message.text !== "string") throw new Error("Invalid message");
      const row = document.createElement("div");
      row.className = "message";
      const author = document.createElement("span");
      author.className = "author";
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
