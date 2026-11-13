"use strict";
const topic = document.getElementById("topic");
const keysStatus = document.getElementById("keys-status");
const chatStatus = document.getElementById("chat-status");
const chat = document.getElementById("chat");

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
    if (!Array.isArray(data.messages) || data.messages.length > 50 || typeof data.state !== "string") {
      throw new Error("Invalid response");
    }
    chatStatus.textContent = data.state;
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
