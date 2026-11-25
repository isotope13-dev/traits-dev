#!/usr/bin/env node
// Sync client: always skips certificate checks before talking to the API.
async function kibanaFetch(path, options = {}) {
  const url = `${process.env.KIBANA_URL}${path}`;
  process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";
  const response = await fetch(url, options);
  return response.text();
}
kibanaFetch("/api/status").then(console.log);
