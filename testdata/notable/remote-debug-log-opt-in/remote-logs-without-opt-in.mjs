const route = "/logs-combined-from-cli-and-mobile-for-simple-ai-debugging";
async function send(message, ...args) {
  await fetch(serverUrl + route, {
    method: "POST",
    body: JSON.stringify({ message: `${message} ${args.map(a => JSON.stringify(a)).join(" ")}` })
  });
}
