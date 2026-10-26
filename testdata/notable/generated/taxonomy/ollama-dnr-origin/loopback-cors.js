const origins = ["http://localhost:11434", "http://127.0.0.1:11434"];
function removeOrigin(id, origin) {
  return {
    id,
    action: {
      type: "modifyHeaders",
      requestHeaders: [{ header: "Origin", operation: "remove" }],
    },
    condition: { urlFilter: `${origin}/*`, resourceTypes: ["xmlhttprequest", "other"] },
  };
}
console.warn("[Ollama CORS] setting local API rules");
declarativeNetRequest.updateDynamicRules(origins.map(removeOrigin));
