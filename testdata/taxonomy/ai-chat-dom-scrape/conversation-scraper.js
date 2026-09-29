const host = location.hostname.includes("gemini.google.com");
const turns = document.querySelectorAll(".conversation-turn");
const aiPage = "gemini.google.com";
const messages = [...turns].map((turn) => turn.innerText);
chrome.runtime.sendMessage({ type: "conversation-export", messages });
