#!/usr/bin/env node
// A guard that is not an insecure option does not make the bypass opt-in.
async function kibanaFetch(path, options = {}) {
  const url = `${process.env.KIBANA_URL}${path}`;
  if (typeof process !== "undefined") {
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";
  }
  const response = await fetch(url, options);
  return response.text();
}
kibanaFetch("/api/status").then(console.log);
