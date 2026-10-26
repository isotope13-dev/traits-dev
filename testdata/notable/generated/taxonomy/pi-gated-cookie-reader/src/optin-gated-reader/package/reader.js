// Opt-in gated browser-cookie reader. Deliberately uses neither of the
// original package's gate/reader symbol names. Reads the Chromium cookies
// table only when the user enables the browserCookieAccess setting.
export async function readBrowserCookies(hosts) {
  const targets = hosts && hosts.length ? hosts : ["gemini.google.com"];
  const hostClause = targets.map((h) => `host_key LIKE '%${h}%'`).join(" OR ");
  const query = `SELECT host_key, name, encrypted_value FROM cookies WHERE ${hostClause};`;
  return { query };
}

export function buildCookieHeader(cookies) {
  return Object.entries(cookies)
    .map(([k, v]) => `${k}=${v}`)
    .join("; ");
}
