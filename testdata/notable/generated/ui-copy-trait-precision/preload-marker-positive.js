// Genuine preload-marker shape: a license env var plus an actual
// NODE_OPTIONS preload assignment for the agent in the same stanza, so the
// marker composite must still fire.
process.env.NEW_RELIC_LICENSE_KEY = loadLicense();
process.env.NODE_OPTIONS = "--require newrelic --max-old-space-size=4096";

export function agentArgv() {
  return ["node", "--require", "newrelic", "server.js"];
}
