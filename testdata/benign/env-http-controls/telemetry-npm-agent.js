// Benign CLI telemetry sender: threads process.env into an event builder that
// extracts only npm_config_user_agent, then POSTs the JSON event. The
// payload-flow engine reports environment/secret body flows for the object
// pass, but no bulk collection is serialized.
function parsePackageManager(userAgent) {
  if (userAgent === void 0) return null;
  const first = userAgent.split(/\s+/)[0];
  if (first === void 0 || first.length === 0) return null;
  if (!first.includes("/")) return null;
  return first;
}

function buildTelemetryEvent(payload, env) {
  return {
    version: payload.version,
    os: env.platform,
    packageManager: parsePackageManager(env.env.npm_config_user_agent),
  };
}

async function postEvent(payload) {
  const event = buildTelemetryEvent(payload, {
    platform: process.platform,
    env: process.env,
  });
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 1500);
  try {
    await fetch(payload.endpoint, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(event),
      signal: controller.signal,
    });
  } finally {
    clearTimeout(timer);
  }
}

module.exports = { postEvent };
