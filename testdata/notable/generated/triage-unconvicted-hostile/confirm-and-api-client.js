// Fixture: destructive-action confirmation beside the tool's own management
// API client. The y/N answer is consumed locally and never reaches the POST
// body (which carries the GraphQL document), so this is an ordinary CLI loop,
// not input exfiltration. Must never match js-input-intercept-exfil.
import { createInterface } from "node:readline/promises";

async function confirm(question, { input, output }) {
  const readline = createInterface({ input, output });
  try {
    const answer = await readline.question(question);
    return ["y", "yes"].includes(answer.trim().toLowerCase());
  } finally {
    readline.close();
  }
}

function createManagementClient({ endpoint, token, fetch = globalThis.fetch }) {
  return { async request(document, ...[variables]) {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ query: document.toString(), variables })
    });
    return response.json();
  } };
}

export async function apply(plan, target, io) {
  if (!await confirm(`Apply ${plan.changes.length} changes to ${target.name}? [y/N] `, io)) return;
  await createManagementClient(target).request(plan.document, plan.variables);
}
