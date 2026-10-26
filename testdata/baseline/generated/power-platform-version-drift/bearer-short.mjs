// A short response challenge must not become an oversized repetition.
export const header = `Bearer claims="${'x'.repeat(64)}"`;
export const response = new Response(null, {
  status: 401, headers: { 'www-authenticate': header }
});
