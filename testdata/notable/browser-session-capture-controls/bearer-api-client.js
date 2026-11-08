export async function api(path, body) {
  const session = {
    accessToken: localStorage.getItem("app.access"),
    refreshToken: localStorage.getItem("app.refresh"),
  };
  return fetch(`/api/${path}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${session.accessToken}`, "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}
