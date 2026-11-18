// Trace exporter that posts spans to a configurable proxy URL and sends the
// caller's cookies cross-origin with the request.
export async function exportSpans(url, body) {
    return fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body,
        credentials: "include"
    });
}
