"use strict";

function createChatRenderer(display) {
  const authorColors = new Map();
  const palette = [
    "#f5c2e7", "#cba6f7", "#f38ba8", "#fab387", "#f9e2af",
    "#a6e3a1", "#94e2d5", "#89dceb", "#74c7ec", "#89b4fa", "#b4befe"
  ];

  return function renderChat(messages) {
    if (!Array.isArray(messages) || messages.length > 50 ||
        !messages.every(message => message && typeof message.author === "string" &&
                        typeof message.text === "string")) {
      throw new Error("Invalid chat response");
    }
    const visible = new Set(messages.map(message => message.author));
    for (const name of authorColors.keys()) {
      if (!visible.has(name)) authorColors.delete(name);
    }
    for (const name of visible) {
      if (!authorColors.has(name)) {
        authorColors.set(name, palette[Math.floor(Math.random() * palette.length)]);
      }
    }
    const nodes = messages.map(message => {
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
  };
}
