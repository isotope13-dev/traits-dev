// WebAuthn management endpoints share the same "keys" substring as a
// credential-file sweep only through the passkeys/ path segment; the
// segment-boundary matcher must not score this API client as a key sweep.
const base = "https://accounts.example.com/_api";
async function deletePasskey(userId, passkeyId) {
  const res = await fetch(`${base}/admin/users/${userId}/passkeys/${passkeyId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error(`delete failed: ${res.status}`);
}
async function registerPasskey() {
  const options = await fetch(`${base}/passkeys/registration/options`, {
    method: "POST",
  }).then((r) => r.json());
  return options;
}
