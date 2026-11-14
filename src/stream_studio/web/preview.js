"use strict";
const scene = document.getElementById("scene");
const sceneChecked = document.getElementById("scene-checked");
const sceneError = document.getElementById("scene-error");
const topic = document.getElementById("topic");
const keysStatus = document.getElementById("keys-status");
const chatStatus = document.getElementById("chat-status");
const chat = document.getElementById("chat");
const renderChat = createChatRenderer(chat);

async function get(path) {
  const response = await fetch(path, {cache: "no-store", signal: AbortSignal.timeout(1000)});
  if (!response.ok) throw new Error("Unavailable");
  return response.json();
}
async function updateScene() {
  try {
    const data = await get("/api/scene");
    if (![data.scene, data.checked_at, data.error].every(value => value === null || typeof value === "string")) {
      throw new Error("Invalid response");
    }
    scene.textContent = data.scene || "No confirmed scene";
    sceneChecked.textContent = data.checked_at ? "Checked: " + data.checked_at : "";
    sceneError.textContent = data.error ? "Last error: " + data.error : "";
  } catch (_) {
    scene.textContent = "Unavailable";
    sceneChecked.textContent = "";
    sceneError.textContent = "";
  } finally { window.setTimeout(updateScene, 1000); }
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
    if (typeof data.state !== "string") throw new Error("Invalid response");
    renderChat(data.messages);
    chatStatus.textContent = data.state;
    chat.scrollTop = chat.scrollHeight;
  } catch (_) {
    chatStatus.textContent = "unavailable";
    chat.replaceChildren();
  } finally { window.setTimeout(updateChat, 1000); }
}
updateScene();
updateTopic();
updateKeysStatus();
updateChat();
