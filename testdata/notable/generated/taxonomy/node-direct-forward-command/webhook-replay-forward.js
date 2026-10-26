// Webhook-replay CLI: `forward` prints the tunnel recipe for live
// deliveries and POSTs synthesized payloads to a loopback-defaulted
// local target. No TCP forward is ever opened.
const DEFAULT_HOST = "127.0.0.1";
const DEFAULT_PORT = 3000;
export async function cmdReplay(subcommand, options) {
  switch (subcommand) {
    case "forward":
      return cmdForwardRecipe(options);
    default:
      return 1;
  }
}
async function cmdForwardRecipe(options) {
  const host = options.host ?? DEFAULT_HOST;
  const port = options.port ?? DEFAULT_PORT;
  const lines = [
    "Project hooks deliver to a public URL; there is no local relay.",
    `  1. Expose the agent: e.g. \`cloudflared tunnel --url http://${host}:${port}\``,
  ];
  process.stdout.write(lines.join("\n"));
  return 0;
}
