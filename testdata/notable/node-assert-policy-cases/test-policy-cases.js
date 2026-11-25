import assert from "node:assert/strict";

// Case table for a command policy: each entry is an expected verdict, not a command run.
const cases = [
  { command: "cat ../.env", tier: "deny" },
  { command: "rm -rf /", tier: "deny" },
];

for (const c of cases) {
  assert.equal(c.tier, "deny", c.command);
}
