function rule(source, id, severity, category, description) {
  return { id, regex: new RegExp(source, "i"), severity, category, description };
}

export const RULES = [
  rule("curl\\s+[^\\n]*\\$KEY", "env_exfil", "critical", "exfiltration", "curl secret"),
  rule("ignore\\s+(?:\\w+\\s+)*(previous|prior)\\s+instructions", "prompt_ignore", "critical", "injection", "ignore previous instructions"),
  rule("crontab", "cron_persist", "medium", "persistence", "cron persistence"),
  rule("npm\\s+install", "unpinned_npm", "medium", "supply_chain", "unpinned npm install"),
];
