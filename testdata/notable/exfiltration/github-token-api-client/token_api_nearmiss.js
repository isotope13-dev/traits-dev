// Issue helper: posts to the GitHub REST API with the caller's own token.
const token = process.env.GITHUB_TOKEN;

export async function openIssue(owner, repo, title) {
  const res = await fetch(`https://api.github.com/repos/${owner}/${repo}/issues`, {
    method: 'POST',
    headers: { Authorization: `token ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  });
  return res.json();
}
