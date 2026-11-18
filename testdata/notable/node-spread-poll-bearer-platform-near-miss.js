// Near-miss for the attested remote-text feed poll: a CLI bundle where a
// version-policy timer, an authenticated API client and a browser opener sit
// in unrelated functions. Each leg appears somewhere in the file, but no timer
// reads a token-authorized text body, and the platform check only chooses the
// command used to open a URL. Each function is ordinary client code.
const POLICY_URL = 'https://dashboard.example-vendor.com/api/cli/policy';

function readPolicy(json) {
  return json.min_version || null;
}

function watchPolicy(version, onRefuse) {
  const timer = setInterval(() => {
    fetch(POLICY_URL, { signal: AbortSignal.timeout(1500) })
      .then((res) => res.json())
      .then((body) => {
        if (readPolicy(body) && version < readPolicy(body)) onRefuse(body);
      })
      .catch(() => {});
  }, 10 * 60000);
  timer.unref?.();
  return () => clearInterval(timer);
}

// Authenticated resource listing. It is an ordinary request: the token comes
// from local config, and the reply is parsed as JSON, not run as code.
const apiCache = new Map();

async function listProjects(apiBase, getAccessToken) {
  const token = getAccessToken();
  const res = await fetch(`${apiBase}/api/cli/projects`, {
    method: 'GET',
    headers: { Accept: 'application/json', Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error(`projects ${res.status}`);
  const projects = await res.json();
  apiCache.set('projects', projects);
  return projects;
}

function describeProjects(projects) {
  return projects.map((p) => `${p.name} (${p.id})`).join('\n');
}

// Opens a dashboard link in the default browser. The platform check selects
// the opener command; no request carries the platform name.
function openDashboard(url) {
  const cmd = process.platform === 'darwin' ? 'open' : process.platform === 'win32' ? 'start' : 'xdg-open';
  return { cmd, args: [url] };
}

module.exports = { watchPolicy, listProjects, describeProjects, openDashboard };
