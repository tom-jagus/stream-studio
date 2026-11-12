"use strict";

const overlay = document.getElementById("overlay");
const viewport = document.getElementById("viewport");
const track = document.getElementById("track");
const topic = document.getElementById("topic");
const copy = document.getElementById("copy");
const pixelsPerSecond = 30;
let currentTopic = null;
let animation = null;

function layout() {
  if (animation) animation.cancel();
  animation = null;
  track.classList.remove("scrolling");
  if (overlay.hidden) return;
  const width = topic.getBoundingClientRect().width;
  if (width + 16 <= viewport.clientWidth) return;
  track.classList.add("scrolling");
  const gap = parseFloat(getComputedStyle(copy).marginLeft);
  const distance = width + gap;
  animation = track.animate(
    [ { transform: "translateX(0)" },
      { transform: `translateX(-${distance}px)` } ],
    { duration: distance / pixelsPerSecond * 1000,
      iterations: Infinity, easing: "linear" }
  );
}

async function poll() {
  try {
    const response = await fetch("/api/topic", {
      cache: "no-store", signal: AbortSignal.timeout(2500)
    });
    if (!response.ok) throw new Error("Topic is unavailable");
    const payload = await response.json();
    if (typeof payload.topic !== "string") throw new Error("Invalid topic");
    if (payload.topic !== currentTopic) {
      currentTopic = payload.topic;
      topic.textContent = currentTopic;
      copy.textContent = currentTopic;
      overlay.hidden = currentTopic.length === 0;
      layout();
    }
  } catch (_) {
    // Keep the last topic during transient errors, including service restarts.
  } finally {
    window.setTimeout(poll, 1000);
  }
}

new ResizeObserver(layout).observe(viewport);
document.fonts.ready.then(layout);
poll();
