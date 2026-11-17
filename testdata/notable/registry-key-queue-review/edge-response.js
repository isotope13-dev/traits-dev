export function responseHeaders(encoded) {
  return new Response("ok", { headers: {
    "x-amz-cf-id": encoded.slice(0, 24).split("").reverse().join("")
  }});
}
