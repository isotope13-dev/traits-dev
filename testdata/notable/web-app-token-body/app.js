// Web app calling its own API; no browser extension API is involved.
export async function tagPage(url, title, accessToken) {
  const res = await fetch("/api/ai-tag", {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${accessToken}` },
    body: JSON.stringify({ url, title, accessToken }),
  });
  return res.json();
}
