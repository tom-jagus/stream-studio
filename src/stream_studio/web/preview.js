"use strict";
const topic = document.getElementById("topic");
const keysStatus = document.getElementById("keys-status");
const chatStatus = document.getElementById("chat-status");
const chat = document.getElementById("chat");
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

async function get(path) {
  const response = await fetch(path, {cache: "no-store", signal: AbortSignal.timeout(1000)});
  if (!response.ok) throw new Error("Unavailable");
  return response.json();
}
async function updateTopic() {
  try {
    const data = await get("/api/topic");
    if (typeof data.topic !== "string") throw new Error("Invalid response");
    topic.textContent = data.topic || "No topic";
  } catch (_) { topic.textContent = "Topic unavailable"; }
  finally { window.setTimeout(updateTopic, 1000); }
}
async function updateKeysStatus() {
  try {
    const data = await get("/api/keys");
    if (!["disabled", "suspended", "presenting"].includes(data.state)) throw new Error("Invalid response");
    keysStatus.textContent = data.state;
  } catch (_) { keysStatus.textContent = "unavailable"; }
  finally { window.setTimeout(updateKeysStatus, 500); }
}
async function updateChat() {
  try {
    const data = await get("/api/chat");
    if (!Array.isArray(data.messages) || data.messages.length > 50 || typeof data.state !== "string" ||
        !data.messages.every(message => message && typeof message.author === "string" && typeof message.text === "string")) {
      throw new Error("Invalid response");
    }
    chatStatus.textContent = data.state;
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
    chat.replaceChildren(...nodes);
    chat.scrollTop = chat.scrollHeight;
  } catch (_) {
    chatStatus.textContent = "unavailable";
    chat.replaceChildren();
  } finally { window.setTimeout(updateChat, 1000); }
}
updateTopic();
updateKeysStatus();
updateChat();
