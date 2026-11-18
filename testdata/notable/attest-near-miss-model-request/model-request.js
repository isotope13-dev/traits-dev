// Near miss for the attest-token gate: an ordinary API client posts host
// metadata as JSON with a bearer key and a platform field. There is no
// challenge endpoint and no server nonce, so no attestation handshake exists.
const API_BASE = 'https://api.example-assistant.test';

async function sendModelRequest(session, prompt) {
  const response = await fetch(`${API_BASE}/v1/chat`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${session}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      prompt,
      metadata: { os: process.platform, arch: process.arch },
    }),
  });
  return response.json();
}

module.exports = { sendModelRequest };
