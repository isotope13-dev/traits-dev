const enabled = process.env.DANGEROUSLY_LOG_TO_SERVER_FOR_AI_AUTO_DEBUGGING;
const route = "/logs-combined-from-cli-and-mobile-for-simple-ai-debugging";
async function send(message, ...args) {
  if (!enabled) return;
  await fetch(serverUrl + route, {
    method: "POST",
    body: JSON.stringify({ message: `${message} ${args.map(a => JSON.stringify(a)).join(" ")}` })
  });
}
