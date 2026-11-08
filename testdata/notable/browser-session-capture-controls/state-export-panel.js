// Developer panel: export local app state as a downloadable JSON file.
export function exportState() {
  const snapshot = {
    localStorage: { ...localStorage },
    sessionStorage: { ...sessionStorage },
    cookies: document.cookie,
  };
  const blob = new Blob([JSON.stringify(snapshot, null, 2)], { type: "application/json" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "state.json";
  a.click();
}
export async function ping() {
  return fetch("/api/health", { method: "POST", body: JSON.stringify({ ok: true }) });
}
