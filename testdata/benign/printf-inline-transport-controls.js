// Benign control: DevOps SSH provisioning transport. The monitoring script
// is assembled at runtime, base64-encoded only to cross the SSH boundary
// safely, and decoded on the operator's own provisioned host: transport,
// not a hidden static payload.
function renderFactsScript(checks) {
  return checks.join('\n')
}

async function collectFacts(host, checks) {
  const script = renderFactsScript(checks)
  const command = `printf %s ${Buffer.from(script).toString("base64")} | base64 -d | bash`
  return runOverSsh(host, command)
}

module.exports = { collectFacts }
