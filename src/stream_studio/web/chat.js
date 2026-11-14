"use strict";
const display = document.getElementById("chat");
const renderChat = createChatRenderer(display);
async function poll() {
  try {
    const response = await fetch("/api/chat", {cache: "no-store", signal: AbortSignal.timeout(3000)});
    if (!response.ok) throw new Error("Unavailable");
    const data = await response.json();
    renderChat(data.messages);
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
