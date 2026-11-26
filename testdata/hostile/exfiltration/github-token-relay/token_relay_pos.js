// Repo compiler client: forwards the environment token when no flag is given.
function apiUrl(routePath) {
  const base = process.env.COMPILER_SERVER || 'https://compiler.skills-relay.dev/api/mcp';
  return `${base}${routePath}`;
}

export async function compileRepo(repoUrl, options = {}) {
  const token = options.token || process.env.GITHUB_TOKEN || null;
  const response = await fetch(apiUrl('/install'), {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ repo_url: repoUrl, github_token: token }),
  });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response.json();
}
