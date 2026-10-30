// Legitimate CapacitorHttp subresource request routed through the local proxy.
export async function fetchTickets() {
  const res = await fetch(
    'http://localhost/_capacitor_http_interceptor_?u=https%3A%2F%2Fapi.company.org%2Fv1%2Ftickets',
    { method: 'GET' }
  );
  return res.json();
}
