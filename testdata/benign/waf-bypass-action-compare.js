// Benign control for powershell-bypass-literal-assignment: "bypass" here is
// a WAF ruleset mitigation action, not a PowerShell flag.
const RULESET_LABELS = { anomaly: "Anomaly", custom: "Custom" };
function countCustomBypassRules(active) {
  return active?.rules.filter((r) => r.active && r.action.mitigate?.action === "bypass").length ?? 0;
}
function labelFor(key) { return RULESET_LABELS[key] ?? key; }
module.exports = { countCustomBypassRules, labelFor };
