// Presence probe: records only WHETHER any CI variable is set. No env value
// reaches the serialized body, so serialize/json::js-json-stringify-env-field
// must stay silent (virgil-cli telemetry shape).
const CI_VARS = ["CI", "GITHUB_ACTIONS", "GITLAB_CI", "CIRCLECI"];
export function buildPayload(ev, version) {
    const payload = JSON.stringify({
        ev,
        v: version,
        ci: CI_VARS.some((k) => process.env[k]),
        ts: Date.now(),
    });
    return payload;
}
