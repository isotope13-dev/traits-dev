// A response-side challenge fixture, with no network implementation.
export const header = `Bearer claims="${'x'.repeat(33000)}"`;
export const response = new Response(null, {
  status: 401, headers: { 'www-authenticate': header }
});
