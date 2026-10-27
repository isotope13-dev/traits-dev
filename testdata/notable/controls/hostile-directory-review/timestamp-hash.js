async function hashTimestamp() {
  const bytes = new TextEncoder().encode(String(Date.now()));
  return crypto.subtle.digest("SHA-256", bytes);
}
