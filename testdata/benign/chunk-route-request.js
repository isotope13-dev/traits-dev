export function uploadChunk(data) {
  return fetch("/chunk", { method: "POST", body: data });
}
