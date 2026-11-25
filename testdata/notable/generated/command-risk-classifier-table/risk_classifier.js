// Risk classifier for shell commands proposed by an agent.
function classifyCommandRisk(command) {
  const s = command.toLowerCase();
  if (s.includes("rm -rf /") || s.includes("rm -fr /") || s.includes(":(){:|:&};:")) return "high";
  if (s.includes("curl") && s.includes("| sh")) return "high";
  return "low";
}
module.exports = { classifyCommandRisk };
