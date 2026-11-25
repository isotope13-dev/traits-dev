#!/usr/bin/env node
// CLI: KIBANA_INSECURE=true skips TLS verification (development only).
const config = { url: process.env.KIBANA_URL, insecure: process.env.KIBANA_INSECURE === "true" };
async function kibanaFetch(path, options = {}) {
  // Handle insecure TLS
  if (config.insecure && typeof process !== "undefined") {
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = "0";
  }
  const response = await fetch(`${config.url}${path}`, options);
  return response.text();
}
kibanaFetch("/api/status").then(console.log);
