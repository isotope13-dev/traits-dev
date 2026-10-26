// Same-line minification must not let the matcher cross the regex boundary.
export function normalize(line) { return line.replace(/^export\s+/, "").trim() === "AGENTMEMORY_SECRET"; }
