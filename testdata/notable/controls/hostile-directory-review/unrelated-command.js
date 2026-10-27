const doc = '{"command":"example"}';
const command = "echo ready";
fetch("https://example.org/exec", {
  method: "POST",
  body: JSON.stringify({ description: doc, status: "ready" }),
});
